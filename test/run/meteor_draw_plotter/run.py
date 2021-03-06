from ploto_gidat.server.common.gidat import run_meteor_draw_task
import warnings


def run():
    """
    Warnings
    --------
    This example is not worked.
    """
    warnings.warn("This example can't run.")
    plot_task = {
        "maplayer": [
            {
                "coutourdata": {
                    "level_num": 18,
                    "levelcolorsarray": [
                        11949068,
                        15429150,
                        15761960,
                        16094780,
                        16098640,
                        16431480,
                        16437910,
                        16445620,
                        11205375,
                        7990271,
                        3981567,
                        41215,
                        24831,
                        13055,
                        5375,
                        192,
                        165,
                        165
                    ],
                    "levelvaluesarray": [
                        243,
                        246.94119262695312,
                        250.8824005126953,
                        254.82350158691406,
                        258.76470947265625,
                        262.7059020996094,
                        266.6470947265625,
                        270.58819580078125,
                        274.5293884277344,
                        278.4706115722656,
                        282.41180419921875,
                        286.3529052734375,
                        290.2940979003906,
                        294.23529052734375,
                        298.176513671875,
                        302.11761474609375,
                        306.0588073730469,
                        310
                    ],
                    "levelwidthsarray": [
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1,
                        1
                    ],
                    "pValueTrans": "0"
                },
                "file_path": "/sstorage1/COMMONDATA/OPER/NWPC/GRAPES_GFS_GMF/Prod-grib/2020021921/ORIG/gmf.gra.2020022000234.grb2",
                "filldata": {
                    "level_num": -842150451,
                    "levelcolorsarray": [
                        11949068,
                        15429150,
                        15761960,
                        16094780,
                        16098640,
                        16431480,
                        16437910,
                        16445620,
                        11205375,
                        7990271,
                        3981567,
                        41215,
                        24831,
                        13055,
                        5375,
                        192,
                        165,
                        165
                    ],
                    "levelvaluesarray": [
                        243,
                        246.94119262695312,
                        250.8824005126953,
                        254.82350158691406,
                        258.76470947265625,
                        262.7059020996094,
                        266.6470947265625,
                        270.58819580078125,
                        274.5293884277344,
                        278.4706115722656,
                        282.41180419921875,
                        286.3529052734375,
                        290.2940979003906,
                        294.23529052734375,
                        298.176513671875,
                        302.11761474609375,
                        306.0588073730469,
                        310
                    ],
                    "levelwidthsarray": [
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0
                    ],
                    "pValueTrans": ""
                },
                "paint_type": "contour",
                "prjType": 2
            },
            {
                "coutourdata": {
                    "level_num": 18,
                    "levelcolorsarray": [
                        11949068,
                        15429150,
                        15761960,
                        16094780,
                        16098640,
                        16431480,
                        16437910,
                        16445620,
                        11205375,
                        7990271,
                        3981567,
                        41215,
                        24831,
                        13055,
                        5375,
                        192,
                        165,
                        165
                    ],
                    "levelvaluesarray": [
                        243,
                        246.94119262695312,
                        250.8824005126953,
                        254.82350158691406,
                        258.76470947265625,
                        262.7059020996094,
                        266.6470947265625,
                        270.58819580078125,
                        274.5293884277344,
                        278.4706115722656,
                        282.41180419921875,
                        286.3529052734375,
                        290.2940979003906,
                        294.23529052734375,
                        298.176513671875,
                        302.11761474609375,
                        306.0588073730469,
                        310
                    ],
                    "levelwidthsarray": [
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0
                    ],
                    "pValueTrans": "0"
                },
                "file_path": "/sstorage1/COMMONDATA/OPER/NWPC/GRAPES_GFS_GMF/Prod-grib/2020021921/ORIG/gmf.gra.2020022000234.grb2",
                "filldata": {
                    "level_num": -842150451,
                    "levelcolorsarray": [
                        11949068,
                        15429150,
                        15761960,
                        16094780,
                        16098640,
                        16431480,
                        16437910,
                        16445620,
                        11205375,
                        7990271,
                        3981567,
                        41215,
                        24831,
                        13055,
                        5375,
                        192,
                        165,
                        165
                    ],
                    "levelvaluesarray": [
                        243,
                        246.94119262695312,
                        250.8824005126953,
                        254.82350158691406,
                        258.76470947265625,
                        262.7059020996094,
                        266.6470947265625,
                        270.58819580078125,
                        274.5293884277344,
                        278.4706115722656,
                        282.41180419921875,
                        286.3529052734375,
                        290.2940979003906,
                        294.23529052734375,
                        298.176513671875,
                        302.11761474609375,
                        306.0588073730469,
                        310
                    ],
                    "levelwidthsarray": [
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0
                    ],
                    "pValueTrans": ""
                },
                "paint_type": "contour",
                "prjType": 0
            }
        ]
    }
    run_meteor_draw_task(plot_task)


if __name__ == "__main__":
    run()
