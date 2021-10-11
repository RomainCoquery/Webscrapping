***Note : ce projet est réalisé pendant ma formation [OpenClassrooms](https://openclassrooms.com/fr/).***

# Webscrapping
### Ce script permet de récupérer les données du site [Books to Scrape](http://books.toscrape.com/) dans un fichier csv.
### Compatible avec Python3 sur tout OS.
### Installation
#### Dézippez le code, créez un environnement virtuel et activez-le :
```
python -m venv .venv
source .venv/bin/activate
```
#### Installation des packages 
```
pip install -r requirements.txt
```
#### Optionnel : Valider le code avec flake8(https://flake8.pycqa.org/en/latest/) et black(https://github.com/psf/black)
```
#pour flake8 :
pip install flake8
flake8 webscrapping_code
#pour black
black {webscrapping_code}
```
#### Lancer le script
```
python -m webscrapping_code
```
Les données sont enregistrées dans le sous dossier ***webscrapping*** du répertoire ***webscrapping_code***.