# coding=utf-8
"""
GISET distributor.

Send message to GISET when one plot task is finished.

task schema:
    {
        "step_type": "distributor",
        "type": "ploto_gidat.distributor.giset_distributor",

        "username": "niuxingy",
        "user_id": "u0184",
        "routing_key": "GFSNEW.niuxingy",
        "test_ID": "TG2000617",

        # "file_path": ".....",

        "action": "diagnosis",
        "viewip": "10.40.23.43",
        "delivery_mode": 2,
        "payload_encoding": "string"
    }

message schema:
    {
        "properties": {
            "content_type": "application/json",
            "headers": {
                "msgid": task["test_ID"],
                "expid": task["test_ID"],
                "userid": task["user_id"],
                "username": task["username"],
                "viewip": "10.40.23.43",
                "action": "diagnosis",
                "deliver_mode": 2,
            }
        },
        "routing_key": task["routing_key"],
        "playload": task["file_path"],
        "payload_encoding": "string"
    }
"""
import typing
import pathlib
import shutil

from flask import json
import requests
from loguru import logger


def run_distributor(
        task: typing.Dict,
        work_dir: typing.Union[str, pathlib.Path],
        config: typing.Dict
):
    distributor_config = config["giset_distributor"]
    # check image
    work_dir = pathlib.Path(work_dir)
    image_list = list(work_dir.glob("*.png"))

    if len(image_list) == 0:
        logger.warning("no image is found.")
        return

    # copy image
    file_path = image_list[0].absolute()
    logger.info(f"find image: {file_path.name}")

    work_dir_name = work_dir.name
    local_base_dir = distributor_config["archive"]["image"]["local_base_dir"]
    notify_base_dir = distributor_config["archive"]["image"]["notify_base_dir"]

    archive_file_path = pathlib.Path(local_base_dir, work_dir_name + "-1.png")
    notify_file_path = pathlib.Path(notify_base_dir, work_dir_name + "-1.png")

    logger.info(f"copy file to {archive_file_path}")
    shutil.copy2(file_path, archive_file_path)

    # send message
    target_config = distributor_config["target"]
    auth_config = target_config["auth"]
    url = target_config["url"].format(**auth_config)

    data = {
        "properties": {
            "content_type": "application/json",
            "headers": {
                "msgid": task["test_ID"],
                "expid": task["test_ID"],
                "userid": task["user_id"],
                "username": task["username"],
                "viewip": "10.40.23.43",
                "action": "diagnosis",
                "deliver_mode": 2,
            }
        },
        "routing_key": task["routing_key"],
        "playload": str(notify_file_path.absolute()),
        "payload_encoding": "string"
    }

    logger.info(f"post message: {json.dumps(data)}")

    # just for test
    with open(f"request_{work_dir_name}.json", "w") as f:
        json.dump(data, f)

    return

    result = requests.post(
        url, json=data
    )
    return




