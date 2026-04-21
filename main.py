import sys
import algorithmes as algo

class Logger:
    """Permet de rediriger le print() vers la console ET un fichier .txt."""
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

def main():
    print("=== PROJET RECHERCHE OPÉRATIONNELLE ===")
    
    continuer = True
    while continuer:
        num_prob = input("\nEntrez le numéro du problème à traiter (1-12) : ")
        fichier = f"probleme{num_prob}.txt"
        
        try:
            n, m, couts, prov, cmd = algo.charger_donnees(fichier)
        except FileNotFoundError:
            print(f"Fichier {fichier} introuvable.")
            continue
            
        print("\nAlgorithme initial :")
        print("1. Nord-Ouest")
        print("2. Balas-Hammer")
        choix_algo = input("Choix (1/2) : ")
        
        # Configuration de la trace
        methode_nom = "no" if choix_algo == "1" else "bh"
        groupe, equipe = "2", "4" # À remplacer par ton vrai groupe
        nom_trace = f"{groupe}-{equipe}-trace{num_prob}-{methode_nom}.txt"
        
        # On active la double écriture (console + fichier)
        sys.stdout = Logger(nom_trace)
        
        print(f"Début de la résolution du problème {num_prob} avec la méthode {methode_nom.upper()}")
        algo.afficher_matrice(couts, [f"P{i+1}" for i in range(n)], [f"C{j+1}" for j in range(m)], "COÛTS INITIAUX")
        
        # Proposition initiale
        if choix_algo == "1":
            prop = algo.algo_nord_ouest(prov, cmd)
        else:
            prop = algo.algo_balas_hammer(couts, prov, cmd)
            
        cout_actuel = algo.calculer_cout_total(couts, prop)
        iteration = 0
        
        # Boucle du Stepping Stone
        optimise = False
        while not optimise:
            print(f"\n--- ITÉRATION {iteration} ---")
            algo.afficher_matrice(prop, [f"P{i+1}" for i in range(n)], [f"C{j+1}" for j in range(m)], "PROPOSITION ACTUELLE")
            print(f"Coût de transport total : {cout_actuel}")
            
            u, v, marginaux, case_amel = algo.calculer_potentiels_et_marginaux(couts, prop)
            
            print(f"Potentiels Fournisseurs (U) : {u}")
            print(f"Potentiels Clients (V)    : {v}")
            algo.afficher_matrice(marginaux, [f"P{i+1}" for i in range(n)], [f"C{j+1}" for j in range(m)], "COÛTS MARGINAUX")
            
            if case_amel is None:
                print("\n✅ La proposition est OPTIMALE !")
                optimise = True
            else:
                print(f"\nArête améliorante trouvée en {case_amel} avec un coût marginal négatif.")
                cycle = algo.trouver_cycle(prop, case_amel)
                print(f"Cycle détecté : {cycle}")
                
                prop, delta = algo.ameliorer_proposition(prop, cycle)
                print(f"Maximisation effectuée : on déplace {delta} unités sur le cycle.")
                cout_actuel = algo.calculer_cout_total(couts, prop)
                iteration += 1
                
        # Restauration de la sortie standard
        sys.stdout.log.close()
        sys.stdout = sys.stdout.terminal
        print(f"\nTrace sauvegardée dans {nom_trace}")
        
        choix_cont = input("\nVoulez-vous traiter un autre problème ? (o/n) : ")
        if choix_cont.lower() != 'o':
            continuer = False

if __name__ == "__main__":
    main()