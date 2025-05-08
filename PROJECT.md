# 🎯 PROJECT.md — API VLR.GG Scraper

> Dernière mise à jour : 2025-05-08 17:39:35 UTC

---

## 🧾 Description rapide

API personnelle qui récupère les données des matchs de Valorant depuis **vlr.gg** via scraping, les stocke en base de données SQLite, et les expose via **FastAPI**.

---

## 🧱 Structure actuelle

### 📁 Endpoints :

- `GET /match/{id}`  
  ➜ Retourne les infos d’un match donné. Scrape si non trouvé en BDD.

### 📦 Base de données :

- `Match` et `MatchDetails` : stockent les infos principales
- `updated_at` : permet de savoir quand la donnée a été insérée ou mise à jour
- `status` (prévu) : indique l'état du match (à venir, en cours, terminé)

### 🛠 Scrapers :

- `get_match_data(id)` : scrape les détails d’un match
- `get_match_list()` : (déjà présent mais à étendre)

---

## ✅ Ce qui fonctionne actuellement

- [x] Scraper de match par ID opérationnel
- [x] Insertion SQLAlchemy en BDD
- [x] Endpoint `/match/<built-in function id>` fonctionnel avec fallback sur scraper
- [x] Champ `updated_at` ajouté et utilisé
- [x] Suppression du script manuel `add_match_details.py`

---

## 🔜 Tâches à faire / Roadmap

### 🔹 Logique de mise à jour

- [ ] Ajouter champ `status` dans `MatchDetails`
- [ ] Déterminer `status` dans le scraper (`planned`, `live`, `finished`)
- [ ] Mettre à jour le champ `status` en BDD
- [ ] Ajouter logique de rafraîchissement conditionnel selon :
  - `live` ➜ toutes les 1 min
  - `planned` ➜ toutes les 15 min
  - `finished` ➜ jamais (ou 1x/jour)

### 🔹 Nouvelles fonctionnalités

- [ ] Endpoint `/live` ➜ retourne les matchs en cours
- [ ] Endpoint `/schedule` ➜ retourne les prochains matchs
- [ ] Endpoint `/results` ➜ retourne les derniers résultats
- [ ] Paramètre `refresh=true` pour forcer un re-scrape

---

## 💡 Notes et réflexions

- ✔ Le status peut souvent être déduit de l’URL de scraping (`/schedule`, `/live`, `/results`)
- ❓ Faut-il filtrer les matchs incomplets (ex : 0-0, scores manquants) ?
- ❓ À terme, envisager PostgreSQL ou Mongo pour plus de scalabilité ?
