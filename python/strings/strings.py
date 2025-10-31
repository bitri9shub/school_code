####################################################################
################# built-in functions for strings ###################
####################################################################
# a=" hello World ! "
# print(a.upper())
# print(a.lower())
# print(a.strip())
# print(a.replace(a[1],'H'))
# b=a.split(" ")
# print(b)
# print(b.join(" "))

#######################################################
################# formating methods ###################
#######################################################

################# method 1 #################
# print('%d %s cost $%.2f' % (6, 'banane', 1.74))

################# method 2 #################
# we can add number inside brackets to modify the order
# print("{0} {2} cost ${1}".format(6,'banane', 1.74))

################# method 3 #################
# quantity = 6
# cost = 1.74
# item = "banane"
# print(f'{quantity} {item} cost ${cost}')