import random

# # Ecrire une fonction qui reçoit une liste de nombres et renvoie une nouvelle
# # contenant uniquement les valeurs uniques en conservant l'ordre d'apparition

ex_list = [1,1,2,3,4,4,5,6,7,8]

# def unique_value(list):
#     temp = []
#     for element in list:
#         if element not in temp:
#             temp.append(element)
#     return temp

# print(unique_value([1,1,2,3,4,4,5,6,7,8]))

# # Transformer cette liste en tuple et afficher: somme, min, max, moyenne
# filtred_list = unique_value(ex_list)
# filtred_tuple = tuple(filtred_list)
# print(f'le tuple: {filtred_tuple}')
# print(f'le max du tuple: {max(filtred_tuple)}')
# print(f'le min du tuple: {min(filtred_tuple)}')
# print(f'la somme du tuple: {sum(filtred_tuple)}')
# print(f'la moyenne du tuple: {sum(filtred_tuple)/len(filtred_tuple)}')

# # Créer une deuxième liste aléatoire de même longueur et produire la somme element par element 
# # en levant ValueError si les longueurs diffèrent

# def elemByElem_sum(list1: list):
#     list2 = [random.randint(1,100)for _ in range(len(list1))]

#     if len(list1) != len(list2):
#         raise ValueError("Les deux listes n'ont pas la même taille.")

#     somme = 0
#     for i in range(len(list1)):
#         somme += list1[i] + list2[i]
    
#     return somme

# print(elemByElem_sum(ex_list))

# # Générer une nouvelle liste contenant les 5 plus grandes valeurs de la liste initiale
# # sans utiliser sort() ni sorted()

# def cinq_plus_grands_elements(list1:list):
#     temp = []
#     for _ in range(5):
#         temp.append(max(list1))
#         list1.remove(max(list1))
#     return temp

# print(cinq_plus_grands_elements(ex_list))

# # Créer une comprehension list renvoyant toutes les valeurs strictement croissantes
# # de la liste (chaque élément doit être > au précédent)

# comprehension_list([10, 2, 3, 9, 4, 18, 5, 90]) -> [2, 3, 9, 18, 90]
# def comprehension_list(list1: list):
#     temp = []
#     if list1[0]>list1[1]:
#         temp.append(list1[1])
#     else:
#         temp.append(list1[0])

#     for i in range(1,len(list1)-1):
#         print(f'{list1[i]}, {list1[i+1]}')
#         if list1[i] < list1[i+1]:
#             temp.append(list1[i+1])
        
#     return temp
# print(comprehension_list([10, 2, 3, 9, 4, 18, 5, 90]))


# # Implémenter un algorithme qui détecte si la liste contient une sub-list triée de longueur >= 3
# # (au moins trois éléments consécutifs sont triés) 
# # [10, 2, 3, 9, 4, 18, 5, 90] -> true (2, 3, 9)
# def sorted_sublist(list1: list):
#     n = len(list1)
#     if n < 3:
#         return False    
#     count_asc = 1
#     for i in range(1, n):
#         if list1[i] > list1[i-1]:
#             count_asc += 1
#             if count_asc == 3:
#                 return True
#         else:
#             count_asc = 1 
#     return False

# print(sorted_sublist([10, 2, 3, 9, 4, 18, 5, 90]))


# # Vérifier si la liste est un palyndrome sans créer une liste inversée
# # [0,0,1,0,0] -> True // [0,1,0,1,1] -> False
# def is_list_palyndrom(list1: list):
#     n = len(list1)
#     for i in range(n // 2):
#         if list1[i] != list1[n - 1 - i]:
#             return False
#     return True
# print(is_list_palyndrom([0,0,1,0,0]))
# print(is_list_palyndrom([0,1,0,1,1]))
