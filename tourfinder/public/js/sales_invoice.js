
frappe.ui.form.on("Purchase Detail Item", {
    create_po: function (frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        if (row.qty > 0 && row.rate > 0 && row.supplier) {
            frappe.call({
                method: "tourfinder.tourfinder.api.create_purchase_order.create_purchase_order",
                args: {
                    "supplier": row.supplier,
                    "item_code": row.item_code,
                    "qty": row.qty,
                    "rate": row.rate,
                    "amount": row.amount,
                    "po_name": row.name
                },
                callback: function (r) {
                    if (r.message) {
                        frappe.msgprint("Purchase Order created: " + r.message);
                        frm.refresh()
                    }
                }
            });
        } else {
            frappe.msgprint("Please enter qty, rate and supplier");
        }

    }
});