from flask import request, json, current_app, jsonify

from ploto_gidat.server.api import api_v1_app


@api_v1_app.route('/gidat/plot/meteor_draw/example', methods=['POST'])
def receive_gidat_plot_example():
    """

    POST DATA
    message
        {
            "task": {}, # task json object
        }

    返回值：
        {
            "status": "ok",
        }
    """
    if 'plot_task' in request.form:
        plot_task = json.loads(request.form['plot_task'])
    elif 'plot_task' in request.json:
        plot_task = json.loads(request.json['plot_task'])
    else:
        return jsonify({
            'status': 'error',
        })

    from ploto.scheduler.rabbitmq.producer.producer import send_message
    scheduler_config = current_app.config['server_config']['broker']['scheduler']
    current_app.logger.info('Sending task to scheduler...')
    send_message(plot_task, config=scheduler_config)

    return jsonify({
        'status': 'ok',
    })
