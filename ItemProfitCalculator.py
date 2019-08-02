class ItemProfitCalculator():

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
                total_time += quantity * time_cost# Time cost for each ingredient crafted
            # if (self.name == "Pure Iron Crystal"):
                # print("{:20} {:20} {:20} {:20} {:20}".format(ingredient, lowest_cost, quantity, quantity * lowest_cost, total_price))
                # print("{:20} {:20} {:20} {:20} {:20}".format(ingredient, time_cost, quantity, quantity * time_cost, total_time))
        
        market_price = self.item_price_manager.get_market_price_for_item(self.name)
        total_price = total_price / self.quantity_produced # Division to get price per item

        if market_price <= total_price:  # If it is cheaper to buy it than to make it yourself
            total_price = market_price
            best_action = "Market Buy"
            total_time = 0
        else:
            best_action = "Craft"
            total_time += self.time_to_produce # How much time in seconds to produce this item
        # if (self.name == "Ship License: Fishing Boat"):
            # exit(1)
        
        total_time /= self.quantity_produced
        self.optimal_craft_cost = total_price
        self.optimal_craft_time = total_time
        self.optimal_craft_action = best_action
        return total_price, total_time, best_action