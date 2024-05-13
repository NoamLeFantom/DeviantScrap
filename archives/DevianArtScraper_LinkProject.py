import requests
from bs4 import BeautifulSoup
import time

import subprocess
import sys
# Récupérer le pseudo à partir des arguments de la ligne de commande
pseudo = sys.argv[1]
print("Pseudo récupéré :", pseudo)



url = "https://www.deviantart.com/"+pseudo+"/gallery"

response = requests.get(url)
html = response.content

soup = BeautifulSoup(html, 'html.parser')
divs = soup.select('div._1xcj5')  # Sélectionne les divs avec les classes spécifiques

print("Debut de scraping sur la page gallery")
with open("links.txt", "w") as file:
    for div in divs:
        time.sleep(1)
        # Trouve le premier lien <a> dans la div
        first_link = div.find('a')
        if first_link:  # Vérifie si un lien a été trouvé dans la div
            href = first_link.get("href")

            print("URL du lien dans la div:" + href)
            file.writelines(href + "\n")
            //dzfzefzefzefzfzfzfzfzfzfzfzfzf
        else:
            print("Aucun lien trouvé dans la div")
print("Fin")
subprocess.run(["python", "DevianArtScraper_DataRecover.py", pseudo])