# -*- coding: utf8 -*-
import pandas as pd

def too_big_get_11(data):
    if data > 10:
        return 11
    elif  data < -10:
        return -11
    else:
        return data


def get_data_real_time(code_info,today):
    today = today.drop('name',axis = 1)
    today['rate'] = today['changepercent']

    data = pd.merge(today, code_info, on='code')

    data['rate'] = data['rate'].apply(too_big_get_11)
    data['rate'] = data['rate'].astype(int)
    return data