import requests
import re
from lxml import etree

def get_character_details(username):
    url = f"https://mapleranks.com/u/{username}"
    response = requests.get(url)

    character_details = {
        'name': None,
        'image_url': None,
        'level': None,
        'class': None,
        'found': False
    }

    if response.status_code == 200:
        tree = etree.HTML(response.content)
        
        # Check for "Not Found"
        not_found = tree.xpath("//div[@id='content']//h2[text()='Not Found']")
        if not_found:
            return character_details
        
        # Find the 'card-body' div
        card_div = tree.xpath("//div[contains(@class, 'card-body') and contains(@class, 'text-center')][1]")
        if not card_div:
            return character_details
        
        # Proceed to extract details from this card div
        card_div = card_div[0]
       

        # TODO: Refactor so that logic is more robust.

        image_tag = card_div.xpath(".//img[@class='card-img-top']/@src")
        name_tag = card_div.xpath(".//h3[@class='card-title text-nowrap']/text()")
        level_class_text = card_div.xpath(".//h5[@class='card-text']/text() | .//p[@class='card-text mb-0']/text()")
        
        character_details['found'] = True


        if image_tag:
            character_details['image_url'] = image_tag[0]

        if name_tag:
            character_details['name'] = name_tag[0].strip()

        if level_class_text and len(level_class_text) == 2:
            level_percentage, class_world = level_class_text
            full_text = f"{level_percentage} {class_world}"
            
            match = re.match(r"Lv\. (\d+) \(([\d.]+)%\) (.+?) in (.+)", full_text)
            if match:
                character_details['level'] = match.group(1)
                character_details['class'] = match.group(3)


    return character_details
