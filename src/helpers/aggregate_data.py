import pandas as pd

from helpers.enrich_data import enriched_column_names


def agg_data(trip: pd.DataFrame):
    columns_to_quartile = [
        enriched_column_names.aceleracao_calculada,
        enriched_column_names.aceleracao_calculada_absoluta,
        enriched_column_names.rpm_motor,
        enriched_column_names.velocidade_veiculo,
        # enriched_column_names.aceleracao,
    ]
    column_names = ["min", "max", "mean", "std", "q1", "q2", "q3"]

    proportion = (
        trip[enriched_column_names.aceleracao_calculada_absoluta] > 15
    ).sum() / len(trip)

    trip = (
        trip[columns_to_quartile]
        .agg(
            [
                "min",
                "max",
                "mean",
                "std",
                lambda x: x.quantile(0.25),
                lambda x: x.quantile(0.5),
                lambda x: x.quantile(0.75),
            ]
        )
        .T
    )
    trip.columns = column_names

    trip = trip.stack().reset_index()
    trip.columns = ["variable", "statistic", "value"]
    trip["statistic_variable"] = trip["variable"] + "_" + trip["statistic"]
    trip = trip[["statistic_variable", "value"]]
    trip = trip.set_index("statistic_variable").T
    trip["aceleracao_brusca_por_periodo"] = proportion
    return trip
