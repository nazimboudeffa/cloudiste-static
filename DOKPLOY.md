# Déployer cloudiste-static sur Dokploy

Tu avais jusqu’ici une **Application statique** Dokploy buildée depuis le dépôt. Pour exécuter
`scan_gpu.py` sur un cron, le montage le plus simple est de passer à un service
**Docker Compose** (choisir bien « Docker Compose », pas « Stack » : Stack ne gère pas `build`).

Tu pourras réutiliser le même domaine : crée le nouveau service, teste-le, ajoute le domaine,
puis supprime l’ancienne application statique.

## Fichiers prêts dans le dépôt

| Fichier | Rôle |
| --- | --- |
| `Dockerfile` | Nginx qui copie les `.html` dans `/usr/share/nginx/html` |
| `docker-compose.yml` | services `web` + `gpu-scan` et volume partagé `gpu-data` |
| `Dockerfile.gpu-scan` | image Python avec `requests`, qui reste allumée |
| `scan_gpu.py` | le scanner Vast.ai / Runpod, avec écriture atomique du JSON |
| `.dockerignore` | évite d’envoyer `.env` et le JSON local dans le contexte de build |

Le site est servi par `web`. Le conteneur `gpu-scan` écrit dans le volume partagé :
`web` le monte en lecture seule sous `/usr/share/nginx/html/data`, donc l’URL publique est
`https://ton-domaine/data/gpu-market.json`.

## 1. Préparer la page

Dans `gpu-market.html`, décommente la balise du `<head>` :

```html
<meta name="gpu-market-data" content="data/gpu-market.json">
```

Vérifie aussi la fréquence du cron dans le `<head>` :

```html
<meta name="gpu-scan-schedule" content="daily">
<meta name="gpu-scan-tz" content="UTC">
```

- `daily` = un scan par jour à minuit (`0 0 * * *`) — réglage actuel.
- `gpu-scan-tz` doit reprendre **le même fuseau que le champ Timezone du job Dokploy** :
  `UTC` par défaut, ou `Europe/Paris` si tu veux minuit à l’heure de Paris.

Pour revenir à un intervalle, mets `content="interval"` puis choisis :

```html
<meta name="gpu-scan-interval" content="360">
```

- `360` pour `0 */6 * * *` (toutes les 6 heures).
- `60` pour `0 * * * *` (toutes les heures).

En mode `daily`, le compte à rebours vise le prochain minuit dans `gpu-scan-tz`. En mode
`interval`, il utilise la date de modification du JSON + l’intervalle. Dans les deux cas c’est
une estimation : si le scan n’a pas tourné à l’heure prévue, la carte affiche « en retard ».

Puis commit et push. Sans la balise `gpu-market-data`, la page essaie d’abord
`gpu-market.json` à la racine, puis `data/gpu-market.json` — ça marche aussi, mais avec un
404 inutile dans la console.

## 2. Créer le service dans Dokploy

1. Dans ton projet Dokploy : **Nouveau service** → **Docker Compose**.
2. Connecte le même dépôt Git et la même branche que ton application statique actuelle.
3. Laisse le chemin du compose à `docker-compose.yml`.
4. Onglet **Environment** : ajoute les variables :
   ```text
   VAST_API_KEY=...
   RUNPOD_API_KEY=...
   ```
   Dokploy les enregistre dans un `.env` sur le serveur. Le compose utilise `${VAST_API_KEY}`
   et `${RUNPOD_API_KEY}` pour les injecter dans `gpu-scan`. Ne mets jamais ces clés dans le dépôt.
5. Clique sur **Deploy**. Le bouton **Preview Compose** permet de vérifier le fichier final
   généré par Dokploy (labels Traefik, réseau, volumes).
6. Onglet **Domains** : ajoute ton domaine existant, port **80**, active le HTTPS.

L’ancienne application statique peut rester active le temps du test : utilise un autre domaine
ou l’URL générée par Dokploy pour le nouveau service, puis bascule le DNS.

## 3. Vérifier que ça tourne

```bash
docker compose ps
curl -I https://ton-domaine/data/gpu-market.json
```

Au début le fichier n’existe pas encore : c’est normal. Lance une première fois le scanner
à la main :

```bash
docker compose exec gpu-scan \
  python /app/scan_gpu.py --taux-eur 0.86 --json /data/gpu-market.json
```

Recharge `https://ton-domaine/gpu-market.html` : les offres doivent apparaître. Vérifie aussi
que `https://ton-domaine/data/gpu-market.json` renvoie bien le tableau JSON.

> Pourquoi `gpu-scan` reste allumé avec `sleep infinity` ? Dokploy exécute les jobs Compose
> avec `docker exec` : le conteneur cible doit être démarré. Un conteneur qui se termine
> immédiatement ne pourrait pas recevoir la commande du cron.

## 4. Planifier le rafraîchissement

Dans le service Compose : **Schedules / Tâches planifiées** → nouveau job.

- Type : **Compose**
- Service cible : `gpu-scan`
- Commande :
  ```bash
  python /app/scan_gpu.py --taux-eur 0.86 --json /data/gpu-market.json
  ```
- **Cron / expression cron** : `0 0 * * *` — minute `0`, heure `0`, tous les jours.
- **Timezone** : `UTC` (valeur par défaut de Dokploy) ou `Europe/Paris`. Mets la **même
  valeur** dans `gpu-scan-tz` du HTML, sinon le compte à rebours affichera une heure décalée.

Si tu avais gardé l’ancien job `0 */6 * * *`, modifie-le plutôt que d’en créer un deuxième :
deux jobs écrivant le même fichier se disputeraient le volume.

Dokploy garde l’historique et les logs de chaque exécution. Le script écrit d’abord un `.tmp`
puis le renomme, ce qui évite qu’une requête lise un JSON partiel.

## 5. Détails importants

- **Variables d’environnement** : dans l’onglet Environment de Dokploy, pas dans le dépôt.
  `.env.example` liste les deux clés nécessaires ; copie-le en `.env` pour un test local.
  `.env` est ignoré par Git et exclu du build Docker par `.dockerignore`.
- **Stack à éviter** : le mode Stack de Dokploy n’autorise pas `build` dans le compose.
- **Volumes** : `gpu-data` est un volume nommé, donc il survit aux redéploiements. Les anciennes
  offres restent affichées tant que le cron n’a pas réécrit le fichier.
- **Cache** : la page ajoute `?t=...` à chaque chargement, mais Cloudflare peut quand même
  mettre le JSON en cache. Prévois une règle **Bypass cache** sur `/data/gpu-market.json`.
- **Migration** : une fois le nouveau service validé, supprime l’ancienne Application statique
  pour éviter deux services sur le même domaine.

## 6. SEO

Les trois pages contiennent : `<title>` optimisé, meta description, `canonical`, `hreflang`
`fr` / `x-default`, Open Graph, Twitter Card, `robots`, `theme-color` et des données structurées
JSON-LD (`SoftwareApplication`, `WebPage`, `Dataset`).

Fichiers publics ajoutés et copiés par le `Dockerfile` : `robots.txt`, `sitemap.xml`,
`favicon.svg` et `og-image.png` (1200 × 630 pour le partage sur les réseaux sociaux).

Les URL canoniques utilisent `https://cloudiste.fr`. **Si ton domaine est différent**, remplace
cette chaîne dans les trois fichiers HTML, dans `robots.txt` et dans `sitemap.xml`, puis
redéploie.

Après déploiement :

1. Vérifier `https://cloudiste.fr/robots.txt` et `https://cloudiste.fr/sitemap.xml`.
2. Soumettre le sitemap dans **Google Search Console** et **Bing Webmaster Tools**.
3. Tester le JSON-LD avec <https://validator.schema.org/> et l’aperçu sociaux avec le
   *Sharing Debugger* de Facebook / *Card Validator* de Twitter.

## Test local avant Dokploy

```bash
docker compose up -d --build
docker compose exec gpu-scan \
  python /app/scan_gpu.py --taux-eur 0.86 --json /data/gpu-market.json
```

Ouvre ensuite `http://localhost/gpu-market.html`.
