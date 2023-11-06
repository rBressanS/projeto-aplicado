from pathlib import Path
from typing import Iterable
import pandas as pd


def normalize(name: str):
    return name.replace(" ", "_").lower()


def get_all_csv_data(directory: Path) -> pd.DataFrame:
    csv_files = list(directory.glob("*.csv"))
    if not csv_files:
        return None
    return pd.concat([pd.read_csv(file, decimal=".", sep=",") for file in csv_files])


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


def get_data() -> dict:
    data_path = Path.cwd() / "data"
    return {
        normalize(driver.name): get_all_routes(driver)
        for driver in data_path.iterdir()
        if driver.is_dir()
    }


if __name__ == "__main__":
    print(get_data())
