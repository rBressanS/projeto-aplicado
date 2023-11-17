from dataclasses import dataclass
import pandas as pd
from helpers.clear_data import column_names, ColumnNames


@dataclass
class EnrichedColumnNames(ColumnNames):
    aceleracao_calculada: str = "aceleracao_calculada"
    aceleracao_calculada_absoluta: str = "aceleracao_calculada_absoluta"


enriched_column_names = EnrichedColumnNames()


def enrich_data(trip: pd.DataFrame):
    trip[enriched_column_names.aceleracao_calculada] = trip[
        column_names.velocidade_veiculo
    ].diff()

    trip[enriched_column_names.aceleracao_calculada_absoluta] = trip[
        enriched_column_names.aceleracao_calculada
    ].abs()
    trip = trip[trip[column_names.velocidade_veiculo] > 0]
    return trip
