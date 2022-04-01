from flask import current_app
from tools import time_series_chart_points
import os
from osgeo import gdal, ogr
from osgeo.gdalconst import GA_ReadOnly
import numpy as np


def get_zonal_timeseries_data(starting_date, ending_date, product, polygons):
    """
    Returns time series data for all pixels within polygon. Code below is used just 
    to create sets of coordinate pairs at pixels centres that are then processed by
    time_series_chart_points.py
    
    Parameters:
        starting_date (str): YYYYMMDD date string of the start of the timeseries.
        ending_date (str): YYYYMMDD date string of the end of the timeseries.
        product (str): Name of the product to extract timeseries from.
        polygons (list): List containing polygon geojson.
    """
    ## Results container.
    polygon_points = []
    ## Get the requested product dataset sample.
    product_location = current_app.config["PRODUCT_LOCATION"]
    files_list = os.listdir(product_location)
    ## Check if datesList element is a valid directory
    dates_list = []
    for anything in files_list:
        if os.path.isdir(f"{product_location}/{anything}"):
            dates_list.append(anything)
        else:
            pass

    ## Get sample raster path. Sample raster is needed to get its properties and create a new in-memory raster that will hold rasterized polygons.
    sample_dataset_path = f"{product_location}/{dates_list[0]}/{product}"
    sample_dataset = os.listdir(sample_dataset_path)[0]
    sample_dataset = f"{sample_dataset_path}/{sample_dataset}"

    ## Open sample raster and get poperties needed.
    in_raster = gdal.Open(sample_dataset, GA_ReadOnly)
    in_cols = in_raster.RasterXSize
    in_rows = in_raster.RasterYSize
    in_geotransform = in_raster.GetGeoTransform()

    ## Create in-memory raster.
    mem_drv = gdal.GetDriverByName("MEM")
    target_raster = mem_drv.Create("", in_cols, in_rows, 1, gdal.GDT_Byte)
    target_raster.SetGeoTransform(in_geotransform)

    ## Open geojson from submitted json..
    source_ds = ogr.Open(polygons[0])
    source_layer = source_ds.GetLayer()

    ## Rasterize
    gdal.RasterizeLayer(target_raster, [1], source_layer, burn_values=[1])

    ## Read raster as numpy array to get the rasterized polygon pixel indices.
    raster_band = target_raster.GetRasterBand(1)
    ras_array = raster_band.ReadAsArray()

    ## Convert array to point coordinates
    count = 0
    polygon_indices = np.where(ras_array != 0)
    for index_y in polygon_indices[0]:
        index_x = polygon_indices[1][count]
        origin_x = in_geotransform[0]
        origin_y = in_geotransform[3]
        pixel_width = in_geotransform[1]
        pixel_height = in_geotransform[5]
        x_coord = origin_x + pixel_width * index_x
        y_coord = origin_y + pixel_height * index_y
        ## Construct each feature so it can be used by the point time series tool.
        point_feature = {"id": count, "product": product, "x": x_coord, "y": y_coord}
        ## Append it to results list.
        polygon_points.append(f"{point_feature}")
        count += 1

    ## Pass the list of points to the point time series tool.
    time_series_chart_polygon_result = time_series_chart_points.get_time_series_data(starting_date, ending_date, product, polygon_points)
    return time_series_chart_polygon_result

if __name__ == "__main__":
    pass