# MySQL Backup / Restore Runbook (3NF)

## Aanbevolen vaste flow

Gebruik bij voorkeur het Django management command. Dat leest dezelfde database-instellingen als de site uit `.env`, maakt een consistente MySQL dump en zet die in `backups/`.

```bash
source venv/bin/activate
python manage.py backup_database
python manage.py verify_data_integrity
```

De backup-map staat in `.gitignore`, zodat databasebestanden niet per ongeluk naar GitHub gaan.

Voor een leesbare `.sql` zonder gzip:

```bash
python manage.py backup_database --plain-sql
```

Voor een andere opslaglocatie, bijvoorbeeld een externe map:

```bash
python manage.py backup_database --output-dir ~/DatabaseBackups/willemii
```

## 1) Full backup (schema + data)
Run from terminal (not in MySQL prompt):

```bash
mysqldump -u <user> -p --single-transaction --routines --triggers --databases willemii_dashboard > backup_willemii_dashboard_full.sql
```

## 2) Schema-only backup
```bash
mysqldump -u <user> -p --no-data --databases willemii_dashboard > backup_willemii_dashboard_schema.sql
```

## 3) Data-only backup
```bash
mysqldump -u <user> -p --no-create-info --databases willemii_dashboard > backup_willemii_dashboard_data.sql
```

## 4) Restore
```bash
mysql -u <user> -p < backup_willemii_dashboard_full.sql
```

## 5) Post-restore sanity checks
```sql
SELECT COUNT(*) FROM main_injurycase;
SELECT COUNT(*) FROM main_hitweekplanentry;
SELECT COUNT(*) FROM main_dayprogramentry;
SELECT COUNT(*) FROM main_anthropometrysession;
SELECT COUNT(*) FROM main_anthropometrymeasurement;
SELECT COUNT(*) FROM main_nutritionintakesession;
SELECT COUNT(*) FROM main_nutritionintakeitem;
```
