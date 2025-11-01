import os 

def create_file(fileName):
    try:
        f = open(f'{fileName}.txt', 'x') 
        f.close()
        print(f"File '{fileName}.txt' created successfully.")
    except FileExistsError:
        print(f"File '{fileName}.txt' already exists.")

def write_file(fileName):
    try:
        sentence = input('Donner une phrase: ')
        sentence += ";"
        with open(f'{fileName}.txt', 'a') as file:
            file.write(sentence)
    except FileNotFoundError:
        print(f"File '{fileName}.txt' not found. Please create it first.")

def read_file(fileName):
    try:
        with open(f'{fileName}.txt', 'r') as file:
            print(file.readline())
    except FileNotFoundError:
        print(f"File '{fileName}.txt' not found.")

def delete_file(fileName):
    try:
        os.remove(f'{fileName}.txt')
        print(f"File '{fileName}.txt' deleted successfully.")
    except FileNotFoundError:
        print(f"File '{fileName}.txt' not found.")

def sentence_frequency(fileName):
    try:
        with open(f'{fileName}.txt', 'r') as file:
            content = file.readline()
            sentences = content.split(';')
            filtered_sentences = []
            for sentence in sentences:
                if sentence.strip(): 
                    filtered_sentences.append(sentence.strip())
            return filtered_sentences
    except FileNotFoundError:
        print(f"File '{fileName}.txt' not found.")
        return []

def word_frequency(fileName):
    sentences = sentence_frequency(fileName)
    if not sentences:
        return []
    
    unflattened_words = [sentence.split(" ") for sentence in sentences]
    words = [element for sublist in unflattened_words for element in sublist]  
    filtered_words = [word.strip() for word in words if word.strip()]  # Added strip()
    return filtered_words

def word_mean_length(fileName):
    word_list = word_frequency(fileName)
    if not word_list:
        return 0
    
    total_length = 0
    for word in word_list:
        total_length += len(word)
    return total_length / len(word_list)

def calculate_word_occurence(word_list):
    word_list = word_frequency(fileName)
    if not word_list:
        return 0
    
    total_length = 0
    for word in word_list:
        total_length += len(word)
    return total_length / len(word_list)

def calculate_word_occurence(fileName):
    word_list = word_frequency(fileName)
    if not word_list:
        return [{}, [], []]

    occur_obj = {}
    for word in word_list:
        if word not in occur_obj:
            occur_obj[word] = 1
        else:
            occur_obj[word] += 1

    # Find most used words
    if occur_obj:
        max_count = max(occur_obj.values())
        most_used = [word for word, count in occur_obj.items() if count == max_count]
        
        # Find least used words
        min_count = min(occur_obj.values())
        less_used = [word for word, count in occur_obj.items() if count == min_count]
    else:
        most_used = []
        less_used = []

    return [occur_obj, most_used, less_used]

# def most_used_words(fileName):
#     word_list = word_frequency(fileName)
#     occurences = calculate_word_occurence(word_list)
#     most_used = []
#     max = 1
#     for valeur in occurences.values():
#         if valeur > max:
#             max = valeur
#     for index, valeur in occurences.items():
#         if max == valeur:
#             most_used.append(index)
#     return most_used

# def less_used_words(fileName):
#     word_list = word_frequency(fileName)  
#     occurences = calculate_word_occurence(word_list)
#     less_used = []
#     min = 1
#     for valeur in occurences.values():
#         if valeur < max:
#             max = valeur
#     for index, valeur in occurences.items():
#         if min == valeur:
#             less_used.append(index)
#     return less_used

def palyndrom_list(fileName):
    sentences_list = sentence_frequency(fileName)
    for sentence in sentences_list:
        words = sentence.split()
        print(f'"{sentence}" has {len(words)} words.')

def words_frequency_in_sentences(fileName):
    sentences_list = sentence_frequency(fileName)
    for sentence in sentences_list:
        print(f'"{sentence}" has {len(sentence)} words.')

while True:
    choix = int(input("""
1. Créer un fichier
2. Ecrire dans un fichier
3. Lire un fichier
4. Analyser un fichier
5. Supprimer un fichier
6. Quitter\n          
    """))
    match(choix):
        case 1:
            fileName = input("Donner le nom d'un fichier: ")
            create_file(fileName)
        case 2:
            fileName = input("Donner le nom d'un fichier: ")
            write_file(fileName)
            while True:
                sous_choix = int(input("""
                    1. Rajouter
                    2. Quitter
                                       
                """))
                match(sous_choix):
                    case 1:
                        write_file(fileName)
                    case 2:
                        break
        case 3:
            fileName = input("Donner le nom d'un fichier: ")
            read_file(fileName)
        case 4:
            # menu:
            fileName = input("Donner le nom d'un fichier: ")
            while True:
                choix = int(input("""
1. Fréquence des mots
2. Longueur moyenne des mots
3. Mots les plus/moins utilisés
4. Detection des palyndromes
5. Longueur des phrases
6. Type de ponctuations utilisées
7. Statistiques par type de mot    
8. Quitter\n                                 
                """))
                match(choix):
                    case 1:
                        print(f'Fréquence des mots: {len(word_frequency(fileName))}.')
                    case 2:
                        print(f'Longueure moyenne des mots: {word_mean_length(fileName)}.')
                    case 3:
                        statistics = calculate_word_occurence(fileName)
                        print(f'Les mots les plus utilisés: {statistics[1]}.')
                        print(f'Les mots les moins utilisés: {statistics[2]}.')
                    case 4:
                        print(f'La liste des palyndromes: {palyndrom_list(fileName)}')
                    case 5:
                        words_frequency_in_sentences(fileName)
                    case 6:
                        print()
                    case 7:
                        print()
                    case 8:
                        break
        case 5:
            fileName = input("Donner le nom d'un fichier: ")
            delete_file(fileName)
        case 6:
            break