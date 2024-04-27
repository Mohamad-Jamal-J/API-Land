from django.shortcuts import render, redirect
import requests
import urllib.parse
from django import template
import json
from secrets import choice

register = template.Library()


def load_json_data(path):
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)


def home_page(request):
    return render(request, 'jokesapp/home_page.html')


def fetch_random_joke(request):
    JOKE_API_URL = "https://icanhazdadjoke.com/"  # Replace with your joke API URL

    headers = {
        'Accept': 'application/json',
    }
    data = {}
    try:
        response = requests.get(JOKE_API_URL, headers=headers)
        if response.status_code == 200:
            data['joke'] = response.json()['joke']
        else:
            data['error'] = f"Error: {response.status_code}"
    except(requests.RequestException, KeyError):
        data['error'] = 'Exception'
    # return data
    return render(request, 'jokesapp/random_jokes.html', data)


def fetch_chandler_comment(request):
    JOKE_API_URL = "https://sarcasmapi.onrender.com/"

    data = {}
    try:
        response = requests.get(JOKE_API_URL)
        if response.status_code == 200:
            data['sarcasm'] = response.json()['sarcasm']
        else:
            data['error'] = f"Error: {response.status_code}"
    except(requests.RequestException, KeyError):
        data['error'] = 'Exception'
    return render(request, 'jokesapp/chandler_comments.html', data)


def get_seinfeld_home_page(request):
    return render(request, 'jokesapp/seinfeld_home_page.html')


def fetch_seinfeld_quote(request):
    seinfeld_quotes = load_json_data('jokesapp/data/seinfeld.json')
    characters = ('Jerry', 'George', 'Kramer', 'Elaine')
    character = request.GET.get('character')
    data = {}

    if seinfeld_quotes:
        if character and character in characters:
            data['results'] = filter_seinfeld_quotes_by_author(seinfeld_quotes, character)
            data['character'] = character
            return render(request, 'jokesapp/seinfeld_character_quotes.html', data)
        else:
            data['quote'] = choice(seinfeld_quotes)
    else:
        data['error'] = "Error: internal"
    return render(request, 'jokesapp/seinfeld_random_quotes.html', data)


def filter_seinfeld_quotes_by_author(quotes_list, author_name):
    filtered_quotes = [quote for quote in quotes_list if quote.get("author") == author_name]
    return filtered_quotes


def redirect_to_page(request):
    if 'page' not in request.GET:
        error_message = "Page Doesn't Exist"
        return render(request, 'jokesapp/home_page.html', {'error': error_message})

    selected_page = request.GET.get('page')
    return redirect(f"/jokes-app/{selected_page}")


def search_for_jokes(request):
    JOKE_API_URL = "https://icanhazdadjoke.com/search?term="
    headers = {
        'Accept': 'application/json',
    }
    data = {}

    if request.method == 'POST':
        try:
            term = request.POST.get('term')
            if term:
                url = f"{JOKE_API_URL}{urllib.parse.quote(term)}"
                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    response = response.json()
                    if response['total_jokes'] > 0:
                        fill_data(data, response, term)
                    else:
                        data['error'] = f"Sorry, No Jokes with the Term '{term}' Were Found!"
                else:
                    data['error'] = f"Error: {response.status_code}"
            else:
                data['error'] = 'No Terms Were Provided'
        except (requests.RequestException, KeyError):
            data['error'] = 'Exception'
    elif 'term' in request.GET and 'page' in request.GET:
        term = request.GET.get('term')
        page = request.GET.get('page', 1)
        url = f"{JOKE_API_URL}{urllib.parse.quote(term)}&page={page}"
        response = requests.get(url, headers=headers)
        response = response.json()
        if response['total_jokes'] > 0:
            fill_data(data, response, term)

    return render(request, 'jokesapp/joke_search_page.html', data)


def fill_data(data, response, term):
    data['total_jokes'] = response['total_jokes']
    data['total_pages'] = response['total_pages']
    data['limit'] = response['limit']
    data['results'] = response['results']
    data['search_term'] = term
    data['current_page'] = response['current_page']
    data['next_page'] = response['next_page']
    data['previous_page'] = response['previous_page']
