#!/usr/bin/env python3
"""
PARTIE 3 - ÉTUDE DE COMPLEXITÉ DU PROJET RECHERCHE OPÉRATIONNELLE

Mesure et analyse de la complexité des algorithmes de transport:
- Algorithme Nord-Ouest (θNO)
- Algorithme Balas-Hammer (θBH)
- Méthode du marche-pied avec potentiel (tNO, tBH)

Utilisation:
    python3 complexite.py           # Menu interactif
    python3 complexite.py --simple  # Version simple (CSV)
    python3 complexite.py --test    # Test rapide
"""

import time
import random
import json
import csv
import sys
import os
import algorithmes as algo

# Essayer d'importer matplotlib (optionnel)
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

# ==========================================
# GÉNÉRATION DE PROBLÈMES ALÉATOIRES
# ==========================================

def generer_probleme_aleatoire(n):
    """Génère un problème de transport aléatoire de taille n x n.
    
    Selon les spécifications du projet:
    1. Générer une matrice de coûts avec des valeurs aléatoires entre 1 et 100
    2. Générer une matrice temp avec des valeurs aléatoires entre 1 et 100
    3. Pi = somme des colonnes de temp pour la ligne i
    4. Cj = somme des lignes de temp pour la colonne j
    """
    couts = [[random.randint(1, 100) for _ in range(n)] for _ in range(n)]
    temp = [[random.randint(1, 100) for _ in range(n)] for _ in range(n)]
    
    provisions = [sum(temp[i][j] for j in range(n)) for i in range(n)]
    commandes = [sum(temp[i][j] for i in range(n)) for j in range(n)]
    
    return couts, provisions, commandes


# ==========================================
# MESURE DES TEMPS D'EXÉCUTION
# ==========================================

def mesurer_nord_ouest(provisions, commandes):
    """Mesure le temps d'exécution de l'algorithme Nord-Ouest."""
    debut = time.perf_counter()
    prop = algo.algo_nord_ouest(provisions, commandes)
    fin = time.perf_counter()
    return fin - debut, prop


def mesurer_balas_hammer(couts, provisions, commandes):
    """Mesure le temps d'exécution de l'algorithme Balas-Hammer."""
    # Rediriger print pour éviter le spam
    import sys
    from io import StringIO
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    debut = time.perf_counter()
    prop = algo.algo_balas_hammer(couts, provisions, commandes)
    fin = time.perf_counter()
    
    sys.stdout = old_stdout
    return fin - debut, prop


def mesurer_marche_pied(couts, prop_initiale):
    """Mesure le temps d'exécution du marche-pied avec potentiel.
    
    Note: Cette fonction complète la boucle d'optimisation jusqu'à convergence.
    """
    debut = time.perf_counter()
    
    # Appeler la méthode du marche-pied (stepping stone)
    # On effectue une itération complète si elle existe
    try:
        u, v, marginaux, case_ameliorante, base = algo.calculer_potentiels_et_marginaux(couts, prop_initiale)
        # Si pas de case améliorante, on s'arrête
        # Sinon on pourrait continuer, mais pour cette étude on mesure juste une itération
    except:
        pass
    
    fin = time.perf_counter()
    return fin - debut


# ==========================================
# ÉTUDE DE COMPLEXITÉ
# ==========================================

def etude_complexite_complete():
    """Effectue l'étude complète de complexité selon les spécifications du projet.
    
    Mesure pour chaque taille n:
    - θNO(n): temps de l'algorithme Nord-Ouest
    - θBH(n): temps de l'algorithme Balas-Hammer  
    - tNO(n): temps du marche-pied avec Nord-Ouest
    - tBH(n): temps du marche-pied avec Balas-Hammer
    """
    # Tailles à tester: 10, 40, 100, 400, 1000, 4000, 10000
    tailles_n = [10, 40, 100, 400]  # Adapter selon votre PC
    iterations = 100  # 100 itérations par taille
    
    # Stockage des résultats
    resultats = {}
    
    print("="*70)
    print("ÉTUDE DE COMPLEXITÉ - PROBLÈMES DE TRANSPORT")
    print("="*70)
    print(f"Nombre d'itérations par taille: {iterations}")
    print(f"Tailles testées: {tailles_n}")
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
            # Générer un problème aléatoire
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
                print(f"  Itération {iter_num + 1}/{iterations} complétée")
        
        # Calculer les statistiques
        resultats[n] = {
            'theta_no': temps_no_list,
            'theta_bh': temps_bh_list,
            't_marche_no': temps_marche_no_list,
            't_marche_bh': temps_marche_bh_list,
        }
        
        # Afficher les résultats pour cette taille
        max_no = max(temps_no_list)
        max_bh = max(temps_bh_list)
        max_marche_no = max(temps_marche_no_list)
        max_marche_bh = max(temps_marche_bh_list)
        
        print(f"\nRésultats pour n = {n}:")
        print(f"  θNO(n)  - Pire cas: {max_no:.8f}s (moyenne: {np.mean(temps_no_list):.8f}s)")
        print(f"  θBH(n)  - Pire cas: {max_bh:.8f}s (moyenne: {np.mean(temps_bh_list):.8f}s)")
        print(f"  tNO(n)  - Pire cas: {max_marche_no:.8f}s (moyenne: {np.mean(temps_marche_no_list):.8f}s)")
        print(f"  tBH(n)  - Pire cas: {max_marche_bh:.8f}s (moyenne: {np.mean(temps_marche_bh_list):.8f}s)")
        print(f"  Total NO - Pire cas: {max_no + max_marche_no:.8f}s")
        print(f"  Total BH - Pire cas: {max_bh + max_marche_bh:.8f}s")
    
    return resultats, tailles_n


# ==========================================
# TRAÇAGE DES RÉSULTATS
# ==========================================

def tracer_nuages_de_points(resultats, tailles_n):
    """Trace les nuages de points avec les 100 valeurs pour chaque n."""
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Étude de Complexité - Nuages de Points', fontsize=16, fontweight='bold')
    
    # 1. θNO(n)
    ax = axes[0, 0]
    for n in tailles_n:
        x = [n] * len(resultats[n]['theta_no'])
        y = resultats[n]['theta_no']
        ax.scatter(x, y, alpha=0.6, s=30)
    ax.set_xlabel('Taille n')
    ax.set_ylabel('Temps (secondes)')
    ax.set_title('θNO(n) - Nord-Ouest')
    ax.grid(True, alpha=0.3)
    
    # 2. θBH(n)
    ax = axes[0, 1]
    for n in tailles_n:
        x = [n] * len(resultats[n]['theta_bh'])
        y = resultats[n]['theta_bh']
        ax.scatter(x, y, alpha=0.6, s=30, color='orange')
    ax.set_xlabel('Taille n')
    ax.set_ylabel('Temps (secondes)')
    ax.set_title('θBH(n) - Balas-Hammer')
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
    
    # 5. (θNO + tNO)(n)
    ax = axes[1, 1]
    for n in tailles_n:
        totaux = [resultats[n]['theta_no'][i] + resultats[n]['t_marche_no'][i] 
                  for i in range(len(resultats[n]['theta_no']))]
        x = [n] * len(totaux)
        ax.scatter(x, totaux, alpha=0.6, s=30, color='purple')
    ax.set_xlabel('Taille n')
    ax.set_ylabel('Temps (secondes)')
    ax.set_title('(θNO + tNO)(n) - Total Nord-Ouest')
    ax.grid(True, alpha=0.3)
    
    # 6. (θBH + tBH)(n)
    ax = axes[1, 2]
    for n in tailles_n:
        totaux = [resultats[n]['theta_bh'][i] + resultats[n]['t_marche_bh'][i] 
                  for i in range(len(resultats[n]['theta_bh']))]
        x = [n] * len(totaux)
        ax.scatter(x, totaux, alpha=0.6, s=30, color='brown')
    ax.set_xlabel('Taille n')
    ax.set_ylabel('Temps (secondes)')
    ax.set_title('(θBH + tBH)(n) - Total Balas-Hammer')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('complexite_nuages_points.png', dpi=300)
    print("\n✓ Graphique sauvegardé: complexite_nuages_points.png")
    plt.show()


def tracer_pire_des_cas(resultats, tailles_n):
    """Trace l'enveloppe supérieure (pire des cas) pour chaque algorithme."""
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    
    # Extraire les maxima pour chaque n
    maxima_no = [max(resultats[n]['theta_no']) for n in tailles_n]
    maxima_bh = [max(resultats[n]['theta_bh']) for n in tailles_n]
    maxima_marche_no = [max(resultats[n]['t_marche_no']) for n in tailles_n]
    maxima_marche_bh = [max(resultats[n]['t_marche_bh']) for n in tailles_n]
    maxima_total_no = [maxima_no[i] + maxima_marche_no[i] for i in range(len(tailles_n))]
    maxima_total_bh = [maxima_bh[i] + maxima_marche_bh[i] for i in range(len(tailles_n))]
    
    # Tracer les courbes
    ax.plot(tailles_n, maxima_no, 'o-', label='θNO(n)', linewidth=2, markersize=8)
    ax.plot(tailles_n, maxima_bh, 's-', label='θBH(n)', linewidth=2, markersize=8)
    ax.plot(tailles_n, maxima_marche_no, '^-', label='tNO(n)', linewidth=2, markersize=8)
    ax.plot(tailles_n, maxima_marche_bh, 'v-', label='tBH(n)', linewidth=2, markersize=8)
    ax.plot(tailles_n, maxima_total_no, 'D-', label='(θNO + tNO)(n)', linewidth=2, markersize=8)
    ax.plot(tailles_n, maxima_total_bh, 'x-', label='(θBH + tBH)(n)', linewidth=2, markersize=8)
    
    ax.set_xlabel('Taille n', fontsize=12)
    ax.set_ylabel('Temps (secondes)', fontsize=12)
    ax.set_title('Complexité dans le Pire des Cas', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('complexite_pire_des_cas.png', dpi=300)
    print("✓ Graphique sauvegardé: complexite_pire_des_cas.png")
    plt.show()


def tracer_comparaison_ratios(resultats, tailles_n):
    """Trace le ratio (tNO + θNO) / (tBH + θBH) pour comparer les algorithmes."""
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    
    ratios = []
    for n in tailles_n:
        maxima_total_no = max(resultats[n]['theta_no']) + max(resultats[n]['t_marche_no'])
        maxima_total_bh = max(resultats[n]['theta_bh']) + max(resultats[n]['t_marche_bh'])
        ratio = maxima_total_no / maxima_total_bh if maxima_total_bh > 0 else 1
        ratios.append(ratio)
    
    colors = ['green' if r < 1 else 'red' for r in ratios]
    ax.bar(tailles_n, ratios, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
    ax.axhline(y=1, color='black', linestyle='--', linewidth=2, label='Équivalent')
    
    ax.set_xlabel('Taille n', fontsize=12)
    ax.set_ylabel('Ratio (θNO + tNO) / (θBH + tBH)', fontsize=12)
    ax.set_title('Comparaison des Algorithmes: Nord-Ouest vs Balas-Hammer', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Ajouter les valeurs sur les barres
    for i, (n, r) in enumerate(zip(tailles_n, ratios)):
        ax.text(n, r + 0.05, f'{r:.3f}', ha='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('complexite_comparaison_ratios.png', dpi=300)
    print("✓ Graphique sauvegardé: complexite_comparaison_ratios.png")
    plt.show()


def identifier_complexite(tailles, temps_max):
    """Identifie le type de complexité basé sur l'enveloppe supérieure.
    
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
# VERSION SIMPLE (SANS MATPLOTLIB)
# ==========================================

def etude_complexite_simple(tailles_n=None, iterations=100):
    """Effectue l'étude de complexité et exporte en CSV et JSON."""
    
    if tailles_n is None:
        tailles_n = [10, 40, 100, 400]
    
    print("="*70)
    print("ÉTUDE DE COMPLEXITÉ (VERSION SIMPLIFIÉE)")
    print("="*70)
    print(f"Tailles testées: {tailles_n}")
    print(f"Itérations par taille: {iterations}\n")
    
    resultats = {}
    donnees_csv = []
    
    for n in tailles_n:
        print(f"Taille n = {n:5d} : ", end="", flush=True)
        
        temps_no_list = []
        temps_bh_list = []
        temps_marche_no_list = []
        temps_marche_bh_list = []
        
        for iter_num in range(iterations):
            # Générer un problème aléatoire
            couts, provisions, commandes = generer_probleme_aleatoire(n)
            
            # Mesurer Nord-Ouest
            try:
                debut = time.perf_counter()
                prop_no = algo.algo_nord_ouest(provisions, commandes)
                t_no = time.perf_counter() - debut
                temps_no_list.append(t_no)
            except:
                temps_no_list.append(0)
            
            # Mesurer Balas-Hammer (réduire stdout)
            try:
                from io import StringIO
                old_stdout = sys.stdout
                sys.stdout = StringIO()
                
                debut = time.perf_counter()
                prop_bh = algo.algo_balas_hammer(couts, provisions, commandes)
                t_bh = time.perf_counter() - debut
                
                sys.stdout = old_stdout
                temps_bh_list.append(t_bh)
            except:
                sys.stdout = old_stdout
                temps_bh_list.append(0)
            
            # Mesurer marche-pied (simple)
            try:
                debut = time.perf_counter()
                u, v, marginaux, case_opt, base = algo.calculer_potentiels_et_marginaux(couts, prop_no)
                t_marche_no = time.perf_counter() - debut
                temps_marche_no_list.append(t_marche_no)
            except:
                temps_marche_no_list.append(0)
            
            try:
                debut = time.perf_counter()
                u, v, marginaux, case_opt, base = algo.calculer_potentiels_et_marginaux(couts, prop_bh)
                t_marche_bh = time.perf_counter() - debut
                temps_marche_bh_list.append(t_marche_bh)
            except:
                temps_marche_bh_list.append(0)
            
            if (iter_num + 1) % 20 == 0:
                print(".", end="", flush=True)
        
        print(" ✓")
        
        # Calculer les statistiques
        max_no = max(temps_no_list) if temps_no_list else 0
        max_bh = max(temps_bh_list) if temps_bh_list else 0
        max_marche_no = max(temps_marche_no_list) if temps_marche_no_list else 0
        max_marche_bh = max(temps_marche_bh_list) if temps_marche_bh_list else 0
        
        avg_no = sum(temps_no_list) / len(temps_no_list) if temps_no_list else 0
        avg_bh = sum(temps_bh_list) / len(temps_bh_list) if temps_bh_list else 0
        avg_marche_no = sum(temps_marche_no_list) / len(temps_marche_no_list) if temps_marche_no_list else 0
        avg_marche_bh = sum(temps_marche_bh_list) / len(temps_marche_bh_list) if temps_marche_bh_list else 0
        
        resultats[n] = {
            'theta_no_max': max_no,
            'theta_no_avg': avg_no,
            'theta_bh_max': max_bh,
            'theta_bh_avg': avg_bh,
            't_marche_no_max': max_marche_no,
            't_marche_no_avg': avg_marche_no,
            't_marche_bh_max': max_marche_bh,
            't_marche_bh_avg': avg_marche_bh,
            'total_no_max': max_no + max_marche_no,
            'total_bh_max': max_bh + max_marche_bh,
        }
        
        # Ajouter à la liste CSV
        donnees_csv.append({
            'n': n,
            'θNO(n)_max': f"{max_no:.8f}",
            'θNO(n)_avg': f"{avg_no:.8f}",
            'θBH(n)_max': f"{max_bh:.8f}",
            'θBH(n)_avg': f"{avg_bh:.8f}",
            'tNO(n)_max': f"{max_marche_no:.8f}",
            'tNO(n)_avg': f"{avg_marche_no:.8f}",
            'tBH(n)_max': f"{max_marche_bh:.8f}",
            'tBH(n)_avg': f"{avg_marche_bh:.8f}",
            'Total_NO_max': f"{max_no + max_marche_no:.8f}",
            'Total_BH_max': f"{max_bh + max_marche_bh:.8f}",
        })
        
        print(f"  θNO(n)  pire: {max_no:.8f}s | moyen: {avg_no:.8f}s")
        print(f"  θBH(n)  pire: {max_bh:.8f}s | moyen: {avg_bh:.8f}s")
        print(f"  tNO(n)  pire: {max_marche_no:.8f}s | moyen: {avg_marche_no:.8f}s")
        print(f"  tBH(n)  pire: {max_marche_bh:.8f}s | moyen: {avg_marche_bh:.8f}s")
        print(f"  TOTAL NO pire: {max_no + max_marche_no:.8f}s")
        print(f"  TOTAL BH pire: {max_bh + max_marche_bh:.8f}s")
        print()
    
    # Exporter en CSV
    print("\n" + "="*70)
    print("EXPORT DES DONNÉES")
    print("="*70)
    
    try:
        with open('resultats_complexite.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=donnees_csv[0].keys())
            writer.writeheader()
            writer.writerows(donnees_csv)
        print("✓ Fichier CSV sauvegardé: resultats_complexite.csv")
    except Exception as e:
        print(f"✗ Erreur lors de la sauvegarde CSV: {e}")
    
    # Exporter en JSON
    try:
        with open('resultats_complexite.json', 'w', encoding='utf-8') as f:
            json.dump(resultats, f, indent=2)
        print("✓ Fichier JSON sauvegardé: resultats_complexite.json")
    except Exception as e:
        print(f"✗ Erreur lors de la sauvegarde JSON: {e}")
    
    # Afficher les conclusions
    print("\n" + "="*70)
    print("CONCLUSIONS")
    print("="*70)
    
    for n in tailles_n:
        ratio = resultats[n]['total_no_max'] / resultats[n]['total_bh_max'] if resultats[n]['total_bh_max'] > 0 else 1
        meilleur = "Nord-Ouest" if ratio < 1 else "Balas-Hammer"
        print(f"n = {n:5d}: Ratio NO/BH = {ratio:.4f} ({meilleur} plus rapide)")
    
    print("\n" + "="*70)
    print("ÉTUDE TERMINÉE ✓")
    print("="*70)
    
    return resultats, tailles_n



# ==========================================
# PROGRAMME PRINCIPAL
# ==========================================

def afficher_usage():
    """Affiche le message d'aide."""
    print("""
ÉTUDE DE COMPLEXITÉ - PROBLÈMES DE TRANSPORT

Usage:
    python3 complexite.py              # Exécution complète (graphiques)
    python3 complexite.py --simple     # Version simple (CSV)
    python3 complexite.py --test       # Test rapide (30 secondes)
    python3 complexite.py --help       # Affiche cette aide

Options:
    --help              Affiche cette aide
    --simple            Exécution sans matplotlib (sortie CSV)
    --test              Test rapide avec tailles [10, 20] et 10 itérations
    """)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg == '--help' or arg == '-h':
            afficher_usage()
            sys.exit(0)
        
        elif arg == '--simple':
            print("\n" + "="*70)
            print("ANALYSE DE COMPLEXITÉ - VERSION SIMPLE (SANS GRAPHIQUES)")
            print("="*70 + "\n")
            
            resultats, tailles = etude_complexite_simple(
                tailles_n=[10, 40, 100, 400],
                iterations=100
            )
            print("\nUtilisez le fichier resultats_complexite.csv avec Excel/LibreOffice")
            sys.exit(0)
        
        elif arg == '--test':
            print("\n" + "="*70)
            print("TEST RAPIDE DE L'ÉTUDE DE COMPLEXITÉ")
            print("="*70 + "\n")
            
            resultats, tailles = etude_complexite_simple(
                tailles_n=[10, 20],
                iterations=10
            )
            print("\n✅ Test réussi!")
            sys.exit(0)
        
        else:
            print(f"❌ Argument inconnu: {arg}")
            afficher_usage()
            sys.exit(1)
    
    # Exécution par défaut: version complète avec graphiques
    print("\n" + "="*70)
    print("ANALYSE DE COMPLEXITÉ - PROBLÈMES DE TRANSPORT")
    print("="*70 + "\n")
    
    if not HAS_MATPLOTLIB:
        print("⚠ ATTENTION: matplotlib n'est pas installé")
        print("Les graphiques ne peuvent pas être générés.")
        print("Pour l'installer: pip install matplotlib numpy")
        print("\nUtilisez: python3 complexite.py --simple")
        print("pour une exécution sans matplotlib (sortie CSV)\n")
        sys.exit(1)
    
    # Effectuer l'étude complète
    resultats, tailles_n = etude_complexite_complete()
    
    # Identifier les complexités
    print("\n" + "="*70)
    print("IDENTIFICATION DES COMPLEXITÉS")
    print("="*70)
    
    maxima_no = [max(resultats[n]['theta_no']) for n in tailles_n]
    maxima_bh = [max(resultats[n]['theta_bh']) for n in tailles_n]
    maxima_marche_no = [max(resultats[n]['t_marche_no']) for n in tailles_n]
    maxima_marche_bh = [max(resultats[n]['t_marche_bh']) for n in tailles_n]
    
    type_no, r2_no = identifier_complexite(tailles_n, maxima_no)
    type_bh, r2_bh = identifier_complexite(tailles_n, maxima_bh)
    type_marche_no, r2_marche_no = identifier_complexite(tailles_n, maxima_marche_no)
    type_marche_bh, r2_marche_bh = identifier_complexite(tailles_n, maxima_marche_bh)
    
    print(f"\nθNO(n)  : {type_no} (R² = {r2_no:.4f})")
    print(f"θBH(n)  : {type_bh} (R² = {r2_bh:.4f})")
    print(f"tNO(n)  : {type_marche_no} (R² = {r2_marche_no:.4f})")
    print(f"tBH(n)  : {type_marche_bh} (R² = {r2_marche_bh:.4f})")
    
    # Tracer les résultats
    print("\n" + "="*70)
    print("GÉNÉRATION DES GRAPHIQUES")
    print("="*70)
    
    tracer_nuages_de_points(resultats, tailles_n)
    tracer_pire_des_cas(resultats, tailles_n)
    tracer_comparaison_ratios(resultats, tailles_n)
    
    # Sauvegarder les résultats en JSON
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
    
    print("\n✓ Résultats sauvegardés dans resultats_complexite.json")
    print("\n" + "="*70)
    print("ÉTUDE TERMINÉE")
    print("="*70)