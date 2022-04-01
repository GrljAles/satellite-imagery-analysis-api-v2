from rasterstats import zonal_stats
from flask import current_app
from datetime import datetime

import os

def calculate_zonal_statistics(product, date, polygon):
    """
    Returns count min max mean std range for the cells within given polygon.
    
    Parameters:
        product (str): Name of the product to extract timeseries from.
        date (str): YYYYMMDD date string of the requested raster.
        polygons (geojson): Geojson with single polygon covering the area of interest.
    """
    statistics ={}
    # Construct the path to dateset
    data_location = current_app.config["PRODUCT_LOCATION"]
    raster_folder_path = f"{data_location}/{date}/{product}/"
    rasters = os.listdir(raster_folder_path)
    for j in rasters:
        if j.endswith("vrt"): # Identify the correct raster.
            raster = j
            
    # Calculate zonal statistics.
    try:
        statistics[date] = zonal_stats(polygon, f"{raster_folder_path}/{raster}", stats="count min max mean std range")
        stat_response = {"product": product, "date": date, "min": round(statistics[date][0]["min"], 2), "max": round(statistics[date][0]["max"], 2), "mean": round(statistics[date][0]["mean"], 2), "std": round(statistics[date][0]["std"], 2), "range": round(statistics[date][0]["range"], 2)}
    except Exception as e:
        # Returns empty result if error occured.
        message = "An error occured while processing the request."
        stat_response = {"product": product, "date": date, "min": "/", "max": "/", "mean": "/", "std": "/", "range": "/", "message": message}
        current_app.logger.error(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}: {e}, {message}")
    return stat_response

if __name__ == "__main__":
    pass