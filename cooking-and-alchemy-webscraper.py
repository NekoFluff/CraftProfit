import requests
from bs4 import BeautifulSoup
import re
import numpy
import os


if __name__ == "__main__":
  from dotenv import load_dotenv
  load_dotenv()

  # URL = "https://www.invenglobal.com/blackdesertonline/recipe/cooking"
  URL = "https://www.invenglobal.com/blackdesertonline/recipe/alchemy"

  page = requests.get(URL)
  soup = BeautifulSoup(page.content, 'html.parser')

  data_arr = []
  rows = soup.find_all('tr')
  for r in rows: 
    recipe = r.find('td', class_='icon')
    materials = r.find('td', class_='materilal')
    method = r.find('td', class_='type')
    products = r.find('td', class_='product')
        # Parse Recipe

    if None in (recipe, materials, method, products):
      continue


    # Materials
    materials = materials.find_all('li')
    materials_arr = []
    for m in materials:
      text = m.find('a').text
      # print('Material:', text)
      parsed_item_name = re.findall(r'^.+(?=x\s\d+)', text)
      substitute_ingredient = re.findall(r'\(.+\)$', text)

      if len(parsed_item_name) > 0:
        parsed_item_name = parsed_item_name[0].strip()
      else:
        parsed_item_name = text.strip()

      if len(substitute_ingredient) > 0:
        substitute_ingredient = substitute_ingredient[0][1:-1].strip()
        parsed_item_name = substitute_ingredient
        print(substitute_ingredient)

      else:
        substitute_ingredient = None


      amount = re.findall(r'\d+$', text)
      if (len(amount) > 0):
        amount = amount[0].strip()
      else:
        amount = 1

      materials_arr.append({
        'Item Name': parsed_item_name,
        'Amount': int(amount)
      })

    # Method of crafting
    method = method.find('div').text.strip()
    time_to_produce = 6

    # Products
    products = products.find_all('li')
    products_arr = []
    for p in products:
      text = p.find('a').text
      parsed_text = re.findall(r'^[\D]+(?=x\d+~?\d?)', text)
      notGuaranteed = len(re.findall(r'%', p.text)) > 0

      if len(parsed_text) > 0:
        parsed_text = parsed_text[0].strip()
      else:
        parsed_text = text.strip()

      values = [int(s) for s in re.findall(r'\d+', text)]
      if len(values) == 0:
        values = [1, 4]
      elif len(values) == 1:
        values = [values[0], values[0]]
      average = numpy.mean(values)
      products_arr.append((parsed_text, values, average))
      

      # Convert to JSON format
      data = {
        'Name': parsed_text,
        'Min Produced': values[0],
        'Max Produced': values[1],
        'Quantity Produced': average,
        'Time to Produce': time_to_produce,
        'Action': method, 
        'Recipe': materials_arr
      }

      # if data['Name'] == 'Beehive Cookie':
      #   print(data)

      if (notGuaranteed):
        data['Not Guaranteed'] = True

      data_arr.append(data)

      # print(recipe, materials_arr, method, products_arr)
      # print(data)


  # Finally update the data on the backend
  from recipesDAO import RecipesDAO
  rDAO = RecipesDAO(os.getenv('BDO_DB_URI'), os.getenv('BDO_NS'))
  rDAO.insertMany(data_arr)
