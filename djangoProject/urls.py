"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from djangoProject import views as manager_views
from django.shortcuts import render
from passwordgeneratorapp import views as password_app_views
from weatherapp import views as weather_app_views
from jokesapp import views as jokes_app_views
from thronesapp import views as thrones_app_views

urlpatterns = [
              path('admin/', admin.site.urls),
              path('', manager_views.index, name='home_page'),
              path('about-me/', lambda request: render(request, 'about_me.html'), name='about_me'),
              path('contact-us/', lambda request: render(request, 'contact_us.html'), name='contact_us'),
              path('redirect-to-app/', manager_views.redirect_to_app, name='redirect_to_app'),
              path('weather-app/', weather_app_views.home_page),
              path('password-generator-app/', password_app_views.home_page, name='passwordgenerator'),
              path('jokes-app/', jokes_app_views.home_page),
              path('redirect-to-joke-page/', jokes_app_views.redirect_to_page, name='redirect_to_joke_page'),
              path('jokes-app/random/', jokes_app_views.fetch_random_joke),
              path('jokes-app/chandler/', jokes_app_views.fetch_chandler_comment),
              path('jokes-app/seinfeld/', jokes_app_views.get_seinfeld_home_page),
              path('jokes-app/seinfeld/quotes', jokes_app_views.fetch_seinfeld_quote
                   , name='seinfeld_character'),
              path('jokes-app/search/', jokes_app_views.search_for_jokes, name='search_for_jokes'),
              path('redirect-to-thrones-page/', thrones_app_views.redirect_to_page,
                   name='redirect_to_thrones_page'),
              path('thrones-app/random/', thrones_app_views.fetch_random_quote),
              path('thrones-app/characters-quotes/', thrones_app_views.fetch_all_characters_quotes,
                   name='characters_quotes'),
              path('thrones-app/houses-information/', thrones_app_views.fetch_all_houses_information,
                   name='houses_information'),
              path('thrones-app/all-quotes/', thrones_app_views.fetch_all_quotes, name='thrones-all-quotes'),
              path('thrones-app/', thrones_app_views.home_page),

]
