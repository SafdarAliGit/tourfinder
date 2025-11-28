import frappe
from datetime import date

@frappe.whitelist()
def create_purchase_order(supplier, item_code, qty, rate, amount, po_name):
    try:
        # ------------------------------------
        # 1. Check if PO already exists
        # ------------------------------------
        existing_po = frappe.db.get_value(
            "Purchase Order",
            {"custom_purchase_order_item": po_name},
            "name"
        )

        if existing_po:
            frappe.throw(f"Purchase Order {existing_po} already created for this item.")

        # ------------------------------------
        # 2. Create new PO
        # ------------------------------------
        po = frappe.new_doc("Purchase Order")
        po.supplier = supplier
        po.schedule_date = date.today()

        po.append("items", {
            "item_code": item_code,
            "qty": float(qty or 0),
            "rate": float(rate or 0),
            "schedule_date": date.today()
        })

        po.custom_purchase_order_item = po_name

        po.insert(ignore_permissions=True)

        # ------------------------------------
        # 3. Update Purchase Detail Item
        # ------------------------------------
        frappe.db.set_value(
            "Purchase Detail Item",
            po_name,
            "po_number",
            po.name
        )

        frappe.db.commit()

        return po.name

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Create Purchase Order Error")
        return {"status": 'error', "message": str(e)}
