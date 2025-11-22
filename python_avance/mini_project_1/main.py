from tkinter import *
from tkinter import messagebox, ttk, TclError
from sqlite3 import *
import hashlib
from datetime import datetime

# ============= PARTIE OUTILS =============
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    db = connect("gestion.db")
    
    # Table User
    db.execute("""CREATE TABLE IF NOT EXISTS User(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            firstName TEXT NOT NULL,
            lastName TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
            )""")
    
    # Table Book
    db.execute("""CREATE TABLE IF NOT EXISTS Book(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bookname TEXT NOT NULL,
            author TEXT NOT NULL,
            pages INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL DEFAULT 0.0
            )""")
    
    # Table Command (Commandes)
    db.execute("""CREATE TABLE IF NOT EXISTS Command(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            total_price REAL NOT NULL,
            order_date TEXT NOT NULL,
            status TEXT DEFAULT 'En attente',
            FOREIGN KEY (user_id) REFERENCES User(id),
            FOREIGN KEY (book_id) REFERENCES Book(id)
            )""")
    
    # Table Stock History
    db.execute("""CREATE TABLE IF NOT EXISTS StockHistory(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            action TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            date TEXT NOT NULL,
            user_id INTEGER,
            FOREIGN KEY (book_id) REFERENCES Book(id),
            FOREIGN KEY (user_id) REFERENCES User(id)
            )""")
    
    db.commit()
    db.close()

def create_user(username, firstName, lastName, password, role):
    try:
        database = connect("gestion.db")
        hashed_pwd = hash_password(password)
        database.execute("INSERT INTO User(username, firstName, lastName, password, role) VALUES (?, ?, ?, ?, ?)",
                   (username, firstName, lastName, hashed_pwd, role))
        database.commit()
        database.close()
        return True
    except Exception as e:
        print(f"Erreur création utilisateur: {e}")
        return False

def authenticate_user(username, password):
    try:
        database = connect("gestion.db")
        hashed_pwd = hash_password(password)
        cursor = database.execute("SELECT * FROM User WHERE username=? AND password=?", 
                                 (username, hashed_pwd))
        user_data = cursor.fetchone()
        database.close()
        
        if user_data:
            return User(*user_data)
        return None
    except Exception as e:
        print(f"Erreur authentification: {e}")
        return None

# ============= PARTIE BACKEND =============
class User:
    def __init__(self, id, username, firstName, lastName, password, role):
        self.id = id
        self.username = username
        self.firstName = firstName
        self.lastName = lastName
        self.password = password
        self.role = role

    # ===== CRUD Users =====
    def read_users(self):
        with connect("gestion.db") as database:
            cursor = database.execute("SELECT * FROM User")
            return cursor.fetchall()
    
    def read_user_by_id(self, user_id):
        with connect("gestion.db") as database:
            cursor = database.execute("SELECT * FROM User WHERE id=?", (user_id,))
            return cursor.fetchone()
    
    def update_user_by_id(self, user_id, username, firstName, lastName, password, role):
        try:
            with connect("gestion.db") as database:
                hashed_pwd = hash_password(password) if password else None
                if hashed_pwd:
                    database.execute("UPDATE User SET username=?, firstName=?, lastName=?, password=?, role=? WHERE id=?",
                                (username, firstName, lastName, hashed_pwd, role, user_id))
                else:
                    database.execute("UPDATE User SET username=?, firstName=?, lastName=?, role=? WHERE id=?",
                                (username, firstName, lastName, role, user_id))
                database.commit()
            return True
        except Exception as e:
            print(f"Erreur mise à jour utilisateur: {e}")
            return False
    
    def delete_user_by_id(self, user_id):
        try:
            with connect("gestion.db") as database:
                database.execute("DELETE FROM User WHERE id=?", (user_id,))
                database.commit()
            return True
        except Exception as e:
            print(f"Erreur suppression utilisateur: {e}")
            return False

    # ===== CRUD Books =====
    def create_book(self, bookname, author, pages, quantity, price=0.0):
        try:
            with connect("gestion.db") as database:
                cursor = database.execute("INSERT INTO Book(bookname, author, pages, quantity, price) VALUES (?, ?, ?, ?, ?)",
                                (bookname, author, pages, quantity, price))
                book_id = cursor.lastrowid
                database.commit()
                
                # Ajouter à l'historique du stock
                self.add_stock_history(book_id, "Ajout initial", quantity)
            return True
        except Exception as e:
            print(f"Erreur création livre: {e}")
            return False

    def read_books(self):
        with connect("gestion.db") as database:
            cursor = database.execute("SELECT * FROM Book")
            return cursor.fetchall()
    
    def search_books(self, search_term):
        with connect("gestion.db") as database:
            cursor = database.execute(
                "SELECT * FROM Book WHERE bookname LIKE ? OR author LIKE ?",
                (f"%{search_term}%", f"%{search_term}%")
            )
            return cursor.fetchall()
    
    def read_book_by_id(self, book_id):
        with connect("gestion.db") as database:
            cursor = database.execute("SELECT * FROM Book WHERE id=?", (book_id,))
            return cursor.fetchone()
    
    def update_book_by_id(self, book_id, bookname, author, pages, quantity, price):
        try:
            with connect("gestion.db") as database:
                database.execute("UPDATE Book SET bookname=?, author=?, pages=?, quantity=?, price=? WHERE id=?",
                            (bookname, author, pages, quantity, price, book_id))
                database.commit()
            return True
        except Exception as e:
            print(f"Erreur mise à jour livre: {e}")
            return False
    
    def delete_book_by_id(self, book_id):
        try:
            with connect("gestion.db") as database:
                database.execute("DELETE FROM Book WHERE id=?", (book_id,))
                database.commit()
            return True
        except Exception as e:
            print(f"Erreur suppression livre: {e}")
            return False
    
    # ===== Stock Management =====
    def add_stock_history(self, book_id, action, quantity):
        try:
            with connect("gestion.db") as database:
                date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                database.execute("INSERT INTO StockHistory(book_id, action, quantity, date, user_id) VALUES (?, ?, ?, ?, ?)",
                            (book_id, action, quantity, date, self.id))
                database.commit()
        except Exception as e:
            print(f"Erreur historique stock: {e}")
    
    def get_stock_history(self, book_id=None):
        with connect("gestion.db") as database:
            if book_id:
                cursor = database.execute("""
                    SELECT sh.*, b.bookname, u.username 
                    FROM StockHistory sh
                    JOIN Book b ON sh.book_id = b.id
                    LEFT JOIN User u ON sh.user_id = u.id
                    WHERE sh.book_id = ?
                    ORDER BY sh.date DESC
                """, (book_id,))
            else:
                cursor = database.execute("""
                    SELECT sh.*, b.bookname, u.username 
                    FROM StockHistory sh
                    JOIN Book b ON sh.book_id = b.id
                    LEFT JOIN User u ON sh.user_id = u.id
                    ORDER BY sh.date DESC
                    LIMIT 50
                """)
            return cursor.fetchall()

class Command:
    """Classe pour gérer les commandes"""
    
    @staticmethod
    def create_command(user_id, book_id, quantity, total_price):
        try:
            with connect("gestion.db") as database:
                date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                database.execute("INSERT INTO Command(user_id, book_id, quantity, total_price, order_date) VALUES (?, ?, ?, ?, ?)",
                            (user_id, book_id, quantity, total_price, date))
                
                # Mettre à jour la quantité du livre
                database.execute("UPDATE Book SET quantity = quantity - ? WHERE id=?", (quantity, book_id))
                database.commit()
            return True
        except Exception as e:
            print(f"Erreur création commande: {e}")
            return False
    
    @staticmethod
    def read_commands(user_id=None):
        with connect("gestion.db") as database:
            if user_id:
                cursor = database.execute("""
                    SELECT c.*, b.bookname, b.author, u.username 
                    FROM Command c
                    JOIN Book b ON c.book_id = b.id
                    JOIN User u ON c.user_id = u.id
                    WHERE c.user_id = ?
                    ORDER BY c.order_date DESC
                """, (user_id,))
            else:
                cursor = database.execute("""
                    SELECT c.*, b.bookname, b.author, u.username 
                    FROM Command c
                    JOIN Book b ON c.book_id = b.id
                    JOIN User u ON c.user_id = u.id
                    ORDER BY c.order_date DESC
                """)
            return cursor.fetchall()
    
    @staticmethod
    def update_command_status(command_id, status):
        try:
            with connect("gestion.db") as database:
                database.execute("UPDATE Command SET status=? WHERE id=?", (status, command_id))
                database.commit()
            return True
        except Exception as e:
            print(f"Erreur mise à jour statut: {e}")
            return False

class Stock:
    """Classe pour gérer les statistiques de stock"""
    
    @staticmethod
    def get_low_stock_books(threshold=5):
        with connect("gestion.db") as database:
            cursor = database.execute("SELECT * FROM Book WHERE quantity <= ? ORDER BY quantity ASC", (threshold,))
            return cursor.fetchall()
    
    @staticmethod
    def get_total_books():
        with connect("gestion.db") as database:
            cursor = database.execute("SELECT COUNT(*), SUM(quantity) FROM Book")
            return cursor.fetchone()
    
    @staticmethod
    def get_total_value():
        with connect("gestion.db") as database:
            cursor = database.execute("SELECT SUM(quantity * price) FROM Book")
            result = cursor.fetchone()
            return result[0] if result[0] else 0.0

# ============= PARTIE FRONTEND =============
class MultiInterfaceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Store - Système de Gestion")
        self.root.geometry("900x700")
        self.current_user = None
        
        # Configuration de la fermeture
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.container = Frame(root)
        self.container.pack(fill="both", expand=True, padx=40, pady=40)

        self.show_home()

    def on_closing(self):
        if messagebox.askokcancel("Quitter", "Voulez-vous quitter l'application?"):
            self.root.destroy()

    def clean_interface(self):
        for component in self.container.winfo_children():
            component.destroy()

    def show_home(self):
        """Page de connexion"""
        self.clean_interface()
        self.current_user = None
        
        title = Label(self.container, text="📚 Book Store", font=("Arial", 24, "bold"), fg="#2c3e50")
        title.pack(pady=20)
        
        subtitle = Label(self.container, text="Connexion", font=("Arial", 16), fg="#7f8c8d")
        subtitle.pack(pady=10)

        # Frame pour le formulaire
        form_frame = Frame(self.container)
        form_frame.pack(pady=30)

        Label(form_frame, text="Nom d'utilisateur:", font=("Arial", 10)).grid(row=0, column=0, sticky=W, pady=5)
        username = StringVar()
        username_input = Entry(form_frame, textvariable=username, width=30, font=("Arial", 10))
        username_input.grid(row=0, column=1, pady=5, padx=10)

        Label(form_frame, text="Mot de passe:", font=("Arial", 10)).grid(row=1, column=0, sticky=W, pady=5)
        password = StringVar()
        password_input = Entry(form_frame, textvariable=password, width=30, show="●", font=("Arial", 10))
        password_input.grid(row=1, column=1, pady=5, padx=10)

        def login():
            if not username.get() or not password.get():
                messagebox.showwarning("Attention", "Veuillez remplir tous les champs")
                return
                
            user = authenticate_user(username.get(), password.get())
            if user:
                self.current_user = user
                messagebox.showinfo("Succès", f"Bienvenue {user.firstName} {user.lastName}!")
                if user.role == "admin":
                    self.show_admin_panel()
                else:
                    self.show_store()
            else:
                messagebox.showerror("Erreur", "Identifiants incorrects")

        # Boutons
        btn_frame = Frame(self.container)
        btn_frame.pack(pady=20)
        
        Button(btn_frame, text="Se connecter", command=login, bg="#27ae60", fg="white", 
               width=20, font=("Arial", 10, "bold"), cursor="hand2").pack(pady=5)
        Button(btn_frame, text="S'inscrire", command=self.show_register, bg="#3498db", fg="white",
               width=20, font=("Arial", 10), cursor="hand2").pack(pady=5)
        
        # Enter pour se connecter
        password_input.bind('<Return>', lambda e: login())

    def show_register(self):
        """Page d'inscription"""
        self.clean_interface()
        
        title = Label(self.container, text="Inscription", font=("Arial", 20, "bold"), fg="#2c3e50")
        title.pack(pady=20)

        # Frame formulaire
        form_frame = Frame(self.container)
        form_frame.pack(pady=20)

        fields = {}
        labels = ["Nom d'utilisateur", "Prénom", "Nom", "Mot de passe", "Confirmer mot de passe"]
        keys = ["username", "firstName", "lastName", "password", "confirm_password"]
        
        for i, (label, key) in enumerate(zip(labels, keys)):
            Label(form_frame, text=f"{label}:", font=("Arial", 10)).grid(row=i, column=0, sticky=W, pady=5, padx=5)
            var = StringVar()
            entry = Entry(form_frame, textvariable=var, width=30, font=("Arial", 10))
            if "password" in key:
                entry.config(show="●")
            entry.grid(row=i, column=1, pady=5, padx=10)
            fields[key] = var

        # Role
        Label(form_frame, text="Rôle:", font=("Arial", 10)).grid(row=len(keys), column=0, sticky=W, pady=5, padx=5)
        role = StringVar(value="user")
        role_frame = Frame(form_frame)
        role_frame.grid(row=len(keys), column=1, pady=5, sticky=W)
        Radiobutton(role_frame, text="Utilisateur", variable=role, value="user").pack(side=LEFT, padx=5)
        Radiobutton(role_frame, text="Admin", variable=role, value="admin").pack(side=LEFT, padx=5)

        def register():
            # Validation
            if not all(fields[k].get().strip() for k in keys):
                messagebox.showwarning("Attention", "Veuillez remplir tous les champs")
                return
            
            if len(fields["password"].get()) < 4:
                messagebox.showwarning("Attention", "Le mot de passe doit contenir au moins 4 caractères")
                return
            
            if fields["password"].get() != fields["confirm_password"].get():
                messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas")
                return
            
            if create_user(fields["username"].get(), fields["firstName"].get(), 
                         fields["lastName"].get(), fields["password"].get(), role.get()):
                messagebox.showinfo("Succès", "Inscription réussie! Vous pouvez maintenant vous connecter.")
                self.show_home()
            else:
                messagebox.showerror("Erreur", "Ce nom d'utilisateur est déjà utilisé")

        # Boutons
        btn_frame = Frame(self.container)
        btn_frame.pack(pady=20)
        
        Button(btn_frame, text="S'inscrire", command=register, bg="#27ae60", fg="white", 
               width=20, font=("Arial", 10, "bold")).pack(pady=5)
        Button(btn_frame, text="Retour", command=self.show_home, bg="#95a5a6", fg="white",
               width=20, font=("Arial", 10)).pack(pady=5)

    def show_store(self):
        """Interface boutique pour utilisateurs"""
        self.clean_interface()
        
        # Header
        header_frame = Frame(self.container, bg="#3498db", height=60)
        header_frame.pack(fill=X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        Label(header_frame, text=f"🛒 Boutique - {self.current_user.firstName} {self.current_user.lastName}", 
              font=("Arial", 16, "bold"), bg="#3498db", fg="white").pack(side=LEFT, padx=20, pady=15)
        
        Button(header_frame, text="Mes Commandes", command=self.show_my_orders, bg="#e74c3c", fg="white",
               font=("Arial", 9), cursor="hand2").pack(side=RIGHT, padx=5, pady=15)
        Button(header_frame, text="Déconnexion", command=self.show_home, bg="#95a5a6", fg="white",
               font=("Arial", 9), cursor="hand2").pack(side=RIGHT, padx=5, pady=15)

        # Barre de recherche
        search_frame = Frame(self.container)
        search_frame.pack(fill=X, pady=10)
        
        Label(search_frame, text="🔍 Rechercher:", font=("Arial", 10)).pack(side=LEFT, padx=5)
        search_var = StringVar()
        search_entry = Entry(search_frame, textvariable=search_var, width=40, font=("Arial", 10))
        search_entry.pack(side=LEFT, padx=5)
        
        def search_books():
            refresh_books(search_var.get())
        
        Button(search_frame, text="Rechercher", command=search_books, bg="#3498db", fg="white",
               cursor="hand2").pack(side=LEFT, padx=5)
        Button(search_frame, text="Tout afficher", command=lambda: refresh_books(""), bg="#95a5a6", fg="white",
               cursor="hand2").pack(side=LEFT, padx=5)

        # Treeview pour afficher les livres
        tree_frame = Frame(self.container)
        tree_frame.pack(fill="both", expand=True, pady=10)

        scrollbar = Scrollbar(tree_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        tree = ttk.Treeview(tree_frame, columns=("ID", "Titre", "Auteur", "Pages", "Quantité", "Prix"), 
                           show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)

        tree.heading("ID", text="ID")
        tree.heading("Titre", text="Titre")
        tree.heading("Auteur", text="Auteur")
        tree.heading("Pages", text="Pages")
        tree.heading("Quantité", text="Stock")
        tree.heading("Prix", text="Prix (DH)")

        tree.column("ID", width=50)
        tree.column("Titre", width=200)
        tree.column("Auteur", width=150)
        tree.column("Pages", width=80)
        tree.column("Quantité", width=80)
        tree.column("Prix", width=100)

        tree.pack(fill="both", expand=True)

        def refresh_books(search_term=""):
            tree.delete(*tree.get_children())
            if search_term:
                books = self.current_user.search_books(search_term)
            else:
                books = self.current_user.read_books()
            
            for book in books:
                # Colorer en rouge si stock faible
                tag = "low_stock" if book[4] <= 5 else ""
                tree.insert("", "end", values=book, tags=(tag,))
            
            tree.tag_configure("low_stock", background="#ffcccc")

        def order_book():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Attention", "Veuillez sélectionner un livre")
                return
            
            book_data = tree.item(selected[0])["values"]
            book_id = book_data[0]
            book_name = book_data[1]
            available_qty = book_data[4]
            price = float(book_data[5])  # Convertir en float
            
            if available_qty <= 0:
                messagebox.showerror("Erreur", "Livre en rupture de stock")
                return
            
            # Dialogue pour la quantité
            qty_window = Toplevel(self.root)
            qty_window.title("Commander")
            qty_window.geometry("350x320")
            qty_window.transient(self.root)
            qty_window.grab_set()
            
            Label(qty_window, text=f"Livre: {book_name}", font=("Arial", 10, "bold")).pack(pady=10)
            Label(qty_window, text=f"Prix unitaire: {price} DH", font=("Arial", 9)).pack(pady=5)
            Label(qty_window, text=f"Stock disponible: {available_qty}", font=("Arial", 9)).pack(pady=5)
            
            Label(qty_window, text="Quantité:", font=("Arial", 10)).pack(pady=10)
            qty_var = IntVar(value=1)
            Spinbox(qty_window, from_=1, to=available_qty, textvariable=qty_var, width=10).pack()
            
            total_label = Label(qty_window, text=f"Total: {price:.2f} DH", font=("Arial", 10, "bold"), fg="#27ae60")
            total_label.pack(pady=10)
            
            def update_total(*args):
                try:
                    quantity = qty_var.get()
                    if quantity:
                        total = float(quantity) * float(price)
                        total_label.config(text=f"Total: {total:.2f} DH")
                except (ValueError, TclError):
                    total_label.config(text=f"Total: {price:.2f} DH")
            
            qty_var.trace_add('write', update_total)
            
            def confirm_order():
                try:
                    quantity = qty_var.get()
                    if quantity <= 0 or quantity > available_qty:
                        messagebox.showwarning("Attention", f"Veuillez entrer une quantité entre 1 et {available_qty}")
                        return
                    
                    total = quantity * price
                    
                    if Command.create_command(self.current_user.id, book_id, quantity, total):
                        messagebox.showinfo("Succès", f"Commande passée avec succès!\n\nLivre: {book_name}\nQuantité: {quantity}\nTotal: {total:.2f} DH")
                        qty_window.destroy()
                        refresh_books()
                    else:
                        messagebox.showerror("Erreur", "Échec de la commande")
                except (ValueError, TclError):
                    messagebox.showerror("Erreur", "Quantité invalide")
            
            # Boutons
            btn_frame = Frame(qty_window)
            btn_frame.pack(pady=15)
            
            Button(btn_frame, text="✓ Confirmer la commande", command=confirm_order, 
                   bg="#27ae60", fg="white", width=20, font=("Arial", 10, "bold"),
                   cursor="hand2").pack(pady=5)
            
            Button(btn_frame, text="✗ Annuler", command=qty_window.destroy, 
                   bg="#e74c3c", fg="white", width=20, font=("Arial", 9),
                   cursor="hand2").pack(pady=5)

        Button(self.container, text="📦 Commander", command=order_book, bg="#27ae60", fg="white",
               font=("Arial", 11, "bold"), width=20, cursor="hand2").pack(pady=10)

        refresh_books()

    def show_my_orders(self):
        """Afficher les commandes de l'utilisateur"""
        orders_window = Toplevel(self.root)
        orders_window.title("Mes Commandes")
        orders_window.geometry("800x500")
        orders_window.transient(self.root)
        
        Label(orders_window, text="📋 Mes Commandes", font=("Arial", 16, "bold")).pack(pady=10)
        
        tree_frame = Frame(orders_window)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        tree = ttk.Treeview(tree_frame, columns=("ID", "Livre", "Auteur", "Qté", "Total", "Date", "Statut"),
                           show="headings")
        
        for col in ["ID", "Livre", "Auteur", "Qté", "Total", "Date", "Statut"]:
            tree.heading(col, text=col)
        
        tree.column("ID", width=50)
        tree.column("Qté", width=60)
        tree.column("Total", width=100)
        tree.column("Statut", width=100)
        
        tree.pack(fill="both", expand=True)
        
        orders = Command.read_commands(self.current_user.id)
        for order in orders:
            # Format: id, user_id, book_id, quantity, total_price, order_date, status, bookname, author, username
            tree.insert("", "end", values=(order[0], order[7], order[8], order[3], 
                                          f"{order[4]:.2f} DH", order[5], order[6]))
        
        Button(orders_window, text="Fermer", command=orders_window.destroy, width=15).pack(pady=10)

    def show_admin_panel(self):
        """Panneau d'administration complet"""
        self.clean_interface()
        
        # Header
        header_frame = Frame(self.container, bg="#e74c3c", height=60)
        header_frame.pack(fill=X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        Label(header_frame, text=f"👤 Admin - {self.current_user.firstName} {self.current_user.lastName}", 
              font=("Arial", 16, "bold"), bg="#e74c3c", fg="white").pack(side=LEFT, padx=20, pady=15)
        
        Button(header_frame, text="Déconnexion", command=self.show_home, bg="#95a5a6", fg="white",
               font=("Arial", 9), cursor="hand2").pack(side=RIGHT, padx=20, pady=15)

        # Notebook pour onglets
        notebook = ttk.Notebook(self.container)
        notebook.pack(fill="both", expand=True, pady=10)

        # Onglet 1: Gestion Livres
        self.create_books_tab(notebook)
        
        # Onglet 2: Gestion Utilisateurs
        self.create_users_tab(notebook)
        
        # Onglet 3: Commandes
        self.create_orders_tab(notebook)
        
        # Onglet 4: Stock & Statistiques
        self.create_stats_tab(notebook)

    def create_books_tab(self, notebook):
        """Onglet gestion des livres"""
        books_frame = Frame(notebook)
        notebook.add(books_frame, text="📚 Livres")

        # Formulaire ajout/modification
        form_frame = LabelFrame(books_frame, text="Ajouter / Modifier un livre", font=("Arial", 10, "bold"))
        form_frame.pack(pady=10, padx=10, fill=X)

        book_fields = {}
        labels = ["Titre", "Auteur", "Pages", "Quantité", "Prix (DH)"]
        keys = ["bookname", "author", "pages", "quantity", "price"]
        
        for i, (label, key) in enumerate(zip(labels, keys)):
            Label(form_frame, text=f"{label}:").grid(row=i, column=0, padx=5, pady=5, sticky=W)
            var = StringVar()
            Entry(form_frame, textvariable=var, width=30).grid(row=i, column=1, padx=5, pady=5)
            book_fields[key] = var

        # Variable pour stocker l'ID du livre en cours de modification
        current_book_id = [None]

        def add_or_update_book():
            try:
                # Validation
                if not book_fields["bookname"].get().strip() or not book_fields["author"].get().strip():
                    messagebox.showerror("Erreur", "Titre et Auteur sont obligatoires")
                    return
                
                pages = int(book_fields["pages"].get())
                quantity = int(book_fields["quantity"].get())
                price = float(book_fields["price"].get())
                
                if pages <= 0 or quantity < 0 or price < 0:
                    messagebox.showerror("Erreur", "Valeurs invalides")
                    return
                
                if current_book_id[0]:
                    # Modification
                    if self.current_user.update_book_by_id(current_book_id[0], 
                        book_fields["bookname"].get(), book_fields["author"].get(),
                        pages, quantity, price):
                        messagebox.showinfo("Succès", "Livre modifié!")
                        current_book_id[0] = None
                        add_btn.config(text="Ajouter Livre")
                    else:
                        messagebox.showerror("Erreur", "Échec de la modification")
                else:
                    # Ajout
                    if self.current_user.create_book(
                        book_fields["bookname"].get(),
                        book_fields["author"].get(),
                        pages, quantity, price
                    ):
                        messagebox.showinfo("Succès", "Livre ajouté!")
                    else:
                        messagebox.showerror("Erreur", "Échec de l'ajout")
                
                refresh_books()
                for field in book_fields.values():
                    field.set("")
                    
            except ValueError:
                messagebox.showerror("Erreur", "Pages, Quantité et Prix doivent être des nombres valides")

        btn_frame = Frame(form_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        add_btn = Button(btn_frame, text="Ajouter Livre", command=add_or_update_book, 
                        bg="#27ae60", fg="white", width=15)
        add_btn.pack(side=LEFT, padx=5)
        
        def cancel_edit():
            current_book_id[0] = None
            add_btn.config(text="Ajouter Livre")
            for field in book_fields.values():
                field.set("")
        
        Button(btn_frame, text="Annuler", command=cancel_edit, bg="#95a5a6", 
               fg="white", width=15).pack(side=LEFT, padx=5)

        # Liste des livres
        list_frame = LabelFrame(books_frame, text="Liste des livres", font=("Arial", 10, "bold"))
        list_frame.pack(fill="both", expand=True, pady=10, padx=10)

        # Barre de recherche
        search_frame = Frame(list_frame)
        search_frame.pack(fill=X, pady=5)
        
        Label(search_frame, text="Rechercher:").pack(side=LEFT, padx=5)
        search_var = StringVar()
        Entry(search_frame, textvariable=search_var, width=30).pack(side=LEFT, padx=5)
        
        def search_books():
            refresh_books(search_var.get())
        
        Button(search_frame, text="🔍", command=search_books, width=3).pack(side=LEFT)
        Button(search_frame, text="Tout", command=lambda: refresh_books(""), width=5).pack(side=LEFT, padx=2)

        tree_frame = Frame(list_frame)
        tree_frame.pack(fill="both", expand=True, pady=5)

        scrollbar = Scrollbar(tree_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        tree = ttk.Treeview(tree_frame, columns=("ID", "Titre", "Auteur", "Pages", "Quantité", "Prix"), 
                           show="headings", height=10, yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        for col in ("ID", "Titre", "Auteur", "Pages", "Quantité", "Prix"):
            tree.heading(col, text=col)
        
        tree.column("ID", width=50)
        tree.column("Titre", width=200)
        tree.column("Auteur", width=150)
        tree.column("Pages", width=80)
        tree.column("Quantité", width=80)
        tree.column("Prix", width=100)
        
        tree.pack(fill="both", expand=True)

        def refresh_books(search_term=""):
            tree.delete(*tree.get_children())
            if search_term:
                books = self.current_user.search_books(search_term)
            else:
                books = self.current_user.read_books()
            
            for book in books:
                tag = "low_stock" if book[4] <= 5 else ""
                tree.insert("", "end", values=book, tags=(tag,))
            
            tree.tag_configure("low_stock", background="#ffcccc")

        def edit_book():
            selected = tree.selection()
            if selected:
                book_id = tree.item(selected[0])["values"][0]
                book = self.current_user.read_book_by_id(book_id)
                
                if book:
                    book_fields["bookname"].set(book[1])
                    book_fields["author"].set(book[2])
                    book_fields["pages"].set(book[3])
                    book_fields["quantity"].set(book[4])
                    book_fields["price"].set(book[5])
                    current_book_id[0] = book_id
                    add_btn.config(text="Modifier Livre")

        def delete_book():
            selected = tree.selection()
            if selected:
                book_id = tree.item(selected[0])["values"][0]
                if messagebox.askyesno("Confirmation", "Supprimer ce livre définitivement?"):
                    if self.current_user.delete_book_by_id(book_id):
                        messagebox.showinfo("Succès", "Livre supprimé")
                        refresh_books()
                    else:
                        messagebox.showerror("Erreur", "Échec de la suppression")

        action_frame = Frame(list_frame)
        action_frame.pack(pady=5)
        
        Button(action_frame, text="✏️ Modifier", command=edit_book, bg="#3498db", 
               fg="white", width=12).pack(side=LEFT, padx=5)
        Button(action_frame, text="🗑️ Supprimer", command=delete_book, bg="#e74c3c", 
               fg="white", width=12).pack(side=LEFT, padx=5)
        Button(action_frame, text="🔄 Actualiser", command=lambda: refresh_books(), 
               bg="#95a5a6", fg="white", width=12).pack(side=LEFT, padx=5)

        refresh_books()

    def create_users_tab(self, notebook):
        """Onglet gestion des utilisateurs"""
        users_frame = Frame(notebook)
        notebook.add(users_frame, text="👥 Utilisateurs")

        # Liste des utilisateurs
        list_frame = LabelFrame(users_frame, text="Liste des utilisateurs", font=("Arial", 10, "bold"))
        list_frame.pack(fill="both", expand=True, pady=10, padx=10)

        tree_frame = Frame(list_frame)
        tree_frame.pack(fill="both", expand=True, pady=5)

        scrollbar = Scrollbar(tree_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        tree = ttk.Treeview(tree_frame, columns=("ID", "Username", "Prénom", "Nom", "Rôle"), 
                           show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        for col in ("ID", "Username", "Prénom", "Nom", "Rôle"):
            tree.heading(col, text=col)
        
        tree.column("ID", width=50)
        tree.column("Username", width=150)
        tree.column("Prénom", width=150)
        tree.column("Nom", width=150)
        tree.column("Rôle", width=100)
        
        tree.pack(fill="both", expand=True)

        def refresh_users():
            tree.delete(*tree.get_children())
            users = self.current_user.read_users()
            for user in users:
                # Ne pas afficher le mot de passe
                tree.insert("", "end", values=(user[0], user[1], user[2], user[3], user[5]))

        def view_user_details():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Attention", "Veuillez sélectionner un utilisateur")
                return
            
            user_id = tree.item(selected[0])["values"][0]
            user = self.current_user.read_user_by_id(user_id)
            
            details_window = Toplevel(self.root)
            details_window.title("Détails Utilisateur")
            details_window.geometry("400x300")
            details_window.transient(self.root)
            
            Label(details_window, text="📋 Informations Utilisateur", 
                  font=("Arial", 14, "bold")).pack(pady=10)
            
            info_frame = Frame(details_window)
            info_frame.pack(pady=20, padx=20, fill=BOTH)
            
            Label(info_frame, text=f"ID: {user[0]}", font=("Arial", 10)).pack(anchor=W, pady=5)
            Label(info_frame, text=f"Username: {user[1]}", font=("Arial", 10)).pack(anchor=W, pady=5)
            Label(info_frame, text=f"Prénom: {user[2]}", font=("Arial", 10)).pack(anchor=W, pady=5)
            Label(info_frame, text=f"Nom: {user[3]}", font=("Arial", 10)).pack(anchor=W, pady=5)
            Label(info_frame, text=f"Rôle: {user[5]}", font=("Arial", 10, "bold"), 
                  fg="#e74c3c" if user[5] == "admin" else "#27ae60").pack(anchor=W, pady=5)
            
            Button(details_window, text="Fermer", command=details_window.destroy, 
                   width=15).pack(pady=10)

        def delete_user():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Attention", "Veuillez sélectionner un utilisateur")
                return
            
            user_id = tree.item(selected[0])["values"][0]
            
            if user_id == self.current_user.id:
                messagebox.showerror("Erreur", "Vous ne pouvez pas supprimer votre propre compte!")
                return
            
            if messagebox.askyesno("Confirmation", "Supprimer cet utilisateur définitivement?"):
                if self.current_user.delete_user_by_id(user_id):
                    messagebox.showinfo("Succès", "Utilisateur supprimé")
                    refresh_users()
                else:
                    messagebox.showerror("Erreur", "Échec de la suppression")

        action_frame = Frame(list_frame)
        action_frame.pack(pady=10)
        
        Button(action_frame, text="👁️ Voir Détails", command=view_user_details, 
               bg="#3498db", fg="white", width=15).pack(side=LEFT, padx=5)
        Button(action_frame, text="🗑️ Supprimer", command=delete_user, 
               bg="#e74c3c", fg="white", width=15).pack(side=LEFT, padx=5)
        Button(action_frame, text="🔄 Actualiser", command=refresh_users, 
               bg="#95a5a6", fg="white", width=15).pack(side=LEFT, padx=5)

        refresh_users()

    def create_orders_tab(self, notebook):
        """Onglet gestion des commandes"""
        orders_frame = Frame(notebook)
        notebook.add(orders_frame, text="📦 Commandes")

        # Statistiques
        stats_frame = LabelFrame(orders_frame, text="Statistiques", font=("Arial", 10, "bold"))
        stats_frame.pack(fill=X, pady=10, padx=10)
        
        stats_labels = {
            'total': Label(stats_frame, text="Total commandes: 0", font=("Arial", 10)),
            'pending': Label(stats_frame, text="En attente: 0", font=("Arial", 10), fg="#f39c12"),
            'completed': Label(stats_frame, text="Terminées: 0", font=("Arial", 10), fg="#27ae60"),
            'cancelled': Label(stats_frame, text="Annulées: 0", font=("Arial", 10), fg="#e74c3c")
        }
        
        for i, label in enumerate(stats_labels.values()):
            label.grid(row=0, column=i, padx=20, pady=10)

        # Liste des commandes
        list_frame = LabelFrame(orders_frame, text="Liste des commandes", font=("Arial", 10, "bold"))
        list_frame.pack(fill="both", expand=True, pady=10, padx=10)

        tree_frame = Frame(list_frame)
        tree_frame.pack(fill="both", expand=True, pady=5)

        scrollbar = Scrollbar(tree_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        tree = ttk.Treeview(tree_frame, columns=("ID", "Utilisateur", "Livre", "Qté", "Total", "Date", "Statut"), 
                           show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        for col in ("ID", "Utilisateur", "Livre", "Qté", "Total", "Date", "Statut"):
            tree.heading(col, text=col)
        
        tree.column("ID", width=50)
        tree.column("Utilisateur", width=120)
        tree.column("Livre", width=180)
        tree.column("Qté", width=60)
        tree.column("Total", width=100)
        tree.column("Date", width=140)
        tree.column("Statut", width=100)
        
        tree.pack(fill="both", expand=True)

        def refresh_orders():
            tree.delete(*tree.get_children())
            orders = Command.read_commands()
            
            stats = {'total': 0, 'pending': 0, 'completed': 0, 'cancelled': 0}
            
            for order in orders:
                stats['total'] += 1
                status = order[6]
                if status == "En attente":
                    stats['pending'] += 1
                elif status == "Terminée":
                    stats['completed'] += 1
                elif status == "Annulée":
                    stats['cancelled'] += 1
                
                tree.insert("", "end", values=(order[0], order[9], order[7], order[3], 
                                              f"{order[4]:.2f} DH", order[5], order[6]))
            
            # Mettre à jour les statistiques
            stats_labels['total'].config(text=f"Total commandes: {stats['total']}")
            stats_labels['pending'].config(text=f"En attente: {stats['pending']}")
            stats_labels['completed'].config(text=f"Terminées: {stats['completed']}")
            stats_labels['cancelled'].config(text=f"Annulées: {stats['cancelled']}")

        def change_status():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Attention", "Veuillez sélectionner une commande")
                return
            
            order_id = tree.item(selected[0])["values"][0]
            current_status = tree.item(selected[0])["values"][6]
            
            status_window = Toplevel(self.root)
            status_window.title("Changer le statut")
            status_window.geometry("350x300")
            status_window.transient(self.root)
            status_window.grab_set()
            
            Label(status_window, text="Nouveau statut:", font=("Arial", 11, "bold")).pack(pady=15)
            
            status_var = StringVar(value=current_status)
            
            radio_frame = Frame(status_window)
            radio_frame.pack(pady=10)
            
            for status in ["En attente", "En cours", "Terminée", "Annulée"]:
                Radiobutton(radio_frame, text=status, variable=status_var, 
                           value=status, font=("Arial", 10)).pack(anchor=W, padx=50, pady=5)
            
            def confirm_change():
                if Command.update_command_status(order_id, status_var.get()):
                    messagebox.showinfo("Succès", "Statut mis à jour")
                    status_window.destroy()
                    refresh_orders()
                else:
                    messagebox.showerror("Erreur", "Échec de la mise à jour")
            
            # Boutons
            btn_frame = Frame(status_window)
            btn_frame.pack(pady=25)
            
            Button(btn_frame, text="✓ Confirmer", command=confirm_change, 
                   bg="#27ae60", fg="white", width=15, font=("Arial", 10, "bold"),
                   cursor="hand2").pack(pady=5)
            Button(btn_frame, text="✗ Annuler", command=status_window.destroy, 
                   bg="#e74c3c", fg="white", width=15, font=("Arial", 9),
                   cursor="hand2").pack(pady=5)

        action_frame = Frame(list_frame)
        action_frame.pack(pady=10)
        
        Button(action_frame, text="📝 Changer Statut", command=change_status, 
               bg="#f39c12", fg="white", width=15).pack(side=LEFT, padx=5)
        Button(action_frame, text="🔄 Actualiser", command=refresh_orders, 
               bg="#95a5a6", fg="white", width=15).pack(side=LEFT, padx=5)

        refresh_orders()

    def create_stats_tab(self, notebook):
        """Onglet statistiques et stock"""
        stats_frame = Frame(notebook)
        notebook.add(stats_frame, text="📊 Statistiques")

        # Statistiques générales
        general_frame = LabelFrame(stats_frame, text="Statistiques Générales", 
                                   font=("Arial", 11, "bold"))
        general_frame.pack(fill=X, pady=10, padx=10)

        def refresh_stats():
            total_books, total_quantity = Stock.get_total_books()
            total_value = Stock.get_total_value()
            
            total_books = total_books if total_books else 0
            total_quantity = total_quantity if total_quantity else 0
            
            Label(general_frame, text=f"📚 Nombre de titres différents: {total_books}", 
                  font=("Arial", 11)).grid(row=0, column=0, padx=20, pady=10, sticky=W)
            Label(general_frame, text=f"📦 Quantité totale en stock: {total_quantity}", 
                  font=("Arial", 11)).grid(row=1, column=0, padx=20, pady=10, sticky=W)
            Label(general_frame, text=f"💰 Valeur totale du stock: {total_value:.2f} DH", 
                  font=("Arial", 11, "bold"), fg="#27ae60").grid(row=2, column=0, padx=20, pady=10, sticky=W)

        refresh_stats()

        # Stock faible
        low_stock_frame = LabelFrame(stats_frame, text="⚠️ Alertes Stock Faible", 
                                     font=("Arial", 11, "bold"))
        low_stock_frame.pack(fill=BOTH, expand=True, pady=10, padx=10)

        tree_frame = Frame(low_stock_frame)
        tree_frame.pack(fill="both", expand=True, pady=5)

        tree = ttk.Treeview(tree_frame, columns=("ID", "Titre", "Auteur", "Stock", "Prix"), 
                           show="headings", height=8)
        
        for col in ("ID", "Titre", "Auteur", "Stock", "Prix"):
            tree.heading(col, text=col)
        
        tree.column("ID", width=50)
        tree.column("Titre", width=250)
        tree.column("Auteur", width=200)
        tree.column("Stock", width=80)
        tree.column("Prix", width=100)
        
        tree.pack(fill="both", expand=True)

        def refresh_low_stock():
            tree.delete(*tree.get_children())
            low_stock_books = Stock.get_low_stock_books(threshold=5)
            
            for book in low_stock_books:
                tree.insert("", "end", values=(book[0], book[1], book[2], book[4], 
                                              f"{book[5]:.2f} DH"))
            
            tree.tag_configure("critical", background="#ffcccc")

        # Historique du stock
        history_frame = LabelFrame(stats_frame, text="📜 Historique des Mouvements", 
                                   font=("Arial", 11, "bold"))
        history_frame.pack(fill=BOTH, expand=True, pady=10, padx=10)

        history_tree_frame = Frame(history_frame)
        history_tree_frame.pack(fill="both", expand=True, pady=5)

        history_tree = ttk.Treeview(history_tree_frame, 
                                   columns=("ID", "Livre", "Action", "Qté", "Date", "Utilisateur"), 
                                   show="headings", height=6)
        
        for col in ("ID", "Livre", "Action", "Qté", "Date", "Utilisateur"):
            history_tree.heading(col, text=col)
        
        history_tree.column("ID", width=50)
        history_tree.column("Livre", width=200)
        history_tree.column("Action", width=150)
        history_tree.column("Qté", width=80)
        history_tree.column("Date", width=140)
        history_tree.column("Utilisateur", width=120)
        
        history_tree.pack(fill="both", expand=True)

        def refresh_history():
            history_tree.delete(*history_tree.get_children())
            history = self.current_user.get_stock_history()
            
            for entry in history:
                # Format: id, book_id, action, quantity, date, user_id, bookname, username
                history_tree.insert("", "end", values=(entry[0], entry[6], entry[2], 
                                                      entry[3], entry[4], entry[7] or "Système"))

        action_frame = Frame(stats_frame)
        action_frame.pack(pady=10)
        
        Button(action_frame, text="🔄 Actualiser Tout", 
               command=lambda: [refresh_stats(), refresh_low_stock(), refresh_history()], 
               bg="#3498db", fg="white", width=20, font=("Arial", 10, "bold")).pack()

        refresh_low_stock()
        refresh_history()

# ============= PARTIE EXÉCUTION =============
if __name__ == '__main__':
    init_db()
    root = Tk()
    app = MultiInterfaceApp(root)
    root.mainloop()