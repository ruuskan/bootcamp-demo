import numpy as np
import matplotlib.pyplot as plt
import datetime
from database.operations import search_between
from analysis import aplot

cpi = np.genfromtxt(fname='elinkustannusindeksi.csv',skip_header=3, delimiter=';',converters={0: lambda x: float(x.decode('utf-8').strip('"'))})
euro_conversion = 5.94573
euro_start = 2002

def __value_conversion(st_year, comp_year):
    st_cpi = cpi[cpi[:,0]==st_year,1][0]
    comp_cpi = cpi[cpi[:,0]==comp_year,1][0]
    st_euro = euro_conversion if st_year < euro_start else 1
    comp_euro = euro_conversion if comp_year < euro_start else 1

    conversion_rate = comp_euro*comp_cpi/(st_euro*st_cpi)
    return conversion_rate

def __array_convert(strarray):
    if strarray.split('[')[1].split(']')[0] != '':
        arr = [int(el.strip("' ")) for el in strarray.split('[')[1].split(']')[0].split(',')]
    else:
        arr = []
    return arr

def __data_from_query(query):
    dates = []
    primary = []
    secondary = []
    tertiary = []
    share_count = []
    share_amount = []
    tiers = []

    for row in query:
        dates.append(row.date)
        primary.append(__array_convert(row.primary))
        secondary.append(__array_convert(row.secondary))
        tertiary.append(__array_convert(row.tertiary))
        share_count.append(__array_convert(row.share_count))
        share_amount.append(__array_convert(row.share_amount))
        tiers.append(row.tier_name)

    data = {'date':dates,'primary':primary,'secondary':secondary,'tertiary':tertiary,'share_count':share_count}
    return data

def __primary_stats(data):
    number_count = [0]*40
    number_freq = np.zeros((40,40))
    test = 0
    for nums in data['primary']:
        for num1 in nums:
            for num2 in nums:
                (number_freq[num1-1])[num2-1] += 1
    return (number_freq)

def __heatmap(datamat):

    plt.ioff()
    numbers = [f"{x+1}" for x in range(40)]

    fig, ax = plt.subplots()
    fig.set_size_inches(16,16)
    im = ax.imshow(datamat,cmap='YlGn')
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel('Counts', rotation=-90, va="bottom")

    ax.set_xticks(np.arange(len(numbers)))
    ax.set_yticks(np.arange(len(numbers)))

    ax.set_xticklabels(numbers)
    ax.set_yticklabels(numbers)

    plt.setp(ax.get_xticklabels(), rotation=90, ha="right",va='center',
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(numbers)):
        for j in range(len(numbers)):
            text = ax.text(j, i, datamat[i, j],
                        ha="center", va="center", color="w")

    ax.set_title("Lottery number frequencies with other numbers")
    fig.tight_layout()
    plt.savefig('static/pictures/number_frequencies.svg',format='svg')
    return True

def __barplot():
    #TODO
    return True

def data_analysis(dt_start, dt_end):
    res = search_between(dt_start,dt_end)
    data = __data_from_query(res)
    number_freq = __primary_stats(data)
    __heatmap(number_freq)
    __barplot() 

    1+1
    return 1