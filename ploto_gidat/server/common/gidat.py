import time
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


def generate_meteor_draw_tasks(request_data: dict):
    data_source = request_data["data_source"]

    start_valid_time = request_data["start_time"]
    end_valid_time = request_data["end_time"]

    plot_task_template = request_data['plot_task']

    # get data list
    date_list = get_date_list(start_valid_time, end_valid_time)
    for item in date_list.iterrows():
        start_time = item[1]["start_time"]
        forecast_time = item[1]["forecast_time"]

        data_path = find_local_file(
            "grapes_gfs_gmf/grib2/orig",
            start_time=start_time,
            forecast_time=forecast_time,
        )

        if data_path is None:
            logger.warning("WARNING: data is not found", start_time, forecast_time)
            continue

        plot_task = plot_task_template
        plot_task["maplayer"][0]["file_path"] = str(data_path)
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
        logger.info(message)
        config = current_app.config["server_config"]["scheduler"]
        logger.info("send message...")
        send_message(message, config)
        logger.info("send message...done")


def get_date_list(start_valid_time, end_valid_time):
    start_time = pd.to_datetime(start_valid_time[:10], format="%Y%m%d%H")
    start_forecast_time = pd.to_timedelta(int(start_valid_time[10:]), unit="h")
    end_time = pd.to_datetime(end_valid_time[:10], format="%Y%m%d%H")
    end_forecast_time = pd.to_timedelta(int(end_valid_time[10:]), unit="h")

    forecast_hours = pd.to_timedelta(np.append(np.arange(0, 121, 3), np.arange(126, 241, 6)), unit="h").to_series()

    if start_time == end_time:
        forecast_list = forecast_hours[forecast_hours.between(start_forecast_time, end_forecast_time)]
        return pd.DataFrame(
            data={
                "start_time": [start_time] * len(forecast_list),
                "forecast_time": forecast_list.to_list()
            },
            index=forecast_list.map(lambda x: f"{start_time}+{x}")
        )
    else:
        forecast_list = forecast_hours[forecast_hours >= start_forecast_time]
        date_list = pd.DataFrame(
            data={
                "start_time": [start_time] * len(forecast_list),
                "forecast_time": forecast_list.to_list()
            },
            index=forecast_list.map(lambda x: f"{start_time}+{x}")
        )

        for date in pd.date_range(start=start_time + pd.Timedelta(hours=12), end=end_time - pd.Timedelta(hours=12), freq="12h"):
            d = pd.DataFrame(
                data={
                    "start_time": [date] * len(forecast_hours),
                    "forecast_time": forecast_hours.to_list()
                },
                index=forecast_hours.map(lambda x: f"{date}+{x}")
            )
            date_list = date_list.append(d)

        forecast_list = forecast_hours[forecast_hours <= end_forecast_time]
        d = pd.DataFrame(
            data={
                "start_time": [end_time] * len(forecast_list),
                "forecast_time": forecast_list.to_list()
            },
            index=forecast_list.map(lambda x: f"{end_time}+{x}")
        )
        date_list = date_list.append(d)
        return date_list
