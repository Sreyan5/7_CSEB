"""
Dictionary management functions for Contact Directory & Stock Tracker.

This module demonstrates Python dictionaries, safe value retrieval (.get()),
dictionary iteration (.keys(), .values(), .items()), dictionary methods
(.update(), .pop(), .setdefault(), .copy()), and modular package design.
"""

# Global dictionary storing supplier/customer contact records.
contact_directory = {
    "C101": {
        "name": "Arindam Chatterjee",
        "phone": "9830112233",
        "email": "arindam.c@kolkatatech.in",
        "role": "Hardware Supplier",
        "city": "Kolkata"
    },
    "C102": {
        "name": "Sneha Mukherjee",
        "phone": "9831445566",
        "email": "sneha.m@easternlog.com",
        "role": "Wholesale Distributor",
        "city": "Howrah"
    },
    "C103": {
        "name": "Rajeshwar Sen",
        "phone": "9433778899",
        "email": "rsen@bbitstore.org",
        "role": "Campus Coordinator",
        "city": "Budge Budge"
    }
}

# Global dictionary storing product inventory and stock records.
stock_inventory = {
    "P201": {
        "item_name": "Wireless Optical Mouse",
        "category": "Peripherals",
        "quantity": 45,
        "unit_price": 650.00,
        "reorder_level": 15,
        "supplier_id": "C101"
    },
    "P202": {
        "item_name": "Mechanical Keyboard RGB",
        "category": "Peripherals",
        "quantity": 8,
        "unit_price": 2400.00,
        "reorder_level": 10,
        "supplier_id": "C101"
    },
    "P203": {
        "item_name": "USB-C Multiport Hub",
        "category": "Accessories",
        "quantity": 6,
        "unit_price": 1850.00,
        "reorder_level": 12,
        "supplier_id": "C102"
    },
    "P204": {
        "item_name": "27-inch IPS Monitor",
        "category": "Displays",
        "quantity": 18,
        "unit_price": 14500.00,
        "reorder_level": 5,
        "supplier_id": "C102"
    }
}

# Global variable: counts total dictionary operations across the session.
operation_count = 0


def record_operation():
    """Increase the global operation count after each dictionary action."""
    global operation_count
    operation_count += 1


def add_or_update_contact(contact_id, name, phone, email, role="General Contact", city="Kolkata"):
    """Add a new contact or update an existing contact record using setdefault() and update()."""
    contact_id = contact_id.strip().upper()
    if not contact_id or not name.strip() or not phone.strip():
        raise ValueError("Contact ID, Name, and Phone cannot be empty.")

    record = contact_directory.setdefault(contact_id, {})
    record.update({
        "name": name.strip(),
        "phone": phone.strip(),
        "email": email.strip(),
        "role": role.strip(),
        "city": city.strip()
    })
    record_operation()
    return contact_directory.get(contact_id).copy()


def get_contact_safe(contact_id, default_message="Contact ID not found in directory."):
    """Safely retrieve a contact dictionary using .get() without raising KeyError."""
    contact_id = contact_id.strip().upper()
    record_operation()
    return contact_directory.get(contact_id, default_message)


def remove_contact(contact_id):
    """Remove and return a contact entry safely using .pop() with a default fallback."""
    contact_id = contact_id.strip().upper()
    removed = contact_directory.pop(contact_id, None)
    if removed is None:
        raise ValueError(f"Contact ID '{contact_id}' does not exist.")
    record_operation()
    return removed


def list_all_contacts():
    """Iterate over contact_directory using .items() and return key-value pairs."""
    record_operation()
    return list(contact_directory.items())


def add_or_update_stock(product_id, item_name, category, quantity, unit_price, reorder_level=10, supplier_id="C101"):
    """Add or update a product stock record using dictionary .setdefault() and .update()."""
    product_id = product_id.strip().upper()
    if quantity < 0:
        raise ValueError("Stock quantity cannot be negative.")
    if unit_price <= 0:
        raise ValueError("Unit price must be greater than zero.")
    if reorder_level < 0:
        raise ValueError("Reorder level cannot be negative.")

    entry = stock_inventory.setdefault(product_id, {})
    entry.update({
        "item_name": item_name.strip(),
        "category": category.strip(),
        "quantity": int(quantity),
        "unit_price": float(unit_price),
        "reorder_level": int(reorder_level),
        "supplier_id": supplier_id.strip().upper()
    })
    record_operation()
    return stock_inventory.get(product_id).copy()


def adjust_stock_quantity(product_id, delta_quantity):
    """Adjust stock quantity for an existing product using safe .get() lookup and .update()."""
    product_id = product_id.strip().upper()
    product = stock_inventory.get(product_id)
    if product is None:
        raise ValueError(f"Product ID '{product_id}' not found in stock tracker.")

    new_qty = product.get("quantity", 0) + int(delta_quantity)
    if new_qty < 0:
        raise ValueError(f"Insufficient stock. Current quantity is {product.get('quantity', 0)}.")

    product.update({"quantity": new_qty})
    record_operation()
    return product.copy()


def get_product_safe(product_id, default_message="Product ID not found in stock tracker."):
    """Retrieve a product record safely using .get() and attach supplier details via .get()."""
    product_id = product_id.strip().upper()
    record_operation()
    product = stock_inventory.get(product_id)
    if product is None:
        return default_message

    enriched = product.copy()
    sup_id = enriched.get("supplier_id", "N/A")
    supplier_info = contact_directory.get(sup_id, {})
    enriched["supplier_name"] = supplier_info.get("name", "Unknown Supplier")
    enriched["supplier_phone"] = supplier_info.get("phone", "N/A")
    return enriched


def remove_product(product_id):
    """Remove a product from stock_inventory using dictionary .pop()."""
    product_id = product_id.strip().upper()
    removed = stock_inventory.pop(product_id, None)
    if removed is None:
        raise ValueError(f"Product ID '{product_id}' does not exist in inventory.")
    record_operation()
    return removed


def get_low_stock_items():
    """Iterate over stock_inventory.items() to filter items at or below reorder_level."""
    record_operation()
    low_stock = {}
    for pid, details in stock_inventory.items():
        if details.get("quantity", 0) <= details.get("reorder_level", 0):
            low_stock[pid] = details.copy()
    return low_stock


def calculate_inventory_valuation():
    """Iterate over stock_inventory.values() and .keys() to compute total stock valuation."""
    record_operation()
    total_skus = len(stock_inventory.keys())
    total_units = 0
    total_value = 0.0

    for item in stock_inventory.values():
        qty = item.get("quantity", 0)
        price = item.get("unit_price", 0.0)
        total_units += qty
        total_value += qty * price

    return {
        "total_skus": total_skus,
        "total_units": total_units,
        "total_valuation": round(total_value, 2),
        "total_contacts": len(contact_directory.keys()),
        "operations_performed": operation_count
    }


def get_operation_count():
    """Return total dictionary operations executed."""
    return operation_count