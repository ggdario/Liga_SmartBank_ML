import pandas as pd
import numpy as np


def descarga_partidos_temporada_completa():
    """
    Función que descarga todos los partidos de la temporada de segunda division española y lo guarda en un csv
    Por cada partido guarda dos registros, uno por equipo. El formato de cada fila es:
    Jornada, Equipo, Local/Visitante, Rival
    :return:
    """
    partidos = []

    # Recorremos todas las jornadas de la temporada
    for j in range(1, 43):

        # Se lee la tabla con los partidos de la jornada
        partidos_jornada = pd.read_html(f'https://www.resultados-futbol.com/segunda2022/grupo1/jornada{j}',
                                        attrs={'id': 'tabla1'})[0]

        # Cuando ya están determinados los horarios, se general filas que no son necesarias
        if partidos_jornada.shape[0] > 11:
            partidos_jornada.drop(partidos_jornada.head(15).index, inplace=True)

        # Generamos los registros de los equipos locales y visitantes
        partidos_jornada_local = pd.DataFrame(data={'Jornada': np.full(11, j),
                                                    'Equipo': partidos_jornada.iloc[:, 2],
                                                    'Situacion': np.full(11, 'Local'),
                                                    'Rival': partidos_jornada.iloc[:, 4]})

        partidos_jornada_visitante = pd.DataFrame(data={'Jornada': np.full(11, j),
                                                        'Equipo': partidos_jornada.iloc[:, 4],
                                                        'Situacion': np.full(11, 'Visitante'),
                                                        'Rival': partidos_jornada.iloc[:, 2]})

        # Se juntan los registros de local y visitante
        partidos_jornada = pd.concat([partidos_jornada_local, partidos_jornada_visitante], ignore_index=True)
        partidos_jornada.set_index('Jornada', inplace=True)
        partidos.append(partidos_jornada)

    partidos_2022 = pd.concat(partidos)
    partidos_2022.to_csv('../data/partidos.csv', index=True)


def descarga_partidos_jornada_suelta(jornada):
    """
    Función que descarga los partidos de una jornada de segunda division española y lo guarda en un csv
    Por cada partido guarda dos registros, uno por equipo. El formato de cada fila es:
    Jornada, Equipo, Local/Visitante, Rival
    :param jornada: int, jornada que se quiere descargar
    :return:
    """

    # Se lee la tabla con los partidos de la jornada
    partidos_jornada = pd.read_html(f'https://www.resultados-futbol.com/segunda2022/grupo1/jornada{jornada}',
                                    attrs={'id': 'tabla1'})[0]

    # Si los horarios están determinados, se generan filas que son innecesarias
    if partidos_jornada.shape[0] > 11:
        partidos_jornada.drop(partidos_jornada.head(15).index, inplace=True)

    # Se generan los registros locales
    partidos_jornada_local = pd.DataFrame(data={'Jornada': np.full(11, jornada),
                                                'Equipo': partidos_jornada.iloc[:, 2],
                                                'Situacion': np.full(11, 'Local'),
                                                'Rival': partidos_jornada.iloc[:, 4]})

    # Se generan los registros visitantes
    partidos_jornada_visitante = pd.DataFrame(data={'Jornada': np.full(11, jornada),
                                                    'Equipo': partidos_jornada.iloc[:, 4],
                                                    'Situacion': np.full(11, 'Visitante'),
                                                    'Rival': partidos_jornada.iloc[:, 2]})

    # Se juntan los registros local y visitante y se guarda en un csv
    partidos_jornada = pd.concat([partidos_jornada_local, partidos_jornada_visitante], ignore_index=True)
    partidos_jornada.set_index('Jornada', inplace=True)
    partidos_jornada.to_csv(f'../data/partidos_jornada{jornada}.csv', index=True)


if __name__ == '__main__':
    descarga_partidos_jornada_suelta(38)
