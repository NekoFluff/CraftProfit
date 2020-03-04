import os
import json
from Item import Item
from ItemProfitCalculator import ItemProfitCalculator

# Loads all items in the Recipes folder.
# Entry point for calculations costs for each item


class ItemManager:
    items = {}

    def __init__(self):
        self.getData()

    def getData(self):
        for filename in os.listdir('Recipes'):
            path = 'Recipes/' + filename
            # print(path)
            with open(path) as json_file:
                item_json = json.load(json_file)
                new_item = Item(item_json, item_manager=self)
                self.items[new_item.name] = new_item

        self.item_profit_calculator = ItemProfitCalculator(self.items)

        
    def perform_profit_calculations(self):
        self.item_profit_calculator.calculate_market_craft_costs(self.items)
        print('-'*120)
        self.getData()

        self.item_profit_calculator.calculate_hand_craft_costs(self.items)
        print('-'*120)

        self.item_profit_calculator.calculate_optimal_craft_costs(self.items)
        print('-'*120)

        self.item_profit_calculator.calculate_optimal_per_sec_craft_costs(
            self.items)
        print('-'*120)


if __name__ == "__main__":
    print("Testing ItemManager using all available recipes.")
    item_manager = ItemManager()
    item_manager.perform_profit_calculations()
