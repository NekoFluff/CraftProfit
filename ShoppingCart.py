import math
from RecipeList import RecipeList
from Item import Item
from ItemMarketPriceManager import ItemMarketPriceManager
from ItemProfitCalculator import ItemProfitCalculator

POST_TAX_PERCENT = 0.845

class ShoppingCart:
    cart = []
    item_price_manager = ItemMarketPriceManager()

    def __init__(self, item_manager):
        self.item_manager = item_manager
        self.item_profit_calculator = ItemProfitCalculator()

    def add_recipe_to_cart(self, recipe: RecipeList):
        self.cart.append(recipe)

    def print_shopping_cart(self):
        shopping_cart_total = 0.0
        time_to_craft = 0.0
        for recipe in self.cart:

            # For every recipe
            print('In order to craft {} x {}:'.format(recipe.end_product, recipe.end_product_count))
            print('-'*50)
            ingredient_price = 0.0
            for (ingredient, quantity) in recipe.get_ingredients():
                price = 0.0
                if ingredient in self.item_price_manager.market_prices:
                    price = self.item_price_manager.get_market_price_for_item(ingredient) * quantity
                else: # We are crafting instead of buying
                    ingredient_item = self.item_manager.items[ingredient[:-12]]

                    # print('Optimal Craft Time for {}: {}... {}'.format(ingredient[:-12], ingredient_item.time_to_produce/ingredient_item.quantity_produced * quantity, time_to_craft))
                    time_to_craft += ingredient_item.time_to_produce/ingredient_item.quantity_produced * quantity

                ingredient_price += price
                print("{:35} x {:8} {:10} Silver".format(ingredient, quantity, price))

            shopping_cart_total += ingredient_price
            print('{:57}  Ingredient Total'.format(ingredient_price))
            print()

        recipe_item = self.item_manager.items[self.cart[0].end_product]
        # print('Optimal Craft Time for {}: {}... {}'.format(self.cart[0].end_product, recipe_item.time_to_produce/recipe_item.quantity_produced * self.cart[0].end_product_count, time_to_craft))
        time_to_craft += recipe_item.time_to_produce/recipe_item.quantity_produced * self.cart[0].end_product_count

        print("{:57}  Shopping Cart Total".format(shopping_cart_total))
        market_price = self.item_price_manager.get_market_price_for_item(self.cart[0].end_product)
        market_price_total = market_price * self.cart[0].end_product_count
        print("{:57}  Market Sell Price (Pre Tax)".format(market_price_total))
        market_price_total = market_price_total * POST_TAX_PERCENT
        print("{:57}  Market Sell Price (After Tax)".format(market_price_total))
        print("{:57}  Profit".format(market_price_total - shopping_cart_total))
        print("{:57.2f}  Profit Margin".format((market_price_total - shopping_cart_total)/shopping_cart_total))
        
        print("{:57}  Market Sell Price (Per Item)".format(market_price))
        print("{:57}  Market Sell Price (Per Item, After Tax)".format(market_price * POST_TAX_PERCENT))
        print("{:57}  Silver Spent (Per Item)".format(shopping_cart_total/self.cart[0].end_product_count))
        print("{:57}  Profit (Per Item)".format(market_price * POST_TAX_PERCENT - shopping_cart_total/self.cart[0].end_product_count))
        
        print()

        print("{:57.2f}  Total Craft Time (Seconds)".format(time_to_craft))
        print("{:57.2f}  Total Craft Time (Minutes)".format(time_to_craft/60))
        print("{:57.2f}  Total Craft Time (Hours)".format(time_to_craft/60/60))
        print("{:57.2f}  Profit (Silver/Hour)".format((market_price_total - shopping_cart_total)/(time_to_craft/60/60)))

        print('-'*120)

        count = int(input('How many did you actually make?\t'))
        print("{:57.2f}  Actual Profit (After Tax)".format(count*market_price*POST_TAX_PERCENT - shopping_cart_total))
        print("{:57.2f}  Actual Profit Margin".format((count*market_price*POST_TAX_PERCENT - shopping_cart_total)/(shopping_cart_total)))
        print("{:57.2f}  Actual Profit (Silver/Hour)".format((count*market_price*POST_TAX_PERCENT - shopping_cart_total)/(time_to_craft/60/60)))
        print("{:57.2f}  Actual Craft Ratio (Generally/Expected 2.5 Craft Ratio)".format(count/(self.cart[0].end_product_count/recipe_item.quantity_produced)))


    def add_item_to_cart(self, item: Item, shopping_cart_quantity: int):
        recipe = item.get_optimal_recipe()
        new_recipe = RecipeList(item.name, shopping_cart_quantity)
        self.add_recipe_to_cart(new_recipe)

        if recipe != None:
            for (ingredient, quantity_per_ingredient) in recipe.get_ingredients():
                ingredient_item = item.item_manager.items[ingredient]
                num_ingredient_needed = math.ceil(int(shopping_cart_quantity) * int(quantity_per_ingredient))
                
                num_ingredient_needed = max(quantity_per_ingredient, math.ceil(num_ingredient_needed/item.quantity_produced))
                # num_ingredient_needed = num_ingredient_needed + int(quantity_per_ingredient) - num_ingredient_needed % int(quantity_per_ingredient)
                
                optimal_item_action = self.item_profit_calculator.get_optimal_action_for_item(ingredient_item)
                if (optimal_item_action == "Market Buy"):
                    #  Add to shopping cart
                    #  How many of item X you want to make * ingredients needed per item X / quantity produced of item X
                    #  print("Added ingredient/quantity pair: {}, {}".format(ingredient, num_ingredient_needed))
                    new_recipe.add_ingredient(ingredient, num_ingredient_needed)
                elif (optimal_item_action == "Craft"):
                    #  Recursive call to find item needed to craft this item
                    new_recipe.add_ingredient(ingredient + ' [You Craft]', num_ingredient_needed)
                    self.add_item_to_cart(ingredient_item, num_ingredient_needed)
                else:
                    print('Error. Invalid optimal craft action.', ingredient, optimal_item_action)
        
    def clear_cart(self):
        self.cart.clear()