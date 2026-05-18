import gzip
import os
import shutil
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Maakt een consistente MySQL-backup van de Django database."

    def add_arguments(self, parser):
        parser.add_argument(
            "--output-dir",
            default=str(settings.BASE_DIR / "backups"),
            help="Map waarin de backup wordt geplaatst. Default: <project>/backups",
        )
        parser.add_argument(
            "--plain-sql",
            action="store_true",
            help="Schrijf .sql in plaats van .sql.gz.",
        )
        parser.add_argument(
            "--keep-days",
            type=int,
            default=30,
            help="Verwijder backups van deze database ouder dan dit aantal dagen. Gebruik 0 om opruimen uit te zetten.",
        )

    def handle(self, *args, **options):
        db = settings.DATABASES["default"]
        engine = db.get("ENGINE", "")
        if "mysql" not in engine:
            raise CommandError(f"backup_database ondersteunt nu alleen MySQL, niet: {engine}")

        dump_bin = shutil.which("mysqldump")
        if dump_bin is None:
            raise CommandError("mysqldump is niet gevonden. Installeer/activeer MySQL client tools.")

        name = db.get("NAME")
        user = db.get("USER")
        password = db.get("PASSWORD") or ""
        host = db.get("HOST") or "localhost"
        port = str(db.get("PORT") or "3306")

        if not name or not user:
            raise CommandError("Database NAME en USER moeten ingesteld zijn.")

        output_dir = Path(options["output_dir"]).expanduser().resolve()
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        suffix = "sql" if options["plain_sql"] else "sql.gz"
        output_path = output_dir / f"{name}_{timestamp}.{suffix}"

        command = [
            dump_bin,
            f"--host={host}",
            f"--port={port}",
            f"--user={user}",
            "--single-transaction",
            "--routines",
            "--triggers",
            "--databases",
            name,
        ]

        env = os.environ.copy()
        if password:
            env["MYSQL_PWD"] = password

        self.stdout.write(f"Backup maken voor database '{name}'...")
        try:
            if options["plain_sql"]:
                with output_path.open("wb") as dump_file:
                    subprocess.run(command, env=env, stdout=dump_file, stderr=subprocess.PIPE, check=True)
            else:
                with gzip.open(output_path, "wb") as dump_file:
                    subprocess.run(command, env=env, stdout=dump_file, stderr=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError as exc:
            message = exc.stderr.decode("utf-8", errors="replace").strip()
            raise CommandError(f"mysqldump mislukt: {message}") from exc

        size_mb = output_path.stat().st_size / (1024 * 1024)
        self.stdout.write(self.style.SUCCESS(f"Backup opgeslagen: {output_path} ({size_mb:.2f} MB)"))

        keep_days = options["keep_days"]
        if keep_days and keep_days > 0:
            cutoff = datetime.now() - timedelta(days=keep_days)
            removed = 0
            for candidate in output_dir.glob(f"{name}_*.sql*"):
                if candidate == output_path or not candidate.is_file():
                    continue
                modified_at = datetime.fromtimestamp(candidate.stat().st_mtime)
                if modified_at < cutoff:
                    candidate.unlink()
                    removed += 1
            self.stdout.write(self.style.SUCCESS(f"Oude backups opgeruimd: {removed} ouder dan {keep_days} dagen."))
