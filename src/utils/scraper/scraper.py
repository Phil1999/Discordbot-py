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
        'found'             : False
    }

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        not_found_tag = soup.select_one('#content h2')
        
        if not_found_tag and "Not Found" in not_found_tag.text:
            return character_details
        
        character_details['found'] = True

        img_selector = 'img.card-img-top'
        level_selector = 'h5.card-text'
        class_world_selector = 'p.card-text'
        name_selector = 'h3.card-title'

        image_tag = soup.select_one(img_selector)
        level_tag = soup.select_one(level_selector)
        class_world_tag = soup.select_one(class_world_selector)
        name_tag = soup.select_one(name_selector)


        if image_tag:
            character_details['image_url'] = image_tag['src']
            
        if level_tag:
            character_details['level_percentage'] = level_tag.text
        
        if class_world_tag:
            character_details['class_and_world'] = class_world_tag.text

        if name_tag:
            character_details['name'] = name_tag.text
     

    return character_details

