import random
from django.shortcuts import render
from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from secrets import choice

excluded_chars = ['[', ']', '{', '}', '(', ')', '=', '>', '<', '"', "'", ';', ':', '\\', '/', ',', '.']
custom_punctuation = ''.join([char for char in punctuation if char not in excluded_chars])


options = [i for i in range(8, 25)]


def home_page(request):
    data = {'characters_options': options}
    pool = save_choices_if_any(request, data)
    if request.GET.get('action') == 'strong':
        password = strong_password_generator()
    elif request.GET.get('action') == 'custom' and data['length'] not in options:
        data['error'] = f"Length ({data['length']}) isn't allowed, please choose from options."
        password = ''
    else:
        password = custom_password_generator(pool, data['length'])
    data['password'] = password
    return render(request, 'passwordgeneratorapp/home_page.html', data)


def strong_password_generator():
    pool = ascii_lowercase + ascii_uppercase + digits
    password = ''
    for _ in range(16):
        password += choice(pool)
        if (_ + 1) % random.randint(3, 6) == 0:
            password += choice(custom_punctuation)
    return password


def custom_password_generator(pool, length):
    # password = ''.join(choice(pool) for _ in range(length))
    # return password
    password = ''
    for _ in range(length):
        password += choice(pool)
        if custom_punctuation in pool and (_ + 1) % random.randint(3, 5) == 0:
            password += choice(custom_punctuation)
    return password


def save_choices_if_any(request, data):
    pool = ''+ascii_lowercase
    if request.GET.get('uppercase'):
        data['uppercase'] = True
        pool += ascii_uppercase
    if request.GET.get('digits'):
        data['digits'] = True
        pool += digits
    if request.GET.get('symbol'):
        data['symbol'] = True
        pool += custom_punctuation
    length = int(request.GET.get('length', 16))
    data['length'] = length
    return pool
