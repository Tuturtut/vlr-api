# Valorant Live Scores API

Une API RESTful pour récupérer les scores des matchs Valorant en direct, à venir et terminés depuis [vlr.gg](https://www.vlr.gg).

---

## Installation

1. Clonez le projet :

```bash
git clone https://github.com/Tuturtut/vlr-api.git
cd vlr-api
```

2. Installez les dépendances :

```bash
pip install -r requirements.txt
```

3. Lancez l'API:

```bash
uvicorn app.main:app --reload
```

> ⚠️ Attention
>
> Assurez-vous d’avoir Python 3.9+ installé.

## Endpoints

| Méthode | Route                 | Description                                                             |
| :-----: | :-------------------- | :---------------------------------------------------------------------- |
|   GET   | `/matches`            | Liste tous les matchs de la base de données (option : `size`, `status`) |
|   GET   | `/matches/match/{id}` | Récupère un match spécifique par ID, scrappe si absent                  |
|   GET   | `/matches/planned`    | Liste des matchs prévus                                                 |
|   GET   | `/matches/live`       | Liste des matchs en direct                                              |
|   GET   | `/matches/ended`      | Liste des matchs terminés                                               |
| DELETE  | `/matches/match/{id}` | Supprime un match spécifique de la base de données                      |

## Exemple de réponse

```json
{
  "12345": {
    "match_id": 12345,
    "team_1": "Team A",
    "team_2": "Team B",
    "team_1_score": 13,
    "team_2_score": 11,
    "score_named_with_dash": "Team A 13 - 11 Team B",
    "score_with_dash": "13 - 11",
    "score_named_with_colon": "Team A 13 : 11 Team B",
    "score_with_colon": "13 : 11",
    "games": [...],
    "status": "ended",
    "updated_at": "2025-06-07T10:00:00Z",
    "seconds_until_match": null,
    "scheduled_time": "2025-06-08T15:00:00Z"
  }
}
```

## Notes

Cette API n'est pas officielle et utilise du scraping pour récupérer les données. Elle n'est donc pas a but commerciale.

Le scraping est fait sur vlr.gg, respectez leurs conditions d’utilisation.

Le projet est en développement, si vous avez la moindre proposition, question ou conseil, n'hesitez surtout pas !

## Contact

Si vous avez des questions ou souhaitez contribuer :

GitHub : Tuturtut
Discord : tut1ur
