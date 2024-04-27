
from django.shortcuts import render, redirect
import requests
from django import template
import json
from secrets import choice

register = template.Library()


def load_json_data(path):
    with open(path, 'r') as file:
        return json.load(file)


houses_options = load_json_data('thronesapp/data/houses.json')
characters_options = load_json_data('thronesapp/data/characters.json')


def home_page(request):
    return render(request, 'thronesapp/home_page.html')


def redirect_to_page(request):
    if 'page' not in request.GET:
        error_message = "Page Doesn't Exist"
        return render(request, 'thronesapp/home_page.html', {'error': error_message})

    selected_page = request.GET.get('page')
    return redirect(f"/thrones-app/{selected_page}")


def fetch_random_quote(request):
    QUOTE_API_URL = "https://api.gameofthronesquotes.xyz/v1/random"
    data = {}
    try:
        response = requests.get(QUOTE_API_URL)
        if response.status_code == 200:
            data['sentence'] = response.json()['sentence']
            data['character'] = response.json()['character']
        else:
            data['error'] = f"Error: {response.status_code}"
    except(requests.RequestException, KeyError):
        data['error'] = 'Exception'
    return render(request, 'thronesapp/random_quote.html', data)


def fetch_all_characters_quotes(request):
    QUOTE_API_URL = "https://api.gameofthronesquotes.xyz/v1/characters"
    author_name = request.GET.get('author')
    data = {'characters_options': characters_options}
    is_character = False
    if author_name:
        for option in characters_options:
            if author_name == option['slug']:
                is_character = True

        if is_character:
            QUOTE_API_URL = f"https://api.gameofthronesquotes.xyz/v1/character/{author_name}"
            data['slug'] = author_name
        else:
            data['error'] = f"Error: {author_name} is not a valid slug, please stick to the characters options"
            return render(request, 'thronesapp/characters_quote_page.html', data)

    try:
        response = requests.get(QUOTE_API_URL)
        if response.status_code == 200:
            data['results'] = response.json()
        else:
            data['error'] = f"Error: {response.status_code}"
    except(requests.RequestException, KeyError):
        data['error'] = 'Exception'
    return render(request, 'thronesapp/characters_quote_page.html', data)


def fetch_all_houses_information(request):
    HOUSE_API_URL = "https://api.gameofthronesquotes.xyz/v1/houses"
    house_name = request.GET.get('house')
    data = {'houses_options': houses_options}
    is_house = False
    if house_name:
        for house in houses_options:
            if house_name == house['slug']:
                is_house = True

        if is_house:
            HOUSE_API_URL = f"https://api.gameofthronesquotes.xyz/v1/house/{house_name}"
            data['slug'] = house_name
        else:
            data['error'] = f"Error: {house_name} is not a valid slug, please stick to the house options"
            return render(request, 'thronesapp/house_quote_page.html', data)

    try:
        response = requests.get(HOUSE_API_URL)
        if response.status_code == 200:
            data['results'] = response.json()
        else:
            data['error'] = f"Error: {response.status_code}"
    except(requests.RequestException, KeyError):
        data['error'] = 'Exception'
    return render(request, 'thronesapp/house_quote_page.html', data)


def fetch_all_quotes(request):
    choices = (3, 7, 9)
    chosen = choice(choices)
    QUOTE_API_URL = f"https://api.gameofthronesquotes.xyz/v1/random/{chosen}"
    data = {'choice': chosen}
    try:
        response = requests.get(QUOTE_API_URL)
        if response.status_code == 200:
            data['results'] = response.json()
        else:
            data['error'] = f"Error: {response.status_code}"
    except(requests.RequestException, KeyError):
        data['error'] = 'Exception'
    return render(request, 'thronesapp/all_quote_page.html', data)
