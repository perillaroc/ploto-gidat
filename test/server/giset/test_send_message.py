import requests
import json


def receive_message():
    plot_task = {
        "maplayer": [
            {
                "typeOfLevel": "surface",
                "paint_type": "contour",
                "filldata": {
                    "levelwidthsarray": [
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1
                    ],
                    "level_num": 7,
                    "levelvaluesarray": [
                        0.10000000149011612,
                        10,
                        25,
                        50,
                        100,
                        200,
                        0
                    ],
                    "pValueTrans": "",
                    "levelcolorsarray": [
                        16777215,
                        5950882,
                        2263842,
                        16760320,
                        16711936,
                        16187642,
                        5245579
                    ]
                },
                "level": "0",
                "file_identification": "grapes_gfs",
                "coutourdata": {
                    "levelwidthsarray": [
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1
                    ],
                    "level_num": 7,
                    "levelvaluesarray": [
                        0.10000000149011612,
                        10,
                        25,
                        50,
                        100,
                        200,
                        0
                    ],
                    "pValueTrans": "0",
                    "levelcolorsarray": [
                        16777215,
                        5950882,
                        2263842,
                        16760320,
                        16711936,
                        16187642,
                        5245579
                    ]
                },
                "prjType": "liner",
                "cal_template": "accumulated deficiency",
                "shortName": "acpcp",
                "meteor_type": "rainfall",
                "file_path": "/sstorage1/COMMONDATA/OPER/NWPC/GRAPES_GFS_GMF/Prod-grib/2020021921/ORIG/gmf.gra.2020022000234.grb2"
            }
        ]
    }

    data = {
        "data_source": {
            "system_name": "grapes_gfs_gmf",
            "username": "niuxingy",
            "user_id": "u0184",
            "data_type": "storage",
            "routing_key": "GFSNEW.niuxingy",
            "test_ID": "TG2000639"
        },
        "start_time": "2020051012000",
        "step": "6",
        "hh_list": [
            "12"
        ],
        "end_time": "2020051512000",
        "fcstlen": "24",
        "plot_task": plot_task
    }


    requests.post(
        url="http://10.40.23.43:6301/api/v1/giset/plot/meteor-draw/ploto",
        json=data,
    )


if __name__ == "__main__":
    receive_message()
