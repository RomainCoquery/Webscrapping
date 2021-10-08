import os.path
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv


main_url = 'http://books.toscrape.com/'


def get_parsed(url):
    """Fonction pour appeler et analyser une page du site"""
    response = requests.get(url)
    if response.ok:
        return BeautifulSoup(response.content, 'html.parser')


def get_categories_urls(url):
    """Récupération des liens de chaque catégorie"""
    category_url = []
    for list_url in get_parsed(url).find_all('ul')[2].find_all('a', href=True):
        category_url.append([urljoin(url, list_url['href']), list_url.text.strip()])
    return category_url


def get_pages_for_category(category_url):
    """Récupération de toutes les pages des catégories du site"""
    category_page_url = [category_url]
    next_button = get_parsed(category_url).find('li', class_='next')
    while next_button:
        page = urljoin(category_url, (next_button.find('a')['href']))
        next_button = get_parsed(page).find('li', class_='next')
        category_page_url.append(page)
    return category_page_url


def get_books_urls_for_page(category_page_url):
    """Récupération des liens des pages dans les catégories"""
    book_urls = []
    category_page = get_parsed(category_page_url)
    for element in category_page.find_all('h3'):
        book_urls.append(urljoin(category_page_url, element.a.get('href')))
    return book_urls


def get_book_data(books_url):
    """Récupérer les données d un livre"""
    star_rating = {'zero': '0', 'One': '1', 'Two': '2', 'Three': '3', 'Four': '4', 'Five': '5'}
    soup = get_parsed(books_url)
    product_page_url = books_url
    title = soup.find("div", class_="product_main").find("h1").text
    category = soup.find("ul", class_="breadcrumb").find_all("a")
    category = category[2].text
    product_description = soup.find("article", class_="product_page").find("p", recursive=False)
    # gestion des livres qui n ont pas de description
    if product_description is not None:
        product_description = product_description.text
    img = soup.find("div", class_="thumbnail").find("img")
    img_url = urljoin(main_url, img['src'])
    # renommage du titre des images pour correspondre aux limitations des os
    img_name_str = title.lower()[:255]
    img_name = ''.join(x for x in img_name_str if x.isalnum() or x in ' ').replace(' ', '-')
    product_info = soup.find_all("td")
    universal_product_code = product_info[0].text
    price_excluding_tax = product_info[2].text
    price_including_tax = product_info[3].text
    stock = product_info[5].text
    number_available = stock.replace("In stock (", "").replace(" available)", "")
    review_rating = star_rating[soup.find(class_="star-rating")['class'][1]]
    return {
        'product_page_url': product_page_url,
        'title': title,
        'category': category,
        'img_url': img_url,
        'img_name': img_name,
        'universal_product_code': universal_product_code,
        'price_excluding_tax': price_excluding_tax,
        'price_including_tax': price_including_tax,
        'number_available': number_available,
        'review_rating': review_rating,
        'product_description': product_description,
    }


def get_book_image(img_url, destination, filename):
    """Récupération des images et écriture dans un dossier image de la catégorie"""
    response = requests.get(img_url)
    file = open(destination + filename + '.jpg', "wb")
    file.write(response.content)
    file.close()


def main():
    for category_url, category_name in get_categories_urls(main_url):
        print(f'récupération de la catégorie {category_name}')
        # Création du dossier webscrapping
        if not os.path.exists('webscrapping'):
            os.mkdir('webscrapping')
        # création de dossier par catégorie
        path_category = 'webscrapping/' + category_name
        if not os.path.exists('webscrapping/' + category_name):
            os.mkdir('webscrapping/' + category_name)
        # création du dossier image par catégorie
        if not os.path.exists('webscrapping/' + category_name + '/img'):
            os.mkdir('webscrapping/' + category_name + '/img')
        # création de fichiers csv avec les noms de colonnes pour chaque catégorie
        with open(f"{path_category}/{category_name}.csv", 'w',
                  encoding='utf-8-sig', newline='') as file:
            fieldnames = ['product_page_url', 'title', 'category', 'img_url', 'img_name',
                          'universal_product_code', 'price_excluding_tax', 'price_including_tax',
                          'number_available', 'review_rating', 'product_description']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for category_page in get_pages_for_category(category_url):
                for book_url in get_books_urls_for_page(category_page):
                    # scrapping des données et des images dans chaque catégorie
                    book_data = get_book_data(book_url)
                    writer.writerow(book_data)
                    (get_book_image(book_data['img_url'], 'webscrapping/' + category_name + '/img/',
                                    book_data['img_name']))


if __name__ == "__main__":
    main()
