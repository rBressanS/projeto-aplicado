from pathlib import Path
import pandas as pd


def normalize(name: str):
    return name.replace(" ", "_").lower()


def get_all_csv_data(directory: Path) -> pd.DataFrame:
    csv_files = list(directory.glob("*.csv"))
    if not csv_files:
        return None
    dfs = []
    for file in csv_files:
        df = pd.read_csv(file, decimal=".", sep=",")
        df["file"] = file.name
        df.index = pd.to_datetime(df["time"], format="%H:%M:%S.%f")
        df = df.resample("5S").last().interpolate(method="time")
        dfs.append(df)
    return pd.concat(dfs)


def get_all_trips(route_dir: Path) -> dict:
    return {
        normalize(trip.name): get_all_csv_data(trip)
        for trip in route_dir.iterdir()
        if trip.is_dir()
    }


def get_all_routes(driver_dir: Path) -> dict:
    return {
        normalize(route.name): get_all_trips(route)
        for route in driver_dir.iterdir()
        if route.is_dir()
    }


def get_data(data_path: str = None) -> dict:
    if data_path is None:
        data_path = Path.cwd() / "data"
    else:
        data_path = Path(data_path)
    return {
        normalize(driver.name): get_all_routes(driver)
        for driver in data_path.iterdir()
        if driver.is_dir()
    }


if __name__ == "__main__":
    print(get_data())
