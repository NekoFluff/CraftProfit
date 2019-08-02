from Item import Item
from ItemMarketPriceManager import ItemMarketPriceManager


class ItemProfitCalculator():
    market_craft = {}
    hand_craft = {}
    optimal_craft = {}
    item_included_in_output = {}
    
    __instance = None

    def __new__(cls):
        if ItemProfitCalculator.__instance is None:
            ItemProfitCalculator.__instance = object.__new__(cls)
        return ItemProfitCalculator.__instance

    def __init__(self):
        self.item_price_manager = ItemMarketPriceManager()


    def get_market_craft_cost_for_item(self, item: Item) -> (int, float):

        if item.market_craft_cost != None:
            return item.market_craft_cost,  market_craft_time
        # If it's a raw material (Unable to be crafted), so we pretend that we can only buy it off the market. 
        elif len(item.recipes) == 0: 
            return self.item_price_manager.get_market_price_for_item(item.name), 0.0

        recipe = item.recipes[0]

        total_cost = 0
        total_time = 0.0

        for (ingredient, quantity) in recipe.get_ingredients():
            total_cost += quantity * self.item_price_manager.get_market_price_for_item(ingredient)
            
        total_cost = total_cost / item.quantity_produced # Division to get price per item
        total_time += item.time_to_produce # How much time in seconds to produce this item
        total_time /= item.quantity_produced

        item.market_craft_cost = total_cost
        return total_cost, total_time

    def get_hand_craft_cost_for_item(self, item: Item) -> (int, float):
        if item.hand_craft_cost != None:
            return item.hand_craft_cost, item.hand_craft_time
        # If it's a raw material (Unable to be crafted), so we pretend that we can only buy it off the market. 
        elif len(item.recipes) == 0: 
            return self.item_price_manager.get_market_price_for_item(item.name), 0.0

        recipe = item.recipes[0]

        total_cost = 0
        total_time = 0.0
        for (ingredient, quantity) in recipe.get_ingredients():
            subcost, subtime = self.get_hand_craft_cost_for_item(item.item_manager.items[ingredient])
            total_cost += quantity * subcost
            total_time += quantity * subtime

        total_cost /= item.quantity_produced # Division to get price per item
        total_time += item.time_to_produce # How much time in seconds to produce this item
        total_time /= item.quantity_produced

        item.hand_craft_cost = total_cost
        item.hand_craft_time = total_time
        return total_cost, total_time

    def get_optimal_craft_cost_for_item(self, item: Item) -> (int, float, str):
        if item.optimal_craft_cost != None:
            return item.optimal_craft_cost, item.optimal_craft_time, item.optimal_craft_action
        # If it's a raw material (Unable to be crafted), so we pretend that we can only buy it off the market. 
        elif len(item.recipes) == 0: 
            return self.item_price_manager.get_market_price_for_item(item.name), 0, "Market Buy"

        recipe = item.recipes[0]

        total_price = 0
        total_time = 0.0
        best_action = "Market Buy"
        for (ingredient, quantity) in recipe.get_ingredients():
            lowest_cost, time_cost, best_action = self.get_optimal_craft_cost_for_item(item.item_manager.items[ingredient])
            # Compute the total minimum cost
            total_price += quantity * lowest_cost
            if best_action != "Market Buy":
                total_time += quantity * time_cost# Time cost for each ingredient crafted
            # if (item.name == "Pure Iron Crystal"):
                # print("{:20} {:20} {:20} {:20} {:20}".format(ingredient, lowest_cost, quantity, quantity * lowest_cost, total_price))
                # print("{:20} {:20} {:20} {:20} {:20}".format(ingredient, time_cost, quantity, quantity * time_cost, total_time))
        
        market_price = self.item_price_manager.get_market_price_for_item(item.name)
        total_price = total_price / item.quantity_produced # Division to get price per item

        if market_price <= total_price:  # If it is cheaper to buy it than to make it yourself
            total_price = market_price
            best_action = "Market Buy"
            total_time = 0
        else:
            best_action = "Craft"
            total_time += item.time_to_produce # How much time in seconds to produce this item
        # if (item.name == "Ship License: Fishing Boat"):
            # exit(1)
        
        total_time /= item.quantity_produced
        item.optimal_craft_cost = total_price
        item.optimal_craft_time = total_time
        item.optimal_craft_action = best_action
        return total_price, total_time, best_action