import requests
from bs4 import BeautifulSoup

def get_character_details(username):

    queryString = f"https://mapleranks.com/u/{username}"

    url = queryString

    response = requests.get(url)

    character_details = {
        'name'              : None,
        'image_url'         : None,
        'found'             : False
    }

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        not_found_tag = soup.select_one('#content h2')
        
        if not_found_tag and "Not Found" in not_found_tag.text:
            return character_details
        
        character_details['found'] = True

        img_selector = 'img.card-img-top'
        name_selector = 'h3.card-title'

        image_tag = soup.select_one(img_selector)
        name_tag = soup.select_one(name_selector)


        if image_tag:
            character_details['image_url'] = image_tag['src']
            
        if name_tag:
            character_details['name'] = name_tag.text
     

    return character_details

