import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np

file_name = r"28012023_paxton_semi_freehold_standard.csv"


def plot_price_vs_year(input_dataframe) -> None:
    """plot every sale, year vs price, just for fun
    take in the dataframe from the imported csv"""
    date = input_dataframe["deed_date"]
    price = input_dataframe["price_paid"]
    date_year = [d[:4] for d in date] #take just the year from the date
    date_sorted, price_sorted = zip(*sorted(zip(date_year, price))) #sort into year order
    fig, ax = plt.subplots()
    ax.scatter(date_sorted, price_sorted)
    plt.show()


def current_value(input_file, house_request_no, house_request_road) -> int:
    #open csv
    col_names = ["price_paid", "deed_date", "paon", "street"]
    df = pd.read_csv(file_name,usecols=col_names)
    #check request exists
    row_num_request = df[(df['paon'] == str(house_request_no)) & (df['street'] == house_request_road)].index.tolist()[0]
    print(f"Row is {row_num_request}")
    plot_price_vs_year(df)
    
    #loop through rows
    #for each no + street combo, find all entries
    #if only one entry, ignore
    
    
    return 999999


if __name__ == "__main__":
    house_number = 63
    house_road = "Gordon Road"
    print(f"Current price of {house_number} {house_road} should be {current_value(file_name, house_number, house_road.upper())}")
    