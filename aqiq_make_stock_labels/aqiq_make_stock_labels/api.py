import frappe

@frappe.whitelist()
def make_purchase_stock_label(name):
    check = frappe.db.get_value(
        "Purchase Stock Label", {"purchase_receipt": name}, "name"
    )
    if check:
        link_field = "<a href='/app/purchase-stock-label/{0}'>{0}</a>".format(check)
        frappe.throw("Purchase Stock Label already exists " + link_field)
    
    self = frappe.get_doc("Purchase Receipt", name)
    new = frappe.new_doc("Purchase Stock Label")
    new.company = self.company
    new.purchase_receipt = self.name
    new.posting_date = self.posting_date
    new.supplier = self.supplier
    new.supplier_name = self.supplier_name
    
    for i in self.items:
        if i.get("custom_box_qty"):
            try:
                count_range = int(i.get("custom_box_qty"))
                idx = 1
                for z in range(count_range):
                    auto_case_no = f"{self.name}-{str(idx).zfill(5)}"
                    idx += 1
                    new.append(
                        "table_nuas",
                        {
                            "item_code": i.get("item_code"),
                            "item_name": i.get("item_name"),
                            "packing_box_qty": i.get("custom_box_qty"),
                            "qty": i.get("qty"),
                            "rate": i.get("rate"),
                            "case_no": auto_case_no,
                            "description": i.description,
                            "sheets_in_box": i.get("sheets_in_box", 0),
                        },
                    )
            except (ValueError, TypeError):
                frappe.msgprint(f"Invalid box quantity for item {i.get('item_code')}")
                continue

    if new.get("table_nuas"):
        new.insert(
            ignore_permissions=True,
            ignore_mandatory=True,
        )
        link_field = "<a href='/app/purchase-stock-label/{0}'>{0}</a>".format(new.name)
        frappe.msgprint("Stock Label has been created " + link_field)
    else:
        frappe.msgprint("No items with box quantity found in the Purchase Receipt")