# Database 3NF Migration Plan (Willem II Dashboard)

## Doel
Een stabiele, uitbreidbare MySQL-structuur voor productie: historie behouden, minder duplicatie, duidelijke relaties, en veilige migratie zonder directe functionele regressies.

## Scope
Alle modules in `main` (dashboard, training, wedstrijd, testdata, revalidatie, voeding, HIT, aanwezigheid, overig).

## Kernprincipes
- Gebruik `Player` als primaire entiteit voor sportgerelateerde data.
- Bewaar **meetdata als tijdreeksen** (immutable records waar mogelijk).
- Vermijd herhaalde tekstvelden voor entiteiten (namen/teams/rollen).
- Splits "masterdata" en "event/measurement data".
- Voeg unieke constraints en indexes toe op natuurlijke sleutels.

## Gevonden 3NF-risico's (huidig)
- `Injury.name` als vrije tekst i.p.v. FK naar `Player`.
- `DayProgram.date` als `CharField` i.p.v. `DateField`.
- `HitWeekPlanning` met kolommen `monday...sunday` (niet rij-georiënteerd).
- `Birthday` en `YouthGuest` dupliceren persoonsgegevens naast `Player/Staff`.
- `Antropometry` bevat veel kolommen met herhaling (`*_m1/m2/m3`), lastig schaalbaar.
- Meerdere modellen missen expliciete constraints/indexes voor querypatronen.

## Target structuur (3NF)

### 1) Core / identity
- `Player` (blijft hoofdentiteit)
- `Staff` (blijft)
- `Team` (nieuw, referentietabel)
- `Role`/`Position` (nieuw, referentietabel waar nodig)

### 2) Kalender / planning
- `CalendarEvent` (nieuw): datum/tijd, type, context.
- `WeeklyPlan` + `WeeklyPlanEntry` (nieuw): vervangt wide day-kolommen.
- `Match` (blijft, met team-relaties optioneel in latere fase)

### 3) Medical / rehab
- `InjuryCase` (nieuw): FK player, blessuretype, fase, status, start/eind.
- `RehabSession` (normaliseren op sessie + onderdelen als child records).
- Historie per wijziging behouden via timestamps.

### 4) Performance / load
- `TrainingSessionMetric` (huidige `TrainingData`), unieke `(player, session_date, source)`.
- `MatchMetric` (huidige `WedstrijdData`), unieke `(player, match_date, source)`.
- `RPEEntry`, `WellnessEntry`, `WeightEntry` blijven event-tabellen met strakkere constraints.

### 5) Growth / dispensatie
- `GrowthProfile` (1-op-1 met player, state)
- `GrowthMeasurement` (tijdreeks, immutable)
- (optioneel) `GrowthAssessment` als snapshot met berekende indicatoren op datum.

### 6) Nutrition
- `NutritionPlanDay` (teamplan)
- `PlayerNutritionIntake` (player-specifiek)
- `AnthropometrySession` + child-tabellen:
  - `AnthropometrySkinfold`
  - `AnthropometryGirth`

## Faseringsstrategie (veilig)

### Fase A - Voorbereiding (geen brekende wijzigingen)
1. Nieuwe 3NF-tabellen toevoegen naast bestaande tabellen.
2. Datamigratie scripts toevoegen (oude -> nieuwe structuur).
3. Read-only verificatie (counts, null-checks, orphan checks).

### Fase B - App omzetten
1. Views/forms per module omzetten naar nieuwe modellen.
2. Dubbel schrijven tijdelijk aan (optioneel) voor risicoloze overgang.
3. Feature flags of module-voor-module switch.

### Fase C - Opschonen
1. Oude velden/tabellen deprecaten.
2. Definitieve constraints aanscherpen.
3. Documenteren van ERD + operationele runbooks.

## Prioriteit (aanbevolen volgorde)
1. Core relaties + Injury + DayProgram + HitWeekPlanning
2. Growth module
3. Revalidatie gym/veld
4. Nutrition/Anthropometry
5. Remaining dashboard modules

## Datakwaliteit checks (verplicht)
- Uniek: dubbele records op `(player, date)` detecteren.
- Referentiële integriteit: orphan records.
- Historiecontrole: laatste record per speler/module vs UI.
- Performance: indexes op `player_id`, datumvelden, veelgebruikte filters.

## Verwachte output per stap
- Migration files
- Data migration commands
- Integrity report (row counts + mismatches)
- Changelog van aangepaste views/templates

