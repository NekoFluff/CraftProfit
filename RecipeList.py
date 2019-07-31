class RecipeList:

    def __init__(self, end_product: str, ingredients: dict):
        self.ingredients = []
        self.end_product = end_product
        for (ingredient) in ingredients:
            quantity = ingredients[ingredient]
            self.add_ingredient(ingredient, quantity)
            # print("Added ingredient:", ingredient, " with quantity:", quantity)

    def add_ingredient(self, ingredient, quantity):
        self.ingredients.append((ingredient, quantity))

    def get_ingredients(self):
        for (ingredient, quantity) in self.ingredients:
            yield (ingredient, quantity)