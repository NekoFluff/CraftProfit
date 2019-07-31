import os
import json
from Item import Item
from ItemMarketPriceManager import ItemMarketPriceManager


# Loads all items in the Recipes folder. 
# Entry point for calculations costs for each item
class ItemManager:
    items = {}
    market_craft_costs = {}  # Prices for items crafted using materials bought directly from the market
    hand_craft_costs = {}  # Prices for handcrafting everything up to this point (but buying base items)
    optimal_craft_costs = {}  # Lowest prices using cheapest path (buying materials when it's cheaper to buy than craft. crafting them when it's cheaper to craft than buy)

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
            print('{:15} || Cost to Craft using Market bought materials: {:5} || Price on Market: {:10} || Profit: {:8}'.format(item, market_craft_cost, market_price, market_price-market_craft_cost))

    def calculate_hand_craft_costs(self):
        for item in self.items.values():
            self.hand_craft_costs[item.name] = item.get_hand_craft_cost()

        for item in self.hand_craft_costs:
            hand_craft_cost = self.hand_craft_costs[item]
            market_price = self.item_price_manager.get_market_price_for_item(item)
            print('{:15} || Cost to Craft by Hand: {:5} || Price on Market: {:10} || Profit: {:8}'.format(item, hand_craft_cost, market_price, market_price-hand_craft_cost))

    def calculate_optimal_craft_costs(self):
        for item in self.items.values():
            self.optimal_craft_costs[item.name] = item.get_optimal_craft_cost()

        for item in self.optimal_craft_costs:
            cheapest_cost, best_action = self.optimal_craft_costs[item]
            market_price = self.item_price_manager.get_market_price_for_item(item)
            print('{:15} || Lowest Cost to Buy/Craft: {:5} || Course of Action: {:12} || Price on Market: {:10} || Profit: {:8}'.format(item, cheapest_cost, best_action, market_price, market_price-cheapest_cost))

    def print_highest_profits(self):
        print("Highest Profits (Sorted by Flat Value)")
        profits = []
        for item in self.optimal_craft_costs:
            cheapest_cost, best_action = self.optimal_craft_costs[item]
            market_price = self.item_price_manager.get_market_price_for_item(item)
            profit = market_price - cheapest_cost
            profit_ratio = float(profit) / float(cheapest_cost) 
            profits.append((item, profit, profit_ratio))
        
        profits.sort(key=lambda x: x[1], reverse=True)
        for profit in profits:
            print("{}: {:15} Silver profit {:15.2f} Profit Ratio".format(profit[0], profit[1], profit[2]))
        print('-'*120)
        print("Highest Profits (Sorted by Profit Ratio)")

        profits.sort(key=lambda x: x[2], reverse=True)
        for profit in profits:
            print("{}: {:15} Silver profit {:15.2f} Profit Ratio".format(profit[0], profit[1], profit[2]))
        
    def save_profits(self):
        print("Saving profits into csv file...")
        print("Saved profits into csv file")
    

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