import time

from flask import current_app


def run_meteor_draw_task(plot_task: dict):
    task = {
        'steps': [
            {
                'step_type': 'plotter',
                'type': 'ploto_gidat.plotter.meteor_draw_plotter',
                'plot_task': plot_task,
            },
        ],
    }

    message = {
        'app': 'ploto',
        'type': 'ploto-gidat',
        'timestamp': time.time(),
        'data': task
    }

    config = current_app.config["server_config"]["ploto"]

    from ploto.run import run_ploto
    run_ploto(message, config)
