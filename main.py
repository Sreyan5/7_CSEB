"""
CONTACT DIRECTORY & STOCK TRACKER
Main program: displays an interactive menu and applies dictionary operations
for managing business contacts and product inventory.
"""

from tracker_package.directory_stock import (
    stock_inventory,
    add_or_update_contact,
    get_contact_safe,
    remove_contact,
    list_all_contacts,
    add_or_update_stock,
    adjust_stock_quantity,
    get_product_safe,
    remove_product,
    get_low_stock_items,
    calculate_inventory_valuation,
    get_operation_count
)


def read_int(prompt):
    """Read an integer and retry if input is non-numeric."""
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def read_float(prompt):
    """Read a floating-point number and retry if input is invalid."""
    while True:
        try:
            return float(input(prompt).strip())
        except ValueError:
            print("Invalid input. Please enter a valid numeric amount.")


def show_menu():
    """Display all Contact Directory and Stock Tracker operations."""
    print("\n======== CONTACT DIRECTORY & STOCK TRACKER ========")
    print("1. View All Contacts (Iterate .items())")
    print("2. Search Contact Safely (.get() Method)")
    print("3. Add / Update Contact (.setdefault() & .update())")
    print("4. Delete Contact (.pop() Method)")
    print("5. View All Stock Inventory (Iterate .items())")
    print("6. Search Product & Supplier Info (.get() Lookup)")
    print("7. Add / Update Product Stock (.update() Method)")
    print("8. Adjust Stock Quantity (Restock / Sale)")
    print("9. Remove Product from Stock (.pop() Method)")
    print("10. Low-Stock Reorder Alert Report")
    print("11. Inventory Valuation & Dictionary Summary (.values())")
    print("0. Exit")
    print("===================================================")


def main():
    # 'running' is a local variable inside main().
    running = True

    while running:
        show_menu()
        choice = input("Choose an option (0-11): ").strip()

        try:
            if choice == "1":
                contacts = list_all_contacts()
                print(f"\n--- Contact Directory ({len(contacts)} records) ---")
                for cid, info in contacts:
                    print(
                        f"[{cid}] {info.get('name')} | Phone: {info.get('phone')} | "
                        f"Email: {info.get('email')} | Role: {info.get('role')} ({info.get('city')})"
                    )

            elif choice == "2":
                cid = input("Enter Contact ID to search (e.g., C101): ").strip()
                result = get_contact_safe(cid)
                if isinstance(result, dict):
                    print("\nContact Found:")
                    for key, val in result.items():
                        print(f"  {key.capitalize()}: {val}")
                else:
                    print("Lookup Result:", result)

            elif choice == "3":
                cid = input("Enter Contact ID (e.g., C104): ").strip()
                name = input("Enter Full Name: ").strip()
                phone = input("Enter Phone Number: ").strip()
                email = input("Enter Email Address: ").strip()
                role = input("Enter Role (press Enter for 'General Contact'): ").strip()
                city = input("Enter City (press Enter for 'Kolkata'): ").strip()
                role_val = role if role else "General Contact"
                city_val = city if city else "Kolkata"
                updated = add_or_update_contact(cid, name, phone, email, role_val, city_val)
                print(f"Contact '{cid.upper()}' saved successfully:", updated)

            elif choice == "4":
                cid = input("Enter Contact ID to delete: ").strip()
                removed = remove_contact(cid)
                print(f"Removed Contact '{cid.upper()}': {removed.get('name')} ({removed.get('phone')})")

            elif choice == "5":
                print(f"\n--- Current Stock Inventory ({len(stock_inventory)} SKUs) ---")
                for pid, item in stock_inventory.items():
                    total_val = item.get("quantity", 0) * item.get("unit_price", 0.0)
                    print(
                        f"[{pid}] {item.get('item_name')} ({item.get('category')}) | "
                        f"Qty: {item.get('quantity')} | Unit Price: Rs.{item.get('unit_price'):.2f} | "
                        f"Reorder Level: {item.get('reorder_level')} | Value: Rs.{total_val:.2f}"
                    )

            elif choice == "6":
                pid = input("Enter Product ID to search (e.g., P201): ").strip()
                result = get_product_safe(pid)
                if isinstance(result, dict):
                    print("\nProduct & Linked Supplier Details:")
                    for key, val in result.items():
                        print(f"  {key}: {val}")
                else:
                    print("Lookup Result:", result)

            elif choice == "7":
                pid = input("Enter Product ID (e.g., P205): ").strip()
                name = input("Enter Item Name: ").strip()
                category = input("Enter Category: ").strip()
                qty = read_int("Enter Initial Quantity: ")
                price = read_float("Enter Unit Price (Rs.): ")
                reorder_text = input("Enter Reorder Level (press Enter for default 10): ").strip()
                sup_text = input("Enter Supplier Contact ID (press Enter for default C101): ").strip()
                reorder_val = int(reorder_text) if reorder_text else 10
                sup_val = sup_text if sup_text else "C101"
                saved = add_or_update_stock(pid, name, category, qty, price, reorder_val, sup_val)
                print(f"Product '{pid.upper()}' updated in stock inventory:", saved)

            elif choice == "8":
                pid = input("Enter Product ID (e.g., P202): ").strip()
                delta = read_int("Enter quantity change (+ to restock, - to deduct): ")
                updated_item = adjust_stock_quantity(pid, delta)
                print(f"Updated '{updated_item.get('item_name')}' -> New Quantity: {updated_item.get('quantity')}")

            elif choice == "9":
                pid = input("Enter Product ID to remove: ").strip()
                removed = remove_product(pid)
                print(f"Removed Product '{pid.upper()}': {removed.get('item_name')}")

            elif choice == "10":
                low_items = get_low_stock_items()
                if not low_items:
                    print("\nAll products are sufficiently stocked above reorder levels.")
                else:
                    print(f"\n--- LOW STOCK ALERT ({len(low_items)} items require reorder) ---")
                    for pid, details in low_items.items():
                        print(
                            f"ALERT [{pid}] {details.get('item_name')}: Current Qty = {details.get('quantity')} "
                            f"(Reorder Level = {details.get('reorder_level')}) | Supplier ID = {details.get('supplier_id')}"
                        )

            elif choice == "11":
                summary = calculate_inventory_valuation()
                print("\n--- Inventory Valuation & Dictionary Summary ---")
                print(f"Total Distinct Products (.keys()) : {summary.get('total_skus')}")
                print(f"Total Stock Units (.values())     : {summary.get('total_units')}")
                print(f"Total Inventory Value (Rs.)       : Rs.{summary.get('total_valuation'):,.2f}")
                print(f"Total Directory Contacts          : {summary.get('total_contacts')}")
                print(f"Session Dictionary Operations     : {summary.get('operations_performed')}")

            elif choice == "0":
                running = False
                print("Thank you for using Contact Directory & Stock Tracker!")

            else:
                print("Invalid menu choice. Please choose an option from 0 to 11.")

        except ValueError as err:
            print("Error:", err)


if __name__ == "__main__":
    main()