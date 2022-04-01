import numpy as np
from flask import current_app
from rasterstats import point_query
from shapely.geometry import Point
from datetime import datetime
import os


def get_coordinates_along_line(p0, p1, resolution):
    """
    Calculates equaly spaced coordinates along line defined by p0 and p1 coordinates.
    
    Parameters:
        p0 (list): Coordiante pair of the beginning of the line.
        p1 (list): Coordiante pair of the end of the line.
        resolution (float): cell size of the selected product.
    """
    # Get single coordinates from pair, make sure they are float.
    x0 = float(p0[0])
    y0 = float(p0[1])
    x1 = float(p1[0])
    y1 = float(p1[1])

    # Get length of the line and calculate the number of point to extract values at based on the resolution of the dataset.
    # The method is not exact as some pixels might be missed because the resolution is exact only in cardinal directions.
    length = int(np.hypot(y1 - y0, x1 - x0))
    num = int(length / resolution)
    # Coordinate pairs along profile to extract values at.
    x, y = np.linspace(x0, x1, num), np.linspace(y0, y1, num)
    ress = []

    for xx, yy in zip(x, y):
        ress.append([xx, yy])

    return ress


def get_profile_chart(product, date, resolution, line):
    """
    Returns distance along profile line - value pairs to construct profile chart.
    
    Parameters:
        product (str): Name of the product to extract profile from.
        date (str): YYYYMMDD date string to identify the correct raster.
        resolution (float): Distance between the extraction points along profile line.
        line (list): Two lists of coordiante pairs defining the profile line.
    """
    # Get coordinates along line to get the values at.
    coordinates = get_coordinates_along_line(line[0], line[1], resolution)
    product_location = current_app.config["PRODUCT_LOCATION"]
    product_location = f"{product_location}/{date}/{product}"
    rasters = os.listdir(product_location)
    for j in rasters:
        if j.endswith("vrt"): # Identify the correct raster.
            raster = j

    profile = {"datasets": []}
    data = []

    # Extract values at coordinate pairs.
    i = 0
    for point in coordinates:
        # Create point.
        pt = Point(point[0], point[1])
        try:
            # Extract
            product_value = point_query([pt], f"{product_location}/{raster}")
            product_value = np.round(product_value, 2)[0]
        except TypeError as e:
            product_value = None
            message = "Some values could not be extracted due to an error."
            current_app.logger.error(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}: {e}, {message}")
            
        data.append({"x": i, "y": product_value})
        i += 1
    profile["datasets"].append(
        {"fid": 0, "label": f"{product}, {date}", "data": data}) # Includes fid and label for future implelentation of multiple lines and multiple products.
    if message:
        profile["message"] = message
    return profile


if __name__ == "__main__":
    pass
