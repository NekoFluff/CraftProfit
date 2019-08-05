from datetime import datetime
from RecipeList import RecipeList


class Item:
    taxed = None
    craft_action = None
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
                self.add_recipe(RecipeList(
                    json['Name'], quantity_produced, recipe))

            self.quantity_produced = float(json['Quantity Produced'])
        
        if 'Taxed' in json:
            self.taxed = bool(json['Taxed'])

        if 'Action' in json:
            self.craft_action = json['Action']

        if 'Time to Produce' in json:
            self.time_to_produce = float(json['Time to Produce'])
            self.adjust_time_to_produce_based_on_action()

    def adjust_time_to_produce_based_on_action(self):
        import json
        if self.craft_action == "Cooking":
            self.time_to_produce -= self.get_time_reduction_buff('Cooking')
        elif self.craft_action == "Alchemy":
            self.time_to_produce -= self.get_time_reduction_buff('Alchemy')

    def get_time_reduction_buff(self, craft_action):
        import json
        if craft_action is not None:
            with open(r'Buffs\{}Buffs.json'.format(craft_action)) as json_file:
                return json.load(json_file)['Time Reduction']
        return 0

    def set_name(self, name: str):
        self.name = name

    def add_recipe(self, recipe: RecipeList):
        self.recipes.append(recipe)

    def get_optimal_recipe(self) -> RecipeList:
        if len(self.recipes) > 0:
            return self.recipes[0]
        else:
            return None

    def update_quantity_produced(self, crafting_ratio: float):
        self.quantity_produced = crafting_ratio
        self.save_json()

    def save_json(self):
        import re
        file_name = re.sub(r'\W+', '', self.name)
        import json
        with open('Recipes/{}.json'.format(file_name), 'w') as json_file:
            json.dump(self.to_dict(), json_file, indent=4, sort_keys=True)

    def to_dict(self) -> {}:
        result = {}
        result['Name'] = self.name
        result['Recipes'] = [recipe.to_dict() for recipe in self.recipes]
        result['Time to Produce'] = self.time_to_produce + self.get_time_reduction_buff(self.craft_action)
        result['Quantity Produced'] = self.quantity_produced
        result['Last Updated'] = datetime.now().__str__()

        if self.craft_action != None:
            result['Action'] = self.craft_action
        if self.taxed != None:            
            result['Taxed'] = self.taxed

        return result


if __name__ == "__main__":
    print("Running test using Item4.")
    import json
    with open('Recipes/Item4.json') as json_file:
        item_json = json.load(json_file)
        Item(item_json)

    print("Item4 loaded successfully.")
