from flask_restful import Resource, reqparse
from flask import current_app
from datetime import datetime

class ZonalStatistics(Resource):
    def post(self):
        zonal_statistics_parser = reqparse.RequestParser()
        zonal_statistics_parser.add_argument("product", required=True)
        zonal_statistics_parser.add_argument("dates", required=True)
        zonal_statistics_parser.add_argument("zone", required=True)
        zonal_statistics_data = zonal_statistics_parser.parse_args()
        try:
            from tools.zonal_statistics import calculate_zonal_statistics
            zonal_statistics_result = calculate_zonal_statistics(zonal_statistics_data["product"], zonal_statistics_data["dates"], zonal_statistics_data["zone"])
            return zonal_statistics_result

        except Exception as e:
            message = "Something went wrong while processing your request."
            current_app.logger.error(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}: {e}, {message}")
            return {"error": e, "message": message}

class TimeSeriesChartPoints(Resource):
    def post(self):
        time_series_chart_points_parser = reqparse.RequestParser()
        time_series_chart_points_parser.add_argument("starting_date_index", required=True)
        time_series_chart_points_parser.add_argument("ending_date_index", required=True)
        time_series_chart_points_parser.add_argument("points", action="append", required=True)
        time_series_chart_points_parser.add_argument("product", required=True)
        time_series_chart_points_data = time_series_chart_points_parser.parse_args()

        try:
            from tools.time_series_chart_points import get_time_series_data
            time_series_chart_points_result = get_time_series_data(time_series_chart_points_data["starting_date_index"], time_series_chart_points_data["ending_date_index"],  time_series_chart_points_data["product"], time_series_chart_points_data["points"])
            return time_series_chart_points_result
        except Exception as e:
            message = "Something went wrong while processing your request."
            current_app.logger.error(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}: {e}, {message}")
            return {"error": e, "message": message}

class TimeSeriesChartPolygons(Resource):
    def post(self):
        time_series_chart_poly_parser = reqparse.RequestParser()
        time_series_chart_poly_parser.add_argument("starting_date_index", required=True)
        time_series_chart_poly_parser.add_argument("ending_date_index", required=True)
        time_series_chart_poly_parser.add_argument("polygons", action="append", required=True)
        time_series_chart_poly_parser.add_argument("product", required=True)
        time_series_chart_poly_data = time_series_chart_poly_parser.parse_args()

        try:
            from tools.time_series_chart_polygons import get_zonal_timeseries_data
            time_series_chart_polygon_result = get_zonal_timeseries_data(time_series_chart_poly_data["starting_date_index"], time_series_chart_poly_data["ending_date_index"],  time_series_chart_poly_data["product"], time_series_chart_poly_data["polygons"])
            return  time_series_chart_polygon_result
        except Exception as e:
            message = "Something went wrong while processing your request."
            current_app.logger.error(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}: {e}, {message}")
            return {"error": e, "message": message}

class ProfileChart(Resource):
    def post(self):
        profile_chart_parser = reqparse.RequestParser()
        profile_chart_parser.add_argument("product", required=True)
        profile_chart_parser.add_argument("dates", required=True)
        profile_chart_parser.add_argument("length", required=True)
        profile_chart_parser.add_argument("resolution", type=int, location="json", required=True)
        profile_chart_parser.add_argument("p0", type=list, location="json", required=True)
        profile_chart_parser.add_argument("p1", type=list, location="json", required=True)
        profile_chart_data = profile_chart_parser.parse_args()

        try:
            from tools.profile_chart import get_profile_chart
            profile_chart_result = get_profile_chart(profile_chart_data["product"], profile_chart_data["dates"], profile_chart_data["resolution"], [profile_chart_data["p0"], profile_chart_data["p1"]])
            return profile_chart_result
        except Exception as e:
            message = "Something went wrong while processing your request."
            current_app.logger.error(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}: {e}, {message}")
            return {"error": e, "message": message}