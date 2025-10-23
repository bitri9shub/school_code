import sqlite3
# la création du fichier gestion.db
db=sqlite3.connect("gestion.db")

def create_table():
    # rien ne s'affiche dans le terminal mais normalement,
    # ça sert à créer une table person avec deux colonnes code et name
    db.execute("create table if not exists person(code integer, name text)") 

def insert_element_table(code, name):
    # insérer une valeur (10, "karim") dans la table
    db.execute("insert into person(code,name) values(?,?)", (code, name))
    # insérer d'autres valeurs
    # db.execute("insert into person(code,name) values(?,?)", (11, "Amal"))
    # db.execute("insert into person(code,name) values(?,?)", (12, "Reda"))

def delete_table(code):
    # suprimer l'utilisateur avec id=10
    db.execute(f'delete from person where code={code}')

def update_table(code,name):
    # modifier le nom de Reda à Radi
    db.execute(f"update person set name={name} where code={code}")

def affichage_colonnes():
    # affichage des colonnes
    # créer les tables à partir des tuples
    db.row_factory=sqlite3.Row
    # selection des éléments souhaités
    cursor=db.execute("select distinct * from person")
    db.commit()
    for row in cursor:
        print(row["code"], row["name"])
    # fermer la base de données
    db.close()

# /!\ si une table existe au préalable mais avec une structure différente et 
# tu la redéfinies, que va faire ton code.


create_table()
insert_element_table(1,'ahmed')
insert_element_table(2,'morad')
insert_element_table(3,'abdellah')
insert_element_table(4,'karim')
insert_element_table(12,'mouad')
affichage_colonnes()
