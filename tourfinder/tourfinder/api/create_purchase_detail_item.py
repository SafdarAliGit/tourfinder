def create_purchase_detail_item(doc, method):
    existing_items = {row.item_code for row in doc.custom_purchase_detail_item}

    for item in doc.items:
        if item.item_code not in existing_items:
            # Add only if NOT already present
            doc.append("custom_purchase_detail_item", {
                "item_code": item.item_code,
                "qty": item.qty
            })
