import pandas as pd

from ploto_gidat.server.common.giset import get_date_list


def test_get_date_list():
    start_time = pd.to_datetime("2020-11-01 00:00:00")
    end_time = pd.to_datetime("2020-11-03 00:00:00")
    start_hours = [0, 12]
    forecast_length = 96
    forecast_step = 6

    df = get_date_list(
        start_time=start_time,
        end_time=end_time,
        start_hours=start_hours,
        forecast_length=forecast_length,
        forecast_step=forecast_step,
    )
    print(df)


if __name__ == "__main__":
    test_get_date_list()
