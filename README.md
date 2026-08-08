# Suivi de migration ERP/CRM & gestion du changement

⚠️ **Projet personnel (POC)** — démonstration de compétences. Données simulées, aucun outil ERP/CRM propriétaire connecté.

Plan de cutover par phase (extraction, transformation, chargement, validation), réconciliation des enregistrements migrés (avant/après), et suivi des tickets support pendant la période d'hypercare post go-live.

## Objectif
Démontrer la logique de pilotage d'une migration système : suivi des tâches critiques, contrôle de la fiabilité des données migrées, et mesure de l'adoption utilisateur via le volume de tickets support dans les semaines suivant le go-live.

## Stack
Streamlit, Pandas, Plotly.

## Lancer en local
```
pip install -r requirements.txt
streamlit run app.py
```

Playbook complet (Définitions/Process/Documentation/Templates) : [`PLAYBOOK.md`](PLAYBOOK.md).
