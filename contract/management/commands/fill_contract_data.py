import random
import datetime

from django.core.management.base import BaseCommand
from django.db import transaction

from organization.models import Organization
from contract.models import Contract


class Command(BaseCommand):
    help = 'Tashkilotlar uchun sinov shartnomalari (Contract) yaratadi.'

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                organizations = Organization.objects.all()
                if not organizations.exists():
                    self.stdout.write(
                        self.style.ERROR("Avval ma'lumotlar bazasida kamida bitta Organization modeli bo'lishi kerak."))
                    return

                self.stdout.write(self.style.SUCCESS("Shartnoma ma'lumotlari kiritilmoqda..."))

                self.create_contracts(organizations)

                self.stdout.write(self.style.SUCCESS('✅ Shartnoma maʼlumotlari muvaffaqiyatli kiritildi.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ma'lumotlar kiritishda xatolik yuz berdi: {e}"))

    def create_contracts(self, organizations):
        suppliers = ['Artel', 'Texno-Makon', 'MediaPark', 'Elmakon', 'Asaxiy']

        for org in organizations:
            self.stdout.write(f'  -> {org.name} uchun shartnomalar yaratilmoqda...')
            for i in range(1, random.randint(3, 7)):  # Har bir tashkilot uchun 3 dan 7 gacha shartnoma yaratamiz
                contract_number = f'{random.randint(1000, 9999)}-{i}'
                contract_date = datetime.date.today() - datetime.timedelta(days=random.randint(30, 365))
                contract_supplier = random.choice(suppliers)
                contract_description = f'{contract_supplier}dan uskuna sotib olish boʻyicha shartnoma.'

                Contract.objects.get_or_create(
                    organization=org,
                    number=contract_number,
                    defaults={
                        'date': contract_date,
                        'description': contract_description,
                        'supplier': contract_supplier
                    }
                )
        self.stdout.write(self.style.SUCCESS('  - Shartnomalar yaratildi.'))
