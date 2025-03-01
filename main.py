import time

import pandas as pd
import random

classement = []
pseudo = []
while  True:
    path = "mots.csv"
    texte2 = pd.read_csv(path, sep=";")
    mots_d = texte2['mots']
    texte = []
    saisie_utilisateur = []

    while True:
        g = input("Combien de mots voulez-vous ? : ")
        try:
            g = int(g)
            break
        except ValueError:
            print("Ce n'est pas un nombre, essaye encore.")

    for a in range(g):
        r = random_number = random.randint(1, 1000)
        texte.append(mots_d[r])

    i = 0
    input("Appuyez sur Entrée quand vous êtes prêt...")
    heure_debut = time.time()
    for mot in texte:
        print(f"Tapez le texte suivant: {texte[i]}")
        i = i + 1
        saisie = input("Commencez à taper: ")
        saisie_utilisateur.append(saisie)
    heure_fin = time.time()
    temps = heure_fin - heure_debut
    faux = 0
    total = len(texte)
    z = 0

    for utilisateur in saisie_utilisateur:
        if utilisateur == texte[z]:
            print("vous avez correctement hortography le mots : " + utilisateur)
            z = z + 1

        else:
            print("vous avez mal hortigraphier le mots : " + texte[z])
            z = z + 1
            faux = faux + 1
    score = total - faux
    temps = int(temps)
    point = score / temps * 100
    print(f"votre score final est de {score}/{total} en {temps} segonde pour un score de {int(point)}%")
    classement.append(point)
    classement_trie = sorted(classement, reverse=True)

    print("-----------------")
    print("   classement    ")
    for i in classement_trie:
        print("  ", int(i)," points",)
    print("-----------------")