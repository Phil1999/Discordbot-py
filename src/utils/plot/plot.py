import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib
from datetime import datetime, date, timedelta
import numpy as np
import os
import math
import statistics

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
    
def comparison(df, users, num_weeks):
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
        s = [x.lower() for x in user_list]
        wrong_ign = [x for x in users if x.lower() not in s]
        return wrong_ign
  
    # Create our dataframe
    userDF = pd.DataFrame(df.copy(), columns = ['Date'] + user_list)
    min_weeks = 0
    for i, user in enumerate(user_list):
        if -1 in userDF[user].tolist():
            if i == 0:
                min_weeks = userDF[user].value_counts()[-1]
            else:
                temp = userDF[user].value_counts()[-1]
                if temp < min_weeks:
                    min_weeks = temp
    if min_weeks != 0:
        userDF = userDF.iloc[-(len(userDF) -min_weeks):]
    #userDF = userDF.replace(-1, np.NAN)
    #userDF = userDF.replace(0, np.NAN)

    
    # If user wants last n weeks
    if num_weeks is not None:
        userDF = userDF.iloc[-num_weeks:]

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
    titlestr= ' vs. '.join(user_list)
    for i, user in enumerate(user_list):
        u = userDF[user]
        # plot initial line for each user
        ax.plot(date, u, color = colors[i], marker = 'o', linewidth = 1.7, label = user)

        # add glow effect to each line
        for n in range(1, n_shades+1):
            ax.plot(date, u, color = colors[i], linewidth=2+(diff_linewidth*n),
                    alpha = alpha_value)
            
        # add colour underneath line
        ax.fill_between(date, 0, u, alpha = 0.1, color = colors[i])

    # grid colour
    ax.grid(color='#2A3459')

    # Border (spines) set to invisible
    spines = False
    ax.spines['top'].set_visible(spines)
    ax.spines['bottom'].set_visible(spines)
    ax.spines['left'].set_visible(spines)
    ax.spines['right'].set_visible(spines)

    # set x tick labels
    ax.set_xticks(xtick)
    ax.set_xticklabels(xtick, rotation = 30, fontsize = 13)

    plt.yticks(fontsize = 13)
    # set legends equal to labels
    ax.legend(fancybox = True, framealpha=1, facecolor = '#212946', labelcolor = 'white', fontsize = 12)

    # set y label
    ax.set_ylabel('Score')
    ax.set_ylim(-0.001)

    # make graph slightly wider and set title
    if num_users > 1:
        fig.set_figwidth(12)
        ax.set_title(f'GPQ Scores ({titlestr})', fontsize = 14)
    else:
        fig.set_figwidth(7.5)
        ax.set_title('GPQ Scores', fontsize = 14)

    # save graph
    imgdir = 'assets/images'
    if not os.path.exists(imgdir):
        os.makedirs(imgdir)
    plt.tight_layout()
        
    plt.savefig(f'{imgdir}/graph.png')
    plt.close(fig)

    return True

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
    
    scores = [x for x in scores if x != -1]

    numZeros = userDF[name][userDF[name] == 0].count()
    ptcp = round((len(scores)-numZeros) / len(scores) * 100,0)

    scores = [x for x in scores if x != 0]
    user_dict = {}
    if len(scores) > 0:
        minScore = min(scores)
        maxScore = max(scores)
        meanScore = int(round(statistics.mean(scores),0))
        medianScore = statistics.median(scores)

        minScore_formatted = f"{minScore:,}"
        maxScore_formatted = f"{maxScore:,}"  
        meanScore_formatted = f"{meanScore:,}"
        medianScore_formatted = f"{medianScore:,}"

        
        user_dict['min'] = minScore_formatted
        user_dict['max'] = maxScore_formatted
        user_dict['mean'] = meanScore_formatted
        user_dict['ptcp'] = str(ptcp) + '%'
        user_dict['median'] = medianScore_formatted

        rank, num_participants = userRank(df.copy(), name)
        user_dict['rank'] = rank
        user_dict['numptcp'] = num_participants
    else:
        user_dict['min'] = 0
        user_dict['max'] = 0
        user_dict['mean'] = 0
        user_dict['ptcp'] = str(ptcp) + '%'
        user_dict['rank'] = None

    return user_dict

def userRank(df, user):
    # get rank this week - start by getting last row of dataset
    ranks_df = df.T.iloc[:,-1:].reset_index()
    ranks_df = ranks_df.drop([0])
    ranks_df = ranks_df.replace(-1, 0)
    mask = ranks_df.iloc[:,1] == 0
    ranks_df = ranks_df[~mask]
    num_participants = ranks_df.shape[0]

    ranks_df['Rank'] = ranks_df.iloc[:,1].rank(method = 'max', ascending = False)
    if user in ranks_df.iloc[:,0].tolist():
        rank = int(ranks_df.loc[ranks_df.iloc[:,0] == user]['Rank'].tolist()[0])
    else:
        rank = None
    return(rank, num_participants)

