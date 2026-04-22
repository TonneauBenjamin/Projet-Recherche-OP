import math

# ==========================================
# 1. LECTURE ET AFFICHAGE
# ==========================================

def charger_donnees(chemin_fichier):
    """Lit un fichier au format :
       n m
       c11 ... c1m p1
       ...
       cn1 ... cnm pn
       d1 ... dm
    """
    with open(chemin_fichier, 'r', encoding='utf-8') as f:
        contenu = f.read()

    mots = contenu.replace(',', ' ').split()
    valeurs = [int(m) for m in mots if m.lstrip('-').isdigit()]

    n, m = valeurs[0], valeurs[1]
    couts, provisions = [], []
    index = 2
    for _ in range(n):
        couts.append(valeurs[index: index + m])
        index += m
        provisions.append(valeurs[index])
        index += 1
    commandes = valeurs[index: index + m]
    return n, m, couts, provisions, commandes


def afficher_matrice(matrice, titres_lignes, titres_colonnes, nom=""):
    """Affiche une matrice avec colonnes a largeur fixe."""
    W = 8   # largeur colonne
    L = 10  # largeur label ligne

    print(f"\n--- {nom} ---")
    en_tete = " " * L + "".join(f"{c:>{W}}" for c in titres_colonnes)
    print(en_tete)
    print("-" * len(en_tete))
    for i, ligne in enumerate(matrice):
        row = f"{titres_lignes[i]:<{L}}" + "".join(f"{ligne[j]:>{W}}" for j in range(len(ligne)))
        print(row)
    print()


def calculer_cout_total(couts, proposition):
    return sum(
        couts[i][j] * proposition[i][j]
        for i in range(len(couts))
        for j in range(len(couts[0]))
    )


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
        if prov[i] == 0 and cmd[j] == 0:
            i += 1
            j += 1
        elif prov[i] == 0:
            i += 1
        else:
            j += 1
    return prop


def penalite(liste):
    """Ecart entre les deux plus petits couts actifs d'une ligne/colonne."""
    valeurs = sorted(v for v in liste if v is not None)
    if len(valeurs) >= 2:
        return valeurs[1] - valeurs[0]
    if len(valeurs) == 1:
        return valeurs[0]
    return -1


def algo_balas_hammer(couts, provisions, commandes):
    n, m = len(provisions), len(commandes)
    prop = [[0] * m for _ in range(n)]
    prov, cmd = provisions.copy(), commandes.copy()
    actif = [[couts[i][j] for j in range(m)] for i in range(n)]

    etape = 1
    while sum(prov) > 0 and sum(cmd) > 0:
        pen_l = [penalite(actif[i]) if prov[i] > 0 else -1 for i in range(n)]
        pen_c = [penalite([actif[i][j] for i in range(n)]) if cmd[j] > 0 else -1 for j in range(m)]

        max_pl = max(pen_l)
        max_pc = max(pen_c)

        print(f"\n  Etape {etape}:")
        print(f"    Penalites lignes   : {pen_l}   -> max = {max_pl} (ligne {pen_l.index(max_pl) + 1})")
        print(f"    Penalites colonnes : {pen_c}  -> max = {max_pc} (colonne {pen_c.index(max_pc) + 1})")

        if max_pl >= max_pc:
            i = pen_l.index(max_pl)
            valides = [(actif[i][k], k) for k in range(m) if actif[i][k] is not None and cmd[k] > 0]
            _, j = min(valides)
            print(f"    -> Choisir ligne {i + 1}, cout min = {actif[i][j]} a ({i + 1},{j + 1})")
        else:
            j = pen_c.index(max_pc)
            valides = [(actif[k][j], k) for k in range(n) if actif[k][j] is not None and prov[k] > 0]
            _, i = min(valides)
            print(f"    -> Choisir colonne {j + 1}, cout min = {actif[i][j]} a ({i + 1},{j + 1})")

        flux = min(prov[i], cmd[j])
        prop[i][j] = flux
        prov[i] -= flux
        cmd[j] -= flux
        print(f"    -> Allouer {flux} a ({i + 1},{j + 1})")

        if prov[i] == 0:
            for k in range(m):
                actif[i][k] = None
        if cmd[j] == 0:
            for k in range(n):
                actif[k][j] = None

        etape += 1

    return prop


# ==========================================
# 3. MARCHE-PIED (STEPPING STONE)
# ==========================================

def _union_find(taille):
    parent = list(range(taille))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[px] = py

    def meme(x, y):
        return find(x) == find(y)

    return union, meme


def calculer_potentiels_et_marginaux(couts, prop):
    """Retourne (u, v, marginaux, case_ameliorante, base).

    base est l'ensemble des cases (i,j) formant la base de potentiels
    (cases > 0 + cases fictives ajoutees pour gerer la degenerescence).
    """
    n, m = len(couts), len(couts[0])

    base = set((i, j) for i in range(n) for j in range(m) if prop[i][j] > 0)

    # Completer la base pour rendre le graphe bipartite connexe
    union, meme = _union_find(n + m)
    for (i, j) in base:
        union(i, n + j)

    for i in range(n):
        for j in range(m):
            if (i, j) not in base and not meme(i, n + j):
                base.add((i, j))
                union(i, n + j)

    # Calcul des potentiels : Ui + Vj = Cij sur chaque case de base
    u, v = [None] * n, [None] * m
    u[0] = 0

    changed = True
    while changed:
        changed = False
        for (i, j) in base:
            if u[i] is not None and v[j] is None:
                v[j] = couts[i][j] - u[i]
                changed = True
            elif v[j] is not None and u[i] is None:
                u[i] = couts[i][j] - v[j]
                changed = True

    u = [0 if x is None else x for x in u]
    v = [0 if x is None else x for x in v]

    # Couts marginaux sur les cases hors base
    marginaux = [[0] * m for _ in range(n)]
    min_marg, case_amel = 0, None

    for i in range(n):
        for j in range(m):
            if (i, j) not in base:
                marg = couts[i][j] - u[i] - v[j]
                marginaux[i][j] = marg
                if marg < min_marg:
                    min_marg = marg
                    case_amel = (i, j)

    return u, v, marginaux, case_amel, base


def trouver_cycle(base, depart, n, m):
    """DFS alterne ligne/colonne depuis `depart` pour trouver un cycle elementaire.

    base    : ensemble des cases de base (incluant les eventuelles cases fictives).
    depart  : case entrante (hors base).
    Retourne la liste ordonnee des cases du cycle, ou None si introuvable.
    """
    bases = list(base)

    def dfs(chemin, visite, next_dir):
        curr = chemin[-1]

        # Tentative de fermeture du cycle vers depart
        if len(chemin) >= 4:
            if next_dir == 'H' and curr[0] == depart[0]:
                return chemin
            if next_dir == 'V' and curr[1] == depart[1]:
                return chemin

        if len(chemin) > 2 * (n + m):
            return None

        for node in bases:
            if node in visite:
                continue
            if next_dir == 'H' and node[0] == curr[0]:
                visite.add(node)
                res = dfs(chemin + [node], visite, 'V')
                if res:
                    return res
                visite.discard(node)
            elif next_dir == 'V' and node[1] == curr[1]:
                visite.add(node)
                res = dfs(chemin + [node], visite, 'H')
                if res:
                    return res
                visite.discard(node)
        return None

    # Premier mouvement horizontal (meme ligne que depart)
    for node in bases:
        if node[0] == depart[0]:
            res = dfs([depart, node], {node}, 'V')
            if res:
                return res

    # Premier mouvement vertical (meme colonne que depart)
    for node in bases:
        if node[1] == depart[1]:
            res = dfs([depart, node], {node}, 'H')
            if res:
                return res

    return None


def ameliorer_proposition(prop, cycle):
    """Deplace delta unites le long du cycle (+delta positions paires, -delta impaires)."""
    cases_neg = [cycle[k] for k in range(1, len(cycle), 2)]
    delta = min(prop[i][j] for i, j in cases_neg)

    for k, (i, j) in enumerate(cycle):
        if k % 2 == 0:
            prop[i][j] += delta
        else:
            prop[i][j] -= delta

    return prop, delta
