import json
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction

from inventory.models import AircraftModel, ComponentType, Tag

DEFAULT_CATALOG = Path(__file__).resolve().parents[2] / "catalog" / "dji_agras_t50.json"


class Command(BaseCommand):
    help = (
        "Import a parts catalog JSON file into the shared component catalog. "
        "Existing entries are matched by part number and updated; images are left alone."
    )

    def add_arguments(self, parser):
        parser.add_argument("path", nargs="?", default=str(DEFAULT_CATALOG))

    @transaction.atomic
    def handle(self, *args, path, **options):
        catalog = json.loads(Path(path).read_text())
        aircraft, _ = AircraftModel.objects.get_or_create(**catalog["aircraft"])

        created = 0
        for part in catalog["parts"]:
            component_type, was_created = ComponentType.objects.update_or_create(
                part_number=part["part_number"],
                defaults={
                    "name": part["name"],
                    "diagram_name": part["diagram_name"],
                    "diagram_number": part["diagram_number"],
                    "status": ComponentType.APPROVED,
                },
            )
            created += was_created
            component_type.aircraft_models.add(aircraft)
            component_type.tags.add(
                *[Tag.objects.get_or_create(name=name.lower())[0] for name in part["tags"]]
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"{len(catalog['parts'])} parts for {aircraft}: "
                f"{created} created, {len(catalog['parts']) - created} updated."
            )
        )
