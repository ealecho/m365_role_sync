import frappe
import requests

@frappe.whitelist()
def run_sync(docname=None, silent=False):
    """Manual trigger callable from button or API"""
    if not docname:
        doc = frappe.get_all("M365 Role Sync Config", filters={"active": 1}, limit=1)
        if not doc:
            return "No active configuration found."
        doc = frappe.get_doc("M365 Role Sync Config", doc[0].name)
    else:
        doc = frappe.get_doc("M365 Role Sync Config", docname)

    token_resp = requests.post(
        f"https://login.microsoftonline.com/{doc.tenant_id}/oauth2/v2.0/token",
        data={
            "grant_type": "client_credentials",
            "scope": "https://graph.microsoft.com/.default",
            "client_id": doc.client_id,
            "client_secret": doc.get_password("client_secret"),
        },
        timeout=20,
    ).json()
    access_token = token_resp.get("access_token")
    if not access_token:
        frappe.throw("Failed to obtain Graph API token")

    headers = {"Authorization": f"Bearer {access_token}"}
    users = requests.get(
        "https://graph.microsoft.com/v1.0/users?$select=id,mail",
        headers=headers,
        timeout=25,
    ).json().get("value", [])

    role_map = {i.group_id: i.erp_role for i in doc.role_mappings}
    changed = 0

    for u in users:
        email = u.get("mail")
        if not email or not frappe.db.exists("User", email):
            continue

        groups_resp = requests.get(
            f"https://graph.microsoft.com/v1.0/users/{u['id']}/memberOf?$select=id",
            headers=headers,
            timeout=20,
        ).json()
        group_ids = [g["id"] for g in groups_resp.get("value", [])]
        mapped_roles = [r for gid, r in role_map.items() if gid in group_ids]

        user = frappe.get_doc("User", email)
        current = {r.role for r in user.roles}
        new = set(mapped_roles)
        if new != current:
            user.remove_roles(*current)
            if new:
                user.add_roles(*new)
            user.flags.ignore_permissions = True
            user.save()
            changed += 1

    msg = f"M365 sync complete — {changed} users updated."
    frappe.logger().info(msg)
    if not silent:
        return msg
    return None
