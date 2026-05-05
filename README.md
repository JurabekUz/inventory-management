# Asset & Inventory Management System with QR Integration

A robust, enterprise-grade Inventory Management System built with Python/Django, designed to streamline organizational asset tracking, employee assignments, and stocktaking processes using QR-code technology.

## 🚀 Key Features

- **QR-Code Integration:** Scan and verify assets instantly using built-in QR code functionality for efficient check-ins/check-outs.
- **Organization & Multi-role Management:** Comprehensive structure for managing departments, organizations, and hierarchical user roles.
- **Employee Asset Tracking:** Track which assets are assigned to which employees with a full history log.
- **Stocktaking & Inventory Control:** Real-time stock monitoring and automated stocktaking modules to prevent discrepancies.
- **Contract Management:** Handle legal and operational contracts related to asset procurement and assignments.
- **Modular Architecture:** Clean separation of concerns with dedicated apps for `inventory`, `contract`, `organization`, and `users`.

## 🛠 Tech Stack

- **Backend:** Python 3.x, Django, Django REST Framework (DRF)
- **Database:** PostgreSQL (recommended)
- **Other:** QR Code Generation/Scanning logic, Service-Layer Architecture

## 📂 Project Structure

```text
├── config/           # Project settings and WSGI/ASGI configuration
├── inventory/        # Asset management and stock logic
├── organization/     # Corporate structure and branches
├── employee/         # Staff management and asset assignment
├── stocktaking/      # Auditing and inventory verification
├── contract/         # Documentation and procurement contracts
├── users/            # Custom User model and Authentication
├── common/ & utils/  # Reusable mixins, helpers, and base classes
└── manage.py         # Django entry point
