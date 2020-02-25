from flask import request, json, current_app, jsonify

from ploto_gidat.server.api import api_v1_app
from ploto_gidat.server.common.gidat import run_meteor_draw_task


@api_v1_app.route('/gidat/plot/meteor_draw/example', methods=['POST'])
def receive_gidat_plot_example():
    """

    POST DATA
        {
            "plot_task": {}, # task json object
        }

    返回值：
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
