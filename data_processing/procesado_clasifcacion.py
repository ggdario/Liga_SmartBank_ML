#!/usr/bin/env python
# coding: utf-8

import pandas as pd


def calculo_resultado(x):
    """
    Función que devuelve si un partido acaba en victoria, empate
    o derrota en función de la diferencia numérica de goles

    :param x: valor numérico sobre el que se calcula el resultado
    :return: valor de victoria (V), empate (E), o derrota (D)
    """
    if x > 0:
        return 'V'
    elif x < 0:
        return 'D'
    elif x == 0:
        return 'E'
    else:
        pass


def zona_tabla(x):
    """
    Función que devuelve la zona de la tabla en función de la posición

    :param x: Posición numérica en la tabla
    :return: Zona de la tabla
    """
    if x <= 2:
        return 'Asc Directo'
    elif x <= 6:
        return 'Play off'
    elif x <= 11:
        return 'Media Alta'
    elif x <= 17:
        return 'Media Baja'
    else:
        return 'Descenso'


def procesar_clasificacion():
    """
    Función que calcula valores nuevos a partir de los descargados de la web
    :return:
    """

    # Lectura de la clasificación descargada de internet y ordenación por jornada
    clasif_orig = pd.read_csv('../data/clasif.csv', index_col=0)
    clasif_orig.sort_values(by='Jornada', inplace=True)

    # Cálculo de los puntos de los equipos en cada jornada
    clasif_orig['Puntos Jornada'] = clasif_orig.groupby('Equipo')['Puntos'].transform(lambda x: x - x.shift())

    # Media a 3 y 5 partidos de los equipos a lo largo de la liga
    clasif_orig['Puntos 3J'] = clasif_orig.groupby('Equipo')['Puntos Jornada'].transform(lambda x: x.rolling(3).mean())
    clasif_orig['Puntos 5J'] = clasif_orig.groupby('Equipo')['Puntos Jornada'].transform(lambda x: x.rolling(5).mean())

    # Obtención de la zona de la tabla en la que se encontraban los equipos
    clasif_orig['Zona'] = clasif_orig['Posicion'].apply(lambda x: zona_tabla(x))

    # Media de puntos a lo largo de la temporada
    clasif_orig['Media Puntos'] = clasif_orig['Puntos'] / clasif_orig['J']

    # Goles a favor, en contra y diferencia en la última jornada
    clasif_orig['F ultima'] = clasif_orig.groupby('Equipo')['F'].transform(lambda x: x - x.shift(1))
    clasif_orig['C ultima'] = clasif_orig.groupby('Equipo')['C'].transform(lambda x: x - x.shift(1))
    clasif_orig['Dif ultima'] = clasif_orig['F ultima'] - clasif_orig['C ultima']

    # Escritua de victoria (V), empate (E) o derrota (D) en la última jornada
    clasif_orig['Res ultima'] = clasif_orig['Dif ultima'].apply(lambda x: calculo_resultado(x))

    # Guardado de los datos
    clasif_orig.to_csv('../data/clasif_procesada.csv', index=True)


if __name__ == '__main__':
    procesar_clasificacion()
