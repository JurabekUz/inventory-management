import random
import datetime

from django.core.management.base import BaseCommand
from django.db import transaction

from organization.models import Organization
from common.models import InventoryGroup, InventoryType, MeasureUnit
from contract.models import Contract
from inventory.models import Inventory


class Command(BaseCommand):
    help = 'Tashkilotlar uchun sinov inventar maʼlumotlarini yaratadi.'

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                organizations = Organization.objects.all()
                if not organizations.exists():
                    self.stdout.write(
                        self.style.ERROR("Avval ma'lumotlar bazasida kamida bitta Organization modeli bo'lishi kerak."))
                    return

                self.stdout.write(self.style.SUCCESS("Inventar ma'lumotlari kiritilmoqda..."))

                self.create_inventories(organizations)

                self.stdout.write(self.style.SUCCESS('✅ Barcha inventar maʼlumotlari muvaffaqiyatli kiritildi.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ma'lumotlar kiritishda xatolik yuz berdi: {e}"))

    def create_inventories(self, organizations):
        # Mantiqiy bog'liqlikni ta'minlash uchun ma'lumotlar
        inventory_data = {
            'Kompyuter texnikasi': {
                'type': 'Inventar jihoz',
                'measure_unit': 'dona',
                'names': ['Noutbuk', 'Monitor', 'Tizim blok', 'Klaviatura', 'Sichqoncha']
            },
            'Mebel': {
                'type': 'Inventar jihoz',
                'measure_unit': 'dona',
                'names': ['Ofis stoli', 'Ofis stuli', 'Shkaf', 'Sofa']
            },
            'Kanselyariya tovarlari': {
                'type': 'Bir martalik sarf materiallari',
                'measure_unit': 'paket',
                'names': ['A4 qogʻozi', 'Flomaster', 'Qalam toʻplami']
            },
            'Xomashyo / Material': {
                'type': 'Xomashyo / Material',
                'measure_unit': ['kg', 'litr'],
                'names': ['Yogʻoch', 'Metall', 'Plastik granulalar', 'Boʻyoq']
            },
        }

        for org in organizations:
            self.stdout.write(f'  -> {org.name} uchun inventarlar yaratilmoqda...')

            # Mavjud Contract, InventoryType, MeasureUnit va InventoryGroup ma'lumotlarini olish
            contracts = list(Contract.objects.filter(organization=org))
            inventory_types = {obj.name: obj for obj in InventoryType.objects.filter(organization=org)}
            measure_units = {obj.name: obj for obj in MeasureUnit.objects.filter(organization=org)}
            inventory_groups = {obj.name: obj for obj in
                                InventoryGroup.objects.filter(organization=org, parent__isnull=False)}

            if not contracts or not inventory_types or not measure_units or not inventory_groups:
                self.stdout.write(self.style.WARNING(
                    f"    - '{org.name}' uchun yetarli ma'lumotlar topilmadi. O'tkazib yuborilmoqda."))
                continue

            for group_name, data in inventory_data.items():
                if group_name not in inventory_groups:
                    self.stdout.write(
                        self.style.WARNING(f"    - '{group_name}' inventar guruhi topilmadi. Oʻtkazib yuborilmoqda..."))
                    continue

                # Topilgan InventoryGroup obyektini olish
                group = inventory_groups[group_name]

                for inventory_name in data['names']:
                    # Mantiqiy bog'liqlik asosida model obyektlarini olish
                    inv_type = inventory_types.get(data['type'])

                    if isinstance(data['measure_unit'], list):
                        unit_name = random.choice(data['measure_unit'])
                    else:
                        unit_name = data['measure_unit']

                    measure_unit = measure_units.get(unit_name)

                    # Agar kerakli obyekt topilmasa, keyingi qadamga o'tish
                    if not inv_type or not measure_unit:
                        self.stdout.write(self.style.WARNING(
                            f"    - '{inventory_name}' uchun kerakli 'type' yoki 'measure_unit' topilmadi. Oʻtkazib yuborilmoqda..."))
                        continue

                    # Tasodifiy contract tanlash
                    random_contract = random.choice(contracts)

                    # Yangi inventar yaratish
                    amount = random.randint(1, 20)
                    price = random.randint(100000, 5000000)
                    total_value = amount * price
                    date = datetime.date.today() - datetime.timedelta(days=random.randint(30, 365))

                    Inventory.objects.get_or_create(
                        organization=org,
                        name=inventory_name,
                        full_name=f"{inventory_name} - {random_contract.number}",
                        group=group,
                        type=inv_type,
                        contract=random_contract,
                        measure_unit=measure_unit,
                        amount=amount,
                        price=price,
                        total_value=total_value,
                        qqs=random.choice([True, False]),
                        date=date,
                    )

        self.stdout.write(self.style.SUCCESS('  - Inventar yozuvlari yaratildi.'))
