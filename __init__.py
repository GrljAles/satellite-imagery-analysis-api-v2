from flask import Flask
from flask_restful import Api
import logging
from flask import json, Response
from datetime import datetime


app = Flask(__name__)
app.config.from_object("config.Config")

api = Api(app)

# Extensions
logging.basicConfig(level=logging.DEBUG)
handler = logging.FileHandler("./log.log")
app.logger.addHandler(handler)

#Error handlers
@app.errorhandler(404)
def handle_404_error(_error):
    app.logger.error(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}: {_error}")
    return {"message": "Not found."}
    
@app.errorhandler(500)
def handle_500_error(_error):
    app.logger.error(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}: {_error}")
    return {"message": "Internal server error."}

# Endpoints
from resources import tool_resources

api.add_resource(tool_resources.ZonalStatistics, "/api/zonalstatistics")
api.add_resource(tool_resources.TimeSeriesChartPoints, "/api/tschartpoints")
api.add_resource(tool_resources.TimeSeriesChartPolygons, "/api/tschartpolygons")
api.add_resource(tool_resources.ProfileChart, "/api/profilechart")

if __name__ == "__main__":
    app.run(debug=True, threaded=True)