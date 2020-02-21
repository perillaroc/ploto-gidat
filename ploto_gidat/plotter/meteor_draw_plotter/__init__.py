import os
from pathlib import Path
import subprocess
import json

from loguru import logger


def run_plotter(plotter_task: dict, work_dir: str, config: dict):
    """
    run meteor_draw plotter

    Parameters
    ----------
    plotter_task:
        a dict config of plotter task.
        {
            'step_type': 'plotter',
            'type': 'ploto_gidat.plotter.meteor_draw_plotter',
            'plot_task': plot_task,
        }
    work_dir: str

    config: dict
        {
            'meteor_draw_plotter': {
                'path': "/home/wangdp/project/gidat/meteor_draw/package/",
                "program": "meteormap",
            },
        }

    """
    logger.info('running meteor_draw_plotter...')

    plot_task = plotter_task["plot_task"]
    with open("task.json", "w") as f:
        json.dump(f, plot_task)

    envs = os.environ.copy()
    envs["LD_LIBRARY_PATH"] = f"{config['meteor_draw_plotter']['path']}:{envs.get('LD_LIBRARY_PATH','')}"

    logger.info("run meteor_draw program...")
    program_path = Path(config["meteor_draw_plotter"]["path"], config["meteor_draw_plotter"]["program"])
    ncl_command = [
        f"{program_path} ./task.json"
    ]
    logger.info("ncl command: {ncl_command}".format(ncl_command=' '.join(ncl_command)))
    result = subprocess.run(
        ncl_command,
        env=envs,
        # start_new_session=True,
        shell=True,
    )

    logger.info('running meteor_draw_plotter...done')
