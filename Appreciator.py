import pandas as pd
import os
from dotenv import load_dotenv
import time
import openai

import re

import os

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def quit():
    input("Appuyez sur entrée pour quitter")
    exit()

def is_openai_key(key: str) -> bool:
    pattern = r'^sk-[A-Za-z0-9-_]{32,}$'
    return bool(re.match(pattern, key))

def create_env_file(key: str):
    with open("api_key.env", "w") as f:
        f.write(f"OPENAI_API_KEY={key}\n")

def load_api_key():
    # Vérifie si le fichier 'api_key.env' existe
    if not os.path.isfile('api_key.env'):
        #print("Erreur : le fichier 'api_key.env' n'existe pas.")
        return False
    else:
        # Charge les variables d'environnement à partir du fichier 'api_key.env'
        load_dotenv('api_key.env')
        try:
            # Essaie de charger la clé API de OpenAI
            openai.api_key = os.getenv('OPENAI_API_KEY')
            # Vérifie si la clé API est None
            if openai.api_key is None:
                return False
            else:
                if is_openai_key(openai.api_key):
                    print("Votre clé OpenAI semble valide.")
                    return True
                else:
                    print("La clé enregistrée semble incorrecte : elle doit être au format \"sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\", les \"x\" étant des caractères alphanumériques (ou un tiret). Il faut enregistrer une nouvelle clé.")
                    return False
        except Exception as e:
            return True

def envoyerMessage(msg, model='gpt-3.5-turbo'):
    while True:
        try:
            completion = openai.ChatCompletion.create(
                model=model,
                messages=[{"role":"user", "content":msg}]
            )
            reponse = completion.choices[0].message.content
            if reponse == "None" or reponse is None:
                continue
            else:
                return reponse
        except openai.error.RateLimitError as e:
            print("Limite de taux atteinte. On attend deux secondes...")
            time.sleep(2)
            print("On réessaie...")
        except openai.error.APIConnectionError as e:
            print("Impossible de se connecter à l'API. On attend deux secondes...")
            time.sleep(2)
            print("On réessaie...")

#def synthetiser(trimestre1, trimestre2):

def synthetiser(periodes_arg):
    # Créez une liste de chaînes formatées pour chaque période
    global id_periodes
    periodes = [f'{id_periodes.capitalize()} {k + 1} : {str(v)}' for k, v in enumerate(periodes_arg)]
    
    # Joignez toutes les chaînes de la liste avec '\n' pour obtenir une seule chaîne
    periodes_str = '\n'.join(periodes)

    msg = f"Je suis un professeur de philosophie et je dois rédiger l'appréciation annuelle pour chaque élève. Je vais te donner l'appréciation du premier semestre, puis celle du second semestre, et tu vas m'en faire une synthèse courte, qui ne prendra pas plus de deux phrases. Fais attention à masquer toutes les informations personnelles sur l'élève : son nom, son prénom, son genre. Il s'agit de faire un bilan de l'année : il ne faut donc pas faire mention du futur, et ne pas mentionner le futur. Anonymise l'appréciation, on ne doit pas savoir si l'élève est de sexe masculin ou féminin.\nExemple de synthèse :\nTrimestre 1 :Elève très sérieuse ; le travail du cours et de la méthode est solide. De très bonnes interventions à l'oral.\n2. Un bac blanc très réussi montre que vous avez de réelles qualités de réflexion et d'expression. Attention à la méthode cependant, qui vous empêche parfois les exprimer.\nSynthèse : Du sérieux et de l'implication, avec des bonnes interventions à l'oral et de réelles qualités de réflexion et d'expression. La maîtrise de la méthode a cependant manqué d'un peu de rigueur.\n\nAppréciations à synthétiser :\n{periodes_str}\nSynthèse : "
    #print (msg)
    return envoyerMessage(msg)

###############################
        

print("Ce programme est destiné à synthétiser les appréciations du livret scolaire dans le cadre de l'utilisation de Pronote.")

key_loaded = load_api_key()

if not key_loaded:
    print("\nJe n'ai pas pu trouver de clé OpenAI dans la configuration. C'est parfaitement normal si c'est la première fois que vous lancez ce programme.")
    
    while not key_loaded:
        print("\n\t- Pour plus d'explications sur ce qu'est une clé OpenAI, tapez 1\n\t- Pour savoir comment obtenir une clé OpenAI, tapez 2\n\t- >>> Pour entrer votre clé OpenAI, tapez 3\n\t- Pour quitter, tapez 4")
        reponse = input("> ")
        if reponse == "1":
            print("Une clé OpenAI, ou OpenAI API key, est une séquence unique de caractères qui sert d'identifiant lors de l'interaction avec les services d'OpenAI. Elle est utilisée pour authentifier les demandes que vous faites à l'API d'OpenAI, permettant ainsi à OpenAI de vérifier qui fait la demande et d'appliquer les restrictions d'accès appropriées.\n\nEn d'autres termes, une clé OpenAI est comme une carte d'identité numérique que vous présentez à OpenAI chaque fois que vous voulez utiliser leurs services. Elle est essentielle pour utiliser les modèles d'apprentissage automatique d'OpenAI, comme GPT-3, pour générer du texte, traduire des langues, répondre à des questions, et plus encore.\n\nIl est crucial de garder votre clé OpenAI sécurisée et de ne pas la partager, car toute personne ayant accès à votre clé peut l'utiliser pour faire des demandes à l'API d'OpenAI en votre nom.")
        elif reponse == "2":
            print("Pour obtenir une clé API OpenAI, vous devez suivre les étapes suivantes :\n\t1. Créez un compte sur OpenAI. Vous pouvez vous rendre sur leur site web à l'adresse suivante : https://beta.openai.com/signup/ et suivre les instructions pour créer un compte.\n\t2. Une fois que vous avez un compte, connectez-vous et accédez à votre tableau de bord (Dashboard).\n\t3. Dans le tableau de bord, vous verrez un onglet ou une section appelée \"API Keys\" ou \"Clés API\". Cliquez dessus.\n\t4. Dans cette section, vous aurez la possibilité de générer une nouvelle clé API. En général, il y a un bouton ou un lien intitulé \"Create New Key\" ou \"Générer une nouvelle clé\". Cliquez dessus.\n\t5. Une nouvelle clé API sera générée pour vous. Elle sera une longue chaîne de caractères alphanumériques. Assurez-vous de copier cette clé et de la stocker en lieu sûr.\n\t6. Important : Ne partagez jamais votre clé API avec personne. Elle donne accès à votre compte OpenAI et peut être utilisée pour effectuer des actions qui pourraient vous être facturées.")
        elif reponse == "3":
            key = input("Entrez ici votre clé OpenAI : ")
            if is_openai_key(key):
                create_env_file(key)
                key_loaded = load_api_key()
            else:
                print("\nCe que vous avez entré ne correspond pas à une clé OpenAI. Veuillez réessayer.")
        elif reponse == "4":
            exit()
        else:
            print("Commande invalide.")

clear_terminal()
document_loaded = False
while not document_loaded :
    reponse = 0
    while not reponse == "4":
        print("\nAvant de continuer, vous devez mettre dans le presse-papier l'ensemble des appréciations de la classe qui vous intéresse, sur la page \"livret scolaire\" du client Pronote.\n\t- Pour supprimer la configuration de votre clé OpenAI, tapez 1.\n\t- Pour savoir comment télécharger le client Pronote, tapez 2.\n\t- Pour savoir comment copier les appréciations, tapez 3.\n\t- >>> Pour commencer la synthèse des appréciations, tapez 4.\n\t- Pour quitter, tapez 5")
        reponse = input("> ")
        print ("\n")
        if reponse == "1":
            os.remove("api_key.env")
            print("Le fichier de configuration de votre clé OpenAI a été supprimé. Relancez le programme pour ajouter une nouvelle clé.")
            quit()
        elif reponse == "2":
            print("Pour télécharger le client Pronote, vous pouvez vous rendre sur le site d'Index Education. Il s'agit de la version PRONOTE pour les utilisateurs.")
        elif reponse == "3":
            print ("Quand vous vous êtes connecté sur Pronote, allez dans l'onglet \"Résultats\".\nEnsuite, rendez-vous dans le sous-onglet \"Livret scolaire\" ; dans ce sous-onglet, à la droite de \"Livret scolaire\", il y a un bouton central \"Saisie des appréciations annuelles par service\", qui fait une sorte de T. Cliquez dessus.\nEn haut à droite de l'ensemble des appréciations, vous trouverez un petit bouton avec deux feuilles juxtaposées : c'est le bouton pour copier les appréciations dans le presse-papier. Cliquez dessus.")
        elif reponse == "5":
            exit()
    try:
        # Tente de lire le contenu du presse-papier comme un CSV
        df = pd.read_clipboard(sep=',')
    except pd.errors.ParserError:
        # Si une erreur se produit, affiche un message d'erreur et quitte
        print("Erreur : Le contenu du presse-papier n'est pas un CSV valide. Veuillez recommencer l'opération.")
        continue

    if df.shape[0] <= 1:  # Si le DataFrame a une ligne ou moins
            print("Erreur : Les données CSV doivent contenir au moins deux lignes. Assurez-vous d'avoir correctement copié vos données.")
            continue
    # Identifie le numéro de la colonne qui contient le mot "élèves" (insensible à la casse)
    colonne_nom = None
    for i, nom in enumerate(df.columns):
        if 'élèves' in nom.lower(): 
            colonne_nom = i
            break

    if colonne_nom is None:
        print("Erreur : Aucune colonne contenant 'élèves' trouvée. Assurez-vous que vous avez copié le bon document.")
        continue

    # Identifie le numéro de la colonne qui contient le mot "appréciations" (insensible à la casse)

    try:
        colonne_appreciation = df.columns.str.lower().tolist().index('appréciations')
    except ValueError:
        print("Erreur : Aucune colonne contenant 'appréciations' trouvée. Assurez-vous que vous avez copié le bon document.")
        continue        

    document_loaded = True

# Supprime l'en-tête du tableau
df.columns = range(df.shape[1])

# Supprime les colonnes qui ne sont pas "nom" ou "appréciation"
df = df.iloc[:, [colonne_nom, colonne_appreciation]]
nb_periodes = df[0].first_valid_index()
id_periodes = "période"
if nb_periodes == 2:
    id_periodes = "semestre"
elif nb_periodes == 3:
    id_periodes = "trimestre"

clear_terminal()
print(f"Nombre de périodes détectées : {nb_periodes} ({id_periodes}s)\n")


# Initialiser les listes
synthese = []
nom = []

# Parcourir le dataframe en sautant nb_periodes + 1 lignes à chaque fois (nb périodes + 1 appréciation annuelle)
for i in range(0, len(df), nb_periodes + 1):
    # Vérifier si les valeurs B sont non nulles
    '''if pd.notnull(df.iloc[i, 4]) and pd.notnull(df.iloc[i+1, 4]):
        # Concaténer B[i] et B[i+1], et enlever les espaces en trop'''
    print(df.iloc[i+nb_periodes, 0] + f" ({int(i / (nb_periodes + 1)) + 1}/{int(len(df) / (nb_periodes + 1))})") #on affiche la progression
    tempSynth = synthetiser(df.iloc[i:i + nb_periodes, 1]) #on synthétise toutes les appréciations
    synthese.append(tempSynth)
    print(tempSynth) #on print seulement l'appréciation, on a déjà print le nom

    
    # Ajouter A[i+2] à la liste nom
    if i+2 < len(df) and pd.notnull(df.iloc[i+2, 0]):
        nom.append(df.iloc[i+2, 0])

# Créer un nouveau dataframe avec les listes créées
nouveau_df = pd.DataFrame({
    'Nom': nom,
    'Synthese': synthese
})

# Sauvegarder le nouveau dataframe en tant que csv
nouveau_df.to_csv('livret_scolaire.csv', index=False)
print("\n\n********** FIN DE LA GENERATION **********\nLe résultat a été enregistré dans le fichier \"livret_scolaire.csv\", situé dans le même dossier que ce programme. Ouvrez-le avec un tableur pour retrouver l'ensemble de vos appréciations.\n")
quit()
