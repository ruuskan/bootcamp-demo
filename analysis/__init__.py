import numpy as np
import matplotlib.pyplot as plot
import datetime
from database.operations import search_between

cpi = np.genfromtxt(fname='elinkustannusindeksi.csv',skip_header=3, delimiter=';',converters={0: lambda x: float(x.decode('utf-8').strip('"'))})
euro_conversion = 5.94573
euro_start = 2002

def __conversion(st_year, comp_year):
    st_cpi = cpi[cpi[:,0]==st_year,1][0]
    comp_cpi = cpi[cpi[:,0]==comp_year,1][0]
    st_euro = euro_conversion if st_year < euro_start else 1
    comp_euro = euro_conversion if comp_year < euro_start else 1

    conversion_rate = comp_euro*comp_cpi/(st_euro*st_cpi)
    return conversion_rate

def data_analysis(dt_start, dt_end):
    res = search_between(dt_start,dt_end)
    1+1
    return 1