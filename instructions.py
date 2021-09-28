import requests
from bs4 import BeautifulSoup as bs

main_url = "https://books.toscrape.com/"
purl = "https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html"


def get_parsed(url):
    """Fonction pour appeler et analyser une page du site"""
    response = requests.get(url)
    soup = bs(response.content, 'html.parser')
    return soup


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


def list_url_category():
    """Récupération des url des catégories"""
    for list_url in get_parsed(main_url).find('ul', class_="nav nav-list").find_all('a', href=True):
        print(main_url + list_url['href'])


def product_book(purl):
    """Récupérer les données d un livre"""
    soup = get_parsed(purl)
    product_page_url = purl
    title = soup.find("div", class_="product_main").find("h1").string
    category = soup.find("ul", class_="breadcrumb").find_all("a")
    category = category[2].string
    product_description = soup.find("article", class_="product_page").find("p", recursive=False).string
    try:
        product_description = product_description
    except AttributeError:
        product_description = ''
    img = soup.find("div", class_="thumbnail").find("img")
    img_url = img['src'].replace('../../', main_url)
    product_info = soup.find("table", class_="table-striped").find_all("td")
    universal_product_code = product_info[0].string
    price_excluding_tax = product_info[2].string
    price_including_tax = product_info[3].string
    stock = product_info[5].string
    number_available = stock.replace("In stock (", "").replace(" available)", "")
    review_rating = product_rating(str(soup.find("p", class_="star-rating")))
    return product_page_url, title, category, img_url, universal_product_code,\
        price_excluding_tax, price_including_tax, number_available, review_rating, \
        product_description,


print(product_book(purl))
print(list_url_category())
