# PARTIE 3 - Étude de Complexité

## 🚀 Utilisation Rapide

```bash
python3 complexite.py              # Exécution complète (graphiques)
python3 complexite.py --simple     # Sans matplotlib (CSV)
python3 complexite.py --test       # Test rapide (1 minute)
python3 complexite.py --help       # Affiche l'aide
```

## 📊 Interprétation des Résultats

### Fichiers Générés

#### Version Complète (avec matplotlib)
- **complexite_nuages_points.png**: Les 100 valeurs de temps pour chaque taille
  - Permet de voir la dispersion des mesures
  - Plus le nuage est dense, plus reproductibles sont les résultats

- **complexite_pire_des_cas.png**: Enveloppe supérieure (maximum pour chaque n)
  - Représente la complexité théorique
  - La courbe la plus basse = algorithme le plus efficace

- **complexite_comparaison_ratios.png**: Ratio (θNO + tNO) / (θBH + tBH)
  - Ratio < 1: Nord-Ouest est plus rapide
  - Ratio > 1: Balas-Hammer est plus rapide

#### Version Simple (sans matplotlib)
- **resultats_complexite.csv**: Données exploitables par Excel/LibreOffice
  - θNO(n)_max, θNO(n)_avg
  - θBH(n)_max, θBH(n)_avg
  - tNO(n)_max, tNO(n)_avg
  - tBH(n)_max, tBH(n)_avg
  - Total_NO_max, Total_BH_max

- **resultats_complexite.json**: Format structuré pour traitement ultérieur

### 2. Identification de Complexité

Le programme affiche automatiquement le type O(n) identifié avec un score R².

**Interprétation du R²:**
- R² > 0.95: Très bon ajustement
- 0.85 < R² ≤ 0.95: Bon ajustement
- 0.75 < R² ≤ 0.85: Acceptable
- R² ≤ 0.75: Mauvais ajustement

**Types courants:**
- **O(log n)**: Très efficace, croissance lente
- **O(n)**: Linéaire, croissance proportionnelle
- **O(n log n)**: Quasi-linéaire, bon compromis
- **O(n²)**: Quadratique, croissance rapide
- **O(n³)**: Cubique, très inefficace pour grandes entrées

### 3. Analyse Nord-Ouest vs Balas-Hammer

#### Nord-Ouest (θNO(n))
- Algorithme simple et rapide
- Pas de calculs de pénalités
- Peut donner des solutions non-optimales
- Complexité généralement **O(n)** ou **O(n log n)**

#### Balas-Hammer (θBH(n))
- Algorithme plus complexe
- Calcul des pénalités à chaque étape
- Meilleure solution initiale
- Complexité généralement **O(n²)** ou **O(n³)**

### 4. Interprétation Pratique

#### Exemple d'Analyse

**Résultat observé:**
```
n = 100:
  θNO(n)  pire: 0.00001234s | moyen: 0.00001000s
  θBH(n)  pire: 0.00005678s | moyen: 0.00005000s
  tNO(n)  pire: 0.00002345s | moyen: 0.00002100s
  tBH(n)  pire: 0.00001234s | moyen: 0.00001100s
  TOTAL NO pire: 0.00003579s
  TOTAL BH pire: 0.00006912s
```

**Interprétation:**
- Nord-Ouest seul: 5x plus rapide que Balas-Hammer seul
- Mais le marche-pied avec BH est plus rapide (moins d'itérations)
- Total: Nord-Ouest est plus rapide (~1.9x)

### 5. Points Importants pour le Rapport

1. **Description de l'étude**
   - Tailles testées
   - Nombre d'itérations
   - Machine utilisée

2. **Résultats principaux**
   - Complexité de chaque algorithme
   - Justification par les graphiques

3. **Comparaison**
   - Quel algorithme initial est meilleur?
   - Impact du marche-pied

4. **Conclusion**
   - Quand utiliser Nord-Ouest?
   - Quand utiliser Balas-Hammer?

### 6. Gabarit de Section "Complexité" du Rapport

```markdown
## 3. Étude de Complexité

### 3.1 Méthodologie
- Tailles testées: [indiquer]
- 100 itérations par taille pour robustesse
- Machine: [processeur, RAM]

### 3.2 Résultats Expérimentaux
- Nord-Ouest: O(n) avec R² = [valeur]
- Balas-Hammer: O(n²) avec R² = [valeur]
- Marche-pied: O(n) avec R² = [valeur]

### 3.3 Graphiques
[Inclure les 3 graphiques générés]

### 3.4 Analyse Comparative
- Ratio moyen: [calcul]
- Meilleur algorithme initial: [conclusion]

### 3.5 Conclusion
[Recommandations d'utilisation]
```

### 7. Tableaux pour le Rapport

**Tableau 1: Temps d'exécution par taille (pire des cas)**

| n | θNO(n) (ms) | θBH(n) (ms) | tNO(n) (ms) | tBH(n) (ms) | Total NO | Total BH |
|---|---|---|---|---|---|---|
| 10 | ... | ... | ... | ... | ... | ... |
| 40 | ... | ... | ... | ... | ... | ... |
| 100 | ... | ... | ... | ... | ... | ... |

**Tableau 2: Identification de complexité**

| Algorithme | Complexité | R² | Note |
|---|---|---|---|
| θNO(n) | O(n) | 0.98 | Très bon |
| θBH(n) | O(n²) | 0.96 | Très bon |
| Marche-pied | O(n) | 0.95 | Très bon |

### 8. Troubleshooting

**Résultats incohérents?**
- Réexécuter sur machine plus stable
- Augmenter le nombre d'itérations

**Graphiques plats?**
- Augmenter les tailles testées (trop petit = bruit)
- Vérifier que l'algorithme marche correctement

**Trop lent?**
- Réduire les tailles: `[10, 40, 100]` au lieu de `[10, 40, 100, 400, 1000]`
- Réduire les itérations: `50` au lieu de `100`

---

**Ressources additionnelles:**
- Section 3 du sujet du projet
- Définitions 3.1 à 3.4 (complexité)
- Tableau 3.1 (qualifications de complexité)
