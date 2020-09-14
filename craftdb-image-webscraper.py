import requests
from bs4 import BeautifulSoup
import re
import numpy
import os


if __name__ == "__main__":
  from dotenv import load_dotenv
  load_dotenv()

  onlyTakeFirstMaterial = True # Set to true for the chopping page. False for all others
  onlyTakeFirstProduct = True # Set to true for the chopping page. False for all others

  URLs = [
    # Set onlyTakeFirstMaterial to true for the chopping page. False for all others 
    # Set onlyTakeFirstProduct to true for the chopping page. False for all others
    "https://www.invenglobal.com/blackdesertonline/craft/Chopping?crafttype=Product",
  ]

  # URLs = [

  #   "https://www.invenglobal.com/blackdesertonline/craft/Drying?crafttype=Product",
  #   "https://www.invenglobal.com/blackdesertonline/craft/Filtering?crafttype=Product",
  #   "https://www.invenglobal.com/blackdesertonline/craft/Grinding?crafttype=Product",
  #   "https://www.invenglobal.com/blackdesertonline/craft/Heating?crafttype=Product",
  #   "https://www.invenglobal.com/blackdesertonline/craft/Imperial%20Alchemy%20Packaging?crafttype=Product",
  #   "https://www.invenglobal.com/blackdesertonline/craft/Imperial%20Cuisine%20Packaging?crafttype=Product",
  #   "https://www.invenglobal.com/blackdesertonline/craft/Shaking?crafttype=Product",
  #   "https://www.invenglobal.com/blackdesertonline/craft/Simple%20Alchemy?crafttype=Product",
  #   "https://www.invenglobal.com/blackdesertonline/craft/Simple%20Cooking?crafttype=Product",

  # #---------------------------------------------------
  #   "https://www.invenglobal.com/blackdesertonline/craft/Armor%20Workshop?crafttype=Gear",
  #   "https://www.invenglobal.com/blackdesertonline/craft/Carpentry%20Workshop?crafttype=Gear",
  #   "https://www.invenglobal.com/blackdesertonline/craft/Jeweler?crafttype=Gear",
  #   "https://www.invenglobal.com/blackdesertonline/craft/Jeweler?crafttype=Gear",
  #   "https://www.invenglobal.com/blackdesertonline/craft/Handcraft%20Workshop?crafttype=Gear",
  #   "https://www.invenglobal.com/blackdesertonline/craft/Manos%20Jeweler?crafttype=Gear",
  #   "https://www.invenglobal.com/blackdesertonline/craft/Weapon%20Workshop?crafttype=Gear",

  # #-----------------------------------------------------------
  #   "https://www.invenglobal.com/blackdesertonline/craft/Ceramics%20Workshop?crafttype=Life",
  #   "https://www.invenglobal.com/blackdesertonline/craft/Costume%20Mill?crafttype=Life",
  #   "https://www.invenglobal.com/blackdesertonline/craft/Costume%20Workbench?crafttype=Life",
  #   "https://www.invenglobal.com/blackdesertonline/craft/Furniture%20Workshop?crafttype=Life",
  #   "https://www.invenglobal.com/blackdesertonline/craft/Horse%20Gear%20Workshop?crafttype=Life",
  #   "https://www.invenglobal.com/blackdesertonline/craft/Refinery?crafttype=Life",
  #   "https://www.invenglobal.com/blackdesertonline/craft/Ship%20Part%20Workshop?crafttype=Life",
  #   "https://www.invenglobal.com/blackdesertonline/craft/Shipyard?crafttype=Life",
  #   "https://www.invenglobal.com/blackdesertonline/craft/Siege%20Weapon%20Workshop?crafttype=Life",
  #   "https://www.invenglobal.com/blackdesertonline/craft/Tool%20Workshop?crafttype=Life",
  #   "https://www.invenglobal.com/blackdesertonline/craft/Wagon%20Part%20Workshop?crafttype=Life",
  #   "https://www.invenglobal.com/blackdesertonline/craft/Wagon%20Workshop?crafttype=Life",

  # #---------------------------------------------------------
  #   "https://www.invenglobal.com/blackdesertonline/craft/Crops%20Factory?crafttype=Process",
  #   "https://www.invenglobal.com/blackdesertonline/craft/Fish%20Factory?crafttype=Process",
  #   "https://www.invenglobal.com/blackdesertonline/craft/Mineral%20Workbench?crafttype=Process",
  #   "https://www.invenglobal.com/blackdesertonline/craft/Mushroom%20Factory?crafttype=Process",
  #   "https://www.invenglobal.com/blackdesertonline/craft/Wood%20Workbench?crafttype=Process",

  # #---------------------------------------------------------
  #   "https://www.invenglobal.com/blackdesertonline/craft/Elephant%20Nursery?crafttype=Guild",
  #   "https://www.invenglobal.com/blackdesertonline/craft/Guild%20Craft?crafttype=Guild",
  #   "https://www.invenglobal.com/blackdesertonline/craft/Guild%20Shipyard?crafttype=Guild",
  #   "https://www.invenglobal.com/blackdesertonline/craft/Imperial%20Trade%20Packing?crafttype=Guild",
  #   "https://www.invenglobal.com/blackdesertonline/craft/Mount%20Part%20Workshop?crafttype=Guild"
  # ]

  for URL in URLs:
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    data_arr = []
    rows = soup.find_all('tr')
    for r in rows: 
      icon = r.find('td', class_='crafticon')
      recipe = r.find('td', class_='recipe')
      materials = r.find('td', class_='material')
      method = r.find('td', class_='leadtime')
      products = r.find('td', class_='product')
      if None in (recipe, materials, method, products):
        continue

      # Parse image
      print(icon.find("img"))
      image_src = icon.find("img").attrs.get('data-src')

      # Parse Recipe
      recipe = recipe.find('span').text

      # Materials
      materials = materials.find_all('li')
      materials_arr = []
      for m in materials:
        text = m.find('span').text
        # print('Material:', text)
        parsed_item_name = re.findall(r'^.+(?=x\d+)', text)

        if len(parsed_item_name) > 0:
          parsed_item_name = parsed_item_name[0].strip()
        else:
          parsed_item_name = text.strip()

        amount = re.findall(r'\d+$', text)
        if (len(amount) > 0):
          amount = amount[0].strip()
        else:
          amount = 1

        materials_arr.append({
          'Item Name': parsed_item_name,
          'Amount': int(amount)
        })

        if onlyTakeFirstMaterial:
          break


      # Method of crafting
      method = method.find('div').contents
      time_to_produce = 6
      if (len(method) > 3):
        time_to_produce = method[4].strip()
        time_to_produce = int(re.findall(r'\d+', time_to_produce)[0]) * 60
      method = method[2].strip()

      # Products
      products = products.find_all('li')
      products_arr = []

      for p in products:
        text = p.find('span').text
        parsed_text = re.findall(r'^[\D]+(?=x\d+~?\d?)', text)

        if len(parsed_text) > 0:
          parsed_text = parsed_text[0].strip()
        else:
          parsed_text = text.strip()

        values = [int(s) for s in re.findall(r'\d+', text)]
        if len(values) == 0:
          values = [1, 1]
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
          'Recipe': materials_arr,
          'Image': image_src
        }
        data_arr.append(data)

        # print(recipe, materials_arr, method, products_arr)
        print(data)
        
        if (onlyTakeFirstProduct):
          break


    # Finally update the data on the backend
    from recipesDAO import RecipesDAO
    rDAO = RecipesDAO(os.getenv('BDO_DB_URI'), os.getenv('BDO_NS'))

    # Start by deleting old entries
    deleteMe = [{'Name': d['Name'], 'Action': d['Action'], 'Time to Produce': d['Time to Produce']} for d in data_arr]
    print('Delete:', deleteMe)
    rDAO.deleteIngredients(deleteMe)

    # Then insert
    rDAO.insertMany(data_arr)
