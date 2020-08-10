
import os
import json

items = []

for filename in os.listdir('Recipes'):
    path = 'Recipes/' + filename

    with open(path) as json_file:
        item_json = json.load(json_file)
        print(item_json)
        items.append(item_json)

with open('all_recipes.json', 'w') as json_file:
    json.dump(items, json_file, indent=4, sort_keys=True)


# Reformat market prices 
new_prices = []
with open('./Market_Prices/market_prices.json') as json_file:
    prices = json.load(json_file)
    
    for k,v in prices.items():
        v['Name'] = k
        new_prices.append(v)

with open('reformatted_market_prices.json', 'w') as json_file:
    json.dump(new_prices, json_file, indent=4, sort_keys=True)

