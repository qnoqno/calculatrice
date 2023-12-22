import tkinter as tk
from tkinter import ttk
from math import sqrt, log, log10

class Calculatrice(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Calculatrice")
        self.geometry("400x600")
        self.resizable(False, False)

        style = ttk.Style()
        style.configure('TButton', font=('Arial', 16), padding=5, width=3)

        self.creer_widgets()

    def creer_widgets(self):
        # afficher resultat
        self.affichage_resultat = tk.Entry(self, font=('Arial', 24), bd=5, insertwidth=4, justify='right')
        self.affichage_resultat.grid(row=0, column=0, columnspan=4, pady=(20, 10), sticky="nsew")

        # bouton de base d'une calculette
        boutons_standard = [
            ('%', 1, 0), ('CE', 1, 1), ('C', 1, 2), ('⌫', 1, 3),
            ('1/x', 2, 0), ('x²', 2, 1), ('√', 2, 2), ('/', 2, 3),
            ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('*', 3, 3),
            ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('-', 4, 3),
            ('1', 5, 0), ('2', 5, 1), ('3', 5, 2), ('+', 5, 3),
            ('+/-', 6, 0), ('0', 6, 1), ('.', 6, 2), ('=', 6, 3),
        ]

        for (texte, ligne, colonne) in boutons_standard:
            bouton = ttk.Button(self, text=texte, command=lambda t=texte: self.gerer_clic_bouton(t))
            bouton.grid(row=ligne, column=colonne, padx=5, pady=5, sticky="nsew")

        self.bouton_scientifique = ttk.Button(self, text="Sci", command=self.basculer_scientifique, style='Scientific.TButton')
        self.bouton_scientifique.grid(row=7, column=0, columnspan=4, pady=(20, 10), padx=5, sticky="nsew")

        self.mode_scientifique = False

        ttk.Style().configure('Scientific.TButton', font=('Arial', 16), padding=5, width=3)
        

    #PoUR chauqe nouveau bouton erreur + affichage 
    def gerer_clic_bouton(self, valeur):
        if valeur == '=':
            try:
                resultat = eval(self.affichage_resultat.get())
                self.affichage_resultat.delete(0, tk.END)
                self.affichage_resultat.insert(tk.END, str(resultat))
            except:
                self.affichage_resultat.delete(0, tk.END)
                self.affichage_resultat.insert(tk.END, "Erreur")
        elif valeur in {'C', 'CE'}:
            self.affichage_resultat.delete(0, tk.END)
        elif valeur == '⌫':
            texte_actuel = self.affichage_resultat.get()
            self.affichage_resultat.delete(0, tk.END)
            self.affichage_resultat.insert(tk.END, texte_actuel[:-1])
        elif valeur == '+/-':
            texte_actuel = self.affichage_resultat.get()
            if texte_actuel and texte_actuel[0] == '-':
                self.affichage_resultat.delete(0)
            else:
                self.affichage_resultat.insert(0, '-')
        elif valeur == 'x²':
            try:
                resultat = eval(self.affichage_resultat.get()) ** 2
                self.affichage_resultat.delete(0, tk.END)
                self.affichage_resultat.insert(tk.END, str(resultat))
            except:
                self.affichage_resultat.delete(0, tk.END)
                self.affichage_resultat.insert(tk.END, "Erreur")
        elif valeur == '√':
            try:
                resultat = sqrt(eval(self.affichage_resultat.get()))
                self.affichage_resultat.delete(0, tk.END)
                self.affichage_resultat.insert(tk.END, str(resultat))
            except:
                self.affichage_resultat.delete(0, tk.END)
                self.affichage_resultat.insert(tk.END, "Erreur")
        elif valeur == '1/x':
            try:
                resultat = 1 / eval(self.affichage_resultat.get())
                self.affichage_resultat.delete(0, tk.END)
                self.affichage_resultat.insert(tk.END, str(resultat))
            except:
                # erreur
                self.affichage_resultat.delete(0, tk.END)
                self.affichage_resultat.insert(tk.END, "Erreur")
        elif valeur in {'(', ')'}:
            # ajout parentehse
            texte_actuel = self.affichage_resultat.get()
            self.affichage_resultat.delete(0, tk.END)
            self.affichage_resultat.insert(tk.END, texte_actuel + valeur)
        elif valeur in {'xy', '10^x', 'log', 'ln'}:
            # ajout valeur
            texte_actuel = self.affichage_resultat.get()
            self.affichage_resultat.delete(0, tk.END)
            self.affichage_resultat.insert(tk.END, texte_actuel + valeur)
        else:
            texte_actuel = self.affichage_resultat.get()
            self.affichage_resultat.delete(0, tk.END)
            self.affichage_resultat.insert(tk.END, texte_actuel + valeur)

    def basculer_scientifique(self):
        # changer le mode 
        if self.mode_scientifique:
            self.mode_scientifique = False
        else:
            # parenthese test
            self.boutons_parentheses = [
                {'texte': '(', 'ligne': 7, 'colonne': 0, 'commande': lambda t='(': self.gerer_clic_bouton(t)},
                {'texte': ')', 'ligne': 7, 'colonne': 1, 'commande': lambda t=')': self.gerer_clic_bouton(t)},
            ]

            for bouton_info in self.boutons_parentheses:
                bouton = ttk.Button(self, text=bouton_info['texte'], command=bouton_info['commande'])
                bouton.grid(row=bouton_info['ligne'], column=bouton_info['colonne'], padx=5, pady=5, sticky="nsew")

            # bouton scientifique en plus des parentheses
            self.boutons_scientifiques = [
                {'texte': 'xy', 'ligne': 8, 'colonne': 0, 'commande': lambda t='xy': self.gerer_clic_bouton(t)},
                {'texte': '10^x', 'ligne': 8, 'colonne': 1, 'commande': lambda t='10^x': self.gerer_clic_bouton(t)},
                {'texte': 'log', 'ligne': 8, 'colonne': 2, 'commande': lambda t='log': self.gerer_clic_bouton(t)},
                {'texte': 'ln','ligne': 8, 'colonne': 3, 'commande': lambda t='ln': self.gerer_clic_bouton(t)},
            ]

            for bouton_info in self.boutons_scientifiques:
                bouton = ttk.Button(self, text=bouton_info['texte'], command=bouton_info['commande'])
                bouton.grid(row=bouton_info['ligne'], column=bouton_info['colonne'], padx=5, pady=5, sticky="nsew")

            self.mode_scientifique = True


# execute code
calculatrice = Calculatrice()


calculatrice.mainloop()

