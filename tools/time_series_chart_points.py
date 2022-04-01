from email import message
import os
from tools.misc_module import get_dates_between_two_dates
from rasterstats import point_query
from shapely.geometry import Point
from flask import current_app
from datetime import datetime
import ast


def get_time_series_data(starting_date, ending_date, product, points):
    """
    Extracts values from several rasters over same area for different dates at multiple locations and returns time series for these locations.
    
    Parameters:
        starting_date (str): YYYYMMDD date string of the start of the timeseries.
        ending_date (str): YYYYMMDD date string of the end of the timeseries.
        product (str): Name of the product to extract timeseries from.
        points (list): List of coordinate pairs (dict) to extract values at.
    """
    # Get avalable dates
    data_location = current_app.config["PRODUCT_LOCATION"]
    files_list = os.listdir(data_location)
    
    # Check if files_list elements is a valid directory
    dates_list = []
    for anything in files_list:
        if os.path.isdir(f"{data_location}/{anything}"):
            dates_list.append(data_location)
        else:
            pass
        
    # Get list of dates between timeseries endig and starting dates
    valid_dates = get_dates_between_two_dates(
        starting_date, ending_date, dates_list)

    # Returned object structure (customised for chart.js timeseries chart)
    timeseries = {"datasets": []}

    # Loop first the points list...
    for point in points:
        point = ast.literal_eval(point)
        # ...and then valid dates
        data = []
        for date_string in valid_dates:
            date_to_return = f"{date_string[0:4]}-{date_string[4:6]}-{date_string[6:8]}"
            
            # Construct the path to dateset
            raster_folder_path = f"{data_location}/{date_string}/{product}/"
            rasters = os.listdir(raster_folder_path)
            for j in rasters:
                if j.endswith("vrt"): # Identify the correct raster.
                    raster = j
            
            # Create point.
            pt = Point(point["x"], point["y"])
            
            # Extract value
            try:
                product_value = point_query(
                    [pt], f"{raster_folder_path}/{raster}")
                data.append({"x": date_to_return, "y": product_value})
            except Exception as e:
                data.append({"x": date_to_return, "y": None})
                message = "Some values could not be extracted due to an error."
                current_app.logger.error(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}: {e}, {message}")
                
            # Sort the list of extracted values by corresponding date.
            data.sort(key=lambda x: datetime.strptime(x["x"], "%Y-%m-%d"))
        timeseries["datasets"].append(
            {"fid": point["id"], "label": f"{product}, x: {round(point['x'], 4)}, y: {round(point['y'], 4)}", "data": data})
        if message:
            timeseries["message"] = message
    return timeseries

if __name__ == "__main__":
    pass
