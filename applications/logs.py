import os
import pandas as pd


def mission_planner_logs(url):

    data = pd.read_table(str(url), delim_whitespace=True)

    df = pd.DataFrame(data)
    df.to_csv('media/me.csv',)
    datatest = pd.DataFrame((pd.read_csv('media/me.csv', index_col=0)))
    d = datatest.drop(['WPL', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3',
                       'Unnamed: 4', 'Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7', '110'], axis=1)
    z = d[d != 0.].dropna(axis=0)
    cols = list(z)
    cols[0], cols[1] = cols[1], cols[0]
    f = z.loc[:, cols]
    e = f.values.tolist()
    return e
