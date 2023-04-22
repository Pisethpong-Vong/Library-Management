// Copyright (c) 2023, pong and contributors
// For license information, please see license.txt

frappe.ui.form.on('Members', {
	before_save: function(frm) {
		frm.doc.full_name = frm.doc.first_name + frm.doc.last_name
	}
});
