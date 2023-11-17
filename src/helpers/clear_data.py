from helpers.get_data import get_data
import pandas as pd

from dataclasses import dataclass, fields

from helpers.mapper import mapper


@dataclass
class ColumnNames:
    aceleracao: str = "aceleracao"
    altitude_gps: str = "altitude_gps"
    distancia_percorrida: str = "distancia_percorrida"
    distancia_percorrida_total: str = "distancia_percorrida_total"
    espaco_livre_no_tanque_combustivel: str = "espaco_livre_no_tanque_combustivel"
    nivel_combustivel_porcentagem: str = "nivel_combustivel_porcentagem"
    nivel_combustivel_litros: str = "nivel_combustivel_litros"
    posicao_acelerador_d: str = "posicao_acelerador_d"
    posicao_acelerador_e: str = "posicao_acelerador_e"
    rpm_motor: str = "rpm_motor"
    temperatura_arrefecimento: str = "temperatura_arrefecimento"
    velocidade_gps: str = "velocidade_gps"
    velocidade_veiculo: str = "velocidade_veiculo"
    velocidade_media: str = "velocidade_media"
    velocidade_media_gps: str = "velocidade_media_gps"
    latitude_gps: str = "latitude_gps"
    longitude_gps: str = "longitude_gps"
    file: str = "file"


column_names = ColumnNames()


def clear_data(trip: pd.DataFrame) -> pd.DataFrame:
    # convert time column to datetime with format of HH:MM:SS.000
    # trip.index = pd.to_datetime(trip["time"], format="%H:%M:%S.%f")
    trip.rename(columns={col: col.lower() for col in trip.columns}, inplace=True)
    trip.rename(
        columns={
            "aceleração (m/s²)": column_names.aceleracao,
            "altitude (gps) (m)": column_names.altitude_gps,
            "distância percorrida (km)": column_names.distancia_percorrida,
            "distância percorrida (total) (km)": column_names.distancia_percorrida_total,
            "espaço livre no tanque de combustível (l)": column_names.espaco_livre_no_tanque_combustivel,
            "nível de combustível (%) (%)": column_names.nivel_combustivel_porcentagem,
            "nível de combustível (v) (l)": column_names.nivel_combustivel_litros,
            "posição do pedal do acelerador d (%)": column_names.posicao_acelerador_d,
            "posição do pedal do acelerador e (%)": column_names.posicao_acelerador_e,
            "rpm do motor (rpm)": column_names.rpm_motor,
            "temperatura do líquido de \r\narrefecimento do motor (℃)": column_names.temperatura_arrefecimento,
            "velocidade (gps) (km/h)": column_names.velocidade_gps,
            "velocidade do veículo (km/h)": column_names.velocidade_veiculo,
            "velocidade média (km/h)": column_names.velocidade_media,
            "velocidade média (gps) (km/h)": column_names.velocidade_media_gps,
            "latitude": column_names.latitude_gps,
            "longtitude": column_names.longitude_gps,
            "file": column_names.file,
        },
        inplace=True,
    )
    trip.drop(
        columns=[
            col
            for col in trip.columns
            if col not in map(lambda x: x.name, fields(column_names))
        ],
        inplace=True,
    )

    trip[column_names.posicao_acelerador_d] = trip[
        column_names.posicao_acelerador_d
    ].apply(
        lambda x: (x - trip[column_names.posicao_acelerador_d].min())
        / (
            trip[column_names.posicao_acelerador_d].max()
            - trip[column_names.posicao_acelerador_d].min()
        )
        * 100
    )
    trip[column_names.posicao_acelerador_e] = trip[
        column_names.posicao_acelerador_e
    ].apply(
        lambda x: (x - trip[column_names.posicao_acelerador_e].min())
        / (
            trip[column_names.posicao_acelerador_e].max()
            - trip[column_names.posicao_acelerador_e].min()
        )
        * 100
    )
    return trip


def get_clean_data():
    data = get_data()
    clean_data = mapper(clear_data, data)
    return clean_data


if __name__ == "__main__":
    data: dict = get_clean_data()
    for driver, driver_obj in data.items():
        print(driver)
        for route, route_obj in driver_obj.items():
            print("\t" + route)
            for trip, trip_obj in route_obj.items():
                print("\t\t" + trip)
                print("\t\t\t" + str(trip_obj.shape) + str(list(trip_obj.columns)))

    # print(data)
