import requests
from bs4 import BeautifulSoup
import json
import os
import re
import tkinter as tk
import tkinter.font as tkFont
from tkinter.scrolledtext import ScrolledText

class App:
    def __init__(self, root):
        # setting title
        root.title("")
        # setting window size
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, screenwidth, screenheight / 10)
        root.geometry(alignstr)
        root.resizable(width=True, height=True)

        Label_Name_Retrieve = tk.Label(root)
        ft = tkFont.Font(family='Times', size=10)
        Label_Name_Retrieve["font"] = ft
        Label_Name_Retrieve["fg"] = "#333333"
        Label_Name_Retrieve["justify"] = "center"
        Label_Name_Retrieve["text"] = "Pseudo à récupérer :"
        Label_Name_Retrieve.place(x=50, y=110, width=250, height=25)

        self.Input_Label_Name_Retrieve = tk.Entry(root)
        self.Input_Label_Name_Retrieve["borderwidth"] = "1px"
        self.Input_Label_Name_Retrieve["font"] = ft
        self.Input_Label_Name_Retrieve["fg"] = "#333333"
        self.Input_Label_Name_Retrieve["justify"] = "center"
        self.Input_Label_Name_Retrieve.place(x=250, y=110, width=200, height=25)

        Label_Tag_Retrieve = tk.Label(root)
        Label_Tag_Retrieve["font"] = ft
        Label_Tag_Retrieve["fg"] = "#333333"
        Label_Tag_Retrieve["justify"] = "center"
        Label_Tag_Retrieve["text"] = "Spécifique tag :"
        Label_Tag_Retrieve.place(x=125, y=160, width=100, height=25)

        self.Input_Label_Tag_Retrieve = tk.Entry(root)
        self.Input_Label_Tag_Retrieve["borderwidth"] = "1px"
        self.Input_Label_Tag_Retrieve["font"] = ft
        self.Input_Label_Tag_Retrieve["fg"] = "#000001"
        self.Input_Label_Tag_Retrieve["justify"] = "center"
        self.Input_Label_Tag_Retrieve.place(x=250, y=160, width=70, height=25)

        Label_CheckBox_activeTag = tk.Label(root)
        Label_CheckBox_activeTag["font"] = ft
        Label_CheckBox_activeTag["fg"] = "#333333"
        Label_CheckBox_activeTag["justify"] = "center"
        Label_CheckBox_activeTag["text"] = "Activer les tags spécifique :"
        Label_CheckBox_activeTag.place(x=25, y=210, width=250, height=25)

        Button_Start = tk.Button(root)
        Button_Start["bg"] = "#f0f0f0"
        Button_Start["font"] = ft
        Button_Start["fg"] = "#000000"
        Button_Start["justify"] = "center"
        Button_Start["text"] = "Start"
        Button_Start.place(x=250, y=260, width=70, height=25)
        Button_Start["command"] = self.Button_Start

        Label_Log = tk.Message(root)
        Label_Log["font"] = ft
        Label_Log["fg"] = "#333333"
        Label_Log["justify"] = "center"
        Label_Log["text"] = "Log :"
        Label_Log.place(x=0, y=310, width=650, height=52)

        self.CheckBox_activeTag = tk.Checkbutton(root)
        self.CheckBox_activeTag["font"] = ft
        self.CheckBox_activeTag["fg"] = "#333333"
        self.CheckBox_activeTag["justify"] = "center"
        self.CheckBox_activeTag.place(x=225, y=210, width=70, height=25)
        self.CheckBox_activeTag["offvalue"] = "0"
        self.CheckBox_activeTag["onvalue"] = "1"
        self.CheckBox_activeTag["command"] = self.CheckBox_activeTag_command

        self.Button_Tag_add = tk.Button(root)
        self.Button_Tag_add["bg"] = "#f0f0f0"
        self.Button_Tag_add["font"] = ft
        self.Button_Tag_add["fg"] = "#000000"
        self.Button_Tag_add["justify"] = "center"
        self.Button_Tag_add["text"] = "Ajouter"
        self.Button_Tag_add["command"] = self.Button_Tag_add_command

        self.console = tk.Text(root, wrap=tk.WORD, width=80, height=24)
        self.console.place(x=650, y=50)  # Adjust the position as needed

    def CheckBox_activeTag_command(self):
        if self.CheckBox_activeTag.getvar(self.CheckBox_activeTag['variable']) == '1':  # Vérifie si la case à cocher est cochée
            self.write_to_console("Activer tag spécifique")
            self.Button_Tag_add.place(x=350, y=160, width=70, height=25)
        else:
            self.write_to_console("désactiver les tags spécifiques")
            self.Button_Tag_add.place_forget()

    def Button_Tag_add_command(self):
        # Récupère le tag noté dans Input_Label_Tag_Retrieve
        tag = self.Input_Label_Tag_Retrieve.get()

        if tag.strip():
            with open("custom_list.txt", "a") as file:
                file.write(re.sub(r'\s+', ' ', tag.lstrip()) + "\n")
                self.write_to_console("Tag ajouté avec succès : " + tag)
        else:
            self.write_to_console("Ce tag ne peut pas être ajouté")

    def Button_Start(self):
        pseudo = self.Input_Label_Name_Retrieve.get()
        page = 1
        self.write_to_console("Début de la phase d'extraction des URL vers les projets")

        url = ""
        open("links.txt", "w").close()

        while True:
            url = f"https://www.deviantart.com/{pseudo}/gallery/all?page={page}"
            response = requests.get(url)
            if response.status_code == 200:
                html = response.content
                soup = BeautifulSoup(html, 'html.parser')
                divs = soup.select('div._1xcj5')

                self.write_to_console(f"Début du scraping sur la page gallery {url}")

                if divs:
                    with open("links.txt", "a") as file:
                        for div in divs:
                            first_link = div.find('a')
                            if first_link:
                                href = first_link.get("href")
                                self.write_to_console("URL du lien dans la div: " + href)
                                file.writelines(href + "\n")
                            else:
                                self.write_to_console(f"Aucun lien trouvé dans la div de la page {page}")
                else:
                    self.write_to_console("Cette page est vide")
                    break

                self.write_to_console(f"Fin de la récupération des liens de la page {page}")
                page += 1
            else:
                self.write_to_console(f"Le lien pour la page {page} n'existe pas.")
                break

        # Fonction pour télécharger une image à partir de son URL et la sauvegarder dans un dossier
        def telecharger_image(url, nom_dossier, nom_fichier):
            if not os.path.exists(nom_dossier):
                os.makedirs(nom_dossier)
            output_folder = os.path.join(nom_dossier, nom_fichier)
            reponse = requests.get(url)
            if reponse.status_code == 200:
                with open(output_folder, 'wb') as f:
                    f.write(reponse.content)
                self.write_to_console(f"L'image a été téléchargée avec succès sous le nom {nom_fichier} dans le dossier {nom_dossier}")
            else:
                self.write_to_console(f"Impossible de télécharger l'image. Statut de la réponse : {reponse.status_code}")

        def remplacer_caracteres_speciaux(chaine):
            caracteres_speciaux = {
                "<": "_", ">": "_", ":": "_", "“": "_",
                "/": "_", "\\": "_", "|": "_", "?": "_", "*": "_"
            }
            for caractere, equivalent in caracteres_speciaux.items():
                chaine = re.sub(re.escape(caractere), equivalent, chaine)
            return chaine

        def get_info_from_link(url, custom_list):
            response = requests.get(url)
            if response.status_code == 200:
                html = response.content
                soup = BeautifulSoup(html, 'html.parser')

                title_tag = soup.find('h1', class_='_33gAi')
                description_tag = soup.find('div', class_='legacy-journal')
                image_tag = soup.find('img', class_='_28lPU')
                detail_tags = soup.find_all('span', class_='_1nwad')

                details_content = [detail_tag.text.strip() for detail_tag in detail_tags]

                if self.CheckBox_activeTag.getvar(self.CheckBox_activeTag['variable']) == '1':
                    filtered_details = [detail for detail in details_content if detail in custom_list]
                    if filtered_details:
                        if title_tag:
                            titre_content = remplacer_caracteres_speciaux(title_tag.text.strip())
                            description_content = description_tag.text.strip() if description_tag else "Pas de description proposée par l'auteur"
                            image_link = image_tag['src'] if image_tag else None
                            nom_fichier = titre_content + ".png"
                            pseudo = "uploads"
                            telecharger_image(image_link, pseudo, nom_fichier)
                            return {"titre": titre_content, "description": description_content, "details": filtered_details}
                        else:
                            self.write_to_console("Balise h1 avec la classe spécifique non trouvée.")
                            return None
                    else:
                        self.write_to_console("Aucun détail correspondant à la liste personnalisée trouvé.")
                        return None
                else:
                    if title_tag:
                        titre_content = remplacer_caracteres_speciaux(title_tag.text.strip())
                        description_content = description_tag.text.strip() if description_tag else "Pas de description proposée par l'auteur"
                        image_link = image_tag['src'] if image_tag else None
                        nom_fichier = titre_content + "_1.png"
                        pseudo = "uploads"
                        telecharger_image(image_link, pseudo, nom_fichier)
                        return {"titre": titre_content, "description": description_content, "image_link": image_link, "details": details_content}
                    else:
                        self.write_to_console("Balise h1 avec la classe spécifique non trouvée.")
                        return None
            else:
                self.write_to_console("Impossible de récupérer les informations à partir du lien : " + url)
                return None

        custom_list = []
        if self.CheckBox_activeTag.getvar(self.CheckBox_activeTag['variable']) == '1':
            with open("custom_list.txt", "r") as file:
                custom_list = file.read().splitlines()

        with open("links.txt", "r") as file:
            links = file.readlines()

        links = [link.strip() for link in links]

        data = {}
        output_file = "./projects.json"
        if os.path.exists(output_file):
            with open(output_file, "r") as json_file:
                try:
                    data = json.load(json_file)
                except json.JSONDecodeError:
                    data = {}

        existing_titles = {proj_info['titre'] for proj_info in data.values() if 'titre' in proj_info}
        next_project_index = max([int(re.search(r'\d+', key).group()) for key in data.keys()] or [0]) + 1

        for i, link in enumerate(links, start=1):
            self.write_to_console("Récupération d'informations pour le lien : " + link)
            project_info = get_info_from_link(link, custom_list)
            if project_info and project_info['titre'] not in existing_titles:
                project_key = f"projet{next_project_index}"
                data[project_key] = project_info
                existing_titles.add(project_info['titre'])
                next_project_index += 1

        with open(output_file, "w") as json_file:
            json.dump(data, json_file, indent=4)

    def write_to_console(self, text):
        self.console.insert(tk.END, text + '\n')
        self.console.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    app.write_to_console("Welcome to the console!")
    root.mainloop()

# zyavera
# pyinstaller --onefile --icon=DeviantScrap.ico --name="DeviantScrap" DeviantScrap.py