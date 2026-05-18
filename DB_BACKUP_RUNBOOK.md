# MySQL Backup / Restore Runbook (3NF)

## Aanbevolen vaste flow

Gebruik bij voorkeur het Django management command. Dat leest dezelfde database-instellingen als de site uit `.env`, maakt een consistente MySQL dump en zet die in `backups/`.

```bash
source venv/bin/activate
python manage.py backup_database --keep-days 30
python manage.py verify_data_integrity
```

De backup-map staat in `.gitignore`, zodat databasebestanden niet per ongeluk naar GitHub gaan.

`--keep-days 30` bewaart de laatste 30 dagen en ruimt oudere backups automatisch op. Gebruik `--keep-days 0` als je nooit automatisch wilt opruimen.

## Automatische server-backup met cron

Open op de server de root crontab:

```bash
crontab -e
```

Voeg deze regel toe om elke nacht om 03:15 een backup te maken:

```cron
15 3 * * * cd /var/www/Dashboard-Willem-II- && /var/www/Dashboard-Willem-II-/venv/bin/python manage.py backup_database --output-dir /var/backups/willemii-dashboard --keep-days 30 >> /var/log/willemii-dashboard-backup.log 2>&1
```

Maak de backupmap alvast aan:

```bash
mkdir -p /var/backups/willemii-dashboard
```

Handmatig testen:

```bash
cd /var/www/Dashboard-Willem-II-
/var/www/Dashboard-Willem-II-/venv/bin/python manage.py backup_database --output-dir /var/backups/willemii-dashboard --keep-days 30
python manage.py verify_data_integrity
```

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
