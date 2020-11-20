import time

from flask import request, json, current_app, jsonify
import pandas as pd

from ploto.run import run_ploto
from ploto_gidat.server.api import api_v1_app
from ploto_gidat.server.common.giset import (
    generate_and_send_meteor_draw_tasks,
    generate_meteor_draw_tasks,
)



@api_v1_app.route('/giset/plot/meteor-draw/example', methods=['POST'])
def receive_giset_plot_example():
    """
    Run plot task in server.

    POST DATA
        {
            "plot_task": {}, # task json object
        }

    RETURN DATA：
        {
            "status": "ok",
        }
    """
    request_data = request.json

    data_source = request_data["data_source"]

    start_valid_time = request_data["start_time"]
    end_valid_time = request_data["end_time"]
    forecast_length = int(request_data["fcstlen"])
    forecast_step = int(request_data["step"])
    start_hours = [int(f) for f in request_data["hh_list"]]

    plot_task_template = request_data['plot_task']

    start_time = pd.to_datetime(start_valid_time[:10], format="%Y%m%d%H")
    end_time = pd.to_datetime(end_valid_time[:10], format="%Y%m%d%H")

    tasks = generate_meteor_draw_tasks(
        data_source,
        start_time,
        end_time,
        start_hours,
        forecast_length,
        forecast_step,
        plot_task_template,
    )

    config = current_app.config["server_config"]["ploto"]

    for task in tasks:
        message = {
            'app': 'ploto',
            'type': 'ploto-gidat',
            'timestamp': time.time(),
            'data': task
        }
        run_ploto(message, config)

    return jsonify({
        'status': 'ok',
    })


@api_v1_app.route('/giset/plot/meteor-draw/ploto', methods=['POST'])
def receive_giset_plot_ploto():
    """
    Generate plot tasks and send to RabbitMQ

    POST DATA
        {
            "plot_task": {}, # task json object
        }

    返回值：
        {
            "status": "ok",
        }
    """
    request_data = request.json

    generate_and_send_meteor_draw_tasks(request_data)

    return jsonify({
        'status': 'ok',
    })
