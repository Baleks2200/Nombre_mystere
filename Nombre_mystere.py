"""
===============================================================
Jeu "Contrôle vol.1" — Jeu de devinette de nombre aléatoire
---------------------------------------------------------------
Auteur : (Belousov Aleksandr)
Version : 1.0
Langue  : Français
---------------------------------------------------------------
Ce programme permet à l'utilisateur de :
    • Créer un pseudo valide (4 à 16 caractères)
    • Jouer à un jeu de devinette (200–250)
    • Sauvegarder ses résultats dans un fichier TXT et JSON
    • Afficher le top 10 des meilleurs joueurs
    • Rechercher un joueur par pseudo
===============================================================
"""

import os
import random
import time
import unidecode
import json

nicknames = []
nickname_temp = []
filename = "nicknames_top.txt"
json_file = "nicknames_top.json"

print(r"""
        ____        _   _                 
       |  _ \ _   _| |_| |__   ___  _ __  
       | |_) | | | | __| '_ \ / _ \| '_ \ 
       |  __/| |_| | |_| | | | (_) | | | |
       |_|    \__, |\__|_| |_|\___/|_| |_|
              |___/ <===~~~~   Controle vol.1   ~~~~===>
""")

#===================== Liste des menus avec des menus en menu =======================

def liste_menu():
    """
        Affiche le menu principal du programme et permet à l'utilisateur
        de choisir entre trois options :
            1. Accéder au menu des résultats (classement, recherche)
            2. Démarrer une nouvelle partie
            3. Quitter le programme

        La fonction tourne en boucle jusqu'à ce que l'utilisateur choisisse de quitter.
        """

    while True:
        print("\n=== Menu de Démarrage ===")
        print("1 : Menu des Résultats")
        print("2 : Menu de Partie")
        print("3 ou 'exit' : Quitter")

        choix = input("Entrée votre choix: ").strip().lower()

        if choix == "1":
            menu_resultat()
        elif choix == "2":
            menu_partie()
        elif choix in ["3", "exit"]:
            print("À la prochaine !")
            break
        else:
            print("Choix invalide, réessayez.")


#=================== Sauvegarde des pseudos ===================
def menu_resultat():
    """
        Affiche le classement des joueurs sous forme de tableau (TOP 10).
        Donne ensuite à l'utilisateur la possibilité :
            - de rechercher un joueur spécifique par pseudo,
            - de revenir au menu principal,
            - ou de quitter le programme.

        Gère automatiquement les erreurs si le fichier est vide ou inexistant.
        """
    try:
        if not os.path.exists(filename):
            raise FileNotFoundError("Le fichier n'existe pas encore.")

        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()

        player_lines = [
            line.strip() for line in lines
            if line.strip() and not line.startswith(("Numéro", "=", "=>"))
        ]

        if not player_lines:
            raise FileNotFoundError("Aucun joueur enregistré dans le fichier.")

        players = []
        for line in player_lines:
            parts = line.split()
            if len(parts) >= 4:
                num, name, points, essays = parts[:4]
                players.append((int(points), name, essays, num))

        players_sorted = sorted(players, key=lambda x: x[0])[:10]

        print("\n" "===== TOP 10 des Joueur(e)s =====" "\n")
        print(f"{'Rang':<6}{'Nom':<15}{'Temps(s)':<12}{'Essais':<10}")
        print("=" * 45)

        for idx, (points, name, essays, num) in enumerate(players_sorted, start=1):
            print(f"{idx:<6}{name:<15}{points:<12}{essays:<10}")

    except FileNotFoundError as e:
        print(f"{e}")
    except Exception as e:
        print(f"Une erreur est survenue: {e}")

    while True:
        print("\n1 : Rechercher un joueur par pseudo")
        print("2 : Retour au menu principal")
        print("3 ou 'exit' : Quitter le programme")

        choix = input("Votre choix: ").strip().lower()

        if choix == "1":
            rechercher_joueur()
            break
        elif choix == "2":
            return
        elif choix in ["3", "exit"]:
            print("À la prochaine !")
            exit()
        else:
            print("Choix invalide, réessayez.")


# ======== recherche_par_pseudo ========
def rechercher_joueur():
    """
        Permet à l'utilisateur de rechercher un joueur dans le fichier TXT
        en entrant son pseudo. Si le pseudo n’existe pas, une erreur est affichée.

        Le résultat affiche :
            - Numéro
            - Nom du joueur
            - Temps (points)
            - Nombre d’essais
        """
    nickname_input = input("\nEntrez le pseudo du joueur à rechercher: ").strip()

    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()

        player_lines = [
            line for line in lines
            if line.strip() and not line.startswith(("Numéro", "=", "=>"))
        ]

        if not player_lines:
            raise FileNotFoundError("Aucun joueur enregistré dans le fichier.")

        found_lines = [line for line in player_lines if nickname_input.lower() in line.lower()]
        if not found_lines:
            raise ValueError(f"Le joueur '{nickname_input}' n'existe pas dans le fichier.")

        print("\n=>=>=> Résultat de la recherche <=<=<=\n")
        print(f"{'Numéro':<10}{'Name':<15}{'Points':<10}{'Essays':<10}")
        print("=" * 45)
        for line in found_lines:
            parts = line.split()
            if len(parts) >= 4:
                num, name, points, essays = parts[:4]
                print(f"{num:<10}{name:<15}{points:<10}{essays:<10}")

    except FileNotFoundError as e:
        print(f"{e}")
    except ValueError as e:
        print(f"{e}")
    except Exception as e:
        print(f"Une erreur est survenue: {e}")
    finally:
        input("\n" "Appuyez sur Entrée pour revenir au menu des résultats...")
        menu_resultat()



#===================== Creation de pseudos et l'envoi =====================================

def menu_partie():
    """
    Demande à l'utilisateur de choisir un pseudonyme avant de commencer la partie.

    Règles :
        - Longueur entre 4 et 16 caractères
        - Aucun symbole interdit (., :, &, etc.)
        - Le pseudo ne peut pas être vide ou égal à 'exit'

    Une fois validé, le pseudo est sauvegardé, et la partie démarre.
    """

    censure = [":", ".", ",", "&", "~", " "]
    print("\n" "==== Avant démarrer le jeu il faut choisir son pseudo ====")

    while True:
        nickname = unidecode.unidecode(input("\n" "Choisissez votre 'Pseudo' {Le 'Pseudo' doit contenire de 4 à 16 caractères:}""\n"))
        if len(nickname) < 4:
            print("Le pseudo doit contenir au moins 4 caractères.")
        elif len(nickname) > 16:
            print("Le pseudo ne peut pas dépasser 16 caractères.")
        elif any(symbol in nickname for symbol in censure):
            print("Les symboles suivants sont interdits:", censure)
        elif nickname.lower() == "exit":
            print("Le pseudo ne peut pas être 'exit'")
        elif nickname.strip() == "":
            print("Le pseudo ne peut pas être vide")
        else:
            nicknames.clear()
            nickname_temp.clear()
            nicknames.append(nickname)
            nickname_temp.append(nickname)
            print("Bonne chance,", nickname, "!")
            jeux()
            break


#===== Game =====
def jeux():
    """
       Lance le jeu de devinette :
       L'utilisateur doit deviner un nombre aléatoire entre 200 et 250.
       À chaque tentative, le programme indique :
           - “+ C’est plus +” si le nombre proposé est trop petit
           - “- C’est moins -” si le nombre proposé est trop grand
           - “Bien joué !” lorsque le nombre est correct

       À la fin, le temps total et le nombre d’essais sont enregistrés.
       """
    essays = 0
    start_time = time.time()
    x = random.randint(200, 250)
    print("\n" "Le jeu commence!")

    while True:
        essays += 1
        try:
            g = int(input("Votre choix: "))
        except ValueError:
            print("Veuillez entrer un nombre valide.")
            continue

        if g < x:
            print("+ C’est plus +")
        elif g > x:
            print("- C’est moins -")
        else:
            print("Bien joué!", nicknames[0])
            end_time = time.time()
            temps_du_jeux = round(end_time - start_time)
            nickname_temp.append(temps_du_jeux)
            nickname_temp.append(essays)
            print(f"Temps: {temps_du_jeux}s | Essais: {essays}")
            sauvegarde_resultat(nickname_temp)
            break


# ======== save_results ========
def sauvegarde_resultat(nickname_temp):
    """
        Sauvegarde les résultats du joueur dans deux formats :
            - Fichier texte (.txt) pour lecture humaine
            - Fichier JSON (.json) pour traitement automatique

        Si un joueur existe déjà :
            - Son temps est mis à jour seulement s’il est meilleur (plus court).
        Sinon :
            - Un nouvel enregistrement est ajouté.

        Les données sont ensuite triées et réécrites dans les deux fichiers.
        """
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            f.write("=>=>=>=>=>=> TOP des Joueur(e)s <=<=<=<=<=<=\n")
            f.write(f"{'Numéro':<10}{'Name':<15}{'Points':<10}{'Essays':<10}\n")
            f.write("=" * 45 + "\n")

    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    players = [
        line for line in lines
        if line.strip() and not line.startswith(("Numéro", "=", "=>"))
    ]

    existing = []
    for line in players:
        parts = line.split()
        if len(parts) >= 4:
            num, name, points, essays = parts[:4]
            existing.append((num, name, int(points), int(essays)))

    name, points, essays = nickname_temp
    points = int(points)
    essays = int(essays)

    for idx, (num, pname, ppoints, pessays) in enumerate(existing):
        if pname == name:
            if points < ppoints:
                existing[idx] = (num, name, points, essays)
                print(f"Le résultat a été amélioré par {name} !")
            break
    else:
        num = str(len(existing) + 1)
        existing.append((num, name, points, essays))

    with open(filename, "w", encoding="utf-8") as f:
        f.write("=>=>=>=>=>=> TOP des Joueur(e)s <=<=<=<=<=<=\n")
        f.write(f"{'Numéro':<10}{'Name':<15}{'Points':<10}{'Essays':<10}\n")
        f.write("=" * 45 + "\n")
        for i, (num, name, points, essays) in enumerate(existing, start=1):
            f.write(f"{i:<10}{name:<15}{points:<10}{essays:<10}\n")

    json_data = [
        {"rank": i, "name": name, "points": points, "essays": essays}
        for i, (num, name, points, essays) in enumerate(existing, start=1)
    ]

    with open(json_file, "w", encoding="utf-8") as jf:
        json.dump(json_data, jf, indent=4, ensure_ascii=False)

    print(f"Le fichier - '{filename}' et '{json_file}' has been up to load")

    print(r"""
                  ________________________
                 /                        \
                /  ______________________  \
               |  |                      |  |
               |  |      [=======]        |  |
               |  |      [_______]        |  |
               |  |______________________ |  |
               |                          |  |
               |    ####################     |  
               |    #    Y  Б  Е  Й     #    |
               |    ####################     |
               |                          |  |
               |__________________________|__|
                 \__________________________/
                       \______________/
                          \________/
    """)


# ======== start ========
liste_menu()