from random import randint
from django.shortcuts import render
from django.http import HttpRequest
from timeit import default_timer


def shop_index(request: HttpRequest):
    purchases = [
        {'customer': 'Боб', 'item': 'шляпа', 'price': 500},
        {'customer': 'Моника', 'item': 'шоколадка', 'price': 100},
        {'customer': 'Тайлер', 'item': 'гитара', 'price': 900},
        {'customer': 'Джош', 'item': 'машина', 'price': 5000},
        {'customer': 'Ник', 'item': 'футболка', 'price': 700},
    ]
    context = {
        'time_running': default_timer(),
        'random_num': randint(1, 100),
        'purchases': purchases,
        'test_string': 'Каждый охотник желает знать где сидит фазан',
    }
    return render(request, 'shopapp/shop-index.html', context=context)
