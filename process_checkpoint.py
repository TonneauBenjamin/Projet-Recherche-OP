import json

with open('checkpoint_complexite.json') as f:
    data = json.load(f)

result = {}
for n, vals in data.items():
    no_vals = vals['theta_no']
    bh_vals = vals['theta_bh']
    no_max = max(no_vals)
    no_moy = sum(no_vals) / len(no_vals)
    bh_max = max(bh_vals)
    bh_moy = sum(bh_vals) / len(bh_vals)
    result[n] = {
        "n": int(n),
        "iterations": len(no_vals),
        "no_max": no_max,
        "no_moy": no_moy,
        "bh_max": bh_max,
        "bh_moy": bh_moy
    }

with open('summary_complexite.json', 'w') as f:
    json.dump(result, f, indent=2)