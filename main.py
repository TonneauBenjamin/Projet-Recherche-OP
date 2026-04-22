import sys
import os
import algorithmes as algo


class Logger:
    """Redirige print() vers la console ET un fichier .txt simultanement."""
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()


# ── A MODIFIER selon votre equipe ──────────────────────────────────────────────
EQUIPE = "4"   # numero d'equipe (ex: "4")
GROUPE = "BN"  # prefixe groupe (ex: "BN")
# ───────────────────────────────────────────────────────────────────────────────


def main():
    os.makedirs("traces", exist_ok=True)

    print("=== PROJET RECHERCHE OPERATIONNELLE ===")
    print(f"Groupe : {GROUPE}  |  Equipe : {EQUIPE}")

    continuer = True
    while continuer:
        num_prob = input("\nNumero du probleme (1-12) : ").strip()
        fichier = f"entrees/probleme{num_prob}.txt"

        try:
            n, m, couts, prov, cmd = algo.charger_donnees(fichier)
        except FileNotFoundError:
            print(f"Fichier '{fichier}' introuvable.")
            continue
        except Exception as e:
            print(f"Erreur de lecture : {e}")
            continue

        print("\nAlgorithme de proposition initiale :")
        print("  1. Nord-Ouest")
        print("  2. Balas-Hammer")
        choix = input("Choix (1/2) : ").strip()

        methode = "no" if choix == "1" else "bh"
        nom_trace = f"traces/{GROUPE}-{EQUIPE}-trace{num_prob}-{methode}.txt"

        sys.stdout = Logger(nom_trace)
        try:
            _resoudre(n, m, couts, prov, cmd, choix, methode, num_prob)
        finally:
            log = sys.stdout.log
            sys.stdout = sys.stdout.terminal
            log.close()

        print(f"\nTrace sauvegardee dans : {nom_trace}")

        rep = input("\nAutre probleme ? (o/n) : ").strip().lower()
        if rep != 'o':
            continuer = False


def _resoudre(n, m, couts, prov, cmd, choix, methode, num_prob):
    titres_l = [f"P{i + 1}" for i in range(n)]
    titres_c = [f"C{j + 1}" for j in range(m)]

    print(f"\n{'=' * 60}")
    print(f"  PROBLEME {num_prob}  —  Methode : {methode.upper()}")
    print(f"  Fournisseurs : {n}   Clients : {m}")
    print(f"{'=' * 60}")

    algo.afficher_matrice(couts, titres_l, titres_c, "TABLEAU DES COUTS")
    print(f"Provisions : {prov}")
    print(f"Commandes  : {cmd}")

    # --- Proposition initiale ---
    if choix == "1":
        print("\n--- Methode Nord-Ouest ---")
        prop = algo.algo_nord_ouest(prov, cmd)
    else:
        print("\n--- Methode Balas-Hammer ---")
        prop = algo.algo_balas_hammer(couts, prov, cmd)

    algo.afficher_matrice(prop, titres_l, titres_c, "PROPOSITION INITIALE")
    cout_actuel = algo.calculer_cout_total(couts, prop)
    print(f"Cout initial : {cout_actuel}")

    # --- Boucle Marche-Pied ---
    iteration = 0
    optimise = False

    while not optimise:
        print(f"\n{'─' * 50}")
        print(f"  ITERATION {iteration}")
        print(f"{'─' * 50}")

        u, v, marginaux, case_amel, base = algo.calculer_potentiels_et_marginaux(couts, prop)

        print(f"Potentiels U (fournisseurs) : {u}")
        print(f"Potentiels V (clients)      : {v}")
        algo.afficher_matrice(marginaux, titres_l, titres_c, "COUTS MARGINAUX")

        if case_amel is None:
            print(f"\n*** SOLUTION OPTIMALE atteinte a l'iteration {iteration} ***")
            print(f"Cout total optimal : {cout_actuel}")
            algo.afficher_matrice(prop, titres_l, titres_c, "ALLOCATION FINALE")
            optimise = True
        else:
            i_a, j_a = case_amel
            print(f"Case ameliorante : ({i_a + 1},{j_a + 1})  (cout marginal = {marginaux[i_a][j_a]})")

            cycle = algo.trouver_cycle(base, case_amel, n, m)

            if cycle is None:
                print("ATTENTION : aucun cycle trouve (degenerescence non resolue). Arret.")
                break

            cycle_affiche = [(i + 1, j + 1) for i, j in cycle]
            print(f"Cycle : {cycle_affiche}")

            prop, delta = algo.ameliorer_proposition(prop, cycle)

            if delta == 0:
                print("ATTENTION : pivot degenere (delta = 0). Arret pour eviter le cyclage.")
                break

            print(f"Deplacement de {delta} unites sur le cycle.")
            cout_actuel = algo.calculer_cout_total(couts, prop)
            print(f"Nouveau cout : {cout_actuel}")
            iteration += 1


if __name__ == "__main__":
    main()
