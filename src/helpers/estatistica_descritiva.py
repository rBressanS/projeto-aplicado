from clear_data import clear_data
from enrich_data import enrich_data
from get_data import get_data
from mapper import mapper
import pandas as pd


if __name__ == "__main__":
    data = get_data()
    clean_data = mapper(clear_data, data)
    enriched_data = mapper(enrich_data, clean_data)
    df: pd.DataFrame = None
    for driver in enriched_data:
        for route in enriched_data[driver]:
            for trip_name in enriched_data[driver][route]:
                trip = enriched_data[driver][route][trip_name]
                trip["driver"] = driver
                trip["route"] = route
                trip["trip"] = trip_name
                if df is None:
                    df = trip
                else:
                    df = pd.concat([df, trip])
    from ydata_profiling import ProfileReport

    profile = ProfileReport(df, title="Pandas Profiling Report")
    profile.to_file("report.html")
