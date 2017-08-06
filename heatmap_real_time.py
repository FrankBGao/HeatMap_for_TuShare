# -*- coding: utf8 -*-
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure
from bokeh.embed import components

from datetime import datetime


def get_index(data):
    data['index_len'] = range(len(data))
    return data

def get_heatmap(day,one_day):
    one_day = one_day.drop_duplicates()
    print len(one_day)
    # I don't want 创业板
    one_day['code_is'] = one_day['code'].apply(lambda x: x[0])
    one_day = one_day[one_day['code_is'] != '3']

    one_day = one_day.groupby('c_name', as_index=False).apply(get_index)
    romans = one_day['c_name'].drop_duplicates().values  # [str(x) for x in range(0, one_day['index_len'].max())]


    group_range = [str(x) for x in range(0, one_day['index_len'].max())]

    colormap = {
        -11: '#005824',
        -10: '#005824',
        -9: '#1A693B',
        -8: '#347B53',
        -7: '#4F8D6B',
        -6: '#699F83',
        -5: '#83B09B',
        -4: '#9EC2B3',
        -3: '#B8D4CB',
        -2: '#D2E6E3',
        -1: '#EDF8FB',
        0: '#ededed',
        1: '#ffcfdc',
        2: '#ffcccc',
        3: '#ff8080',
        4: '#ff5959',
        5: '#ff4040',
        6: '#d90000',
        7: '#b20000',
        8: '#7f0000',
        9: '#660000',
        10: '#400000',
        11: '#400000'
    }
    if 'trade' in one_day.columns:
        source = ColumnDataSource(
            data=dict(
                group=[unicode(x) for x in one_day["c_name"]],
                period=[unicode(y) for y in one_day["index_len"]],
                type_color=[colormap[x] for x in one_day["rate"]],
                code=one_day["code"],
                amount=one_day["amount"],
                trade=one_day["trade"],
                c_name=one_day["c_name"],
                name=one_day["name"],
                rate=one_day["rate"],
                volume=one_day["volume"],
                high=one_day["high"],
                low=one_day["low"],
                open=one_day["open"],
            )
        )
        p = figure(title=u"今日大盘行情"+ str(datetime.now()) , tools="pan,wheel_zoom,box_zoom,reset,save,hover",
                   x_range=group_range, y_range=list(reversed(romans)))
    else:
        source = ColumnDataSource(
            data=dict(
                group=[unicode(x) for x in one_day["c_name"]],
                period=[unicode(y) for y in one_day["index_len"]],
                type_color=[colormap[x] for x in one_day["rate"]],
                code=one_day["code"],
                amount=one_day["amount"],
                close=one_day["close"],
                c_name=one_day["c_name"],
                name=one_day["name"],
                rate=one_day["rate"],
                volume=one_day["volume"],
                high=one_day["high"],
                low=one_day["low"],
                open=one_day["open"],
            )
        )
        p = figure(title=u"大盘行情" + day, tools="pan,wheel_zoom,box_zoom,reset,save,hover",
                   x_range=group_range, y_range=list(reversed(romans)))


    p.plot_width = 1200
    p.toolbar_location = None
    p.outline_line_color = None

    p.rect("period", "group", 0.9, 0.9, source=source,
           fill_alpha=0.6, color="type_color")

    p.select_one(HoverTool).tooltips = [
        ("c_name", "@c_name"),
        ("name", "@name"),
        ("code", "@code"),
        ("rate", "@rate"),
        ("volume", "@volume"),
        ("amount", "@amount"),
        ("high", "@high"),
        ("low", "@low"),
        ("open", "@open"),
        ("close", "@close"),
        ("trade", "@trade"),
    ]
    script, div = components(p)
    return div + script
