import discord, os
from utils.sheets import *

async def update_db(attachment: discord.Attachment):
        
     # Reading attachments
    if attachment:
        file = attachment

        if not file.filename.endswith('csv'):
            return "Please send a .csv file"


        save_path = "assets/data"
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        file_saved_name = "data.csv"
        file_path = os.path.join(save_path, file_saved_name)

        await file.save(file_path)

        export_valid = await csv_to_sheets()
        if export_valid:
            update_valid = await update_data()
        else:
            return "It is too early to update culvert data."
        
        if update_valid:
            return "Data update was successful."
        else:
            return "Data update was unsuccessful."



async def db_to_local():
    
    database_to_local()

    return "Success"
