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
            print('In order to craft {} x {}:'.format(
                recipe.end_product, recipe.end_product_count))
            print('-'*50)
            total_ingredients_price = 0.0
            for (ingredient, quantity) in recipe.get_ingredients():
                price = 0.0
                ingredient_time = 0.0
                if ingredient in self.item_price_manager.market_prices:
                    price = self.item_price_manager.get_market_price_for_item(
                        ingredient, True) * quantity
                else:  # We are crafting instead of buying
                    ingredient_item = self.item_manager.items[ingredient[:-12]]

                    # print('Optimal Craft Time for {}: {}... {}'.format(ingredient[:-12], ingredient_item.time_to_produce/ingredient_item.quantity_produced * quantity, time_to_craft))

                    ingredient_time = ingredient_item.time_to_produce / \
                        ingredient_item.quantity_produced * quantity
                time_to_craft += ingredient_time
                total_ingredients_price += price
                if ingredient_time != 0:
                    print("{:33} {:10,.0f} Silver   x {:8,} = {:10,}  Silver {:8.2f} minutes".format(
                        ingredient, price/quantity, quantity, price, ingredient_time/60))
                else:
                    print("{:33} {:10,.0f} Silver   x {:8,} = {:10,}  Silver".format(
                        ingredient, price/quantity, quantity, price))

            shopping_cart_total += total_ingredients_price
            print('{:77.0f}  Ingredient Total'.format(total_ingredients_price))
            recipe_price = self.item_price_manager.get_market_price_for_item(recipe.end_product, True)
            cost_of_ingredients_for_single_item = (total_ingredients_price/recipe.end_product_count)
            print('Market Price: {:,.2f}, Crafting Price: {:,.2f} (You save {:,.2f} silver per item made, not including sub ingredients)'.format(
                recipe_price, cost_of_ingredients_for_single_item, recipe_price - cost_of_ingredients_for_single_item))
            print()

        recipe_item = self.item_manager.items[self.cart[0].end_product]
        # print('Optimal Craft Time for {}: {}... {}'.format(self.cart[0].end_product, recipe_item.time_to_produce/recipe_item.quantity_produced * self.cart[0].end_product_count, time_to_craft))
        recipe_time = recipe_item.time_to_produce / \
            recipe_item.quantity_produced * self.cart[0].end_product_count
        time_to_craft += recipe_time

        print("{:77,.2f}  Seconds to Craft 1 x {}".format(recipe_time/self.cart[0].end_product_count, recipe_item.name))
        print("{:77,.2f}  Minutes to Craft {} x {}".format(
            recipe_time/60, self.cart[0].end_product_count, recipe_item.name))
        print("{:77,.2f}  Total Craft Time (Minutes)".format(time_to_craft/60))
        print("{:77,.0f}  Shopping Cart Total".format(shopping_cart_total))
        market_price = self.item_price_manager.get_market_price_for_item(
            self.cart[0].end_product, True)
        market_price_total = market_price * self.cart[0].end_product_count
        print("{:77,.0f}  Market Sell Price (Pre Tax)".format(market_price_total))
        market_price_total = market_price_total * POST_TAX_PERCENT
        print("{:77,.0f}  Market Sell Price (After Tax)".format(market_price_total))
        print("{:77,.0f}  Profit".format(
            market_price_total - shopping_cart_total))
        
        if shopping_cart_total > 0:
            print("{:77,.2f}  Profit Margin".format(
                (market_price_total - shopping_cart_total)/shopping_cart_total))
        else:
            print("{:77,.2f}  Profit Margin".format(float('inf')))

        print()
        print("{:77,}  Market Sell Price (Per Item)".format(market_price))
        print("{:77,}  Market Sell Price (Per Item, After Tax)".format(
            market_price * POST_TAX_PERCENT))
        print("{:77,}  Silver Spent (Per Item)".format(
            shopping_cart_total/self.cart[0].end_product_count))
        print("{:77,}  Profit (Per Item)".format(market_price *
                                                POST_TAX_PERCENT - shopping_cart_total/self.cart[0].end_product_count))

        print()

        if time_to_craft > 0:
            print("{:77,.2f}  Profit (Silver/Hour)".format((market_price_total -
                                                       shopping_cart_total)/(time_to_craft/60/60)))
        else:
            print("{:77,.2f}  Profit (Silver/Hour)".format(float('inf')))

        print('-'*120)

        count = int(input('How many did you actually make?\t'))
        market_price = int(input('How much are you selling it for?\t'))
        print("{:77,.2f}  Actual Profit (After Tax)".format(
            count*market_price*POST_TAX_PERCENT - shopping_cart_total))
        print("{:77,.2f}  Actual Profit Margin".format(
            (count*market_price*POST_TAX_PERCENT - shopping_cart_total)/(shopping_cart_total)))
        print("{:77,.2f}  Actual Profit (Silver/Hour)".format((count*market_price *
                                                              POST_TAX_PERCENT - shopping_cart_total)/(time_to_craft/60/60)))

        craft_ratio = count / \
            (self.cart[0].end_product_count/recipe_item.quantity_produced)
        print(
            "{:77,.2f}  Actual Craft Ratio (Generally/Expected 2.5 Craft Ratio)".format(craft_ratio))
        self.item_price_manager.update_item_market_price(
            recipe_item.name, market_price)
        recipe_item.update_quantity_produced(craft_ratio)

    def add_item_to_cart(self, item: Item, shopping_cart_quantity: int):
        self.item_profit_calculator.get_optimal_per_sec_craft_cost_for_item(item, item.get_optimal_recipe())

        recipe = item.get_optimal_recipe()
        new_recipe = RecipeList(item.name, shopping_cart_quantity)
        self.add_recipe_to_cart(new_recipe)

        if recipe != None:
            for (ingredient, quantity_per_ingredient) in recipe.get_ingredients():
                ingredient_item = item.item_manager.items[ingredient]
                num_ingredient_needed = math.ceil(
                    int(shopping_cart_quantity) * int(quantity_per_ingredient))

                num_ingredient_needed = max(quantity_per_ingredient, math.ceil(
                    num_ingredient_needed/item.quantity_produced))
                if (num_ingredient_needed % int(quantity_per_ingredient) != 0):
                    print("Buy additional ingredients for padding: [{} Per Recipe] [{} Additional]".format(int(quantity_per_ingredient), num_ingredient_needed % int(quantity_per_ingredient)))
                    num_ingredient_needed = num_ingredient_needed + \
                        int(quantity_per_ingredient) - \
                        num_ingredient_needed % int(quantity_per_ingredient)

                optimal_item_action = self.item_profit_calculator.get_optimal_action_for_item(
                    ingredient_item)
                if (optimal_item_action == "Market Buy"):
                    #  Add to shopping cart
                    #  How many of item X you want to make * ingredients needed per item X / quantity produced of item X
                    #  print("Added ingredient/quantity pair: {}, {}".format(ingredient, num_ingredient_needed))
                    new_recipe.add_ingredient(
                        ingredient, num_ingredient_needed)
                elif (optimal_item_action == "Craft"):
                    #  Recursive call to find item needed to craft this item
                    new_recipe.add_ingredient(
                        ingredient + ' [You Craft]', num_ingredient_needed)
                    self.add_item_to_cart(
                        ingredient_item, num_ingredient_needed)
                else:
                    print('Error. Invalid optimal craft action.',
                          ingredient, optimal_item_action)

    def clear_cart(self):
        self.cart.clear()
        self.item_profit_calculator.optimal_per_sec_craft.clear()

