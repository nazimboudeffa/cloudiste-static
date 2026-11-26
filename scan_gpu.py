#!/usr/bin/env python3
"""Scanne Vast.ai et Runpod à la recherche de GPU hébergés en France.

Installation :  pip install requests
Clés API    :  export VAST_API_KEY="..."   et   export RUNPOD_API_KEY="..."
Exemples    :  python scan_gpu.py
               python scan_gpu.py --gpu "H100" --taux-eur 0.86
               python scan_gpu.py --taux-eur 0.86 --json gpu-market.json
                   (génère les données de cloudsgpu.html)
"""
import argparse, json, os, sys
import requests

PAYS = "FR"
TIMEOUT = 30


def vast_offres():
    """Offres Vast.ai dont la machine est en France (filtre geolocation)."""
    cle = os.environ.get("VAST_API_KEY")
    if not cle:
        print("VAST_API_KEY manquante : Vast.ai ignoré", file=sys.stderr)
        return []
    corps = {
        "limit": 300,
        "type": "on-demand",
        "verified": {"eq": True},
        "rentable": {"eq": True},
        "rented": {"eq": False},
        "geolocation": {"in": [PAYS]},
        "order": [["dph_total", "asc"]],
    }
    r = requests.post("https://console.vast.ai/api/v0/bundles/",
                      headers={"Authorization": f"Bearer {cle}"},
                      json=corps, timeout=TIMEOUT)
    r.raise_for_status()
    res = []
    for o in r.json().get("offers", []):
        n = o.get("num_gpus") or 1
        res.append({
            "source": "Vast.ai",
            "gpu": (o.get("gpu_name") or "?").replace("_", " "),
            "nb_gpu": n,
            "lieu": o.get("geolocation", PAYS),
            "type": "À la demande",
            "usd_gpu_h": round(o["dph_total"] / n, 4),
            "ram_go": round((o.get("cpu_ram") or 0) / 1024),
            "vcpu": o.get("cpu_cores_effective"),
        })
    return res


def runpod_offres():
    """GPU Runpod disposant d'un datacenter en France (filtre countryCodes)."""
    cle = os.environ.get("RUNPOD_API_KEY")
    if not cle:
        print("RUNPOD_API_KEY manquante : Runpod ignoré", file=sys.stderr)
        return []
    res = []
    for cloud, champ in (("SECURE", "secure"), ("COMMUNITY", "community")):
        r = requests.get(
            "https://api.runpod.io/v2/catalog/gpus",
            headers={"Authorization": f"Bearer {cle}"},
            params={"include": "AVAILABILITY", "product": "POD",
                    "countryCodes": PAYS, "cloud": cloud},
            timeout=TIMEOUT)
        r.raise_for_status()
        for g in r.json().get("gpus", []):
            if g.get("availability") in (None, "NONE"):
                continue
            prix = (g.get("price") or {}).get(champ)
            if prix is None:
                continue
            dcs = ", ".join(d["name"] for d in g.get("dataCenters", [])) or PAYS
            res.append({
                "source": f"Runpod ({champ.lower()})",
                "gpu": g["name"],
                "nb_gpu": 1,
                "lieu": dcs,
                "type": "À la demande",
                "usd_gpu_h": round(prix, 4),
                "stock": g["availability"],
            })
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gpu", help="filtre sur le nom du GPU (ex. H100)")
    ap.add_argument("--taux-eur", type=float, help="taux USD→EUR (ex. 0.86)")
    ap.add_argument("--json", help="écrit les résultats dans ce fichier JSON")
    a = ap.parse_args()

    offres = []
    for f in (vast_offres, runpod_offres):
        try:
            offres += f()
        except requests.RequestException as e:
            print(f"Erreur {f.__name__} : {e}", file=sys.stderr)

    if a.gpu:
        offres = [o for o in offres if a.gpu.lower() in o["gpu"].lower()]
    offres.sort(key=lambda o: o["usd_gpu_h"])
    if a.taux_eur:
        for o in offres:
            o["eur_gpu_h"] = round(o["usd_gpu_h"] * a.taux_eur, 4)

    if a.json:
        dossier = os.path.dirname(os.path.abspath(a.json))
        os.makedirs(dossier, exist_ok=True)
        temporaire = a.json + ".tmp"
        with open(temporaire, "w", encoding="utf-8") as fh:
            json.dump(offres, fh, ensure_ascii=False, indent=2)
        os.replace(temporaire, a.json)

    if not offres:
        print("Aucune offre trouvée en France pour ces critères.")
        return
    col = "eur_gpu_h" if a.taux_eur else "usd_gpu_h"
    dev = "€" if a.taux_eur else "$"
    print(f"{'Source':<20}{'GPU':<22}{'Nb':>3}  {'Prix '+dev+'/GPU·h':>13}  Lieu")
    for o in offres:
        print(f"{o['source']:<20}{o['gpu'][:21]:<22}{o['nb_gpu']:>3}  {o[col]:>13.3f}  {o['lieu']}")


if __name__ == "__main__":
    main()
