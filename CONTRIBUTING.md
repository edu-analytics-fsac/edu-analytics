# Contribuer à EduAnalytics

## Rôles

| Rôle | Membre |
|------|--------|
| Release Manager | ABBA Badreddine |
| Intégrateur·rice | à définir |
| Documentaliste | à définir |
| Développeur·se | tous |

## Branches

- `main` : production
- `develop` : intégration
- `feature/<nom>` part de `develop`
- `release/<x.y.z>` part de `develop`
- `hotfix/<x.y.z>` part de `main`

## Règles

- Pas de push direct sur `main` ni `develop` : tout passe par une Pull Request avec 1 approbation minimum.
- Pas d'auto-merge : le relecteur qui approuve est celui qui fusionne.
- `git push --force` interdit sur `main` et `develop` ; `--force-with-lease` toléré sur sa propre branche `feature/*` après un rebase.
- Une issue par fonctionnalité, assignée à son auteur, liée à la PR (`Closes #<n>`).

## Convention de commits

`feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:` suivi d'un message à l'impératif.
Exemple : `feat(cleaning): drop duplicate rows`

## Nom des PR

`[feature/<nom>] Description courte`

## Ordre de relecture

Le membre n relit la PR du membre n+1, le dernier relit le premier. À compléter avec l'ordre de l'équipe :
AMROUS Sara → BAROUDI Yassine → ABBA BadrEddine → AGOUZOUL Mohamed Reda → BOUKHATEM Mohammed → INCHALLAH Oussama → (retour à AMROUS Sara)
