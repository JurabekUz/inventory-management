from django.core.management.base import BaseCommand
from django.db import transaction

from organization.models import Organization
from common.models import (
    Department,
    InventoryGroup,
    InventoryType,
    MeasureUnit,
    NumberTypes,
)


class Command(BaseCommand):
    help = 'Tashkilotlar uchun sinov maʼlumotlarini (Department, InventoryType, InventoryGroup, MeasureUnit) yaratadi.'

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                organizations = Organization.objects.all()
                if not organizations.exists():
                    self.stdout.write(
                        self.style.ERROR("Avval ma'lumotlar bazasida kamida bitta Organization modeli bo'lishi kerak."))
                    return

                self.stdout.write(self.style.SUCCESS("Ma'lumotlar bazasiga ma'lumotlar kiritilmoqda..."))

                self.create_departments(organizations)
                self.create_inventory_types(organizations)
                self.create_measure_units(organizations)
                self.create_inventory_groups(organizations)

                self.stdout.write(self.style.SUCCESS('✅ Barcha maʼlumotlar muvaffaqiyatli kiritildi.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ma'lumotlar kiritishda xatolik yuz berdi: {e}"))

    def create_departments(self, organizations):
        department_names = ['Buxgalteriya', 'Sotuv boʻlimi', 'Ishlab chiqarish', 'Marketing', 'IT boʻlimi', 'Omborxona']
        for org in organizations:
            for name in department_names:
                Department.objects.get_or_create(
                    organization=org,
                    name=name
                )
        self.stdout.write(self.style.SUCCESS('  - Boʻlimlar yaratildi.'))

    def create_inventory_types(self, organizations):
        inventory_type_names = ['Zaxira qismlar', 'Xomashyo / Material', 'Bir martalik sarf materiallari',
                                'Inventar jihoz']
        for org in organizations:
            for name in inventory_type_names:
                InventoryType.objects.get_or_create(
                    organization=org,
                    name=name
                )
        self.stdout.write(self.style.SUCCESS('  - Inventar turlari yaratildi.'))

    def create_measure_units(self, organizations):
        measure_unit_data = [
            {'name': 'dona', 'number_type': NumberTypes.integer},
            {'name': 'kg', 'number_type': NumberTypes.optional},
            {'name': 'metr', 'number_type': NumberTypes.optional},
            {'name': 'litr', 'number_type': NumberTypes.optional},
            {'name': 'komplekt', 'number_type': NumberTypes.integer},
            {'name': 'paket', 'number_type': NumberTypes.integer},
        ]
        for org in organizations:
            for unit in measure_unit_data:
                MeasureUnit.objects.get_or_create(
                    organization=org,
                    name=unit['name'],
                    defaults={'number_type': unit['number_type']}
                )
        self.stdout.write(self.style.SUCCESS('  - Oʻlchov birliklari yaratildi.'))

    def create_inventory_groups(self, organizations):
        inventory_group_names = {
            'Asosiy': ['Xizmat mashinalari', 'Mebel', 'Kompyuter texnikasi'],
            'Qoʻshimcha': ['Ofis jihozlari', 'Kanselyariya tovarlari', 'Xomashyo / Material'],
        }

        for org in organizations:
            # Asosiy guruhlarni yaratish
            for parent_name, children_names in inventory_group_names.items():
                parent_group, created = InventoryGroup.objects.get_or_create(
                    organization=org,
                    name=parent_name,
                    parent=None  # Asosiy guruh uchun parent None bo'ladi
                )

                # Bolakay guruhlarni yaratish
                for child_name in children_names:
                    InventoryGroup.objects.get_or_create(
                        organization=org,
                        name=child_name,
                        parent=parent_group
                    )
        self.stdout.write(self.style.SUCCESS('  - Inventar guruhlari yaratildi.'))
