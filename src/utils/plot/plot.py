import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib
from datetime import datetime, date, timedelta
import numpy as np
import gspread
import os
import math

def update_data():
    gc = gspread.service_account()

    # Input sheet
    sh = gc.open('culvert')
    wks = sh.worksheet('Input')
    dat = wks.get_all_records()
    date = dat[0]['Date']

    # Data sheet
    wks2 = sh.worksheet('Main Data')
    df = pd.DataFrame(wks2.get_all_records())
    cn = list(df.columns.values)[1:]
    current_names = [x.lower() for x in cn]

    # If date does not exist, add it to main sheet
    if (df['Date'] != date).any():
       df.loc[-1] = date

    for user in dat:
        name = user['Name']
        score = user['Score']
        if name.lower() not in current_names:
            df[name] = 0
        df.loc[df['Date'] == date, name] = score

    wks2.update([df.columns.values.tolist()] + df.values.tolist())

def get_data():
    gc = gspread.service_account()
    sh = gc.open('culvert')
    wks = sh.worksheet('Main Data')
    df = pd.DataFrame(wks.get_all_records())
    return df

def xLabelTicks(df):
    today = str(date.today())
    df = df[(df['Date'] <= today)]
    dates = df['Date'].tolist()
    length = len(dates)
    step = math.ceil(length/8)
    if step > 1:
        newdates = dates[::step]
        return newdates
    else:
        return dates
    
def userGraph(df, users):
    # Convert user input to lowercase
    users = [x.lower() for x in users]

    # Get the length of users, max 4
    num_users = len(users)

    user_list = []

    # Get the existing names in our database
    names = list(df.columns.values)[1:]

    '''
    If an existing name in our database is in our user input,
    then we add it to the list of names we will use.
    '''
    for n in names:
        if num_users == len(user_list):
            break
        if n.lower() in users:
            user_list.append(n)
    
    # If true, this means that we did not find the user data for our input
    if num_users != len(user_list):
        print('IGN input is wrong')
        return None
  
    # Create our dataframe
    userDF = pd.DataFrame(df.copy(), columns = ['Date'] + user_list)
    userDF = userDF.replace('', 0)
    
    date = userDF['Date']

    # Get the right x tick labels so it's not overcrowded
    xtick = xLabelTicks(userDF)

    plt.style.use("dark_background")
    for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
        plt.rcParams[param] = '0.9'  # very light grey
    for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
        plt.rcParams[param] = '#212946'  # bluish dark grey
    colors = [
    '#08F7FE',  # teal/cyan
    '#FE53BB',  # pink
    '#F5D300',  # yellow
    '#00ff41',  # matrix green
    ]

    n_shades = 10
    diff_linewidth = 1.05
    alpha_value = 0.3 / n_shades
    titlestr = ''

    fig, ax = plt.subplots()
    for i, user in enumerate(user_list):
        u = userDF[user]
        # plot initial line for each user
        ax.plot(date, u, color = colors[i], marker = 'o', linewidth = 0.8, label = user)

        # add glow effect to each line
        for n in range(1, n_shades+1):
            ax.plot(date, u, color = colors[i], linewidth=2+(diff_linewidth*n),
                    alpha = alpha_value)
            
        # add colour underneath line
        ax.fill_between(date, 0, u, alpha = 0.1, color = colors[i])

        # determine the title
        if (i+1) < num_users:
            s = user + ' vs. '
            titlestr += s
        else:
            titlestr += user

    # grid colour
    ax.grid(color='#2A3459')

    # Border (spines) set to invisible
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # set x tick labels
    ax.set_xticks(xtick)
    ax.set_xticklabels(xtick, rotation = 30)

    # set legends equal to labels
    ax.legend(fancybox = True, framealpha=1, facecolor = '#212946', labelcolor = 'white')

    # set title and y label
    ax.set_title(titlestr)
    ax.set_ylabel('Score')

    # make graph slightly wider
    fig.set_figwidth(7)

    # save graph
    imgdir = 'assets/images'
    if not os.path.exists(imgdir):
        os.makedirs(imgdir)
    plt.tight_layout()
        
    plt.savefig(f'{imgdir}/graph.png')
    plt.close(fig)
