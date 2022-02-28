# Evaluate the month of February in 2022 to obtain results with the test csv.

from datetime import datetime

import matplotlib.pyplot as plt
import numpy
import pandas
from matplotlib.dates import DateFormatter, DayLocator


def get_data_from_csv():
    # Date format
    custom_date_parser = lambda x: datetime.strptime(x, "%d-%m-%Y %H:%M:%S")

    # Import data from csv and convert to date format
    dataframe = pandas.read_csv('data.csv',
                                parse_dates=['arrival_date', 'departure_date'],
                                date_parser=custom_date_parser)
    dataframe['time_warehouse'] = pandas.to_timedelta(dataframe['time_warehouse'])

    return dataframe


def dates_from_month(month, year):
    # Format for start date and end date
    start_date = f"{year}-{month}-1"
    start_date = pandas.to_datetime(start_date)
    # In case it is the last month of the year
    if month == 12:
        stop_date = f"{year + 1}-1-1"
    else:
        stop_date = f"{year}-{month + 1}-1"
    stop_date = pandas.to_datetime(stop_date)

    return numpy.arange(start_date, stop_date, dtype='datetime64[D]')


def graphing_statistics(month, year, pedidos_activos, days_array):
    # Get the full name of the month
    datetime_object = datetime.strptime(str(month), "%m")
    month_name = datetime_object.strftime("%B")

    # Graphing statistics
    date_form = DateFormatter("%d-%m")
    fig, ax = plt.subplots(figsize=(15, 8))
    ax.plot(days_array, pedidos_activos, label=month_name, marker='o')
    ax.legend(loc='upper right')
    ax.set_ylabel('Number of active packages')
    ax.set_xlabel('Date')
    ax.set_title(f"Monthly Consolidated\n{month_name} - {year}")
    ax.xaxis.set_major_formatter(date_form)
    ax.xaxis.set_major_locator(DayLocator(interval=2))
    ax.grid(axis='y', color='gray', linestyle='dashed')
    plt.show()


def monthly_consolidated(month, year):
    # Import the dataframe extracted from csv
    dataframe = get_data_from_csv()

    # Create an array of dates in the selected month
    days_array = dates_from_month(month, year)

    # Fill in the number of active orders per days in the selected month
    active_package = []
    for day in days_array:
        sum = 0
        for i in range(len(dataframe)):
            if dataframe['arrival_date'][i] <= day <= dataframe['departure_date'][i]:
                sum += 1
        active_package.append(sum)

    # Graphing statistics
    graphing_statistics(month, year, active_package, days_array)


if __name__ == '__main__':
    # Data validation
    while True:
        try:
            month = int(input("Enter the number of the month to be evaluated: "))
            year = int(input("Enter the number of the year to be evaluated: "))
            if 1 <= month <= 12 and 1 <= year <= 9999:
                break
            else:
                print('Enter a valid month or year number')
        except ValueError:
            print("Oops!  That was no valid number.  Try again...")
    monthly_consolidated(month, year)
