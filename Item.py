from RecipeList import RecipeList
from ItemPriceManager import ItemPriceManager


class Item:
    def __init__(self, item_json: dict):
        self.recipes = []
        self.load_json(item_json)
        self.item_price_manager = ItemPriceManager()

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
        # (Unable to be crafted)
        # It's a raw material, so we pretend that we can only buy it off the market. 
        if len(self.recipes) == 0: 
            return self.item_price_manager.get_market_price_for_item(self.name)

        recipe = self.recipes[0]

        total_cost = 0
        for (ingredient, quantity) in recipe.get_ingredients():
            total_cost += quantity * self.item_price_manager.get_market_price_for_item(self.name)

        return total_cost

if __name__ == "__main__":
    print("Running test using Item4.")
    import json
    with open('Recipes/Item4.json') as json_file:
        item_json = json.load(json_file)
        Item(item_json)

    print("Item4 loaded successfully.")    
