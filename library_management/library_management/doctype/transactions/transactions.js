// Copyright (c) 2023, pong and contributors
// For license information, please see license.txt

frappe.ui.form.on('Transactions', {
	after_save: function(frm) {
		frappe.call({
			method: 'library_management.api.update_stock',
			args: {
				type: frm.doc.type,
				title: frm.doc.title,
				docname: frm.doc.name,
				qty: frm.doc.qty,
				rent_fee: null
			},
		})
	},
	refresh: function(frm){
		if(frm.doc.docstatus == 1 && frm.doc.type == 'Issue'){
			frm.add_custom_button('Update Type', () => {
				let d = new frappe.ui.Dialog({
					title: 'Enter Type',
					fields: [
						{
							label: 'Type',
							fieldname: 'type',
							fieldtype: 'Select',
							options: 'Return',
							default: "Return"
						},
						{
							label: 'Rent Fee',
							fieldname: 'rent_fee',
							fieldtype: 'Float'
						},
					],
					primary_action_label: 'Submit',
					primary_action(values) {
						frappe.call({
							method: 'library_management.api.update_stock',
							args: {
								type: values.type,
								title: frm.doc.title,
								docname: frm.doc.name,
								qty: frm.doc.qty,
								rent_fee: values.rent_fee
							},
							callback:(r) =>{
								if(r.message == "done"){
									frappe.show_alert({
										message:__("Type is Updated"),
										indicator:'green'
									}, 5);
									
									frm.reload_doc();
								}
								else{
									frappe.show_alert({
										message:__("Can't Type status"),
										indicator:'yellow'
									}, 5);
								}
							}
						})
						d.hide();
					}
				});
				
				d.show();
			})
		}
	}
});
