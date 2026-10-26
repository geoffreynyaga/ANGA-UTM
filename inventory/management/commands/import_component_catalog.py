import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from inventory.models import AircraftModel, ComponentType, Tag

DEFAULT_CATALOG = Path(__file__).resolve().parents[2] / "catalog" / "dji_agras_t50.json"


class DryRun(Exception):
    pass


class Command(BaseCommand):
    help = (
        "Import a parts catalog JSON file into the shared component catalog. "
        "Existing entries are matched by part number and updated; images are left alone. "
        "No stock, units or requests are created."
    )

    def add_arguments(self, parser):
        parser.add_argument("path", nargs="?", default=str(DEFAULT_CATALOG))
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be created or updated, then roll back.",
        )

    def handle(self, *args, path, dry_run, **options):
        catalog = json.loads(Path(path).read_text())
        part_numbers = {part["part_number"] for part in catalog["parts"]}
        for part in catalog["parts"]:
            parent = part.get("parent")
            if parent and parent not in part_numbers:
                raise CommandError(
                    f"{part['part_number']}: parent {parent} is not in the catalog."
                )

        try:
            with transaction.atomic():
                summary = self.import_catalog(catalog)
                if dry_run:
                    raise DryRun
        except DryRun:
            self.stdout.write(self.style.WARNING(f"Dry run, nothing saved. {summary}"))
            return
        self.stdout.write(self.style.SUCCESS(summary))

    def import_catalog(self, catalog):
        aircraft, _ = AircraftModel.objects.get_or_create(**catalog["aircraft"])
        tags = {}

        def tag(name):
            name = name.strip().lower()
            if name not in tags:
                tags[name] = Tag.objects.get_or_create(name=name)[0]
            return tags[name]

        saved = {}
        created = 0
        for part in catalog["parts"]:
            component_type, was_created = ComponentType.objects.update_or_create(
                part_number=part["part_number"],
                defaults={
                    "name": part["name"],
                    "diagram_name": part["diagram_name"],
                    "diagram_number": part["diagram_number"],
                    "is_serialized": part.get("is_serialized", False),
                    "status": ComponentType.APPROVED,
                },
            )
            created += was_created
            component_type.aircraft_models.add(aircraft)
            component_type.tags.add(*[tag(name) for name in part["tags"]])
            saved[part["part_number"]] = component_type

        # Set parents after every row exists, so file order does not matter.
        for part in catalog["parts"]:
            component_type = saved[part["part_number"]]
            parent = saved.get(part.get("parent"))
            if component_type.parent_id != (parent.pk if parent else None):
                component_type.parent = parent
                component_type.save(update_fields=["parent"])

        total = len(catalog["parts"])
        return f"{total} parts for {aircraft}: {created} created, {total - created} updated."
