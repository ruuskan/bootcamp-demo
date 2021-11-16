import numpy as np
import matplotlib.pyplot as plt
import datetime
from database.operations import search_between

cpi = np.genfromtxt(fname='elinkustannusindeksi.csv',skip_header=3, delimiter=';',converters={0: lambda x: float(x.decode('utf-8').strip('"'))})
euro_conversion = 5.94573
euro_start = 2002

def __value_conversion(st_year, comp_year):
    """
    Returns float

    Get conversion rate of Finnish currency from starting year and the effective value in comparison year

    Parameters:
    st_year: int for starting year
    comp_year: int for comparison year
    """
    st_year = 2020 if st_year > 2020 else st_year
    comp_year = 2020 if comp_year > 2020 else comp_year
    st_cpi = cpi[cpi[:,0]==st_year,1][0]
    comp_cpi = cpi[cpi[:,0]==comp_year,1][0]
    st_euro = euro_conversion if st_year < euro_start else 1
    comp_euro = euro_conversion if comp_year < euro_start else 1

    conversion_rate = comp_euro*comp_cpi/(st_euro*st_cpi)
    return conversion_rate

def __array_convert(strarray):
    """
    Returns list

    Make stringified arrays (lists) to lists

    Parameters:
    strarray: stringified array from database
    """
    if strarray.split('[')[1].split(']')[0] != '':
        arr = [int(el.strip("' ")) for el in strarray.split('[')[1].split(']')[0].split(',')]
    else:
        arr = []
    return arr

def __data_from_query(query):
    """
    Returns dictionary of lists

    Transforms data from database to easier format

    Parameters:
    query: sqlalchemy query object
    """
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

    data = {'date':dates,'primary':primary,'secondary':secondary,'tertiary':tertiary,'share_count':share_count,
            'share_amount' : share_amount, 'tier_names' : tiers}
    return data

def __primary_stats(data):
    """
    Returns numpy ndarray

    Get the occurrances of primary numbers in winning lines

    Parameters:
    data: dictionary of data
    """
    number_freq = np.zeros((40,40))
    for nums in data['primary']:
        for num1 in nums:
            for num2 in nums:
                (number_freq[num1-1])[num2-1] += 1
    return (number_freq)

def __heatmap(datamat):
    """
    Plotting heatmap

    Parameters:
    datamat: numpy ndarray object of data to be plotted
    """
    datamat = np.triu(datamat)
    plt.ioff()
    numbers = [f"{x+1}" for x in range(40)]

    fig, ax = plt.subplots()
    fig.set_size_inches(10,10)
    im = ax.imshow(datamat,cmap='YlGn')
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel('Counts', rotation=-90, va="bottom")

    ax.xaxis.tick_top()
    ax.set_xticks(np.arange(len(numbers)))
    ax.set_yticks(np.arange(len(numbers)))

    ax.set_xticklabels(numbers)
    ax.set_yticklabels(numbers)

    plt.setp(ax.get_xticklabels(), rotation=90, ha="left",va='center',
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    # for i in range(len(numbers)):
    #     for j in range(len(numbers)):
    #         text = ax.text(j, i, datamat[i, j],
    #                     ha="center", va="center", color="w")

    ax.set_title("Lottery number frequencies with other numbers")
    fig.tight_layout()
    plt.savefig('static/pictures/a_number_frequencies.svg',format='svg')
    plt.close()
    return True

def __interesting_values(data):
    """
    Returns dictionary

    Get interesting values from the data

    Parameters:
    data: dictionary of data
    """
    sum_all = 0
    sum_jackpot = 0
    count_jackpot = 0
    count_winner = 0
    most_jackpot_winners = 0
    most_winners = 0
    biggest_win = 0
    smallest_jackpot = 999999999999
    least_winners = 999999999999

    #HOTFIX
    if type(min(data['date'])) != str:
        first_draw = datetime.datetime.strftime(min(data['date']),'%d/%m/%Y')
        last_draw = datetime.datetime.strftime(max(data['date']),'%d/%m/%Y')
    else:
        first_draw = datetime.datetime.strftime(datetime.datetime.strptime(min(data['date']),'%Y-%m-%d %H:%M:%S.%f'),'%d/%m/%Y')
        last_draw = datetime.datetime.strftime(datetime.datetime.strptime(max(data['date']),'%Y-%m-%d %H:%M:%S.%f'),'%d/%m/%Y')
    
    draw_count = len(data['date'])
    for i in range(len(data['share_count'])):
        sum_jackpot += data['share_amount'][i][0]/100
        count_jackpot += data['share_count'][i][0]
        most_winners = np.sum(np.array(data['share_count'][i])) if np.sum(np.array(data['share_count'][i])) > most_winners else most_winners
        most_jackpot_winners = data['share_count'][i][0] if data['share_count'][i][0] > most_jackpot_winners else most_jackpot_winners
        biggest_win = data['share_amount'][i][0]/100 if data['share_amount'][i][0]/100 > biggest_win else biggest_win
        smallest_jackpot =  data['share_amount'][i][0]/100 if (data['share_amount'][i][0]/100 < smallest_jackpot) & (data['share_count'][i][0] > 0) else smallest_jackpot
        least_winners = np.sum(np.array(data['share_count'][i])) if np.sum(np.array(data['share_count'][i])) < least_winners else least_winners
        for k in range(len(data['share_count'][i])):
            sum_all += data['share_amount'][i][k]/100 * data['share_count'][i][k]
            count_winner += data['share_count'][i][k]
    smallest_jackpot = 0 if smallest_jackpot >= 199999999999 else smallest_jackpot
    least_winners = 0 if least_winners >= 199999999999 else least_winners
    interesting_values={'sum_all':sum_all,'sum_jackpot':sum_jackpot,'count_winner':count_winner,'count_jackpot':count_jackpot,
                        'most_jackpot_winners':most_jackpot_winners,'most_winners':most_winners,'biggest_win':biggest_win,
                        'smallest_jackpot':smallest_jackpot,'least_winners':least_winners,'first_draw':first_draw,'last_draw':last_draw,
                        'draw_count':draw_count}
    return interesting_values

def __barplot():
    #TODO
    return True

def data_analysis(dt_start, dt_end):
    """
    Returns dictionary of calculated values

    Parameters:
    dt_start: string formatted starting date
    dt_end: string formatted ending date
    """
    res = search_between(dt_start,dt_end)
    data = __data_from_query(res)
    if data['date'] == []:
        return {}
    interesting_data = __interesting_values(data)
    number_freq = __primary_stats(data)
    __heatmap(number_freq)
    __barplot() 

    return interesting_data