import math

# ==========================================
# 1. LECTURE ET AFFICHAGE
# ==========================================
def charger_donnees(chemin_fichier):
    with open(chemin_fichier, 'r', encoding='utf-8') as f:
        mots = f.read().split()
    valeurs = [int(m) for m in mots if m.lstrip('-').isdigit()]
    
    n, m = valeurs[0], valeurs[1]
    couts, provisions = [], []
    index = 2
    for _ in range(n):
        couts.append(valeurs[index : index + m])
        index += m
        provisions.append(valeurs[index])
        index += 1
    commandes = valeurs[index : index + m]
    return n, m, couts, provisions, commandes

def afficher_matrice(matrice, titres_lignes, titres_colonnes, nom=""):
    print(f"\n--- {nom} ---")
    en_tete = " " * 8 + "".join([f"| {titres_colonnes[j]:<5} " for j in range(len(titres_colonnes))])
    print(en_tete)
    print("-" * len(en_tete))
    for i in range(len(matrice)):
        ligne = f"{titres_lignes[i]:<7} " + "".join([f"| {matrice[i][j]:>5} " for j in range(len(matrice[i]))])
        print(ligne)
    print("\n")

def calculer_cout_total(couts, proposition):
    return sum(couts[i][j] * proposition[i][j] for i in range(len(couts)) for j in range(len(couts[0])))

# ==========================================
# 2. PROPOSITIONS INITIALES
# ==========================================
def algo_nord_ouest(provisions, commandes):
    n, m = len(provisions), len(commandes)
    prop = [[0] * m for _ in range(n)]
    prov, cmd = provisions.copy(), commandes.copy()
    i, j = 0, 0
    while i < n and j < m:
        flux = min(prov[i], cmd[j])
        prop[i][j] = flux
        prov[i] -= flux
        cmd[j] -= flux
        if prov[i] == 0: i += 1
        if j < m and cmd[j] == 0: j += 1
    return prop

def penalite(liste):
    valeurs = sorted([v for v in liste if v is not None])
    if len(valeurs) >= 2: return valeurs[1] - valeurs[0]
    elif len(valeurs) == 1: return valeurs[0]
    return -1

def algo_balas_hammer(couts, provisions, commandes):
    n, m = len(provisions), len(commandes)
    prop = [[0] * m for _ in range(n)]
    prov, cmd = provisions.copy(), commandes.copy()
    couts_actifs = [[couts[i][j] for j in range(m)] for i in range(n)]
    
    while sum(prov) > 0 and sum(cmd) > 0:
        pen_lignes = [penalite(ligne) if prov[i] > 0 else -1 for i, ligne in enumerate(couts_actifs)]
        pen_cols = [penalite([couts_actifs[i][j] for i in range(n)]) if cmd[j] > 0 else -1 for j in range(m)]
        
        max_pen_l = max(pen_lignes)
        max_pen_c = max(pen_cols)
        
        if max_pen_l >= max_pen_c:
            i = pen_lignes.index(max_pen_l)
            j = min((couts_actifs[i][k], k) for k in range(m) if couts_actifs[i][k] is not None)[1]
        else:
            j = pen_cols.index(max_pen_c)
            i = min((couts_actifs[k][j], k) for k in range(n) if couts_actifs[k][j] is not None)[1]
            
        flux = min(prov[i], cmd[j])
        prop[i][j] = flux
        prov[i] -= flux
        cmd[j] -= flux
        
        if prov[i] == 0:
            for k in range(m): couts_actifs[i][k] = None
        elif cmd[j] == 0:
            for k in range(n): couts_actifs[k][j] = None
            
    return prop

# ==========================================
# 3. MARCHE-PIED (STEPPING STONE)
# ==========================================
def calculer_potentiels_et_marginaux(couts, prop):
    n, m = len(couts), len(couts[0])
    u, v = [None]*n, [None]*m
    u[0] = 0 # Fixation arbitraire du premier potentiel
    
    # Calcul des potentiels (Ui + Vj = Cij sur les cases occupées)
    modifie = True
    while modifie:
        modifie = False
        for i in range(n):
            for j in range(m):
                if prop[i][j] > 0:
                    if u[i] is not None and v[j] is None:
                        v[j] = couts[i][j] - u[i]
                        modifie = True
                    elif v[j] is not None and u[i] is None:
                        u[i] = couts[i][j] - v[j]
                        modifie = True
    
    # Remplacer les None restants par 0 (cas de graphe non connexe / dégénéré simple)
    u = [0 if x is None else x for x in u]
    v = [0 if x is None else x for x in v]

    # Calcul des coûts marginaux (Cij - Ui - Vj sur les cases vides)
    marginaux = [[0] * m for _ in range(n)]
    min_marg, case_ameliorante = 0, None
    
    for i in range(n):
        for j in range(m):
            if prop[i][j] == 0:
                marg = couts[i][j] - (u[i] + v[j])
                marginaux[i][j] = marg
                if marg < min_marg:
                    min_marg = marg
                    case_ameliorante = (i, j)
                    
    return u, v, marginaux, case_ameliorante

def trouver_cycle(prop, depart):
    n, m = len(prop), len(prop[0])
    cases_occupees = [(i, j) for i in range(n) for j in range(m) if prop[i][j] > 0]
    cases_occupees.append(depart)
    
    # Parcours DFS pour trouver un cycle alterné
    def dfs(noeud_actuel, chemin, direction_prec):
        if len(chemin) > 3 and noeud_actuel == depart:
            return chemin
        
        for voisin in cases_occupees:
            if voisin == noeud_actuel or (voisin in chemin and voisin != depart):
                continue
            
            meme_ligne = (voisin[0] == noeud_actuel[0])
            meme_colonne = (voisin[1] == noeud_actuel[1])
            
            if meme_ligne and direction_prec != 'H':
                res = dfs(voisin, chemin + [voisin], 'H')
                if res: return res
            elif meme_colonne and direction_prec != 'V':
                res = dfs(voisin, chemin + [voisin], 'V')
                if res: return res
        return None

    cycle = dfs(depart, [depart], None)
    return cycle[:-1] if cycle else None

def ameliorer_proposition(prop, cycle):
    # Les cases aux indices impairs dans le cycle perdent du flux, les pairs en gagnent
    cases_negatives = [cycle[i] for i in range(1, len(cycle), 2)]
    delta = min(prop[i][j] for i, j in cases_negatives)
    
    for k, (i, j) in enumerate(cycle):
        if k % 2 == 0:
            prop[i][j] += delta
        else:
            prop[i][j] -= delta
            
    return prop, delta