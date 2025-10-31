stock = {}

def ajouter_produit():
    print('ajouter un produit')
    nom=input('entrer un choix: ')
    prix=input('entrer le prix: ')
    quatite=int(input('entrer le quantite: '))
    if nom in stock:
        stock[nom]['quatite']+=quatite
    else:
        stock[nom]={
            'prix':prix,
            'quantite':quatite
        }

def supprimer_produit():
    print('supprimer produit')
    produitsup=input('le nom du produit: ')
    if produitsup in stock:
        del stock[produitsup]

def afficher_stock():
    print('stock total')
    
      
while True:
    print("""
    1.ajouter produit
    2.supprimer produit
    3.stock total
    4.quitter
    """)
    choix=int(input('Entrer un choix: '))
    if choix==1:
         ajouter_produit()
    elif choix==2:
          supprimer_produit()
    elif choix==3:
          afficher_stock()
    elif choix==4:
        print('quitter')
        break