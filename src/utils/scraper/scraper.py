import requests, re
from bs4 import BeautifulSoup

def get_character_details(username):

    queryString = f"https://mapleranks.com/u/{username}"

    url = queryString

    response = requests.get(url)

    character_details = {
        'name'              : None,
        'image_url'         : None,
        'level'             : None,
        'class'             : None,
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
        level_percentage_selector = 'h5.card-text'
        class_world_selector = 'p.card-text'

        image_tag = soup.select_one(img_selector)
        name_tag = soup.select_one(name_selector)
        level_percentage_tag = soup.select_one(level_percentage_selector)
        class_world_tag = soup.select_one(class_world_selector)
    
        # We expect the string to look something like: "Lv. 287 (14.512%) Shade in Reboot Kronos"
        level_class_full_text = level_percentage_tag.text + " " + class_world_tag.text

        match = re.match(r"Lv\. (\d+) \(([\d.]+)%\) (.+?) in (.+)", level_class_full_text)
        
        
        if image_tag:
            character_details['image_url'] = image_tag['src']
            
        if name_tag:
            character_details['name'] = name_tag.text

        if level_percentage_tag:
            character_level = match.group(1)
            character_details['level'] = character_level

        if class_world_tag:
            character_class = match.group(3)
            character_details['class'] = character_class
     

    return character_details

