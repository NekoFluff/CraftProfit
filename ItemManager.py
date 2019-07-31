import os
import json
from Item import Item
from ItemMarketPriceManager import ItemMarketPriceManager


# Loads all items in the Recipes folder.
class ItemManager:
    items = {}
    market_craft_costs = {} # Prices for buying the immediate materials necessary for the item
    hand_craft_costs = {} # Prices for handcrafting everything up to this point
    optimal_craft_costs = {} # Prices for handcrafting everything up to this point

    def __init__(self):
        self.item_price_manager = ItemMarketPriceManager()
        for filename in os.listdir('Recipes'):
            path = 'Recipes/' + filename
            print(path)
            with open(path) as json_file:
                item_json = json.load(json_file)
                new_item = Item(item_json, item_manager=self)
                self.items[new_item.name] = new_item

    def calculate_market_craft_costs(self):
        for item in self.items.values():
            self.market_craft_costs[item.name] = item.get_market_craft_cost()

        for item in self.market_craft_costs:
            market_craft_cost = self.market_craft_costs[item]
            market_price = self.item_price_manager.get_market_price_for_item(item)
            print(item, '\t|| Cost to Craft using Market bought materials:', market_craft_cost, 
                  '\t|| Price on Market:', market_price,
                  '\t|| Profit:', market_price-market_craft_cost)
    
    def calculate_hand_craft_costs(self):
        for item in self.items.values():
            self.hand_craft_costs[item.name] = item.get_hand_craft_cost()

        for item in self.hand_craft_costs:
            hand_craft_cost = self.hand_craft_costs[item]
            market_price = self.item_price_manager.get_market_price_for_item(item)
            print(item, '\t|| Cost to Craft by Hand:', hand_craft_cost, 
                  '\t|| Price on Market:', market_price,
                  '\t|| Profit:', market_price-hand_craft_cost)

    def calculate_optimal_craft_costs(self):
        for item in self.items.values():
            self.optimal_craft_costs[item.name] = item.get_optimal_craft_cost()

        for item in self.optimal_craft_costs:
            cheapest_cost, best_action = self.optimal_craft_costs[item]
            market_price = self.item_price_manager.get_market_price_for_item(item)
            print(item, '\t|| Lowest Cost to Buy/Craft:', cheapest_cost,
                  '\t|| Course of Action:', best_action,
                  '\t|| Price on Market:', market_price,
                  '\t|| Profit:', market_price-cheapest_cost)

    def print_highest_profits():
        print("Printing out highest profits")

    def save_profits():
        print("Saving profits")
    

if __name__ == "__main__":
    print("Testing ItemManager using all available recipes.")
    item_manager = ItemManager()
    item_manager.item_price_manager.load_market_prices()
    item_manager.calculate_market_craft_costs()
    print('-'*120)
    item_manager.calculate_hand_craft_costs()
    print('-'*120)
    item_manager.calculate_optimal_craft_costs()
    print('-'*120)
    item_manager.print_highest_profits()
    item_manager.save_profits()
    item_manager.item_price_manager.save_market_prices()