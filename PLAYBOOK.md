# Playbook — Suivi de Migration ERP/CRM & Gestion du Changement

> Guide opératoire structuré en 4 volets (Définitions / Process / Documentation / Templates).
> Projet personnel (POC), données simulées, aucun outil ERP/CRM propriétaire — voir [`README.md`](README.md).
> **Dernière mise à jour** : 08/08/2026

---

## 1. Définitions

| Terme | Définition |
|---|---|
| **Cutover** | Bascule de l'ancien système vers le nouveau, en phases (extraction, transformation, chargement, validation) |
| **Réconciliation** | Comparaison avant/après pour vérifier qu'aucune donnée n'a été perdue ou altérée pendant la migration |
| **Hypercare** | Période de suivi renforcé juste après le go-live, avant retour au support standard |

## 2. Process

```mermaid
flowchart LR
    A[Plan de cutover par phase] --> B[Extraction → Transformation → Chargement]
    B --> C[Réconciliation avant/après]
    C --> D[Suivi hypercare post go-live]
```

1. **Plan de cutover** — tâches critiques séquencées par phase, avec statut de complétion.
2. **Migration** — extraction, transformation, chargement des données de l'ancien vers le nouveau système.
3. **Réconciliation** — comparaison des enregistrements avant/après, pas une confiance aveugle dans le succès technique du transfert.
4. **Hypercare** — volume et nature des tickets support suivis dans les semaines post go-live, comme indicateur indirect d'adoption utilisateur.

**Point de décision réutilisable** : le volume de tickets support en hypercare est un signal d'adoption aussi important que la réconciliation technique — une migration "techniquement réussie" mais que les utilisateurs n'adoptent pas reste un échec de projet.

## 3. Documentation

- [`README.md`](README.md) — positionnement pilotage de migration, disclaimer POC

## 4. Templates réutilisables

- **`generate_taches_cutover()`** (`data/demo_data.py`) — pattern de suivi de plan par phase, transposable à tout projet séquencé en étapes critiques.
- **`generate_reconciliation_donnees()`** — pattern de comparaison avant/après, réutilisable pour toute opération de migration ou de bascule système.
- **`generate_tickets_hypercare()`** — suivi de volume de tickets comme proxy d'adoption, transposable à tout lancement d'outil ou de process auprès d'utilisateurs finaux.

**Règle de transposition** : pour un cas réel, connecter aux données réelles de l'ERP/CRM source et cible — le triptyque plan de cutover / réconciliation / suivi hypercare reste identique quel que soit le système migré.

---

*Gisèle Metouck — Consultante Data Steward & Gouvernance · [GitHub](https://github.com/Kingdmfncr)*
