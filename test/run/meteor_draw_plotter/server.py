import requests
import json


def run():
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
                    "level_num": -842150451,
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
    requests.post(
        url="http://localhost:6301/api/v1/gidat/plot/meteor_draw/example",
        data={
            "plot_task": json.dumps(plot_task),
        }
    )


if __name__ == "__main__":
    run()
