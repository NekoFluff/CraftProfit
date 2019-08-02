import os
import json
import pandas as pd
from Item import Item
from ItemMarketPriceManager import ItemMarketPriceManager

POST_TAX_PERCENT = 0.845

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

        profits = []
        for item in self.market_craft_costs:
            market_craft_cost = self.market_craft_costs[item][0]
            market_craft_time = self.market_craft_costs[item][1]
            market_price = self.item_price_manager.get_market_price_for_item(item)
            print('{:25} || Cost to Craft using Market bought materials: {:15} || Price on Market: {:10} || Profit: {:8}'.format(item, market_craft_cost, market_price, market_price-market_craft_cost))

            # Profit calculations
            profit = (market_price * POST_TAX_PERCENT)- market_craft_cost
            profit_ratio = float(profit) / float(market_craft_cost) 
            profit_per_sec = 0 if market_craft_time == 0 else profit/market_craft_time
            profit_per_hour = profit_per_sec * 3600
            profits.append((item, market_price, market_craft_cost, profit, profit_ratio, market_craft_time, profit_per_hour))

        profits_dataframe = pd.DataFrame(profits, columns=["Item Name", "Market Price", "Market Craft Price", "Profit (Flat)", "Profit Ratio", "Total Crafting Time", "Profit Per Hour"])
        profits_dataframe.to_csv(r'.\Profit\market_craft_profit_values.csv', index=False)
        print('Profits data written to ' + r'.\Profit\market_craft_profit_values.csv')

    def calculate_hand_craft_costs(self):
        for item in self.items.values():
            self.hand_craft_costs[item.name] = item.get_hand_craft_cost()

        profits = []
        for item in self.hand_craft_costs:
            hand_craft_cost = self.hand_craft_costs[item][0]
            hand_craft_time = self.hand_craft_costs[item][1]
            market_price = self.item_price_manager.get_market_price_for_item(item)
            print('{:25} || Cost to Craft by Hand: {:15} || Price on Market: {:10} || Profit: {:8}'.format(item, hand_craft_cost, market_price, market_price-hand_craft_cost))

            # Profit calculations
            profit = (market_price * POST_TAX_PERCENT)- hand_craft_cost
            profit_ratio = float(profit) / float(hand_craft_cost) 
            profit_per_sec = 0 if hand_craft_time == 0 else profit/hand_craft_time
            profit_per_hour = profit_per_sec * 3600
            profits.append((item, market_price, hand_craft_cost, profit, profit_ratio, hand_craft_time, profit_per_hour))

        profits_dataframe = pd.DataFrame(profits, columns=["Item Name", "Market Price", "Hand Craft Price", "Profit (Flat)", "Profit Ratio", "Total Crafting Time", "Profit Per Hour"])
        profits_dataframe.to_csv(r'.\Profit\hand_craft_profit_values.csv', index=False)
        print('Profits data written to ' + r'.\Profit\hand_craft_profit_values.csv')

    def calculate_optimal_craft_costs(self):
        for item in self.items.values():
            self.optimal_craft_costs[item.name] = item.get_optimal_craft_cost()
            
        profits = []
        for item in self.optimal_craft_costs:
            cheapest_price, total_time, best_action = self.optimal_craft_costs[item]
            market_price = self.item_price_manager.get_market_price_for_item(item)

            # Profit calculations
            profit = (market_price * POST_TAX_PERCENT)- cheapest_price
            profit_ratio = float(profit) / float(cheapest_price) 
            profit_per_sec = 0 if total_time == 0 else profit/total_time
            profit_per_hour = profit_per_sec * 3600
            profits.append((item, best_action, market_price, cheapest_price, profit, profit_ratio, total_time, profit_per_hour))

        profits_dataframe = pd.DataFrame(profits, columns=["Item Name", "Course of Action", "Market Price", "Cheapest Buy/Craft Price", "Profit (Flat)", "Profit Ratio", "Total Crafting Time", "Profit Per Hour"])
        profits_dataframe.to_csv(r'.\Profit\optimal_profit_values.csv', index=False)
        print('Profits data written to ' + r'.\Profit\optimal_profit_values.csv')

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
    item_manager.item_price_manager.save_market_prices()