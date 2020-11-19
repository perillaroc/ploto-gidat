from flask import request, json, current_app, jsonify

from ploto_gidat.server.api import api_v1_app
from ploto_gidat.server.common.giset import (
    run_meteor_draw_task,
    generate_and_send_meteor_draw_tasks,
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
    if 'plot_task' in request.form:
        plot_task = json.loads(request.form['plot_task'])
    elif 'plot_task' in request.json:
        plot_task = request.json['plot_task']
    else:
        return jsonify({
            'status': 'error',
        })

    run_meteor_draw_task(plot_task)

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
