#!/usr/bin/env python3
"""
PARTIE 3 - ETUDE DE COMPLEXITE DU PROJET RECHERCHE OPERATIONNELLE

Mesure et analyse de la complexite des algorithmes de transport:
- Algorithme Nord-Ouest (theta_NO)
- Algorithme Balas-Hammer (theta_BH)
- Methode du marche-pied avec potentiel (tNO, tBH)

Utilisation:
    python3 complexite.py           # Execution de l'etude de complexite
"""

import time
import random
import json
import sys
import os
import algorithmes as algo

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# ==========================================
# GENERATION DE PROBLÈMES ALEATOIRES
# ==========================================

def generer_probleme_aleatoire(n):
    """Genere un probleme de transport aleatoire de taille n x n.
    
    Selon les specifications du projet:
    1. Generer une matrice de coûts avec des valeurs aleatoires entre 1 et 100
    2. Generer une matrice temp avec des valeurs aleatoires entre 1 et 100
    3. Pi = somme des colonnes de temp pour la ligne i
    4. Cj = somme des lignes de temp pour la colonne j
    """
    couts = [[random.randint(1, 100) for _ in range(n)] for _ in range(n)]
    temp = [[random.randint(1, 100) for _ in range(n)] for _ in range(n)]
    
    provisions = [sum(temp[i][j] for j in range(n)) for i in range(n)]
    commandes = [sum(temp[i][j] for i in range(n)) for j in range(n)]
    
    return couts, provisions, commandes


# ==========================================
# MESURE DES TEMPS D'EXECUTION
# ==========================================

def mesurer_nord_ouest(provisions, commandes):
    """Mesure le temps d'execution de l'algorithme Nord-Ouest."""
    debut = time.perf_counter()
    prop = algo.algo_nord_ouest(provisions, commandes)
    fin = time.perf_counter()
    return fin - debut, prop


def mesurer_balas_hammer(couts, provisions, commandes):
    """Mesure le temps d'execution de l'algorithme Balas-Hammer."""
    debut = time.perf_counter()
    prop = algo.algo_balas_hammer(couts, provisions, commandes, silencieux=True)
    fin = time.perf_counter()
    return fin - debut, prop


def mesurer_marche_pied(couts, prop_initiale):
    """Mesure le temps d'execution du marche-pied complet avec potentiel."""
    import copy
    prop = copy.deepcopy(prop_initiale)
    n = len(couts)
    m = len(couts[0])
    debut = time.perf_counter()
    try:
        algo.marche_pied_complet(couts, prop, n, m, afficher=False)
    except Exception:
        pass
    fin = time.perf_counter()
    return fin - debut


# ==========================================
# ETUDE DE COMPLEXITE
# ==========================================

def etude_complexite_complete():
    """Effectue l'etude complete de complexite selon les specifications du projet.
    
    Mesure pour chaque taille n:
    - theta_NO(n): temps de l'algorithme Nord-Ouest
    - theta_BH(n): temps de l'algorithme Balas-Hammer  
    - tNO(n): temps du marche-pied avec Nord-Ouest
    - tBH(n): temps du marche-pied avec Balas-Hammer
    """
    
    tailles_n = [10, 40, 100, 400, 1000, 4000, 10000]  
    iterations = 100 
     
    # Stockage des resultats
    resultats = {}
    
    print("="*70)
    print("ETUDE DE COMPLEXITE - PROBLÈMES DE TRANSPORT")
    print("="*70)
    print(f"Nombre d'iterations par taille: {iterations}")
    print(f"Tailles testees: {tailles_n}")
    print()
    
    for n in tailles_n:
        print(f"\n{'='*70}")
        print(f"TAILLE n = {n}")
        print(f"{'='*70}")
        
        temps_no_list = []
        temps_bh_list = []
        temps_marche_no_list = []
        temps_marche_bh_list = []
        
        for iter_num in range(iterations):
            # Generer un probleme aleatoire
            couts, provisions, commandes = generer_probleme_aleatoire(n)
            
            # 1. Mesurer Nord-Ouest
            t_no, prop_no = mesurer_nord_ouest(provisions, commandes)
            temps_no_list.append(t_no)
            
            # 2. Mesurer Balas-Hammer
            t_bh, prop_bh = mesurer_balas_hammer(couts, provisions, commandes)
            temps_bh_list.append(t_bh)
            
            # 3. Mesurer marche-pied avec Nord-Ouest
            t_marche_no = mesurer_marche_pied(couts, prop_no)
            temps_marche_no_list.append(t_marche_no)
            
            # 4. Mesurer marche-pied avec Balas-Hammer
            t_marche_bh = mesurer_marche_pied(couts, prop_bh)
            temps_marche_bh_list.append(t_marche_bh)
            
            if (iter_num + 1) % 10 == 0:
                print(f"  Iteration {iter_num + 1}/{iterations} completee")
        
        # Calculer les statistiques
        resultats[n] = {
            'theta_no': temps_no_list,
            'theta_bh': temps_bh_list,
            't_marche_no': temps_marche_no_list,
            't_marche_bh': temps_marche_bh_list,
        }
        
        # Afficher les resultats pour cette taille
        max_no = max(temps_no_list)
        max_bh = max(temps_bh_list)
        max_marche_no = max(temps_marche_no_list)
        max_marche_bh = max(temps_marche_bh_list)
        
        print(f"\nResultats pour n = {n}:")
        print(f"  theta_NO(n)  - Pire cas: {max_no:.8f}s")
        print(f"  theta_BH(n)  - Pire cas: {max_bh:.8f}s")
        print(f"  tNO(n)  - Pire cas: {max_marche_no:.8f}s")
        print(f"  tBH(n)  - Pire cas: {max_marche_bh:.8f}s")
        print(f"  Total NO - Pire cas: {max_no + max_marche_no:.8f}s")
        print(f"  Total BH - Pire cas: {max_bh + max_marche_bh:.8f}s")
    
    return resultats, tailles_n


# ==========================================
# TRAÇAGE DES RESULTATS
# ==========================================

def tracer_nuages_de_points(resultats, tailles_n):
    """Trace les nuages de points avec les 100 valeurs pour chaque n."""
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Etude de Complexite - Nuages de Points', fontsize=16, fontweight='bold')
    
    # 1. theta_NO(n)
    ax = axes[0, 0]
    for n in tailles_n:
        x = [n] * len(resultats[n]['theta_no'])
        y = resultats[n]['theta_no']
        ax.scatter(x, y, alpha=0.6, s=30)
    ax.set_xlabel('Taille n')
    ax.set_ylabel('Temps (secondes)')
    ax.set_title('theta_NO(n) - Nord-Ouest')
    ax.grid(True, alpha=0.3)
    
    # 2. theta_BH(n)
    ax = axes[0, 1]
    for n in tailles_n:
        x = [n] * len(resultats[n]['theta_bh'])
        y = resultats[n]['theta_bh']
        ax.scatter(x, y, alpha=0.6, s=30, color='orange')
    ax.set_xlabel('Taille n')
    ax.set_ylabel('Temps (secondes)')
    ax.set_title('theta_BH(n) - Balas-Hammer')
    ax.grid(True, alpha=0.3)
    
    # 3. tNO(n)
    ax = axes[0, 2]
    for n in tailles_n:
        x = [n] * len(resultats[n]['t_marche_no'])
        y = resultats[n]['t_marche_no']
        ax.scatter(x, y, alpha=0.6, s=30, color='green')
    ax.set_xlabel('Taille n')
    ax.set_ylabel('Temps (secondes)')
    ax.set_title('tNO(n) - Marche-pied + Nord-Ouest')
    ax.grid(True, alpha=0.3)
    
    # 4. tBH(n)
    ax = axes[1, 0]
    for n in tailles_n:
        x = [n] * len(resultats[n]['t_marche_bh'])
        y = resultats[n]['t_marche_bh']
        ax.scatter(x, y, alpha=0.6, s=30, color='red')
    ax.set_xlabel('Taille n')
    ax.set_ylabel('Temps (secondes)')
    ax.set_title('tBH(n) - Marche-pied + Balas-Hammer')
    ax.grid(True, alpha=0.3)
    
    # 5. (theta_NO + tNO)(n)
    ax = axes[1, 1]
    for n in tailles_n:
        totaux = [resultats[n]['theta_no'][i] + resultats[n]['t_marche_no'][i] 
                  for i in range(len(resultats[n]['theta_no']))]
        x = [n] * len(totaux)
        ax.scatter(x, totaux, alpha=0.6, s=30, color='purple')
    ax.set_xlabel('Taille n')
    ax.set_ylabel('Temps (secondes)')
    ax.set_title('(theta_NO + tNO)(n) - Total Nord-Ouest')
    ax.grid(True, alpha=0.3)
    
    # 6. (theta_BH + tBH)(n)
    ax = axes[1, 2]
    for n in tailles_n:
        totaux = [resultats[n]['theta_bh'][i] + resultats[n]['t_marche_bh'][i] 
                  for i in range(len(resultats[n]['theta_bh']))]
        x = [n] * len(totaux)
        ax.scatter(x, totaux, alpha=0.6, s=30, color='brown')
    ax.set_xlabel('Taille n')
    ax.set_ylabel('Temps (secondes)')
    ax.set_title('(theta_BH + tBH)(n) - Total Balas-Hammer')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('complexite_nuages_points.png', dpi=300)
    print("\n[OK] Graphique sauvegarde: complexite_nuages_points.png")
    plt.show()


def tracer_pire_des_cas(resultats, tailles_n):
    """Trace l'enveloppe superieure (pire des cas) pour chaque algorithme."""
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    
    # Extraire les maxima pour chaque n
    maxima_no = [max(resultats[n]['theta_no']) for n in tailles_n]
    maxima_bh = [max(resultats[n]['theta_bh']) for n in tailles_n]
    maxima_marche_no = [max(resultats[n]['t_marche_no']) for n in tailles_n]
    maxima_marche_bh = [max(resultats[n]['t_marche_bh']) for n in tailles_n]
    maxima_total_no = [maxima_no[i] + maxima_marche_no[i] for i in range(len(tailles_n))]
    maxima_total_bh = [maxima_bh[i] + maxima_marche_bh[i] for i in range(len(tailles_n))]
    
    # Tracer les courbes
    ax.plot(tailles_n, maxima_no, 'o-', label='theta_NO(n)', linewidth=2, markersize=8)
    ax.plot(tailles_n, maxima_bh, 's-', label='theta_BH(n)', linewidth=2, markersize=8)
    ax.plot(tailles_n, maxima_marche_no, '^-', label='tNO(n)', linewidth=2, markersize=8)
    ax.plot(tailles_n, maxima_marche_bh, 'v-', label='tBH(n)', linewidth=2, markersize=8)
    ax.plot(tailles_n, maxima_total_no, 'D-', label='(theta_NO + tNO)(n)', linewidth=2, markersize=8)
    ax.plot(tailles_n, maxima_total_bh, 'x-', label='(theta_BH + tBH)(n)', linewidth=2, markersize=8)
    
    ax.set_xlabel('Taille n', fontsize=12)
    ax.set_ylabel('Temps (secondes)', fontsize=12)
    ax.set_title('Complexite dans le Pire des Cas', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('complexite_pire_des_cas.png', dpi=300)
    print("[OK] Graphique sauvegarde: complexite_pire_des_cas.png")
    plt.show()


def tracer_comparaison_ratios(resultats, tailles_n):
    """Trace le ratio (tNO + theta_NO) / (tBH + theta_BH) pour comparer les algorithmes."""
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    
    ratios = []
    for n in tailles_n:
        maxima_total_no = max(resultats[n]['theta_no']) + max(resultats[n]['t_marche_no'])
        maxima_total_bh = max(resultats[n]['theta_bh']) + max(resultats[n]['t_marche_bh'])
        ratio = maxima_total_no / maxima_total_bh if maxima_total_bh > 0 else 1
        ratios.append(ratio)
    
    colors = ['green' if r < 1 else 'red' for r in ratios]
    ax.bar(tailles_n, ratios, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
    ax.axhline(y=1, color='black', linestyle='--', linewidth=2, label='Equivalent')
    
    ax.set_xlabel('Taille n', fontsize=12)
    ax.set_ylabel('Ratio (theta_NO + tNO) / (theta_BH + tBH)', fontsize=12)
    ax.set_title('Comparaison des Algorithmes: Nord-Ouest vs Balas-Hammer', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Ajouter les valeurs sur les barres
    for i, (n, r) in enumerate(zip(tailles_n, ratios)):
        ax.text(n, r + 0.05, f'{r:.3f}', ha='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('complexite_comparaison_ratios.png', dpi=300)
    print("[OK] Graphique sauvegarde: complexite_comparaison_ratios.png")
    plt.show()


def identifier_complexite(tailles, temps_max):
    """Identifie le type de complexite base sur l'enveloppe superieure.
    
    Teste: O(log n), O(n), O(n log n), O(n²), O(n³), O(k^n)
    Retourne le type ayant le meilleur R²
    """
    types_complexite = {
        'O(log n)': lambda n: np.log(n),
        'O(n)': lambda n: n,
        'O(n log n)': lambda n: n * np.log(n),
        'O(n²)': lambda n: n ** 2,
        'O(n³)': lambda n: n ** 3,
    }
    
    meilleur_type = None
    meilleur_r2 = -np.inf
    
    for nom, func in types_complexite.items():
        # Ajuster les temps avec la fonction
        y_pred = np.array([func(n) for n in tailles])
        y_true = np.array(temps_max)
        
        # Normaliser pour comparer
        y_pred_norm = y_pred / np.max(y_pred)
        y_true_norm = y_true / np.max(y_true)
        
        # Calculer R²
        ss_res = np.sum((y_true_norm - y_pred_norm) ** 2)
        ss_tot = np.sum((y_true_norm - np.mean(y_true_norm)) ** 2)
        r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
        
        if r2 > meilleur_r2:
            meilleur_r2 = r2
            meilleur_type = nom
    
    return meilleur_type, meilleur_r2






# ==========================================
# PROGRAMME PRINCIPAL
# ==========================================

def afficher_usage():
    """Affiche le message d'aide."""
    print("""
ETUDE DE COMPLEXITE - PROBLÈMES DE TRANSPORT

Usage:
    python3 complexite.py              # Execution complete (graphiques)
    python3 complexite.py --help       # Affiche cette aide
    """)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg == '--help' or arg == '-h':
            afficher_usage()
            sys.exit(0)
        
        else:
            print(f"[ERREUR] Argument inconnu: {arg}")
            afficher_usage()
            sys.exit(1)
    
    # Execution par defaut: version complete avec graphiques
    print("\n" + "="*70)
    print("ANALYSE DE COMPLEXITE - PROBLÈMES DE TRANSPORT")
    print("="*70 + "\n")
    
    # Effectuer l'etude complete
    resultats, tailles_n = etude_complexite_complete()
    
    # Identifier les complexites
    print("\n" + "="*70)
    print("IDENTIFICATION DES COMPLEXITES")
    print("="*70)
    
    maxima_no = [max(resultats[n]['theta_no']) for n in tailles_n]
    maxima_bh = [max(resultats[n]['theta_bh']) for n in tailles_n]
    maxima_marche_no = [max(resultats[n]['t_marche_no']) for n in tailles_n]
    maxima_marche_bh = [max(resultats[n]['t_marche_bh']) for n in tailles_n]
    
    type_no, r2_no = identifier_complexite(tailles_n, maxima_no)
    type_bh, r2_bh = identifier_complexite(tailles_n, maxima_bh)
    type_marche_no, r2_marche_no = identifier_complexite(tailles_n, maxima_marche_no)
    type_marche_bh, r2_marche_bh = identifier_complexite(tailles_n, maxima_marche_bh)
    
    print(f"\ntheta_NO(n)  : {type_no} (R² = {r2_no:.4f})")
    print(f"theta_BH(n)  : {type_bh} (R² = {r2_bh:.4f})")
    print(f"tNO(n)  : {type_marche_no} (R² = {r2_marche_no:.4f})")
    print(f"tBH(n)  : {type_marche_bh} (R² = {r2_marche_bh:.4f})")
    
    # Tracer les resultats
    print("\n" + "="*70)
    print("GENERATION DES GRAPHIQUES")
    print("="*70)
    
    tracer_nuages_de_points(resultats, tailles_n)
    tracer_pire_des_cas(resultats, tailles_n)
    tracer_comparaison_ratios(resultats, tailles_n)
    
    # Sauvegarder les resultats en JSON
    donnees_export = {}
    for n in tailles_n:
        donnees_export[str(n)] = {
            'theta_no_max': max(resultats[n]['theta_no']),
            'theta_bh_max': max(resultats[n]['theta_bh']),
            't_marche_no_max': max(resultats[n]['t_marche_no']),
            't_marche_bh_max': max(resultats[n]['t_marche_bh']),
        }
    
    with open('resultats_complexite.json', 'w') as f:
        json.dump(donnees_export, f, indent=2)
    
    print("\n[OK] Resultats sauvegardes dans resultats_complexite.json")
    print("\n" + "="*70)
    print("ETUDE TERMINEE")
    print("="*70)
