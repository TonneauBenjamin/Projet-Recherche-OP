import time
import random
import algorithmes as algo

def generer_probleme_aleatoire(n):
    couts = [[random.randint(1, 100) for _ in range(n)] for _ in range(n)]
    temp = [[random.randint(1, 100) for _ in range(n)] for _ in range(n)]
    
    provisions = [sum(temp[i][j] for j in range(n)) for i in range(n)]
    commandes = [sum(temp[i][j] for i in range(n)) for j in range(n)]
    
    return n, n, couts, provisions, commandes

def etude_complexite():
    tailles_n = [10, 40, 100] # Ajoute 400, 1000, 4000, 10000 si ton PC le supporte
    iterations = 100 # On teste 100 fois par taille comme demandé
    
    print("DÉBUT DE L'ÉTUDE DE COMPLEXITÉ...")
    
    for n in tailles_n:
        temps_no_max, temps_bh_max = 0, 0
        temps_total_no_max, temps_total_bh_max = 0, 0
        
        print(f"\nCalcul pour n = {n} (100 itérations)")
        for _ in range(iterations):
            _, _, couts, prov, cmd = generer_probleme_aleatoire(n)
            
            # Temps Nord-Ouest
            debut = time.perf_counter()
            prop_no = algo.algo_nord_ouest(prov, cmd)
            fin_no = time.perf_counter()
            t_no = fin_no - debut
            
            # Temps Balas-Hammer
            debut = time.perf_counter()
            prop_bh = algo.algo_balas_hammer(couts, prov, cmd)
            fin_bh = time.perf_counter()
            t_bh = fin_bh - debut
            
            # Mise à jour de l'enveloppe supérieure (Pire des cas)
            temps_no_max = max(temps_no_max, t_no)
            temps_bh_max = max(temps_bh_max, t_bh)
            
            # NB : Mesurer la résolution complète avec le Stepping Stone 
            # prendra énormément de temps sur des matrices aléatoires 100x100+. 
            # Tu devras rajouter ici l'appel à la boucle Marche-Pied si nécessaire.
            
        print(f"Pire cas Nord-Ouest   O_NO({n}) : {temps_no_max:.6f} secondes")
        print(f"Pire cas Balas-Hammer O_BH({n}) : {temps_bh_max:.6f} secondes")

if __name__ == "__main__":
    etude_complexite()