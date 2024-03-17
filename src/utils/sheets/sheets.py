import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, date, timedelta
import numpy as np
import gspread
import os

async def update_data():
    gc = gspread.service_account()

    # First back up the data
    backUpData(gc)
    
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
    wks2 = sh.worksheet('Main Data')
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

def backUpData(gc):
    sh = gc.open('culvert')
    main_dat = sh.worksheet('Main Data')
    s = 'Backup'
    try:
        backup = sh.worksheet(s)
    except gspread.exceptions.WorksheetNotFound:
        backup = sh.add_worksheet(title=s, rows = 200, cols = 500)
   
    backup.clear()
    df = pd.DataFrame(main_dat.get_all_records())
    backup.update([df.columns.values.tolist()] + df.values.tolist())

async def csv_to_sheets():
    filepath = f'assets/data/data.csv'
    df = pd.read_csv(filepath, header=None)
    df = df.rename({0:'Original', 1:'Score'}, axis = 'columns')
    df.insert(1, 'Name', "")

    gc = gspread.service_account()
    sh = gc.open('culvert')
    s = 'Input'
    try:
        dat = sh.worksheet(s)
    except gspread.exceptions.WorksheetNotFound:
        dat = sh.add_worksheet(title=s, rows = 100, cols = 100)
    dat.update([df.columns.values.tolist()] + df.values.tolist())

    # Apply formula to each cell that checks dictionary for proper IGN
    cell_list = dat.range("B2:B" + str(len(df) + 1))
    for index, cell in enumerate(cell_list):
        index += 2
        cell.value = "=IFNA(vlookup(A" + f"{index}" \
            + ",'OCR Mappings'!$A$1:$B$50,2,False),A" + f"{index}" + ")"
    dat.update_cells(cell_list, value_input_option='user_entered')

    # Delete the first column and replace formula with actual string value
    df2 = pd.DataFrame(dat.get_all_records())
    dat.update([df2.columns.values.tolist()] + df2.values.tolist())

    cell_list = dat.range("A1:A" + str(len(df) + 1))
    for cell in cell_list:
        cell.value = ""
    dat.update_cells(cell_list)
    
    # Get most recent date and validate that data should be updated
    main_data = sh.worksheet('Main Data')
    datecol = main_data.col_values(1)
    most_recent = datecol[-1]

    dat.update_cell(1,1, 'Date')
    
    valid, current_week = validate_date(most_recent)
    
    if valid:
        dat.update_cell(2,1, current_week.strftime("%Y-%m-%d"))
    else:
        return False
    return True

def validate_date(most_recent):
    dt = datetime.strptime(most_recent, "%Y-%m-%d")
    current_week = timedelta(days = 7) + dt 
    today = datetime.now()
    valid = today - timedelta(days=1, hours = 2) >= current_week

    return valid, current_week