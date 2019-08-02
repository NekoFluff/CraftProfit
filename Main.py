from ItemManager import ItemManager
from ShoppingCart import ShoppingCart

item_manager = ItemManager()


# Get the shopping cart for the item you would like to craft
def prompt_user_for_desired_item():
    desired_item = input('What item would you like to craft?\t')

    if desired_item not in item_manager.items:
        print('{0} does is not a item with a recipe. Please add the recipe for {0} in the Recipes folder.'.format(desired_item))
    else:
        quantity = int(input('How many would you like to craft?\t'))
        item = item_manager.items[desired_item]
        shopping_cart = ShoppingCart(item_manager)
        shopping_cart.add_item_to_cart(item=item, shopping_cart_quantity=quantity)
        shopping_cart.print_shopping_cart()

if __name__ == "__main__":
    print("Testing ItemManager using all available recipes.")
    item_manager.calculate_market_craft_costs()
    print('-'*120)
    item_manager.calculate_hand_craft_costs()
    print('-'*120)
    item_manager.calculate_optimal_craft_costs()
    print('-'*120)
    item_manager.item_price_manager.save_market_prices()

    #---------------
    while True:
        prompt_user_for_desired_item()
    