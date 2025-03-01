import pandas as pd
import random
import sqlite3
import bcrypt
import time
import os

conn_users = sqlite3.connect("users.db")
conn_scores = sqlite3.connect("scores.db")
cursor_users = conn_users.cursor()
cursor_scores = conn_scores.cursor()

cursor_users.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT)''')
conn_users.commit()

cursor_scores.execute('''CREATE TABLE IF NOT EXISTS scores (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT, 
                        score INTEGER)''')
conn_scores.commit()


def get_user_scores_and_max(username):
    cursor_scores.execute("SELECT score FROM scores WHERE username = ?", (username,))
    all_scores = [row[0] for row in cursor_scores.fetchall()]
    if not all_scores:
        print("Aucun score enregistré pour cet utilisateur.")
        return [], 0
    max_score = max(all_scores)
    return all_scores, max_score


def signup():
    while True:
        username = input("Choisissez un pseudo : ")
        cursor_users.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor_users.fetchone():
            print("Ce pseudo est déjà pris, essayez un autre.")
        else:
            break

    password = input("Choisissez un mot de passe : ")
    password2 = input("Confirmez votre mot de passe : ")

    if password == password2:
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        cursor_users.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn_users.commit()
        print("Compte créé avec succès ! Connectez-vous maintenant.")
        return login()

    else:
        print("Les mots de passe ne correspondent pas.")
        time.sleep(1)
        os.system("cls" if os.name == "nt" else "clear")

        return None


def login():
    while True:
        username = input("Entrez votre pseudo : ")
        password = input("Entrez votre mot de passe : ")

        cursor_users.execute("SELECT password FROM users WHERE username = ?", (username,))
        result = cursor_users.fetchone()

        if result and bcrypt.checkpw(password.encode(), result[0]):

            os.system("cls" if os.name == "nt" else "clear")
            print(f"Bienvenue {username} !")
            return username

        else:

            print("Pseudo ou mot de passe incorrect.")
            print("Retour au menu principal...")
            time.sleep(3)
            os.system("cls" if os.name == "nt" else "clear")

            return None


def score_save(username, score):
    cursor_scores.execute("INSERT INTO scores (username, score) VALUES (?, ?)", (username, score))
    conn_scores.commit()


def classement():
    print("--- CLASSEMENT GLOBAL ---")
    cursor_scores.execute("SELECT username, MAX(score) FROM scores GROUP BY username ORDER BY MAX(score) DESC LIMIT 10")
    classement = cursor_scores.fetchall()

    if not classement:
        print("Aucun score enregistré.")
    else:
        for i, (user, score) in enumerate(classement, start=1):
            print(f"{i}. {user} - {score} points")


user = None
while not user:
    print("--- MENU PRINCIPAL ---")
    print("1. Se connecter")
    print("2. S'inscrire")
    choix = input("Choisissez une option : ")

    if choix == "1":

        user = login()

    elif choix == "2":

        user = signup()

    else:
        print("Choix invalide, réessayez.")
        time.sleep(1)
        os.system("cls" if os.name == "nt" else "clear")

while True:
    path = "mots_fr.csv"
    texte2 = pd.read_csv(path, sep=";")
    mots_d = texte2['mots']
    texte = []
    saisie_utilisateur = []

    while True:
        try:
            g = int(input("Combien de mots voulez-vous ? : "))
            break

        except ValueError:
            print("Ce n'est pas un nombre, essaye encore.")

    for _ in range(g):
        r = random.randint(1, len(mots_d) - 1)
        texte.append(mots_d[r])

    input("Appuyez sur Entrée quand vous êtes prêt...")
    heure_debut = time.time()

    for i, mot in enumerate(texte):
        print(f"Tapez le texte suivant: {mot}")
        saisie = input("Commencez à taper: ")
        saisie_utilisateur.append(saisie)
    heure_fin = time.time()

    temps = int(heure_fin - heure_debut)
    os.system("cls" if os.name == "nt" else "clear")
    faux = sum(1 for i in range(len(texte)) if saisie_utilisateur[i] != texte[i])
    score = (len(texte) - faux) / temps * 100
    score = int(score)
    print(f"Votre score final est de {score} points !")
    score_save(user, score)
    classement()
    user_scores, max_score = get_user_scores_and_max(user)
    print(f"Scores de {user}: {user_scores}")
    print(f"Score maximum de {user}: {max_score}")
    rejouer = input("Voulez-vous rejouer ? (oui/non) : ").lower()
    if rejouer != "oui":
        break

conn_users.close()
conn_scores.close()