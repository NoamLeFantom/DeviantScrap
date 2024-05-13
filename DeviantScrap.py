import requests
from bs4 import BeautifulSoup
import time
import json
import os

import tkinter as tk
import tkinter.font as tkFont
from tkinter.scrolledtext import ScrolledText
import subprocess

class App:
    def __init__(self, root):
        # setting title
        root.title("")
        # setting window size
        width=root.winfo_screenwidth()
        height=root.winfo_screenheight()
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth), (screenheight)/10)
        root.geometry(alignstr)
        root.resizable(width=True, height=True)

        Label_Name_Retrieve=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        Label_Name_Retrieve["font"] = ft
        Label_Name_Retrieve["fg"] = "#333333"
        Label_Name_Retrieve["justify"] = "center"
        Label_Name_Retrieve["text"] = "Pseudo à récupérer :"
        Label_Name_Retrieve.place(x=50,y=110,width=250,height=25)

        self.Input_Label_Name_Retrieve=tk.Entry(root)
        self.Input_Label_Name_Retrieve["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.Input_Label_Name_Retrieve["font"] = ft
        self.Input_Label_Name_Retrieve["fg"] = "#333333"
        self.Input_Label_Name_Retrieve["justify"] = "center"
        self.Input_Label_Name_Retrieve["text"] = ""
        self.Input_Label_Name_Retrieve.place(x=250,y=110,width=200,height=25)

        Label_Tag_Retrieve=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        Label_Tag_Retrieve["font"] = ft
        Label_Tag_Retrieve["fg"] = "#333333"
        Label_Tag_Retrieve["justify"] = "center"
        Label_Tag_Retrieve["text"] = "Spécifique tag :"
        Label_Tag_Retrieve.place(x=125,y=160,width=100,height=25)

        self.Input_Label_Tag_Retrieve=tk.Entry(root)
        self.Input_Label_Tag_Retrieve["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.Input_Label_Tag_Retrieve["font"] = ft
        self.Input_Label_Tag_Retrieve["fg"] = "#000001"
        self.Input_Label_Tag_Retrieve["justify"] = "center"
        self.Input_Label_Tag_Retrieve["text"] = ""
        self.Input_Label_Tag_Retrieve.place(x=250,y=160,width=70,height=25)
        
        Label_CheckBox_activeTag=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        Label_CheckBox_activeTag["font"] = ft
        Label_CheckBox_activeTag["fg"] = "#333333"
        Label_CheckBox_activeTag["justify"] = "center"
        Label_CheckBox_activeTag["text"] = "Activer les tags spécifique :"
        Label_CheckBox_activeTag.place(x=25,y=210,width=250,height=25)

        Button_Start=tk.Button(root)
        Button_Start["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        Button_Start["font"] = ft
        Button_Start["fg"] = "#000000"
        Button_Start["justify"] = "center"
        Button_Start["text"] = "Start"
        Button_Start.place(x=250,y=260,width=70,height=25)
        Button_Start["command"] = self.Button_Start

        Label_Log=tk.Message(root)
        ft = tkFont.Font(family='Times',size=10)
        Label_Log["font"] = ft
        Label_Log["fg"] = "#333333"
        Label_Log["justify"] = "center"
        Label_Log["text"] = "Log :"
        Label_Log.place(x=0,y=310,width=650,height=52)

        self.CheckBox_activeTag=tk.Checkbutton(root)
        ft = tkFont.Font(family='Times',size=10)
        self.CheckBox_activeTag["font"] = ft
        self.CheckBox_activeTag["fg"] = "#333333"
        self.CheckBox_activeTag["justify"] = "center"
        self.CheckBox_activeTag["text"] = ""
        self.CheckBox_activeTag.place(x=225,y=210,width=70,height=25)
        self.CheckBox_activeTag["offvalue"] = "0"
        self.CheckBox_activeTag["onvalue"] = "1"
        self.CheckBox_activeTag["command"] = self.CheckBox_activeTag_command

        self.Button_Tag_add=tk.Button(root)
        self.Button_Tag_add["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        self.Button_Tag_add["font"] = ft
        self.Button_Tag_add["fg"] = "#000000"
        self.Button_Tag_add["justify"] = "center"
        self.Button_Tag_add["text"] = "Ajouter"
        self.Button_Tag_add["command"] = self.Button_Tag_add_command

        self.console = tk.Text(root, wrap=tk.WORD, width=80, height=24)
        self.console.place(x=650, y=50)  # Adjust the position as needed

    def CheckBox_activeTag_command(self):
        if self.CheckBox_activeTag.getvar(self.CheckBox_activeTag['variable']) == '1':  # Vérifie si la case à cocher est cochée
            app.write_to_console("Activer tag spécifique")
            print("Activer tag spécifique")
            self.Button_Tag_add.place(x=350,y=160,width=70,height=25)
        else:
            app.write_to_console("desactiver les tag spécifique")
            print("desactiver les tag spécifique")
            self.Button_Tag_add.place_forget()
        
    def Button_Tag_add_command(self):
        # Récupère le tag noté dans Input_Label_Tag_Retrieve
        tag = self.Input_Label_Tag_Retrieve.get()
        
        if tag.strip():
            import re
            with open("custom_list.txt", "a") as file:
                file.write(re.sub(r'\s+', ' ',tag.lstrip()) + "\n")
                app.write_to_console("Tag ajouté avec succès :" + tag)
                print("Tag ajouté avec succès :" + tag) 
        else:
            app.write_to_console("Ce tag ne peux pas être ajouté")
            print("Ce tag ne peux pas être ajouté")
        
    def Button_Start(self):
        pseudo = self.Input_Label_Name_Retrieve.get()

        app.write_to_console("Debut de la phase d'extraction des url vers les projets")
        print("Debut de la phase d'extraction des url vers les projets")
        url = "https://www.deviantart.com/"+pseudo+"/gallery"

        response = requests.get(url)
        html = response.content

        soup = BeautifulSoup(html, 'html.parser')
        divs = soup.select('div._1xcj5')  # Sélectionne les divs avec les classes spécifiques

        app.write_to_console("Debut de scraping sur la page gallery")
        print("Debut de scraping sur la page gallery")
        with open("links.txt", "w") as file:
            for div in divs:
                time.sleep(1)
                # Trouve le premier lien <a> dans la div
                first_link = div.find('a')
                if first_link:  # Vérifie si un lien a été trouvé dans la div
                    href = first_link.get("href")

                    app.write_to_console("URL du lien dans la div:" + href)
                    print("URL du lien dans la div:" + href)
                    file.writelines(href + "\n")
                else:
                    app.write_to_console("Aucun lien trouvé dans la div")
                    print("Aucun lien trouvé dans la div")
        app.write_to_console("Fin")
        print("Fin de la récupération des liens")
        
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
                app.write_to_console("L'image a été téléchargée avec succès sous le nom" + nom_fichier + "dans le dossier" + nom_dossier)
                print("L'image a été téléchargée avec succès sous le nom" + nom_fichier + "dans le dossier" + nom_dossier)
            else:
                app.write_to_console("Impossible de télécharger l'image. Statut de la réponse :" + reponse.status_code)
                print("Impossible de télécharger l'image. Statut de la réponse :" + reponse.status_code)

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

                if self.CheckBox_activeTag.getvar(self.CheckBox_activeTag['variable']) == '1':
                    if filtered_details:
                        if title_tag:
                            # Récupérer le contenu de la balise h1 (titre)
                            titre_content = title_tag.text.strip()
                            # Récupérer le contenu de la balise div (description)
                            
                            description_content=""
                            if description_tag:
                                description_text = description_tag.text.strip()
                                if description_text:
                                    description_content = description_text
                                else:
                                    description_content = "Pas de description proposée par l'auteur"
                            else:
                                description_content = "Pas de description proposée par l'auteur"

                            image_link = image_tag['src'] if image_tag else None  # Si image_tag est None, image_link sera None également
                            nom_fichier=titre_content+".png"
                            telecharger_image(image_link, pseudo, nom_fichier)
                            # Retourner un dictionnaire avec les informations extraites
                            return {"titre": titre_content, "description": description_content, "imageL_Link": image_link, "details": filtered_details}
                        else:
                            app.write_to_console("Balise h1 avec la classe spécifique non trouvée.")
                            print("Balise h1 avec la classe spécifique non trouvée.")
                            return None
                    else:
                        app.write_to_console("Aucun détail correspondant à la liste personnalisée trouvé.")
                        print("Aucun détail correspondant à la liste personnalisée trouvé.")
                        return None
                else:
                    if title_tag:
                        # Récupérer le contenu de la balise h1 (titre)
                        titre_content = title_tag.text.strip()
                        # Récupérer le contenu de la balise div (description)
                        description_content=""
                        if description_tag:
                            description_text = description_tag.text.strip()
                            if description_text:
                                description_content = description_text
                            else:
                                description_content = "Pas de description proposée par l'auteur"
                        else:
                            description_content = "Pas de description proposée par l'auteur"
                        image_link = image_tag['src'] if image_tag else None  # Si image_tag est None, image_link sera None également
                        nom_fichier=titre_content+".png"
                        telecharger_image(image_link, pseudo, nom_fichier)
                        # Retourner un dictionnaire avec les informations extraites
                        return {"titre": titre_content, "description": description_content, "imageL_Link": image_link, "details": details_content}
                    else:
                        app.write_to_console("Balise h1 avec la classe spécifique non trouvée.")
                        print("Balise h1 avec la classe spécifique non trouvée.")
                        return None
            else:
                app.write_to_console("Impossible de récupérer les informations à partir du lien :")
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
            app.write_to_console("Récupération d'informations pour le lien :" + link)
            print("Récupération d'informations pour le lien :" + link)
            project_info = get_info_from_link(link, custom_list)
            if project_info:
                project_key = f"projet{i}"
                data[project_key] = project_info

        # Spécifier le chemin du fichier JSON de sortie
        output_file = pseudo+"/output.json"

        # Écrire le dictionnaire dans le fichier JSON
        with open(output_file, "w") as json_file:
            json.dump(data, json_file, indent=4)

        app.write_to_console("Données écrites avec succès dans le fichier JSON :" + output_file)
        print("Données écrites avec succès dans le fichier JSON :" + output_file)


    def write_to_console(self, text):
        self.console.insert(tk.END, text + '\n')
        self.console.see(tk.END)  # Scroll to the end of the console

if __name__ == "__main__":
    root = tk.Tk()
    with open("custom_list.txt", "a") as file:
        file.write("#")
    app = App(root)
    app.write_to_console("Welcome to the console!") 
    root.mainloop()

# First you need to execute : pip install pyinstaller
# In a second time : pyinstaller --onefile --icon=DeviantScrap.ico --name="DeviantScrap" DeviantScrap.py

