import time
import typing
import itertools
import pathlib
import json

import pandas as pd
import numpy as np
from loguru import logger

from nwpc_data.data_finder import find_local_file
from ploto.scheduler.rabbitmq.producer.producer import send_message


def generate_and_send_meteor_draw_tasks(
        data_source: typing.Dict,
        start_time: pd.Timestamp,
        end_time: pd.Timestamp,
        start_hours: typing.List[int],
        forecast_length: int,
        forecast_step: int,
        plot_task_template: typing.Dict,
        scheduler_config: typing.Dict,
):
    """
    """
    task_iter = generate_meteor_draw_tasks(
        data_source,
        start_time,
        end_time,
        start_hours,
        forecast_length,
        forecast_step,
        plot_task_template,
    )

    for task in task_iter:
        message = {
            'app': 'ploto',
            'type': 'ploto-gidat',
            'timestamp': time.time(),
            'data': task
        }
        logger.info(message)

        logger.info("send message...")
        send_message(message, scheduler_config)
        logger.info("send message...done")


def generate_meteor_draw_tasks(
        data_source: typing.Dict,
        start_time: pd.Timestamp,
        end_time: pd.Timestamp,
        start_hours: typing.List,
        forecast_length: int,
        forecast_step: int,
        plot_task_template: typing.Dict,
) -> typing.Iterable[typing.Dict]:

    # get data list
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

        task = generate_plot_task(
            plot_task_template,
            start_time,
            forecast_time,
            data_source,
        )
        if task is None:
            continue
        yield task


def generate_plot_task(
        plot_task_template: typing.Dict,
        start_time: pd.Timestamp,
        forecast_time: pd.Timedelta,
        data_source: typing.Dict,
) -> typing.Optional[typing.Dict]:
    """
    Generate plot task for GISET.

    Parameters
    ----------
    plot_task_template
    data_path

    Returns
    -------

    """
    data_path = get_data_path(
        data_source,
        start_time=start_time,
        forecast_time=forecast_time,
        data_type="grib2/orig"
    )

    if data_path is None:
        logger.warning("WARNING: data is not found", start_time, forecast_time)
        return None

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
                'type': 'ploto_gidat.distributor.giset_distributor',
                "username": data_source["username"],
                "user_id": data_source["user_id"],
                "routing_key": data_source["routing_key"],
                "test_ID": data_source["test_ID"],
                "meteor_type": plot_task["maplayer"][0]["meteor_type"],
                "start_time": start_time.isoformat(),
                "forecast_time": forecast_time.isoformat(),
            },
        ],
    }

    return task


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
    date_list["start_time"] = date_list["start_date"].map(lambda x: pd.to_datetime(x.date())) + date_list["start_hour"]
    return date_list[["start_time", "forecast_time"]].copy()


def get_data_path(
        data_source: typing.Dict,
        start_time: pd.Timestamp,
        forecast_time: pd.Timedelta,
        data_type: str = "grib2/orig",
) -> typing.Optional[pathlib.Path]:
    system_name = data_source["system_name"]
    exp_id = data_source["test_ID"]
    data_path = find_local_file(
        f"{system_name}/{data_type}",
        start_time=start_time,
        forecast_time=forecast_time,
        data_class="exp",
        exp_id=exp_id,
    )

    return data_path
