# Se importa pandas para leer la web del calendario
import pandas as pd

# Se crea todas las tablas existentes en la url
calendar_all = pd.read_html('https://resultados.as.com/resultados/futbol/segunda/calendario/')

# Se crea la columna jornada para cada una de las tablas
for i in range(len(calendar_all)):
    calendar_all[i]['Jornada'] = i + 1

# Se unen las tablas de cada jornada para tener un único DataFrame
calendario = pd.concat(calendar_all, ignore_index=True).drop_duplicates().drop('Resultado', axis='columns')

# Se renombran las columnas
calendario.columns = ['Local', 'Visitante', 'Jornada']

# Columnas reordenadas

calendario = calendario[['Jornada', 'Local', 'Visitante']]

calendario.to_csv('./../data/calend_smartbank.csv', index=False, sep=',')