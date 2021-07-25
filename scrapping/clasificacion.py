#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from data_processing.procesado_clasifcacion import procesar_clasificacion


def descarga_clasificacion(url='https://www.resultados-futbol.com/segunda2021/grupo1/jornada41'):
    """
    :param url: url sobre la que descargar los resultados
    :return:
    """

    # Se obtiene la jornada del enlace
    jornada = int(url.split('/jornada')[-1])

    # Obtenemos la tabla de la clasificacion
    clasif = pd.read_html(url, attrs={'id': 'tabla2'})[0]

    # Se escogen únicamente algunas de las columnas
    clasif = clasif[['Equipos', 'Equipos.1', 'Puntos', 'J.', 'G.', 'E.', 'P.', 'F.', 'C.']]

    # Se renombran las columnas
    clasif.rename(columns={'Equipos': 'Posicion', 'Equipos.1': 'Equipo', 'J.': 'J',
                           'G.': 'G', 'E.': 'E', 'P.': 'P', 'F.': 'F', 'C.': 'C'}, inplace=True)

    # Se incluye la columna jornada y se establece como índice
    clasif['Jornada'] = jornada
    clasif.set_index(['Jornada'], inplace=True)

    # Cargamos el archivo de clasificacion existente
    clasif_existente = pd.read_csv('../data/clasif.csv', index_col=0)

    # Se comprueba si la jornada ya se descargó anteriormente y de ser así, se reemplaza
    if jornada in clasif_existente.index.unique():
        clasif_existente.drop(jornada, inplace=True)

    # Se une la clasificacion existente y la actual
    clasif = pd.concat([clasif_existente, clasif])
    clasif.sort_values(by=['Jornada', 'Posicion'], inplace=True)

    # Se guarda
    clasif.to_csv('../data/clasif.csv', index=True)

    procesar_clasificacion()

    return 0


if __name__ == '__main__':

    descarga_clasificacion()
