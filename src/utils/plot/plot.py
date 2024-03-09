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
import statistics

def update_data():
    gc = gspread.service_account()

    # Input sheet
    sh = gc.open('culvert')
    wks = sh.worksheet('Input')
    dat = wks.get_all_records()
    date = dat[0]['Date']

    input_names = {}
    for col in dat:
        name = col['Name']
        score = col['Score']
        input_names[name] = score
    names_lower = {k.lower(): v for k, v in input_names.items()}

    # Data sheet
    wks2 = sh.worksheet('temp')
    df = pd.DataFrame(wks2.get_all_records())
    current_names = list(df.columns.values)[1:]


    # If date does not exist, add it to main sheet
    if date not in df['Date'].values:
       df.loc[-1] = date

    # loop through every name in current database
    for name in current_names:
        name_lower = name.lower()
        # if name in database is equal to input list, update the score
        if name_lower in names_lower:
            df.loc[df['Date'] == date, name] = input_names[name]
        # otherwise, the user exists but has not ran, update score to 0
        else:
            df.loc[df['Date'] == date, name] = 0
    # Write these changes
    wks2.update([df.columns.values.tolist()] + df.values.tolist())

    # now that changes are written, pull data into dataframe again
    # we will now iterate of the input names to check for new users

    df = pd.DataFrame(wks2.get_all_records())
    updated_names = list(df.columns.values)[1:]

    un_lower = [x.lower() for x in updated_names]
    for user in dat:
        name = user['Name']
        score = user['Score']
        if name.lower() not in un_lower:
            df[name] = '-'
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
    df = df.loc[(df['Date'] <= today)]
    dates = df['Date'].tolist()
    length = len(dates)
    step = math.ceil(length/8)
    if step > 1:
        newdates = dates[::step]
        return newdates
    else:
        return dates
    
def comparison(df, users):
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
    userDF = userDF.replace(0, np.NAN)
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

    fig, ax = plt.subplots()
    for i, user in enumerate(user_list):
        u = userDF[user]
        # plot initial line for each user
        ax.plot(date, u, color = colors[i], marker = 'none', linewidth = 1.7, label = user)

        # add glow effect to each line
        for n in range(1, n_shades+1):
            ax.plot(date, u, color = colors[i], linewidth=2+(diff_linewidth*n),
                    alpha = alpha_value)
            
        # add colour underneath line
        ax.fill_between(date, 0, u, alpha = 0.1, color = colors[i])

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
    ax.set_title('Culvert Scores')
    ax.set_ylabel('Score')

    # make graph slightly wider
    if num_users > 1:
        fig.set_figwidth(12.5)
    else:
        fig.set_figwidth(7.5)

    # save graph
    imgdir = 'assets/images'
    if not os.path.exists(imgdir):
        os.makedirs(imgdir)
    plt.tight_layout()
        
    plt.savefig(f'{imgdir}/graph.png')
    plt.close(fig)

def stats(df, user):
   # Convert user input to lowercase
    user = user.lower()

    # Get the existing names in our database
    names = list(df.columns.values)[1:]
    name = ''
    for n in names:
        if n.lower() == user:
            name = n
            userDF = pd.DataFrame(df.copy(), columns = ['Date', name])
            break
    
    scores = userDF[name].tolist()
    

    scores = [x for x in scores if x != '-']

    numZeros = userDF[name][userDF[name] == 0].count()
    ptcp = round((len(scores)-numZeros) / len(scores) * 100,0)

    scores = [x for x in scores if x != 0]

    minScore = min(scores)
    maxScore = max(scores)
    meanScore = int(round(statistics.mean(scores),0))
    medianScore = statistics.median(scores)

    minScore_formatted = f"{minScore:,}"
    maxScore_formatted = f"{maxScore:,}"  
    meanScore_formatted = f"{meanScore:,}"
    medianScore_formatted = f"{medianScore:,}"

    user_dict = {}
    user_dict['min'] = minScore_formatted
    user_dict['max'] = maxScore_formatted
    user_dict['mean'] = meanScore_formatted
    user_dict['ptcp'] = str(ptcp) + '%'
    user_dict['median'] = medianScore_formatted

    rank, num_participants = userRank(df.copy(), name)
    user_dict['rank'] = rank
    user_dict['numptcp'] = num_participants

    return user_dict

def userRank(df, user):
    # get rank this week - start by getting last row of dataset
    ranks_df = df.T.iloc[:,-1:].reset_index()
    ranks_df = ranks_df.drop([0])
    ranks_df = ranks_df.replace('-', 0)
    mask = ranks_df.iloc[:,1] == 0
    ranks_df = ranks_df[~mask]
    num_participants = df.shape[0]

    ranks_df['Rank'] = ranks_df.iloc[:,1].rank(method = 'max', ascending = False)
    return(int(ranks_df.loc[ranks_df.iloc[:,0] == user]['Rank'].tolist()[0]), num_participants)
