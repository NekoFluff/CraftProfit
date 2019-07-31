from RecipeList import RecipeList
from ItemMarketPriceManager import ItemMarketPriceManager


class Item:
    market_craft_cost = None
    hand_craft_cost = None
    optimal_craft_cost = None
    optimal_craft_time = 0
    optimal_craft_action = None

    time_to_produce = 0
    quantity_produced = 1

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
                self.add_recipe(RecipeList(json['Name'], recipe))

        if 'Time to Produce' in json:
            self.time_to_produce = json['Time to Produce']
            self.quantity_produced = json['Quantity Produced']

    def set_name(self, name: str):
        self.name = name

    def add_recipe(self, recipe: RecipeList):
        self.recipes.append(recipe)

    def get_market_craft_cost(self) -> int:

        if self.market_craft_cost != None:
            return self.market_craft_cost
        # If it's a raw material (Unable to be crafted), so we pretend that we can only buy it off the market. 
        elif len(self.recipes) == 0: 
            return self.item_price_manager.get_market_price_for_item(self.name)

        recipe = self.recipes[0]

        total_cost = 0
        for (ingredient, quantity) in recipe.get_ingredients():
            total_cost += quantity * self.item_price_manager.get_market_price_for_item(ingredient)

        self.market_craft_cost = total_cost
        return total_cost

    def get_hand_craft_cost(self) -> int:
        if self.hand_craft_cost != None:
            return self.hand_craft_cost
        # If it's a raw material (Unable to be crafted), so we pretend that we can only buy it off the market. 
        elif len(self.recipes) == 0: 
            return self.item_price_manager.get_market_price_for_item(self.name)

        recipe = self.recipes[0]

        total_cost = 0
        for (ingredient, quantity) in recipe.get_ingredients():
            total_cost += quantity * self.item_manager.items[ingredient].get_hand_craft_cost()

        self.hand_craft_cost = total_cost
        return total_cost

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
                total_time += time_cost # Time cost for each ingredient crafted

        market_price = self.item_price_manager.get_market_price_for_item(self.name)

        if market_price <= total_price:  # If it is cheaper to buy it than to make it yourself
            total_price = market_price
            best_action = "Market Buy"
            total_time = 0
        else:
            best_action = "Craft"
            total_time += self.time_to_produce * quantity / self.quantity_produced # How much time in seconds to produce this item

        self.optimal_craft_cost = total_price
        self.optimal_craft_time = total_time
        self.optimal_craft_action = best_action
        return total_price, total_time, best_action

    

if __name__ == "__main__":
    print("Running test using Item4.")
    import json
    with open('Recipes/Item4.json') as json_file:
        item_json = json.load(json_file)
        Item(item_json)

    print("Item4 loaded successfully.")    
