from RecipeList import RecipeList


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
