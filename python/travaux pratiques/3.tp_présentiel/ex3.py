import time
import functools

# 5. Le Décorateur
def moniteur_performance(fonction):
    @functools.wraps(fonction)
    def enveloppe(*args, **kwargs):
        debut = time.time()
        resultat = fonction(*args, **kwargs)
        fin = time.time()
        duree = fin - debut
        nb_args = len(args) + len(kwargs)
        print(f"--- [LOG] Temps: {duree:.6f}s | Params reçus: {nb_args} ---")
        return resultat
    return enveloppe

@moniteur_performance
def analyser(*nums, arrondi=False, **options):
    if not nums:
        raise ValueError("Erreur : Aucun nombre n'a été fourni en entrée.")
    
    liste_nums = list(nums)
    if options.get('strict_positive', False):
        for n in liste_nums:
            if n <= 0:
                raise ValueError(f"Erreur : Le nombre {n} n'est pas strictement positif.")
            
    if options.get('unique', False):
        liste_nums = list(set(liste_nums))
        
    if 'func' in options and callable(options['func']):
        fonction_perso = options['func']
        liste_nums = [fonction_perso(x) for x in liste_nums]
    resultat = liste_nums  
    
    if options.get('somme', False):
        resultat = sum(liste_nums)
        
    elif options.get('moyenne', False):
        resultat = sum(liste_nums) / len(liste_nums)
        
    elif options.get('tri', False):
        inverse = options.get('reverse', False)
        resultat = sorted(liste_nums, reverse=inverse)
        
    elif options.get('max', False):
        resultat = max(liste_nums)
        
    elif options.get('min', False):
        resultat = min(liste_nums)

    if arrondi and isinstance(resultat, (int, float)):
        try:
            resultat = round(resultat)
        except TypeError:
            pass

    return resultat

print("--- Test 1 : Somme ---")
res = analyser(10, 20, 30, somme=True)
print(f"Résultat : {res}\n")

print("--- Test 2 : Moyenne avec doublons et arrondi ---")
res = analyser(10, 10, 20, 5, moyenne=True, unique=True, arrondi=True)
print(f"Résultat : {res}\n")

print("--- Test 3 : Exception strict_positive ---")
try:
    analyser(10, -5, 20, strict_positive=True)
except ValueError as e:
    print(f"Exception attrapée : {e}\n")

print("--- Test 4 : Lambda (carré) + Tri ---")
res = analyser(3, 1, 4, 2, tri=True, func=lambda x: x**2)
print(f"Résultat : {res}\n")

print("--- Test 5 : Liste vide ---")
try:
    analyser()
except ValueError as e:
    print(f"Exception attrapée : {e}\n")