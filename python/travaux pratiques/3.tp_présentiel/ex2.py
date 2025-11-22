# # Créer une dictionnaire contenant des étudiants (id -> {nom, notes})
students_dict = {
    "0001": {
        "nom": "ahmed",
        "notes": [10, 12 ,15]
    },
    "0010": {
        "nom": "karim",
        "notes": [14, 12 ,18]
    },
    "0011": {
        "nom": "Morad",
        "notes": [8, 12 ,20]
    },
    "0100": {
        "nom": "Said",
        "notes": [19, 15 ,15, 20]
    }
}


# # Ajouter, modifier, supprimer un étudiant
def ajouter_etudiant(id: str, name: str, notes: list):
    try:
        students_dict[id] = {"nom": name, "notes": notes}
    except:
        raise ValueError("L'utilisateur existe déjà")

def modifier_etudiant(id: str, name: str, notes: list):
    try:
        students_dict[id] = {"nom": name, "notes": notes}
    except:
        raise ValueError("L'utilisateur n'existe pas")

def supprimer_etudiant(id: str):
    try:
        del students_dict[id]
    except:
        raise ValueError("L'utilisateur n'existe pas")

# ajouter_etudiant("0111", "Achraf", [20,20,12])
# supprimer_etudiant("0100")
# print(students_dict)


# # Ecrire une fonction qui calcule la moyenne de chaque étudiant
def calcul_moyenne(id):
    return sum(students_dict[id]["notes"]) / len(students_dict[id]["notes"])
# print(calcul_moyenne("0001"))

# # Retourer uniquement les étudiants dont la moyenne >=14
def top_students():
    temp = []
    for id_student in students_dict.keys():
        if calcul_moyenne(id_student) >= 14:
            temp.append({students_dict[id_student]["nom"], calcul_moyenne(id_student)})
    return temp

# print(top_students())

# # Créer une dictionnaire inversé: moyenne -> liste des noms
inversed_dict = {}

for id_student in students_dict.keys():
    mean_student = int(calcul_moyenne(id_student))
    try:
        inversed_dict[mean_student].append(students_dict[id_student])
    except:
        inversed_dict[mean_student] = [students_dict[id_student]]
# print(inversed_dict)

# # Créer une fonction détectant les étudiants ayant des notes dupliquées
def students_with_dup_notes(students_dictionnary: dict):
    temp = []
    for student_id in students_dictionnary.keys():
        for i in range(len(students_dictionnary[student_id]["notes"])):
            for j in range(len(students_dictionnary[student_id]["notes"])):
                if i!=j and students_dictionnary[student_id]["notes"][i] == students_dictionnary[student_id]["notes"][j] and (students_dictionnary[student_id]["nom"] not in temp):
                    temp.append(students_dictionnary[student_id]["nom"])
    return temp

# print(students_with_dup_notes(students_dict))

def trier_etudiants(critere):
    items_etudiants = list(students_dict.items())

    if critere == "nom":
        items_etudiants.sort(key=lambda x: x[1]["nom"].lower())

    elif critere == "moyenne":
        items_etudiants.sort(key=lambda x: calcul_moyenne(x[0]), reverse=True)

    elif critere == "nombre_notes":
        items_etudiants.sort(key=lambda x: len(x[1]["notes"]), reverse=True)

    else:
        print("Critère invalide. Choisissez: 'nom', 'moyenne', ou 'nombre_notes'")
        return None

    resultat = {}
    for k, v in items_etudiants:
        resultat[k] = v

    return resultat

# print(trier_etudiants("nom"))
# print(trier_etudiants("moyenne"))
# print(trier_etudiants("nombre_notes"))

def fusionner_dictionnaires(dict1: dict, dict2: dict):
    resultat = dict1.copy()

    for id_student, info_dict2 in dict2.items():
        if id_student not in resultat:
            resultat[id_student] = info_dict2
        else:
            notes_dict1 = resultat[id_student]["notes"]
            moy_dict1 = sum(notes_dict1) / len(notes_dict1) if len(notes_dict1) > 0 else 0

            notes_dict2 = info_dict2["notes"]
            moy_dict2 = sum(notes_dict2) / len(notes_dict2) if len(notes_dict2) > 0 else 0

            if moy_dict2 > moy_dict1:
                resultat[id_student] = info_dict2

    return resultat
students_dict2 = {
    "0001": {"nom": "Ahmed", "notes": [18, 19, 20]},
    "0100": {"nom": "Said", "notes": [2, 4, 5]},
    "9999": {"nom": "Nouvel_Etudiant", "notes": [15, 15, 15]}
}
# print(fusionner_dictionnaires(students_dict, students_dict2))

