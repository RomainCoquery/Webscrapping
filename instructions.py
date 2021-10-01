# -tc- Quelle différence avec final.py ?

import requests
from bs4 import BeautifulSoup as bs

main_url = "http://books.toscrape.com/"
book = "http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html"


def get_parsed(url):
    """Fonction pour appeler et analyser une page du site"""
    response = requests.get(url)
    soup = bs(response.content, 'html.parser')
    return soup


def list_url_category(url):
    """Récupération des liens de chaque catégorie"""
    category_url = []
    for list_url in get_parsed(url).find('ul', class_="nav").find_all('a', href=True):
        category_url.append([url + list_url['href'], list_url.text.strip()])
    category_url.pop(0)
    return category_url


def list_page_category():
    """Récupération des liens des pages dans les catégories"""
    for category_url, category_name in list_url_category(main_url):
        category_page = get_parsed(category_url)
        for element in category_page.find_all('h3'):
            print('http://books.toscrape.com/catalogue/' + element.a.get('href')
                  .replace('../../../', ''))
    return category_url


def product_rating(star):
    """Fonction pour avoir le nombre d etoiles d avis"""
    if "Zero" in star:
        star = 0
    elif "One" in star:
        star = 1
    elif "Two" in star:
        star = 2
    elif "Three" in star:
        star = 3
    elif "Four" in star:
        star = 4
    elif "Five" in star:
        star = 5
    else:
        star = None
    return star


def product_book(book_url):
    """Récupérer les données d un livre"""
    soup = get_parsed(book_url)
    product_page_url = book_url
    title = soup.find("div", class_="product_main").find("h1").text
    category = soup.find("ul", class_="breadcrumb").find_all("a")
    category = category[2].text
    product_description = soup.find("article", class_="product_page").find("p", recursive=False)\
        .text
    try:
        product_description = product_description
    except AttributeError:
        product_description = ''
    img = soup.find("div", class_="thumbnail").find("img")
    img_url = img['src'].replace('../../', main_url)
    product_info = soup.find("table", class_="table-striped").find_all("td")
    universal_product_code = product_info[0].text
    price_excluding_tax = product_info[2].text
    price_including_tax = product_info[3].text
    stock = product_info[5].text
    number_available = stock.replace("In stock (", "").replace(" available)", "")
    review_rating = product_rating(str(soup.find("p", class_="star-rating")))
    return {
        'product_page_url': product_page_url,
        'title': title,
        'category': category,
        'img_url': img_url,
        'universal_product_code': universal_product_code,
        'price_excluding_tax': price_excluding_tax,
        'price_including_tax': price_including_tax,
        'number_available': number_available,
        'review_rating': review_rating,
        'product_description': product_description,
    }


print(product_book(book))
print(list_url_category(main_url))
print(list_page_category())
