# -tc- évite de nommer un module functions.py. Un module contient forcément des
# -tc- des fonctions (ou devrait). Ce n'est donc pas très descriptif

import requests
# -tc- Evite de raccourcir le nom BeautifulSoup par bs. BeautifulSoup est une classe
# -tc- et DOIT avoir un nom qui commence par une majuscule
from bs4 import BeautifulSoup as bs

main_url = 'http://books.toscrape.com/'


def get_parsed(url):
    """Fonction pour appeler et analyser une page du site"""
    response = requests.get(url)
    # -tc- TODO: gérer les erreurs !
    soup = bs(response.content, 'html.parser')
    return soup


def get_categories_urls(url):
    """Récupération des liens de chaque catégorie"""
    category_url = []
    for list_url in get_parsed(url).find('ul', class_="nav").find_all('a', href=True):
        # -tc- utiliser urljoin() pour concaténer les urls, plutôt que l'opérateur +
        category_url.append([url + list_url['href'], list_url.text.strip()])
    # -tc- pourquoi insérer la première url dans la liste si on ne la veut pas ?
    category_url.pop(0)
    return category_url


def get_category_pages(category_url):
    """Récupération des liens des pages dans les catégories"""
    for categories_url, category_name in get_categories_urls(main_url):
        category_page = get_parsed(category_url)
        for element in category_page.find_all('h3'):
            print('http://books.toscrape.com/catalogue/' + element.a.get('href')
                  .replace('../../../', ''))
    return categories_url


def get_pages_for_category(url):
    categories_url = []
    for list_url in get_parsed(url).find('ul', class_="nav").find_all('a', href=True):
        # -tc- utiliser de préférence la fonction urllib.parse.urljoin() pour coller main_url et list_url['href']
        category_url = main_url + list_url['href']
        next_button = get_parsed(category_url).find('li', class_='next')
        while next_button:
            # -tc- comme ci-dessus, utiliser urllib.parse.urljoin() pour coller les morceaux d'url. replace n'est ni nécessaire ni souhaité
            page = category_url.replace('index.html', '') + (next_button.find('a')['href'])
            next_button = get_parsed(page).find('li', class_='next')
            categories_url.append(page)
            # -tc- le continue ici ne sert à rien, à enlever
            continue
    return categories_url


# -tc- Il semblerait plus logique ici d'utiliser un dictionnaire. Plus efficace et... c'est fait pour cela
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
    # -tc- éviter d'usage de \ à l'aide de parenthèses
    # product_description = (
    #     soup
    #     .find("article", class_="product_page")
    #     .find("p", recursive=False)
    #     .text
    # )
    # -tc- attention, l'exception aura lieu ici si pas de description
    product_description = soup.find("article", class_="product_page").find("p", recursive=False)\
        .text
    # -tc- ne sert à rien. Plutôt if product_description is not None:
    try:
        product_description = product_description
    except AttributeError:
        product_description = ''
    img = soup.find("div", class_="thumbnail").find("img")
    # -tc- éviter replace, urllib.parse.urljoin() est faite pour cela
    img_url = img['src'].replace('../../', main_url)
    product_info = soup.find("table", class_="table-striped").find_all("td")
    # -tc- Si une info manque ici, il y aura une KeyError
    universal_product_code = product_info[0].text
    price_excluding_tax = product_info[2].text
    price_including_tax = product_info[3].text
    stock = product_info[5].text
    number_available = stock.replace("In stock (", "").replace(" available)", "")
    # -tc- comme dit plus haut, probablement plus adapté d'utiliser un dictionnaire ici
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


# print(get_categories_urls(main_url))
# print(get_category_pages(main_url))
print(get_pages_for_category(main_url))
# print(product_book(book))

# -tc- dans l'idéal ici, on va ici éviter que la fonction get_pages_for_category(main_url) ne s'exécute lors d'un import.
# if __name__ == "__main__":
#     print(get_pages_for_category(main_url))
# 
# -tc- dans l'idéal, on a également l'habitude de créer une fonction appelée main() pour y mettre le code de démarrage du programme
# def main():
#     print(get_pages_for_category(main_url))
#
# if __name__ == "__main__":
#     print(get_pages_for_category(main_url))
