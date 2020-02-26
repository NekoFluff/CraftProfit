import json
import pandas as pd

from collections import defaultdict
from Item import Item
from ItemMarketPriceManager import ItemMarketPriceManager

POST_TAX_PERCENT = 0.845


class ItemProfitCalculator():
    market_craft = defaultdict(lambda: {})
    hand_craft = defaultdict(lambda: {})
    optimal_craft = defaultdict(lambda: {})
    optimal_per_sec_craft = defaultdict(lambda: {})
    item_included_in_output = defaultdict(lambda: True)

    __instance = None

    def __new__(cls, items: {str: Item} = None):
        if ItemProfitCalculator.__instance is None:
            ItemProfitCalculator.__instance = object.__new__(cls)
        return ItemProfitCalculator.__instance

    def __init__(self, items: {str: Item} = None):
        if items is not None:
            self.read_filter_ingredients_json()
            self.read_other_filters()
            self.apply_filters(items)
        self.item_price_manager = ItemMarketPriceManager()

    def get_market_craft_cost_for_item(self, item: Item) -> (int, float):
        market_craft_item = self.market_craft[item.name]
        total_cost = 0
        total_time = 0.0

        if 'Cost' in market_craft_item:
            total_cost, total_time = market_craft_item['Cost'],  market_craft_item['Time']
        # If it's a raw material (Unable to be crafted), so we pretend that we can only buy it off the market.
        elif len(item.recipes) == 0 or self.item_included_in_output[item.name] == False:
            total_cost, total_time = self.item_price_manager.get_market_price_for_item(
                item.name), 0.0
        else:
            recipe = item.recipes[0]
            for (ingredient, quantity) in recipe.get_ingredients():
                total_cost += quantity * \
                    self.item_price_manager.get_market_price_for_item(
                        ingredient)

            total_cost = total_cost / item.quantity_produced  # Division to get price per item
            # How much time in seconds to produce this item
            total_time += item.time_to_produce
            total_time /= item.quantity_produced

        self.market_craft[item.name]['Cost'] = total_cost
        self.market_craft[item.name]['Time'] = total_time
        return total_cost, total_time

    def get_hand_craft_cost_for_item(self, item: Item) -> (int, float):
        hand_craft_item = self.hand_craft[item.name]
        total_cost = 0
        total_time = 0.0

        if 'Cost' in hand_craft_item:
            total_cost, total_time = hand_craft_item['Cost'], hand_craft_item['Time']
        # If it's a raw material (Unable to be crafted), so we pretend that we can only buy it off the market.
        elif len(item.recipes) == 0 or self.item_included_in_output[item.name] == False:
            total_cost, total_time = self.item_price_manager.get_market_price_for_item(
                item.name), 0.0
        else:
            recipe = item.recipes[0]
            for (ingredient, quantity) in recipe.get_ingredients():
                subcost, subtime = self.get_hand_craft_cost_for_item(
                    item.item_manager.items[ingredient])
                total_cost += quantity * subcost
                total_time += quantity * subtime

            total_cost /= item.quantity_produced  # Division to get price per item
            # How much time in seconds to produce this item
            total_time += item.time_to_produce
            total_time /= item.quantity_produced

        self.hand_craft[item.name]['Cost'] = total_cost
        self.hand_craft[item.name]['Time'] = total_time
        return total_cost, total_time

    def get_optimal_craft_cost_for_item(self, item: Item) -> (int, float, str):
        optimal_craft_item = self.optimal_craft[item.name]
        total_price = 0
        total_time = 0.0
        best_action = "Market Buy"

        if 'Cost' in optimal_craft_item:
            total_price, total_time, best_action = optimal_craft_item[
                'Cost'], optimal_craft_item['Time'], optimal_craft_item['Action']
        # If it's a raw material (Unable to be crafted), so we pretend that we can only buy it off the market.
        elif len(item.recipes) == 0 or self.item_included_in_output[item.name] == False:
            total_price, total_time, best_action = self.item_price_manager.get_market_price_for_item(
                item.name), 0, "Market Buy"
        else:
            recipe = item.recipes[0]
            for (ingredient, quantity) in recipe.get_ingredients():
                lowest_cost, time_cost, best_action = self.get_optimal_craft_cost_for_item(
                    item.item_manager.items[ingredient])
                # Compute the total minimum cost
                total_price += quantity * lowest_cost
                if best_action != "Market Buy":
                    total_time += quantity * time_cost  # Time cost for each ingredient crafted
                # if (item.name == "Pure Iron Crystal"):
                    # print("{:20} {:20} {:20} {:20} {:20}".format(ingredient, lowest_cost, quantity, quantity * lowest_cost, total_price))
                    # print("{:20} {:20} {:20} {:20} {:20}".format(ingredient, time_cost, quantity, quantity * time_cost, total_time))

            market_price = self.item_price_manager.get_market_price_for_item(
                item.name)
            # Division to get price per item
            total_price = total_price / item.quantity_produced

            if market_price <= total_price:  # If it is cheaper to buy it than to make it yourself
                total_price = market_price
                best_action = "Market Buy"
                total_time = 0
            else:
                best_action = "Craft"
                # How much time in seconds to produce this item
                total_time += item.time_to_produce
            # if (item.name == "Ship License: Fishing Boat"):
                # exit(1)
            total_time /= item.quantity_produced

        self.optimal_craft[item.name]['Cost'] = total_price
        self.optimal_craft[item.name]['Time'] = total_time
        self.optimal_craft[item.name]['Action'] = best_action
        return total_price, total_time, best_action

    def get_optimal_per_sec_craft_cost_for_item(self, item: Item) -> (int, float, str):
        optimal_craft_item = self.optimal_per_sec_craft[item.name]
        total_price = 0
        total_time = 0.0
        best_action = "Market Buy"
        item_market_price = self.item_price_manager.get_market_price_for_item(
            item.name)
        market_craft_cost, market_craft_time = self.get_market_craft_cost_for_item(
            item)

        if 'Cost' in optimal_craft_item:
            total_price, total_time, best_action = optimal_craft_item[
                'Cost'], optimal_craft_item['Time'], optimal_craft_item['Action']
        # If it's a raw material (Unable to be crafted), so we pretend that we can only buy it off the market.
        elif len(item.recipes) == 0 or self.item_included_in_output[item.name] == False:
            total_price, total_time, best_action = item_market_price, 0, "Market Buy"
        else:
            recipe = item.recipes[0]
            for (ingredient, quantity) in recipe.get_ingredients():
                lowest_cost, time_cost, ingredient_best_action = self.get_optimal_per_sec_craft_cost_for_item(
                    item.item_manager.items[ingredient])
                ingredient_market_price = self.item_price_manager.get_market_price_for_item(
                    ingredient)
            
            # NEW
            # combination_count = 2 ** len(recipe.ingredients)
            # combinations = [] # 2D array
            # for possibility in range(combination_count):
            #     format_str = '{0:0'+str(len(recipe.ingredients))+'b}'
            #     combinations.append([int(x) for x in list(format_str.format(possibility))])

            # print('Combinations')
            # print(combinations)

            # for combination in combinations:
            #     total_price = 0
            #     total_time = 0
            #     for i in range(len(combination)):
            #         (ingredient, quantity) = recipe.ingredients[i]
            #         if (combination[i] == 0): # 0 is craft ingredient and 1 is buy ingredient
            #             item_price, time_cost, _ = self.get_optimal_per_sec_craft_cost_for_item(
            #             item.item_manager.items[ingredient])
            #             total_price += item_price * quantity
            #             total_time += total_time * quantity
            #         else:
            #             item_price = self.item_price_manager.get_market_price_for_item(
            #             ingredient)
            #             total_price += item_price

            #     # Craft the items using the ingredients
            #     market_price = self.item_price_manager.get_market_price_for_item(
            #         item.name)
                    
            #     # Division to get price per item
            #     total_price = total_price / item.quantity_produced

            #     if market_price <= total_price:  # If it is cheaper to buy it than to make it yourself
            #         total_price = market_price
            #         best_action = "Market Buy"
            #         total_time = 0
            #     else:
            #         best_action = "Craft"
            #         # How much time in seconds to produce this item
            #         total_time += item.time_to_produce

            #     total_time /= item.quantity_produced

            #     # Calculate profit per second
            #     pps = total_price / total_time

            #     # See if it beats any previous values
            #     if pps > old_pss:

            #     # Store path... by updating ingredients as well at item's Cost Time and Action
            # self.optimal_per_sec_craft[item.name]['Cost'] = total_price
            # self.optimal_per_sec_craft[item.name]['Time'] = total_time
            # self.optimal_per_sec_craft[item.name]['Action'] = best_action
            # return total_price, total_time, best_action
            # END NEW

                if ingredient_best_action != 'Market Buy':
                    # If you end up crafting the ingredients, make sure it doesn't negatively impact your profit per second
                    # It may be the case that buying the ingredients off the market will increase your profit per second
                    # But if crafting the ingredients increases your profit per second, then craft it
                    ingredient_profit_per_second = ( # Profit/sec for crafting ingredient
                        ingredient_market_price * POST_TAX_PERCENT - lowest_cost) / time_cost
                    recipe_profit_per_sec = ( # Profit/sec for buying all ingredients. Crafting. Selling.
                        item_market_price * POST_TAX_PERCENT - market_craft_cost) / market_craft_time
                    if ingredient_profit_per_second < recipe_profit_per_sec:
                        ingredient_best_action = 'Market Buy'
                        time_cost = 0
                        lowest_cost = ingredient_market_price # Lowest cost become price on market
                        self.optimal_per_sec_craft[ingredient]['Cost'] = lowest_cost
                        self.optimal_per_sec_craft[ingredient]['Time'] = time_cost
                        self.optimal_per_sec_craft[ingredient]['Action'] = ingredient_best_action

                # Compute the total minimum cost
                total_price += quantity * lowest_cost
                if ingredient_best_action != "Market Buy":
                    total_time += quantity * time_cost  # Time cost for each ingredient crafted
                # if (item.name == "Pure Iron Crystal"):
                    # print("{:20} {:20} {:20} {:20} {:20}".format(ingredient, lowest_cost, quantity, quantity * lowest_cost, total_price))
                    # print("{:20} {:20} {:20} {:20} {:20}".format(ingredient, time_cost, quantity, quantity * time_cost, total_time))

            market_price = self.item_price_manager.get_market_price_for_item(
                item.name)
            # Division to get price per item
            total_price = total_price / item.quantity_produced

            if market_price <= total_price:  # If it is cheaper to buy it than to make it yourself
                total_price = market_price
                best_action = "Market Buy"
                total_time = 0
            else:
                best_action = "Craft"
                # How much time in seconds to produce this item
                total_time += item.time_to_produce
            # if (item.name == "Ship License: Fishing Boat"):
                # exit(1)
            total_time /= item.quantity_produced

        self.optimal_per_sec_craft[item.name]['Cost'] = total_price
        self.optimal_per_sec_craft[item.name]['Time'] = total_time
        self.optimal_per_sec_craft[item.name]['Action'] = best_action
        return total_price, total_time, best_action

    def get_optimal_action_for_item(self, item: Item):
        action = "Market Buy"
        optimal_per_sec_enabled = True
        dict = self.optimal_craft
        if optimal_per_sec_enabled:
            dict = self.optimal_per_sec_craft

        print(item.name, dict[item.name])
        if "Action" in dict[item.name]:
            action = dict[item.name]['Action']

        return action

    def read_filter_ingredients_json(self):
        self.filter_ingredients = []
        with open(r'Filters\FilterIngredients.json') as json_file:
            self.filter_ingredients_json = json.load(json_file)
            if self.filter_ingredients_json['Enabled']:
                self.filter_ingredients = self.filter_ingredients_json['Ingredients']

        for ingredient in self.filter_ingredients:
            self.item_included_in_output[ingredient] = False

    def apply_filters(self, all_items: {str: Item}):
        self.filter_applied = defaultdict(lambda: False)
        for item_name in all_items:
            self.apply_filter_to_item(all_items[item_name])

    def apply_filter_to_item(self, item: Item):
        included = True
        recursive = self.filter_ingredients_json['Recursive']
        if self.filter_applied[item.name] == True:
            included = self.item_included_in_output[item.name]

        elif self.item_included_in_output[item.name] == False:
            included = False
        elif not recursive:
            included = self.update_is_item_included_in_output(item)
        elif recursive:
            recipe = item.get_optimal_recipe()
            if recipe is not None:
                for (ingredient, _) in recipe.get_ingredients():
                    if not self.apply_filter_to_item(item.item_manager.items[ingredient]):
                        included = False

        self.filter_applied[item.name] = True
        self.item_included_in_output[item.name] = included
        return included

    def update_is_item_included_in_output(self, item: Item):
        # If one of the ingredients is in the filter_ingredients list, then skip
        recipe = item.get_optimal_recipe()
        if recipe != None:
            for (ingredient, _) in recipe.get_ingredients():

                if not self.item_included_in_output[ingredient] and self.filter_ingredients_json['Recursive']:
                    self.item_included_in_output[item.name] = False
                    return False

                elif ingredient in self.filter_ingredients:
                    self.item_included_in_output[item.name] = False
                    return False

        return True

    def read_other_filters(self):
        with open(r'Filters\OtherFilters.json') as json_file:
            other_filters_json = json.load(json_file)
            self.skip_recipes_with_higher_profit_per_second_recipes = other_filters_json[
                "Skip Recipes That Use Higher Profit Per Second Recipes"]

    def calculate_market_craft_costs(self, items):
        profits = []
        for item in items.values():
            self.get_market_craft_cost_for_item(item)

            if not self.item_included_in_output[item]:
                continue

            market_craft_cost = self.market_craft[item.name]['Cost']
            market_craft_time = self.market_craft[item.name]['Time']
            market_price = self.item_price_manager.get_market_price_for_item(
                item_name=item.name)
            # print('{:25} || Cost to Craft using Market bought materials: {:15} || Price on Market: {:10} || Profit: {:8}'.format(
                # item.name, market_craft_cost, market_price, market_price-market_craft_cost))

            # Profit calculations
            profit = (market_price * POST_TAX_PERCENT) - market_craft_cost
            profit_ratio = float(profit) / float(market_craft_cost)
            profit_per_sec = 0 if market_craft_time == 0 else profit/market_craft_time
            profit_per_hour = profit_per_sec * 3600
            profits.append((item.name, market_price, market_craft_cost,
                            profit, profit_ratio, market_craft_time, profit_per_hour))

        profits_dataframe = pd.DataFrame(profits, columns=[
                                         "Item Name", "Market Price", "Market Craft Price", "Profit (Flat)", "Profit Ratio", "Total Crafting Time", "Profit Per Hour"])
        profits_dataframe.to_csv(
            r'.\Profit\market_craft_profit_values.csv', index=False)
        print('Profits data written to ' +
              r'.\Profit\market_craft_profit_values.csv')

    def calculate_hand_craft_costs(self, items):
        profits = []
        for item in items.values():
            self.get_hand_craft_cost_for_item(item)

            if not self.item_included_in_output[item.name]:
                continue

            hand_craft_cost = self.hand_craft[item.name]['Cost']
            hand_craft_time = self.hand_craft[item.name]['Time']
            market_price = self.item_price_manager.get_market_price_for_item(
                item.name)
            # print('{:25} || Cost to Craft by Hand: {:15} || Price on Market: {:10} || Profit: {:8}'.format(
                # item.name, hand_craft_cost, market_price, market_price-hand_craft_cost))

            # Profit calculations
            profit = (market_price * POST_TAX_PERCENT) - hand_craft_cost
            profit_ratio = float(profit) / float(hand_craft_cost)
            profit_per_sec = 0 if hand_craft_time == 0 else profit/hand_craft_time
            profit_per_hour = profit_per_sec * 3600
            profits.append((item.name, market_price, hand_craft_cost,
                            profit, profit_ratio, hand_craft_time, profit_per_hour))

        profits_dataframe = pd.DataFrame(profits, columns=[
                                         "Item Name", "Market Price", "Hand Craft Price", "Profit (Flat)", "Profit Ratio", "Total Crafting Time", "Profit Per Hour"])
        profits_dataframe.to_csv(
            r'.\Profit\hand_craft_profit_values.csv', index=False)
        print('Profits data written to ' +
              r'.\Profit\hand_craft_profit_values.csv')

    def calculate_optimal_craft_costs(self, items):
        profits = []

        for item in items.values():
            self.get_optimal_craft_cost_for_item(item)

            if not self.item_included_in_output[item.name]:
                continue

            cheapest_price, total_time, best_action = self.optimal_craft[item.name][
                'Cost'],  self.optimal_craft[item.name]['Time'], self.optimal_craft[item.name]['Action']
            market_price = self.item_price_manager.get_market_price_for_item(
                item.name)

            # Profit calculations
            profit = (market_price * POST_TAX_PERCENT) - cheapest_price
            profit_ratio = float(profit) / float(cheapest_price)
            profit_per_sec = 0 if total_time == 0 else profit/total_time
            profit_per_hour = profit_per_sec * 3600
            profits.append((item.name, best_action, market_price, cheapest_price,
                            profit, profit_ratio, total_time, profit_per_hour))

        profits_dataframe = pd.DataFrame(profits, columns=["Item Name", "Course of Action", "Market Price",
                                                           "Cheapest Buy/Craft Price", "Profit (Flat)", "Profit Ratio", "Total Crafting Time", "Profit Per Hour"])
        profits_dataframe.to_csv(
            r'.\Profit\optimal_profit_values.csv', index=False)
        print('Profits data written to ' +
              r'.\Profit\optimal_profit_values.csv')

    def calculate_optimal_per_sec_craft_costs(self, items):
        profits = []

        for item in items.values():
            self.optimal_per_sec_craft.clear()
            self.get_optimal_per_sec_craft_cost_for_item(item)

            if not self.item_included_in_output[item.name]:
                continue

            cheapest_price, total_time, best_action = self.optimal_per_sec_craft[item.name][
                'Cost'],  self.optimal_per_sec_craft[item.name]['Time'], self.optimal_per_sec_craft[item.name]['Action']
            market_price = self.item_price_manager.get_market_price_for_item(
                item.name)

            # Profit calculations
            profit = (market_price * POST_TAX_PERCENT) - cheapest_price
            profit_ratio = float(profit) / float(cheapest_price)
            profit_per_sec = 0 if total_time == 0 else profit/total_time
            profit_per_hour = profit_per_sec * 3600
            last_updated = self.item_price_manager.get_last_update_for_item(item.name)
            profits.append((item.name, best_action, market_price, cheapest_price,
                            profit, profit_ratio, total_time, profit_per_hour, last_updated))

        profits_dataframe = pd.DataFrame(profits, columns=["Item Name", "Course of Action", "Market Price",
                                                           "Cheapest Buy/Craft Price", "Profit (Flat)", "Profit Ratio", "Total Crafting Time", "Profit Per Hour", "Last Updated"])
        profits_dataframe.to_csv(
            r'.\Profit\optimal_per_sec_profit_values.csv', index=False)
        print('Profits data written to ' +
              r'.\Profit\optimal_per_sec_profit_values.csv')
