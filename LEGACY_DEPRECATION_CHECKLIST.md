# Legacy Deprecation Checklist

Use this checklist before dropping old tables.

## Preconditions
- New 3NF migrations are applied on all environments.
- Reads/writes are fully on new tables.
- At least 1 week stable production behavior.
- Fresh full SQL backup exists.
- `python manage.py verify_legacy_drop_readiness` reports `READY`.

## Preflight migration
- Apply: `0049_deprecate_legacy_tables_preflight` (marker migration, no drop).

## Old -> New mapping
- `main_injury` -> `main_injurycase`
- `main_hitweekplanning` -> `main_hitweekplan` + `main_hitweekplanentry`
- `main_dayprogram` -> `main_dayprogramentry`
- `main_antropometry` -> `main_anthropometrysession` + `main_anthropometrymeasurement`
- `main_playerintake` -> `main_nutritionintakesession` + `main_nutritionintakeitem`
- `main_birthday` -> `main_birthdayprofile` + `main_birthdayrecord`
- `main_youthguest` -> `main_youthguestprofile` + `main_youthguestweek`

## Verification queries (run before drop)
```sql
SELECT COUNT(*) FROM main_injurycase;
SELECT COUNT(*) FROM main_hitweekplanentry;
SELECT COUNT(*) FROM main_dayprogramentry;
SELECT COUNT(*) FROM main_anthropometrysession;
SELECT COUNT(*) FROM main_anthropometrymeasurement;
SELECT COUNT(*) FROM main_nutritionintakesession;
SELECT COUNT(*) FROM main_nutritionintakeitem;
SELECT COUNT(*) FROM main_birthdayrecord;
SELECT COUNT(*) FROM main_youthguestweek;
```

## Drop phase (last step)
Only after preconditions + verification:
```sql
-- Example, do NOT run until approved:
-- DROP TABLE main_injury;
-- DROP TABLE main_hitweekplanning;
-- DROP TABLE main_dayprogram;
-- DROP TABLE main_antropometry;
-- DROP TABLE main_playerintake;
-- DROP TABLE main_birthday;
-- DROP TABLE main_youthguest;
```

Use template: `SQL_DROP_LEGACY_TEMPLATE.sql`
