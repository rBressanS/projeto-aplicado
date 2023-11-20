import pandas as pd
from concurrent.futures import ProcessPoolExecutor


def mapper(func, data):
    with ProcessPoolExecutor() as executor:
        futures = []
        for driver in data:
            for route in data[driver]:
                for trip_name in data[driver][route]:
                    trip: pd.DataFrame = data[driver][route][trip_name]
                    if trip is not None:
                        futures.append(
                            (executor.submit(func, trip), driver, route, trip_name)
                        )
        for future, driver, route, trip_name in futures:
            data[driver][route][trip_name] = future.result()
    return data
