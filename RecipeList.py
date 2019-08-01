class RecipeList:

    def __init__(self, end_product: str, end_product_count: int, ingredients: dict={}):
        self.ingredients = []
        self.end_product = end_product
        self.end_product_count = end_product_count
        for (ingredient) in ingredients:
            quantity = ingredients[ingredient]
            self.add_ingredient(ingredient, quantity)
            # print("Added ingredient:", ingredient, " with quantity:", quantity)

    def add_ingredient(self, ingredient, quantity):
        self.ingredients.append((ingredient, quantity))

    def get_ingredients(self):
        for (ingredient, quantity) in self.ingredients:
            yield (ingredient, quantity)

    def print_recipe_list(self):
        print('In order to craft {} x {}:'.format(self.end_product, self.end_product_count))
        print('-'*50)
        for (ingredient, quantity) in self.get_ingredients():
            print(ingredient, quantity)
        print()