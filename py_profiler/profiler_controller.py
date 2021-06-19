from flask import Blueprint, render_template

#
# @author: anhlt
#
from py_profiler.measure_service import profiling_service

profiler_blueprint = Blueprint("profiler", __name__)

@profiler_blueprint.route("/profiler", methods=["GET"])
def index():
    return profiling_service.as_html()
