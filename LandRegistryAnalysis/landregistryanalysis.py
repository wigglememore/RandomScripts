import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

file_name = r"28012023_paxton_semi_freehold_standard.csv"


def plot_price_vs_year_scatter(input_dataframe: pd.DataFrame) -> None:
    """plot every sale, year vs price, just for fun
    take in the dataframe from the imported csv"""
    date = input_dataframe["deed_date"]
    price = input_dataframe["price_paid"]
    date_year = [d[:4] for d in date] #take just the year from the date
    date_sorted, price_sorted = zip(*sorted(zip(date_year, price))) #sort into year order
    fig, ax = plt.subplots()
    ax.scatter(date_sorted, price_sorted)
    plt.title('All Prices')
    plt.xlabel('Year')
    plt.ylabel('Price')
    plt.show()


def plot_price_increase_line(input_lolol: list) -> None:
    """plot line graph for each housing showing price history,
    take in list-of-lists-of-lists"""
    dates = np.array(input_lolol[0][0])
    for entry in input_lolol:
        p = np.array(entry[1]).astype(np.double)
        pmask = np.isfinite(p)
        plt.plot(dates[pmask], p[pmask])
    plt.title('House Price History')
    plt.xlabel('Year')
    plt.ylabel('Price')
    plt.show()


def calculate_gradient(x: list, y: list) -> float:
    if len(set(x)) == 1:
        return None
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    if slope < 0:
        return None
    return slope


def calculate_current_value(first_sold: int, first_price: int, gradient: float) -> int:
    return first_price + (2023 - first_sold) * gradient


def current_value(input_file, house_request_no, house_request_road) -> int:
    #open csv
    col_names = ["price_paid", "deed_date", "paon", "street"]
    df = pd.read_csv(file_name,usecols=col_names)
    #check request exists
    #row_num_request = df[(df['paon'] == str(house_request_no)) & (df['street'] == house_request_road)].index.tolist()[0]
    ###plot_price_vs_year_scatter(df)
    
    df["house"] = df["paon"] + " " + df["street"] #make new col of house number and road name 
    df["year"] = df.deed_date.str[:4].astype(int) #extract year from full date
    df["price_paid"] = df["price_paid"].astype(int)
    df2 = df[["house","year","price_paid"]] #create new df to make dict from
    df2.set_index("house", inplace=True) #set index to house name
    all_registry_entries = {k: g.to_dict(orient='records') for k, g in df2.groupby(level=0)} #turn into dict, preserve duplicate indices
    multiple_sale_entries = {a: b for a,b in all_registry_entries.items() if len(b) > 1} #extract only those with more than one sale
    
    #line plot of each dict entry and gradient calculation
    min_year = df2["year"].min()
    max_year = df2["year"].max()
    date_axis = list(range(min_year, max_year + 1))
    sales_for_line_plot = []
    slopes = []
    for house in multiple_sale_entries.values():
        dates = []
        prices = []
        for sale in house:
            dates.append(sale["year"])
            prices.append(sale["price_paid"])
        slopes.append(calculate_gradient(dates, prices))
        price_axis = [None] * len(date_axis)
        for year in dates:
            index = date_axis.index(year)
            price_axis[index] = prices[dates.index(year)]
        sales_for_line_plot.append([date_axis, price_axis])
    ###plot_price_increase_line(sales_for_line_plot)
    slopes = [i for i in slopes if i is not None]
    #calculate current value
    gordon = all_registry_entries[str(63) + " " + "GORDON ROAD"]
    return calculate_current_value(gordon[0]["year"], gordon[0]["price_paid"], np.average(slopes))


if __name__ == "__main__":
    house_number = 63
    house_road = "Gordon Road"
    print(f"Current price of {house_number} {house_road} should be {current_value(file_name, house_number, house_road.upper())}")
    