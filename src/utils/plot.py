import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np
import gspread

def update():
    gc = gspread.service_account()
    sh = gc.open('culvert')
    wks = sh.worksheet('Main Data')
    wks2 = sh.worksheet('Input')
    dat = wks2.get_all_records()

    date = dat[0]['Date']

    current_names = wks.get('B1:PQ1')[0]

    df = pd.DataFrame(wks.get_all_records())

    for user in dat:
        name = user['Name']
        score = user['Score']
        if name not in current_names:
            df[name] = 0
        df.loc[df['Date'] == date, name] = score

    wks.update([df.columns.values.tolist()] + df.values.tolist())