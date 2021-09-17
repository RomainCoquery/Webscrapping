import requests
from bs4 import BeautifulSoup

main_url = "https://books.toscrape.com/"
url = "https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html"

page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
product_page_url = url
title = soup.find("div", class_="product_main").find("h1").string
category = soup.find("ul", class_="breadcrumb").find_all("a")
category = category[2].string
product_description = soup.find("article", class_="product_page").find("p", recursive=False).string
try:
    product_description = product_description
except AttributeError:
    description = ""
img = soup.find("div", class_="thumbnail").find("img")
img_url = img['src'].replace('../../', main_url)
product_info = soup.find("table", class_="table-striped").find_all("td")
universal_product_code = product_info[0].string
price_excluding_tax = product_info[2].string
price_including_tax = product_info[3].string
stock = product_info[5].string
number_available = stock.replace("In stock (", "").replace(" available)", "")


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


review_rating = product_rating(str(soup.find("p", class_="star-rating")))
print(product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax,
      number_available, category, review_rating, img_url, product_description)
