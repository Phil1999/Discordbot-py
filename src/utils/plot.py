import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib
from datetime import datetime
import numpy as np
import gspread

def update_data(df):
    gc = gspread.service_account()
    sh = gc.open('culvert')
    wks = sh.worksheet('Input')
    dat = wks.get_all_records()

    date = dat[0]['Date']
    current_names = list(df.columns.values)[1:]

    for user in dat:
        name = user['Name']
        score = user['Score']
        if name not in current_names:
            df[name] = 0
        df.loc[df['Date'] == date, name] = score

    wks.update([df.columns.values.tolist()] + df.values.tolist())

def get_data():
    gc = gspread.service_account()
    sh = gc.open('culvert')
    wks = sh.worksheet('Main Data')
    df = pd.DataFrame(wks.get_all_records())
    return df

def userGraph(df, user):
    userDF = pd.DataFrame(df.copy(), columns = ['Date', user])
    matplotlib.rcParams.update(matplotlib.rcParamsDefault)
    date = userDF['Date']
    u = userDF[user]

    fig, ax = plt.subplots(facecolor = '#2B2D31')
    c1 = '#FF00FF'

    ax.plot(date, u, color = c1, marker = 'D', markersize = 2.5,linewidth =0.5)
    ax.fill_between(date, 0, u, alpha = 0.3, color = c1)
    ax.tick_params(axis='both', colors='white')
    ax.set_title('Culvert Score', color ='white')
    ax.set_facecolor('#2B2D31')
    ax.grid(linestyle = '-', color = '#CFCFCF')
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    fig.set_figwidth(8)
    
    plt.xticks(rotation = 60)
    
    plt.savefig('images/graph.png', bbox_inches = 'tight')
    plt.close(fig)

userGraph(get_data(), 'eveboy')
