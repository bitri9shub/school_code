###############################################
################# fonctions ###################
###############################################
# def say_salamu_alaykom():
#     print("salamu_alaykom".replace('_', ' '))
# say_salamu_alaykom()

###############################################
################# Arguments ###################
###############################################
# def say_salam(name):
#     print(f'assalamu alaykom {name}')
# say_salam('ahmed')

###########################################################
################# Arguments arbitraires ###################
###########################################################
# def say_salam_people(*people):
#     for person in people:
#         print(f'assalmu alaykom {person}')
# say_salam_people('ahmed','mohamed','salah','souhail','abdellah')

#####################################################################
################# Arguments de mots clés (kwargs) ###################
#####################################################################
# def my_function(child3, child2, child1):
#     print('the youngest child is ' + child3)
# my_function(child1='Emil', child2='Tobias', child3='Linus')

#################################################################################
################# Arguments arbitraires de mots clés (kwargs) ###################
#################################################################################
# def my_function(**kid):
#     print('the youngest child is ' + kid["lname"])
# my_function(fname="Tobias", lname="linus")

########################################################
################# Valeurs par Défaut ###################
########################################################
# def say_salam(name='Ahmed'):
#     print(f'assalamu alaykom {name}')
# say_salam()
# say_salam("dak_bo_ras")

#######################################################
################# Valeurs de retour ###################
#######################################################
# def hsasbi(x):
#     return 5 * x
# print(hsasbi(10))

#####################################################
################# fonction lambda ###################
#####################################################
# ma_fonction = lambda x:x*x
# print(ma_fonction(10))

######################################################
################# fonctions utiles ###################
######################################################
# map(Fn: x -> y, Iterator)
# filter(Fn: x -> bool, Iterator)
# reduce(Fn: x,y -> z, Iterator) /!\ should be imported from functools.

################################################
################# Décorateur ###################
################################################
# /!\ 
# Fonction qui prend en argument une autre fonction.
# L'intepreteur qui execute le décorateur.

# @decorator
# def functions(arg):
#     return 'value' 

# def my_decorator(func):
#     def wrapper(*args, **kwargs):
#         print("what happens before funct is executed")
#         result = func(*args, **kwargs)
#         print("what happens after funct is executed")
#         return result
#     return wrapper

# @timeit
# def name():
#     # ...

# Exemple
# import time
# def timeit(funct):
#     def wrapper(*args, **kwargs):
#         start_time = time.time()
#         result= funct(*args, **kwargs)
#         end_time = time.time()
#         print(f'execution time is: {end_time-start_time}')
#         return result
#     return wrapper

# @timeit
# def test_function(a, b):
#     return a+b

# print(test_function(1, 2))

###############################################
################# Remarques ###################
###############################################

# /!\ ce n'est pas un "spread operator".
# def hsasbi_mjahed(*knach):
#     print(knach)
    # s=0
    # for num in knach:
    #     s+=num
    # return s
# print(hsasbi_mjahed([1, 2, 3, 4, 5]))

# /!\ A revoir car ça n'a pas marché.
# une_liste = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
# increment = lambda x:x*x
# print(map(lambda x:x*x, une_liste))

