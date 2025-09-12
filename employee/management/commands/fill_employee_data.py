import random
import datetime

from django.core.management.base import BaseCommand
from django.db import transaction

from common.models import Department
from organization.models import Organization
from employee.models import Position, Employee


class Command(BaseCommand):
    help = 'Tashkilotlar uchun mantiqiy pozitsiyalar va xodimlarni yaratadi.'

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                organizations = Organization.objects.all()
                if not organizations.exists():
                    self.stdout.write(
                        self.style.ERROR("Avval ma'lumotlar bazasida kamida bitta Organization modeli bo'lishi kerak."))
                    return

                self.stdout.write(self.style.SUCCESS("Mantiqiy lavozimlar va xodimlar kiritilmoqda..."))

                self.create_positions(organizations)
                self.create_employees(organizations)

                self.stdout.write(self.style.SUCCESS('✅ Barcha maʼlumotlar muvaffaqiyatli kiritildi.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ma'lumotlar kiritishda xatolik yuz berdi: {e}"))

    def create_positions(self, organizations):
        position_data = {
            'IT boʻlimi': ['Dasturchi', 'Tizim administratori', 'IT mutaxassisi'],
            'Buxgalteriya': ['Bosh buxgalter', 'Buxgalter', 'Moliyaviy menejer'],
            'Sotuv boʻlimi': ['Savdo menejeri', 'Sotuvchi', 'Mijozlar bilan ishlash mutaxassisi'],
            'Ishlab chiqarish': ['Ishlab chiqarish rahbari', 'Muhandis', 'Operator'],
            'Marketing': ['Marketing boʻlimi rahbari', 'Reklama menejeri', 'Kontent menejeri'],
            'Omborxona': ['Ombor mudiri', 'Yuk tashuvchi', 'Hisobchi']
        }

        for org in organizations:
            for department_name, positions in position_data.items():
                for pos_name in positions:
                    Position.objects.get_or_create(
                        organization=org,
                        name=pos_name,
                        full_name=f"{pos_name} ({department_name})",
                    )
        self.stdout.write(self.style.SUCCESS('  - Lavozimlar yaratildi.'))

    def create_employees(self, organizations):
        first_names = ['Ali', 'Vali', 'Guli', 'Sardor', 'Diyor', 'Nigina', 'Aziz', 'Shahnoza']
        last_names = ['Alimov', 'Valiyev', 'Qodirova', 'Sobirov', 'Hamidov', 'Sharipova', 'Rahimov', 'Karimova']

        position_data = {
            'IT boʻlimi': ['Dasturchi', 'Tizim administratori'],
            'Buxgalteriya': ['Bosh buxgalter', 'Buxgalter'],
            'Sotuv boʻlimi': ['Savdo menejeri'],
            'Ishlab chiqarish': ['Muhandis', 'Operator'],
            'Marketing': ['Reklama menejeri'],
            'Omborxona': ['Ombor mudiri', 'Yuk tashuvchi']
        }

        for org in organizations:
            self.stdout.write(f'  -> {org.name} uchun xodimlar yaratilmoqda...')
            for dep_name, pos_names in position_data.items():
                try:
                    department = Department.objects.get(organization=org, name=dep_name)
                except Department.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f"    - '{dep_name}' boʻlimi topilmadi. Oʻtkazib yuborilmoqda..."))
                    continue

                for pos_name in pos_names:
                    try:
                        position = Position.objects.get(organization=org, name=pos_name)
                    except Position.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(f"    - '{pos_name}' lavozimi topilmadi. Oʻtkazib yuborilmoqda..."))
                        continue

                    for _ in range(random.randint(1, 4)):
                        employee_name = f"{random.choice(first_names)} {random.choice(last_names)}"
                        from_date = datetime.date.today() - datetime.timedelta(days=random.randint(30, 1000))

                        Employee.objects.get_or_create(
                            organization=org,
                            name=employee_name,
                            department=department,
                            position=position,
                            from_date=from_date
                        )
        self.stdout.write(self.style.SUCCESS('  - Xodimlar yaratildi.'))
