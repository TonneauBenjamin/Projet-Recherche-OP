import json

with open('checkpoint_complexite.json') as f:
    data = json.load(f)

result = {}
for n, vals in data.items():
    no_vals = vals['theta_no']
    bh_vals = vals['theta_bh']
    no_max = max(no_vals)
    bh_max = max(bh_vals)
    result[n] = {
        "n": int(n),
        "no_max": no_max,
        "bh_max": bh_max
    }

with open('pire_cas_complexite.json', 'w') as f:
    json.dump(result, f, indent=2)