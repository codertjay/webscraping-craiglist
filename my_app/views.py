from django.shortcuts import render
from bs4 import BeautifulSoup
from requests.compat import quote_plus
import requests
from my_app import models


BASE_CRAIGSLIST_URL = 'https://accra.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://accra.craigslist.org/{}_300x300.jpg'


def main(request):
    return render(request,'my_app/main.html')


def new_search(request):
    # i am getting the search from the user search
    search = request.POST.get('search')
    # i am adding the search to the database
    models.search.objects.create(search=search)
    # here i am dding plus to the craiglist url and the search iam using from the screen
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))

    response = requests.get(final_url)
    data = response.text
    # the soup is a variable so i use the beautifulsoup to read the data
    soup = BeautifulSoup(data, features='html.parser')
    # here i am finding all the links that has class result-title
    # post_titles = soup.find_all('a', {'class':'result-title'})
    # print(post_titles[0].get('href'))

    # this is for the post which have the class result-row
    post_listings = soup.find_all('a', {'class':'result-row'})


    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')
            post_image_url =BASE_IMAGE_URL.format(post_image_id)

        else:
            post_image_url ='https: //craigslist/images/peace.jpg'


        final_postings.append((post_title,post_url,post_price,post_image_url))




    search = request.POST.get('search')
    print(search)
    context = {
        'searches': search,
        'final_posting': final_postings
    }
    return render(request, 'my_app/search.html', context)






