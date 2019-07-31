import os
import json
from Item import Item
from ItemPriceManager import ItemPriceManager


# Loads all items in the Recipes folder.
class ItemManager:
    items = []
    market_craft_costs = {}
    item_price_manager = ItemPriceManager()

    def __init__(self):
        for filename in os.listdir('Recipes'):
            path = 'Recipes/' + filename
            print(path)
            with open(path) as json_file:
                item_json = json.load(json_file)
                self.items.append(Item(item_json))

    def calculate_market_craft_costs(self):
        for item in self.items:
            self.market_craft_costs[item.name] = item.get_market_craft_cost()

        for item in self.market_craft_costs:
            market_craft_cost = self.market_craft_costs[item]
            market_price = self.item_price_manager.get_market_price_for_item(item)
            print(item, 'Cost to Craft:', market_craft_cost, 
                  'Price on Market:', market_price,
                  'Profit:', market_price-market_craft_cost)


if __name__ == "__main__":
    print("Testing ItemManager using all available recipes.")
    itemManager = ItemManager()
    # itemManager.item_price_manager.load_market_prices()
    itemManager.calculate_market_craft_costs()
    itemManager.item_price_manager.save_market_prices()