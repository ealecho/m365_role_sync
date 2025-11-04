frappe.ui.form.on("M365 Role Sync Config", {
	refresh(frm) {
		if (!frm.is_new()) {
			frm.add_custom_button("Run Sync Now", () => {
				frappe.call({
					method: "m365_role_sync.m365_role_sync.utils.run_sync",
					args: { docname: frm.doc.name },
					freeze: true,
					freeze_message: "Synchronizing roles from Microsoft 365...",
					callback(r) {
						frappe.msgprint(r.message || "Done");
					},
				});
			});
		}
	},
});
