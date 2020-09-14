import os
import time
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()

# Get reference to DAO
from recipesDAO import RecipesDAO
rDAO = RecipesDAO(os.getenv('BDO_DB_URI'), os.getenv('BDO_NS'))
rDAO.deleteBadImages()

batchSize = 30

# Get missing images
updatedRecipes = []
recipes = list(rDAO.getRecipesWithMissingImage())
totalLength = len(recipes)
for index, recipe in enumerate(recipes): 
  time.sleep(1)
  URL = "https://www.invenglobal.com/blackdesertonline/item/search?word=" + recipe['Name']
  print('#',index+1,'/',totalLength, ':  ', URL)
  page = requests.get(URL)
  soup = BeautifulSoup(page.content, 'html.parser')

  data_arr = []
  rows = soup.find('div', id='blackItemList').find('tbody').find_all('tr')
  for r in rows:
    icon = r.find('td', class_='icon')
    if icon is None: continue

    name = icon.find_all('a')[1].text.strip()
    print('Name:', name)

    # Make sure name matches
    if (name == recipe['Name']):
      # print(r)
      # print(icon)
      
      image_src = icon.find('img').attrs.get('data-src')
      if ('know_' in image_src): 
        continue
      else:
        recipe['Image'] = image_src
        updatedRecipes.append(recipe)
        print('Match:', recipe)

        if len(updatedRecipes) == batchSize:
          rDAO.replaceRecipes(updatedRecipes)
          updatedRecipes = []

        break # Found the image so continue to the next recipe

# Then insert missing images...
if len(updatedRecipes) > 0:
  rDAO.replaceRecipes(updatedRecipes)
