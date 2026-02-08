# File: restaurant/views.py
# Author: Nicholas Sima (nicksima@bu.edu)
# Description: the views function to handle all views for restaurant app

from django.shortcuts import render
from datetime import datetime, timedelta
import random

# Menu items with prices
MENU_ITEMS = {
    'burger': {'name': 'Classic Burger', 'price': 12.99},
    'pizza': {'name': 'Margherita Pizza', 'price': 15.99},
    'salad': {'name': 'Caesar Salad', 'price': 9.99},
    'pasta': {'name': 'Spaghetti Carbonara', 'price': 14.99},
}

# Pizza toppings with prices
PIZZA_TOPPINGS = {
    'pepperoni': {'name': 'Pepperoni', 'price': 1.50},
    'mushrooms': {'name': 'Mushrooms', 'price': 1.00},
    'olives': {'name': 'Olives', 'price': 1.00},
    'extra_cheese': {'name': 'Extra Cheese', 'price': 1.50},
}

# Daily specials list
DAILY_SPECIALS = [
    {'name': 'Grilled Salmon', 'price': 18.99, 'description': 'Fresh Atlantic salmon with lemon butter sauce'},
    {'name': 'BBQ Ribs', 'price': 16.99, 'description': 'Slow-cooked baby back ribs with house BBQ sauce'},
    {'name': 'Lobster Bisque', 'price': 11.99, 'description': 'Creamy lobster soup'},
    {'name': 'Truffle Risotto', 'price': 17.99, 'description': 'Rice with black truffle and parmesan'},
]


def main(request):
    """View for the main restaurant page."""
    template_name = 'restaurant/main.html'
    return render(request, template_name)


def order(request):
    """View for the order page with menu and daily special."""
    template_name = 'restaurant/order.html'

    # random daily special
    daily_special = random.choice(DAILY_SPECIALS)

    context = {
        'menu_items': MENU_ITEMS,
        'pizza_toppings': PIZZA_TOPPINGS,
        'daily_special': daily_special,
    }

    return render(request, template_name, context)


def confirmation(request):
    """View to process order submission and display confirmation."""
    template_name = 'restaurant/confirmation.html'

    if request.POST:
        customer_name = request.POST.get('name', '')
        customer_phone = request.POST.get('phone', '')
        customer_email = request.POST.get('email', '')
        special_instructions = request.POST.get('special_instructions', '')

        ordered_items = []
        total_price = 0.0

        if request.POST.get('burger'):
            ordered_items.append(MENU_ITEMS['burger'])
            total_price += MENU_ITEMS['burger']['price']

        if request.POST.get('pizza'):
            ordered_items.append(MENU_ITEMS['pizza'])
            total_price += MENU_ITEMS['pizza']['price']

            # pizza toppings
            pizza_toppings_ordered = []
            for topping_key, topping_info in PIZZA_TOPPINGS.items():
                if request.POST.get(topping_key):
                    pizza_toppings_ordered.append(topping_info)
                    total_price += topping_info['price']

        if request.POST.get('salad'):
            ordered_items.append(MENU_ITEMS['salad'])
            total_price += MENU_ITEMS['salad']['price']

        if request.POST.get('pasta'):
            ordered_items.append(MENU_ITEMS['pasta'])
            total_price += MENU_ITEMS['pasta']['price']

        # if daily special was ordered
        if request.POST.get('daily_special'):
            special_name = request.POST.get('daily_special_name', 'Daily Special')
            special_price = float(request.POST.get('daily_special_price', 0))
            ordered_items.append({'name': special_name, 'price': special_price})
            total_price += special_price

        minutes_until_ready = random.randint(30, 60)
        # in UTC time, ssh server doesn't have pytz installed
        ready_time = datetime.now() + timedelta(minutes=minutes_until_ready)

        context = {
            'customer_name': customer_name,
            'customer_phone': customer_phone,
            'customer_email': customer_email,
            'special_instructions': special_instructions,
            'ordered_items': ordered_items,
            'pizza_toppings_ordered': pizza_toppings_ordered if request.POST.get('pizza') else [],
            'total_price': round(total_price, 2),
            'ready_time': ready_time.strftime('%I:%M %p'),
            'minutes_until_ready': minutes_until_ready,
        }

        return render(request, template_name, context)
    # unknown request, revert to previous page
    return render(request, 'restaurant/order.html')
