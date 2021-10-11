from webscrapping_code.parse import get_parsed
import requests
from urllib.parse import urljoin


main_url = 'http://books.toscrape.com/'


def get_book_data(books_url):
    """Récupérer les données d un livre"""
    star_rating = {'zero': '0', 'One': '1', 'Two': '2', 'Three': '3',
                   'Four': '4', 'Five': '5'}
    soup = get_parsed(books_url)
    product_page_url = books_url
    title = soup.find("div", class_="product_main").find("h1").text
    category = soup.find("ul", class_="breadcrumb").find_all("a")
    category = category[2].text
    product_description = (soup.find("article", class_="product_page")
                           .find("p", recursive=False))
    # gestion des livres qui n ont pas de description
    if product_description is not None:
        product_description = product_description.text
    img = soup.find("div", class_="thumbnail").find("img")
    img_url = urljoin(main_url, img['src'])
    # renommage du titre des images pour correspondre aux limitations des os
    img_name_str = title.lower()[:255]
    img_name = (''.join(x for x in img_name_str if x.isalnum() or x in ' ')
                .replace(' ', '-'))
    product_info = soup.find_all("td")
    universal_product_code = product_info[0].text
    price_excluding_tax = product_info[2].text
    price_including_tax = product_info[3].text
    stock = product_info[5].text
    number_available = (stock.replace("In stock (", "").replace(" available)",
                                                                ""))
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
    """Récupération des images et écriture dans un dossier image de la
    catégorie"""
    response = requests.get(img_url)
    file = open(destination + filename + '.jpg', "wb")
    file.write(response.content)
    file.close()
