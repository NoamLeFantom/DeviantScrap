import os
import requests
from bs4 import BeautifulSoup
import json

import subprocess

# Fonction pour télécharger une image à partir de son URL et la sauvegarder dans un dossier
def telecharger_image(url, nom_dossier, nom_fichier):
    # Créer le dossier s'il n'existe pas déjà
    if not os.path.exists(nom_dossier):
        os.makedirs(nom_dossier)
    # Chemin complet du fichier où l'image sera sauvegardée
    output_folder = os.path.join(nom_dossier, nom_fichier)
    # Envoyer une requête GET à l'URL de l'image
    reponse = requests.get(url)
    # Vérifier si la requête a réussi (statut 200)
    if reponse.status_code == 200:
        # Ouvrir un fichier en mode binaire pour écrire l'image téléchargée
        with open(output_folder, 'wb') as f:
            # Écrire les données de l'image dans le fichier
            f.write(reponse.content)
        print("L'image a été téléchargée avec succès sous le nom", nom_fichier, "dans le dossier", nom_dossier)
    else:
        print("Impossible de télécharger l'image. Statut de la réponse :", reponse.status_code)

# Fonction pour récupérer les informations à partir d'un lien
def get_info_from_link(url, custom_list):
    response = requests.get(url)
    if response.status_code == 200:
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')

        title_tag = soup.find('h1', class_='_33gAi')
        description_tag = soup.find('div', class_='legacy-journal')
        image_tag = soup.find('img', class_='_28lPU')
        detail_tags = soup.find_all('span', class_='_1nwad')

        # Récupérer le contenu de chaque détail et stocker dans une liste
        details_content = [detail_tag.text.strip() for detail_tag in detail_tags]

        # Filtrer les détails qui sont dans la liste personnalisée
        filtered_details = [detail for detail in details_content if detail in custom_list]

        if filtered_details:
            if title_tag:
                # Récupérer le contenu de la balise h1 (titre)
                titre_content = title_tag.text.strip()
                # Récupérer le contenu de la balise div (description)
                description_content = description_tag.text.strip()
                image_link = image_tag['src'] if image_tag else None  # Si image_tag est None, image_link sera None également
                nom_fichier=titre_content+".png"
                telecharger_image(image_link, output_folder, nom_fichier)
                # Retourner un dictionnaire avec les informations extraites
                return {"titre": titre_content, "description": description_content, "imageL_Link": image_link, "details": filtered_details}
            else:
                print("Balise h1 avec la classe spécifique non trouvée.")
                return None
        else:
            print("Aucun détail correspondant à la liste personnalisée trouvé.")
            return None
    else:
        print("Impossible de récupérer les informations à partir du lien :")
        return None

# Lecture de la liste personnalisée à partir du fichier texte
with open("custom_list.txt", "r") as file:
    custom_list = file.read().splitlines()

# Lecture des liens à partir du fichier texte
with open("links.txt", "r") as file:
    links = file.readlines()

# Supprimer les sauts de ligne des liens
links = [link.strip() for link in links]

# Initialise un dictionnaire pour stocker les données des projets
data = {}

# Parcourir chaque lien et récupérer les informations
for i, link in enumerate(links, start=1):
    print("Récupération d'informations pour le lien :" + link)
    project_info = get_info_from_link(link, custom_list)
    if project_info:
        project_key = f"projet{i}"
        data[project_key] = project_info

# Spécifier le chemin du fichier JSON de sortie
output_file = "output.json"

# Écrire le dictionnaire dans le fichier JSON
with open(output_file, "w") as json_file:
    json.dump(data, json_file, indent=4)

print("Données écrites avec succès dans le fichier JSON :" + output_file)
