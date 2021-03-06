import os
from pathlib import Path
import subprocess
import json
import configparser

from loguru import logger


def run_plotter(task: dict, work_dir: str, config: dict):
    """
    run meteor_draw plotter

    Parameters
    ----------
    task:
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
                "config_file": "config file path",
            },
        }

    """
    logger.info('running meteor_draw_plotter...')

    plot_task = task["plot_task"]
    with open("task.json", "w") as f:
        json.dump(plot_task, f)

    envs = os.environ.copy()
    envs["LD_LIBRARY_PATH"] = f"{config['meteor_draw_plotter']['path']}:{envs.get('LD_LIBRARY_PATH','')}"

    logger.info("run meteor_draw program...")
    program_path = Path(config["meteor_draw_plotter"]["path"], config["meteor_draw_plotter"]["program"])

    config_file_path = config["meteor_draw_plotter"]["config_file"]

    config = configparser.ConfigParser()
    with open(config_file_path, "r") as f:
        config.read_file(f)
    config["path"]["plotfile_path"] = str(work_dir)
    with open("config.ini", "w") as f:
        config.write(f)

    ncl_command = [
        f"{program_path} ./task.json ./config.ini"
    ]
    logger.info("ncl command: {ncl_command}".format(ncl_command=' '.join(ncl_command)))
    result = subprocess.run(
        ncl_command,
        env=envs,
        # start_new_session=True,
        shell=True,
    )

    logger.info('running meteor_draw_plotter...done')
