# coding: utf-8
from datetime import date, timedelta

import pandas as pd

from rescuetime.api.service import Service
from rescuetime.api.access import AnalyticApiKey


def get_apikey():
    with open("apikey", "r") as fileo:
        key = fileo.read()
    return key


apikey = get_apikey()


def get_efficiency():
    try:
        today_date = date.today().strftime("%Y-%m-%d")
        tomorrow_date = (date.today() + timedelta(1)).strftime("%Y-%m-%d")
        s = Service.Service()
        k = AnalyticApiKey.AnalyticApiKey(apikey, s)
        p = {'restrict_begin': today_date,
             'restrict_end': tomorrow_date,
             'restrict_kind': 'efficiency',
             'perspective': 'interval'}
        #YYYY-MM-DD
        d = s.fetch_data(k, p)

        df = pd.DataFrame(d['rows'], columns=d['row_headers'])
        efficiency = df["Efficiency (percent)"]
        dates = df["Date"]
        return int(efficiency.tail(1)), str(dates.tail(1))
    except:
        return "NA", "NA"


