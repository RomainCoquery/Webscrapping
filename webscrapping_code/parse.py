import requests
from bs4 import BeautifulSoup


def get_parsed(url):
    """Fonction pour appeler et analyser une page du site"""
    response = requests.get(url)
    if response.ok:
        return BeautifulSoup(response.content, "html.parser")
