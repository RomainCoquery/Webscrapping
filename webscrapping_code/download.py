from webscrapping_code.category import (get_categories_urls,
                                        get_pages_for_category,
                                        get_books_urls_for_page)
from webscrapping_code.books import get_book_data, get_book_image
import os.path
import csv


main_url = 'http://books.toscrape.com/'


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
        # création fichiers csv avec les noms de colonnes pour chaque catégorie
        with open(f"{path_category}/{category_name}.csv", 'w',
                  encoding='utf-8-sig', newline='') as file:
            fieldnames = ['product_page_url', 'title', 'category', 'img_url',
                          'img_name', 'universal_product_code',
                          'price_excluding_tax', 'price_including_tax',
                          'number_available', 'review_rating',
                          'product_description']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for category_page in get_pages_for_category(category_url):
                for book_url in get_books_urls_for_page(category_page):
                    # scrapping des données et des images dans chaque catégorie
                    book_data = get_book_data(book_url)
                    writer.writerow(book_data)
                    (get_book_image(book_data['img_url'], 'webscrapping/'
                                    + category_name + '/img/',
                                    book_data['img_name']))
