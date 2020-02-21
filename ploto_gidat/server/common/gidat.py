import time


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

    config = {
        'base': {
            'run_base_dir': '/home/wangdp/project/gidat/workspace/run_base',
            'python_exe': '/home/wangdp/.pyenv/versions/anaconda3-2019.10/envs/gidat/bin/python3'
        },
        'meteor_draw_plotter': {
            'path': "/home/wangdp/project/gidat/meteor_draw/package/",
            "program": "meteormap",
        },
    }

    from ploto.run import run_ploto
    run_ploto(message, config)
