# Evaluar el mes de febrero en el 2022 para obtener resultados con el csv de prueba

from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, DayLocator


def csv_import():
    # Formato de fecha
    custom_date_parser = lambda x: datetime.strptime(x, "%d-%m-%Y %H:%M:%S")

    # Importar de datos desde el csv y convertirlos en formato de fecha
    df = pd.read_csv('data.csv',
                     parse_dates=['arrival_date', 'departure_date'],
                     date_parser=custom_date_parser)
    df['time_warehouse'] = pd.to_timedelta(df['time_warehouse'])

    return df


def dates_from_month(month, year):
    # Formato para fecha inicial y fecha final
    start_date = str(year) + '-' + str(month) + '-1'
    start_date = pd.to_datetime(start_date)
    # En caso de que sea el último mes del año
    if month == 12:
        stop_date = str(year + 1) + '-1-1'
    else:
        stop_date = str(year) + '-' + str(month + 1) + '-1'
    stop_date = pd.to_datetime(stop_date)

    return np.arange(start_date, stop_date, dtype='datetime64[D]')


def consolidado_mensual(month, year):
    # Importar el dataframe extraído del csv
    df = csv_import()

    # Crear array de fechas en el mes seleccionado
    days_array = dates_from_month(month, year)

    # Llenar el número de pedidos activos por días en el mes seleccionado
    pedidos_activos = []
    for day in days_array:
        sum = 0
        for i in range(len(df)):
            if df['arrival_date'][i] <= day <= df['departure_date'][i]:
                sum += 1
        pedidos_activos.append(sum)

    # Obtener el nombre completo del mes
    datetime_object = datetime.strptime(str(month), "%m")
    month_name = datetime_object.strftime("%B")

    # Graficar estadísticas
    date_form = DateFormatter("%d-%m")
    fig, ax = plt.subplots(figsize=(15, 8))
    ax.plot(days_array, pedidos_activos, label=month_name, marker='o')
    ax.legend(loc='upper right')
    ax.set_ylabel('Número de paquetes activos')
    ax.set_xlabel('Día del mes')
    ax.set_title("Número de paquetes en bodega por día")
    ax.xaxis.set_major_formatter(date_form)
    ax.xaxis.set_major_locator(DayLocator(interval=2))
    ax.grid(axis='y', color='gray', linestyle='dashed')
    plt.show()


if __name__ == '__main__':
    # Validación de datos
    while True:
        try:
            mes = int(input("Escriba el número del mes a evaluar: "))
            anio = int(input("Escriba el número del año a evaluar: "))
            if 1 <= mes <= 12:
                break
            else:
                print('Ingrese un número de mes valido')
        except ValueError:
            print("Oops!  That was no valid number.  Try again...")
    consolidado_mensual(mes, anio)
