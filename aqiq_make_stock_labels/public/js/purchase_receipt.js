frappe.ui.form.on('Purchase Receipt', {
    refresh(frm) {
        var show_stock_label_btn = function(frm) {
            var show_btn = false;
            for(var d in frm.doc.items) {
                if(frm.doc.items[d].custom_box_qty) {
                    show_btn = true;
                    break;
                }
            }
            
            if(show_btn && frm.doc.docstatus != 2) {
                frm.add_custom_button(__("Make Stock Label"), function() {
                    frappe.call({
                        method: "aqiq_make_stock_labels.aqiq_make_stock_labels.api.make_purchase_stock_label",
                        args: {
                            'name': frm.doc.name
                        },
                        freeze: true,
                        callback: function(r) {
                            if(r.exc) {
                                frappe.msgprint(__("Something went wrong while creating Stock Label"));
                            }
                        }
                    });
                }).addClass('btn-primary');
            }
        }
        show_stock_label_btn(frm);
    }
}); 