import time
import typing
import itertools
import pathlib
import json

from flask import current_app
import pandas as pd
import numpy as np
from loguru import logger

from nwpc_data.data_finder import find_local_file
from ploto.scheduler.rabbitmq.producer.producer import send_message


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


def generate_and_send_meteor_draw_tasks(request_data: dict):
    """

    Parameters
    ----------
    request_data:
    {
        "data_source": {
            "system_name": "grapes_gfs_gmf",
            "username": "niuxingy",
            "user_id": "u0184",
            "data_type": "storage",
            "routing_key": "GFSNEW.niuxingy",
            "test_ID": "TG2000617"
        },
        "start_time": "2020070100000",
        "step": "6",
        "hh_list": [
            "00",
            "12"
        ],
        "end_time": "2020070200000",
        "fcstlen": "96",
        "plot_task": {
            // ...skip...
        }
    }

    Returns
    -------

    """
    data_source = request_data["data_source"]

    start_valid_time = request_data["start_time"]
    end_valid_time = request_data["end_time"]
    forecast_length = int(request_data["fcstlen"])
    forecast_step = int(request_data["step"])
    start_hours = [int(f) for f in request_data["hh_list"]]

    plot_task_template = request_data['plot_task']

    # get data list
    start_time = pd.to_datetime(start_valid_time[:10], format="%Y%m%d%H")
    end_time = pd.to_datetime(end_valid_time[:10], format="%Y%m%d%H")
    date_list = get_date_list(
        start_time,
        end_time,
        start_hours,
        forecast_length,
        forecast_step,
    )

    for item in date_list.iterrows():
        start_time = item[1]["start_time"]
        forecast_time = item[1]["forecast_time"]

        data_path = get_data_path(
            data_source,
            start_time=start_time,
            forecast_time=forecast_time,
            data_type="grib2/orig"
        )

        if data_path is None:
            logger.warning("WARNING: data is not found", start_time, forecast_time)
            continue

        task = generate_plot_task(
            plot_task_template,
            data_path,
            data_source
        )

        message = {
            'app': 'ploto',
            'type': 'ploto-gidat',
            'timestamp': time.time(),
            'data': task
        }
        logger.info(message)
        continue
        config = current_app.config["server_config"]["scheduler"]
        logger.info("send message...")
        send_message(message, config)
        logger.info("send message...done")


def get_date_list(
        start_time: pd.Timestamp,
        end_time: pd.Timestamp,
        start_hours: typing.List[int],
        forecast_length: int,
        forecast_step: int,
) -> pd.DataFrame:
    """
    Get datetime list of start_time and forecast_time for each plot file.

    Parameters
    ----------
    start_time
    end_time
    start_hours
    forecast_length
    forecast_step

    Returns
    -------
    pd.DataFrame

    """
    start_times = pd.date_range(start_time, end_time, freq="D")
    start_hours = [pd.Timedelta(hours=h) for h in start_hours]
    forecast_hours = pd.to_timedelta(np.arange(0, forecast_length, forecast_step), unit="h").to_series()

    date_time_list = itertools.product(
        start_times,
        start_hours,
        forecast_hours
    )

    date_list = pd.DataFrame(
        date_time_list,
        columns=["start_date", "start_hour", "forecast_time"]
    )
    date_list["start_time"] = date_list["start_date"] + date_list["start_hour"]
    return date_list[["start_time", "forecast_time"]].copy()


def get_data_path(
        data_source: typing.Dict,
        start_time: pd.Timestamp,
        forecast_time: pd.Timedelta,
        data_type: str = "grib2/orig",
) -> typing.Optional[pathlib.Path]:
    system_name = data_source["system_name"]
    data_path = find_local_file(
        f"{system_name}/{data_type}",
        start_time=start_time,
        forecast_time=forecast_time,
    )

    return data_path


def generate_plot_task(
        plot_task_template: typing.Dict,
        data_path: pathlib.Path,
        data_source: typing.Dict,
) -> typing.Dict:
    """
    Generate plot task for GISET.

    Parameters
    ----------
    plot_task_template
    data_path

    Returns
    -------

    """
    plot_task = plot_task_template.copy()
    for layer in plot_task["maplayer"]:
        layer["file_path"] = str(data_path)

    task = {
        'steps': [
            {
                'step_type': 'plotter',
                'type': 'ploto_gidat.plotter.meteor_draw_plotter',
                'plot_task': plot_task,
            },
            {
                'step_type': 'distributor',
                'type': 'ploto_gidat.distributor.gidat_distributor',
                "username": data_source["username"],
                "user_id": data_source["user_id"],
                "routing_key": data_source["routing_key"],
                "test_ID": data_source["test_ID"],
            },
        ],
    }

    return task
