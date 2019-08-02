import json
from collections import defaultdict
from Item import Item
from ItemMarketPriceManager import ItemMarketPriceManager


class ItemProfitCalculator():
    market_craft = defaultdict(lambda: {})
    hand_craft = defaultdict(lambda: {})
    optimal_craft = defaultdict(lambda: {})
    item_included_in_output = defaultdict(lambda: True)

    __instance = None

    def __new__(cls):
        if ItemProfitCalculator.__instance is None:
            ItemProfitCalculator.__instance = object.__new__(cls)
        return ItemProfitCalculator.__instance

    def __init__(self):
        self.read_filter_ingredients_json()
        self.read_other_filters()
        self.item_price_manager = ItemMarketPriceManager()

    def get_market_craft_cost_for_item(self, item: Item) -> (int, float):
        self.update_is_item_included_in_output(item)
        market_craft_item = self.market_craft[item.name]

        if 'Cost' in market_craft_item:
            return market_craft_item['Cost'],  market_craft_item['Time']
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

        self.market_craft[item.name]['Cost'] = total_cost
        self.market_craft[item.name]['Time'] = total_time
        return total_cost, total_time

    def get_hand_craft_cost_for_item(self, item: Item) -> (int, float):
        self.update_is_item_included_in_output(item)
        hand_craft_item = self.hand_craft[item.name]

        if 'Cost' in hand_craft_item:
            return hand_craft_item['Cost'], hand_craft_item['Time']
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

        self.hand_craft[item.name]['Cost'] = total_cost
        self.hand_craft[item.name]['Time'] = total_time
        return total_cost, total_time

    def get_optimal_craft_cost_for_item(self, item: Item) -> (int, float, str):
        self.update_is_item_included_in_output(item)

        optimal_craft_item = self.optimal_craft[item.name]

        if 'Cost' in optimal_craft_item:
            return optimal_craft_item['Cost'], optimal_craft_item['Time'], optimal_craft_item['Action']
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
        self.optimal_craft[item.name]['Cost'] = total_price
        self.optimal_craft[item.name]['Time'] = total_time
        self.optimal_craft[item.name]['Action'] = best_action
        return total_price, total_time, best_action

    def get_optimal_action_for_item(self, item):
        action = "Market Buy"
        print(item.name, self.optimal_craft[item.name])
        if "Action" in self.optimal_craft[item.name]:
            action = self.optimal_craft[item.name]['Action']
        return action
    
    def read_filter_ingredients_json(self):
        self.filter_ingredients = []
        with open(r'Filters\FilterIngredients.json') as json_file:
            self.filter_ingredients_json = json.load(json_file)
            if self.filter_ingredients_json['Enabled']:
                self.filter_ingredients = self.filter_ingredients_json['Ingredients']

        for ingredient in self.filter_ingredients:
            self.item_included_in_output[ingredient] = False


    def update_is_item_included_in_output(self, item: Item):
        # If one of the ingredients is in the filter_ingredients list, then skip
        recipe = item.get_optimal_recipe()
        if recipe != None:
            for (ingredient, _) in recipe.get_ingredients():

                if not self.item_included_in_output[ingredient] and self.filter_ingredients_json['Recursive']:
                    self.item_included_in_output[item.name] = False
                    return

                if ingredient in self.filter_ingredients:
                    self.item_included_in_output[item.name] = False
                    return


    def read_other_filters(self):
        with open(r'Filters\OtherFilters.json') as json_file:
            other_filters_json = json.load(json_file)
            self.skip_recipes_with_higher_profit_per_second_recipes = other_filters_json["Skip Recipes That Use Higher Profit Per Second Recipes"]

            