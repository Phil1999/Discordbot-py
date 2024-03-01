import requests
from bs4 import BeautifulSoup

def get_character_details(username):

    queryString = f"https://mapleranks.com/u/{username}"

    url = queryString

    response = requests.get(url)

    character_details = {
        'name'              : None,
        'image_url'         : None,
        'class_and_world'   : None,
        'level_percentage'  : None,
        'found'             : False,
    }

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        didnt_find_character_tag = soup.select_one('#content h2')

        if not didnt_find_character_tag == "Not Found":
            character_details['found'] = True
            
        image_tag = soup.select_one('img.card-img-top')
        level_tag = soup.select_one('h5.card-text')
        class_world_tag = soup.select_one('p.card-text')
        name_tag = soup.select_one('h3.card-title')


        if image_tag:
            character_details['image_url'] = image_tag['src']
            
        if level_tag:
            character_details['level_percentage'] = level_tag.text
        
        if class_world_tag:
            character_details['class_and_world'] = class_world_tag.text

        if name_tag:
            character_details['name'] = name_tag.text
     

    return character_details

