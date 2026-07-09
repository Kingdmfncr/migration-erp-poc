"""Donnees demo — migration ERP/CRM simulee. Aucune donnee reelle,
aucun outil ERP/CRM propriétaire connecte."""
import random
from datetime import date, timedelta

import pandas as pd

random.seed(29)

MODULES = ["Clients & Contacts", "Catalogue Produits", "Commandes", "Facturation",
           "Stocks", "Utilisateurs & Droits"]

PHASES = ["Extraction", "Transformation", "Chargement", "Validation"]

TICKET_TYPES = ["Bug bloquant", "Question fonctionnelle", "Demande de formation", "Anomalie de donnee"]


def generate_taches_cutover(n: int = 18) -> pd.DataFrame:
    today = date.today()
    rows = []
    for i in range(n):
        module = random.choice(MODULES)
        phase = PHASES[min(i // (n // len(PHASES) + 1), len(PHASES) - 1)]
        statut = random.choices(["Termine", "En cours", "A faire", "Bloque"], weights=[5, 3, 2, 1])[0]
        echeance = today + timedelta(days=random.randint(-5, 20))
        rows.append({
            "id_tache": f"CUT-{i+1:03d}",
            "module": module,
            "phase": phase,
            "responsable": random.choice(["Equipe IT", "Equipe Metier", "Prestataire", "Direction de projet"]),
            "echeance": echeance,
            "statut": statut,
        })
    return pd.DataFrame(rows)


def generate_reconciliation_donnees() -> pd.DataFrame:
    """Comparaison du nombre d'enregistrements avant/apres migration, par module."""
    rows = []
    for module in MODULES:
        avant = random.randint(500, 45_000)
        ecart_pct = random.choices([0, 0, 0.1, 0.5, 2.3], weights=[5, 3, 2, 1, 1])[0]
        apres = int(avant * (1 - ecart_pct / 100))
        rows.append({
            "module": module,
            "enregistrements_avant": avant,
            "enregistrements_apres": apres,
            "ecart": avant - apres,
            "ecart_pct": round(ecart_pct, 2),
            "statut": "Conforme" if ecart_pct == 0 else "A verifier" if ecart_pct < 1 else "Ecart significatif",
        })
    return pd.DataFrame(rows)


def generate_tickets_hypercare(jours: int = 21) -> pd.DataFrame:
    """Volume de tickets support pendant la periode d'hypercare post go-live."""
    today = date.today()
    rows = []
    ticket_id = 1
    for j in range(jours, 0, -1):
        d = today - timedelta(days=j)
        # Pic les premiers jours, decroissance progressive (courbe d'adoption classique)
        intensite = max(1, int(12 * (1 - j / jours) ** 0.5 * random.uniform(0.7, 1.3)))
        for _ in range(intensite):
            rows.append({
                "id_ticket": f"TCK-{ticket_id:04d}",
                "date": d,
                "type": random.choices(TICKET_TYPES, weights=[2, 5, 3, 2])[0],
                "module": random.choice(MODULES),
                "resolu": random.random() > 0.15,
            })
            ticket_id += 1
    return pd.DataFrame(rows)
