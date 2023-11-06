from get_data import get_data
import pandas as pd

from dataclasses import dataclass, fields, asdict


@dataclass
class __ColumnNames:
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


column_names = __ColumnNames()


def get_clear_data():
    data = get_data()
    for driver in data:
        for route in data[driver]:
            for trip_name in data[driver][route]:
                trip: pd.DataFrame = data[driver][route][trip_name]
                # convert time column to datetime with format of HH:MM:SS.000
                trip.index = pd.to_datetime(trip["time"], format="%H:%M:%S.%f")
                trip.rename(
                    columns={col: col.lower() for col in trip.columns}, inplace=True
                )
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
                        "longitude": column_names.longitude_gps,
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
                trip.fillna(method="ffill", inplace=True)
                trip.fillna(method="bfill", inplace=True)
    return data


if __name__ == "__main__":
    data = get_clear_data()
    print(data)
