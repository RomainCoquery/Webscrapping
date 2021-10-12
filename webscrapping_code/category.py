from webscrapping_code.parse import get_parsed
from urllib.parse import urljoin


def get_categories_urls(url):
    """Récupération des liens de chaque catégorie"""
    category_url = []
    for list_url in get_parsed(url).find_all("ul")[2].find_all("a", href=True):
        category_url.append([urljoin(url, list_url["href"]), list_url.text.strip()])
    return category_url


def get_pages_for_category(category_url):
    """Récupération de toutes les pages des catégories du site"""
    category_page_url = [category_url]
    next_button = get_parsed(category_url).find("li", class_="next")
    while next_button:
        page = urljoin(category_url, (next_button.find("a")["href"]))
        next_button = get_parsed(page).find("li", class_="next")
        category_page_url.append(page)
    return category_page_url


def get_books_urls_for_page(category_page_url):
    """Récupération des liens des pages dans les catégories"""
    book_urls = []
    category_page = get_parsed(category_page_url)
    for element in category_page.find_all("h3"):
        book_urls.append(urljoin(category_page_url, element.a.get("href")))
    return book_urls
