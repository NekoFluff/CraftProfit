from RecipeList import RecipeList
from ItemMarketPriceManager import ItemMarketPriceManager

class Item:
    market_craft_cost = None
    market_craft_time = None
    hand_craft_cost = None
    hand_craft_time = None
    optimal_craft_cost = None
    optimal_craft_time = None
    optimal_craft_action = "Market Buy"

    include_in_output = True

    time_to_produce = 0.0
    quantity_produced = 1.0

    def __init__(self, item_json: dict, item_manager=None):
        self.recipes = []
        self.load_json(item_json)
        self.item_price_manager = ItemMarketPriceManager()
        self.item_manager = item_manager

    def load_json(self, json: dict):
        self.set_name(json['Name'])
        
        # If there are recipes for this item, add them to the recipes list
        if 'Recipes' in json:
            for recipe in json['Recipes']:
                print('Added recipes', json['Recipes'], 'to', json['Name'])

                quantity_produced = 1
                if 'Quantity Produced' in json:
                    quantity_produced = json['Quantity Produced']
                self.add_recipe(RecipeList(json['Name'], quantity_produced, recipe))

        if 'Time to Produce' in json:
            self.time_to_produce = float(json['Time to Produce'])
            self.quantity_produced = float(json['Quantity Produced'])

    def set_name(self, name: str):
        self.name = name

    def add_recipe(self, recipe: RecipeList):
        self.recipes.append(recipe)

    def get_market_craft_cost(self) -> (int, float):

        if self.market_craft_cost != None:
            return self.market_craft_cost,  market_craft_time
        # If it's a raw material (Unable to be crafted), so we pretend that we can only buy it off the market. 
        elif len(self.recipes) == 0: 
            return self.item_price_manager.get_market_price_for_item(self.name), 0.0

        recipe = self.recipes[0]

        total_cost = 0
        total_time = 0.0

        for (ingredient, quantity) in recipe.get_ingredients():
            total_cost += quantity * self.item_price_manager.get_market_price_for_item(ingredient)
            
        total_cost = total_cost / self.quantity_produced # Division to get price per item
        total_time += self.time_to_produce # How much time in seconds to produce this item
        total_time /= self.quantity_produced

        self.market_craft_cost = total_cost
        return total_cost, total_time

    def get_hand_craft_cost(self) -> (int, float):
        if self.hand_craft_cost != None:
            return self.hand_craft_cost, self.hand_craft_time
        # If it's a raw material (Unable to be crafted), so we pretend that we can only buy it off the market. 
        elif len(self.recipes) == 0: 
            return self.item_price_manager.get_market_price_for_item(self.name), 0.0

        recipe = self.recipes[0]

        total_cost = 0
        total_time = 0.0
        for (ingredient, quantity) in recipe.get_ingredients():
            subcost, subtime = self.item_manager.items[ingredient].get_hand_craft_cost()
            total_cost += quantity * subcost
            total_time += quantity * subtime

        total_cost /= self.quantity_produced # Division to get price per item
        total_time += self.time_to_produce # How much time in seconds to produce this item
        total_time /= self.quantity_produced

        self.hand_craft_cost = total_cost
        self.hand_craft_time = total_time
        return total_cost, total_time

    def get_optimal_craft_cost(self) -> (int, float, str):
        if self.optimal_craft_cost != None:
            return self.optimal_craft_cost, self.optimal_craft_time, self.optimal_craft_action
        # If it's a raw material (Unable to be crafted), so we pretend that we can only buy it off the market. 
        elif len(self.recipes) == 0: 
            return self.item_price_manager.get_market_price_for_item(self.name), 0, "Market Buy"

        recipe = self.recipes[0]

        total_price = 0
        total_time = 0.0
        best_action = "Market Buy"
        for (ingredient, quantity) in recipe.get_ingredients():
            lowest_cost, time_cost, best_action = self.item_manager.items[ingredient].get_optimal_craft_cost()
            # Compute the total minimum cost
            total_price += quantity * lowest_cost
            if best_action != "Market Buy":
                total_time += quantity * time_cost# Time cost for each ingredient crafted
            # if (self.name == "Pure Iron Crystal"):
                # print("{:20} {:20} {:20} {:20} {:20}".format(ingredient, lowest_cost, quantity, quantity * lowest_cost, total_price))
                # print("{:20} {:20} {:20} {:20} {:20}".format(ingredient, time_cost, quantity, quantity * time_cost, total_time))
        
        market_price = self.item_price_manager.get_market_price_for_item(self.name)
        total_price = total_price / self.quantity_produced # Division to get price per item

        if market_price <= total_price:  # If it is cheaper to buy it than to make it yourself
            total_price = market_price
            best_action = "Market Buy"
            total_time = 0
        else:
            best_action = "Craft"
            total_time += self.time_to_produce # How much time in seconds to produce this item
        # if (self.name == "Ship License: Fishing Boat"):
            # exit(1)
        
        total_time /= self.quantity_produced
        self.optimal_craft_cost = total_price
        self.optimal_craft_time = total_time
        self.optimal_craft_action = best_action
        return total_price, total_time, best_action

    def get_optimal_recipe(self) -> RecipeList:
        if len(self.recipes) > 0:
            return self.recipes[0]
        else:
            return None


if __name__ == "__main__":
    print("Running test using Item4.")
    import json
    with open('Recipes/Item4.json') as json_file:
        item_json = json.load(json_file)
        Item(item_json)

    print("Item4 loaded successfully.")    
