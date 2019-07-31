from RecipeList import RecipeList
from ItemMarketPriceManager import ItemMarketPriceManager


class Item:
    market_craft_cost = None
    hand_craft_cost = None
    optimal_craft_cost = None
    optimal_craft_action = None

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

    def get_optimal_craft_cost(self) -> (int, str):
        if self.optimal_craft_cost != None:
            return self.optimal_craft_cost, self.optimal_craft_action
        # If it's a raw material (Unable to be crafted), so we pretend that we can only buy it off the market. 
        elif len(self.recipes) == 0: 
            return self.item_price_manager.get_market_price_for_item(self.name), "Market Buy"

        recipe = self.recipes[0]

        total_cost = 0
        optimal_action = "Market Buy"
        for (ingredient, quantity) in recipe.get_ingredients():
            lowest_cost, best_action = self.item_manager.items[ingredient].get_optimal_craft_cost()

            # Compute the total minimum cost
            total_cost += quantity * lowest_cost
            if best_action != "Market Buy":
                best_action = "Craft"

        market_price = self.item_price_manager.get_market_price_for_item(self.name)

        if market_price <= total_cost:  # If it is cheaper to buy it than to make it yourself
            total_cost = market_price
            best_action = "Market Buy"
        else:
            best_action = "Craft"

        self.optimal_craft_cost = total_cost
        self.optimal_craft_action = best_action
        return total_cost, best_action

    

if __name__ == "__main__":
    print("Running test using Item4.")
    import json
    with open('Recipes/Item4.json') as json_file:
        item_json = json.load(json_file)
        Item(item_json)

    print("Item4 loaded successfully.")    
