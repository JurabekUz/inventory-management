import random
import datetime

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from organization.models import Organization
from inventory.models import Inventory
from employee.models import Employee
from users.models import User
from stocktaking.models import Stocktaking, Inspection


class Command(BaseCommand):
    help = 'Belgilangan tashkilot uchun inventarizatsiya va tekshirish maʼlumotlarini yaratadi.'

    def add_arguments(self, parser):
        parser.add_argument('organization_id', type=str, help='Maʼlumotlar yaratiladigan tashkilotning IDsi.')

    def handle(self, *args, **options):
        organization_id = options['organization_id']

        try:
            organization = Organization.objects.get(id=organization_id)
        except Organization.DoesNotExist:
            raise CommandError(f'IDsi {organization_id} boʻlgan tashkilot topilmadi.')

        try:
            with transaction.atomic():
                inventories = list(Inventory.objects.filter(organization=organization)[::2])
                employees = list(Employee.objects.filter(organization=organization))
                users = list(User.objects.filter(org=organization))

                if not inventories or not employees or not users:
                    self.stdout.write(self.style.ERROR(
                        f"Tashkilot '{organization.name}' uchun yetarli ma'lumotlar (Inventory, Employee yoki User) topilmadi."
                    ))
                    return

                self.stdout.write(self.style.SUCCESS(
                    f"Tashkilot '{organization.name}' uchun inventarizatsiya va tekshirish ma'lumotlari kiritilmoqda..."
                ))

                self.create_stocktaking_and_inspections(inventories, employees, users)

                self.stdout.write(self.style.SUCCESS('✅ Barcha maʼlumotlar muvaffaqiyatli kiritildi.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ma'lumotlar kiritishda xatolik yuz berdi: {e}"))

    def create_stocktaking_and_inspections(self, inventories, employees, users):

        for inventory in inventories:
            random_employee = random.choice(employees)
            stocktaking_date = inventory.date + datetime.timedelta(days=random.randint(10, 30))

            stocktaking, created = Stocktaking.objects.get_or_create(
                inventory=inventory,
                employee=random_employee,
                defaults={
                    'date': stocktaking_date,
                    'terminate_date': stocktaking_date + datetime.timedelta(days=random.randint(1, 5))
                }
            )

            if created:
                self.stdout.write(f'  -> {inventory.name} uchun inventarizatsiya yozuvi yaratildi.')

            inspection_count = random.randint(3, 4)
            for _ in range(inspection_count):
                random_user = random.choice(users)
                created_at = stocktaking.date + datetime.timedelta(days=random.randint(1, 5))

                Inspection.objects.get_or_create(
                    stocktaking=stocktaking,
                    user=random_user,
                    defaults={'created_at': created_at}
                )
                self.stdout.write(f'    -> Tekshirish yozuvi qoʻshildi.')
