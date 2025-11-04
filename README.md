# M365 Role Sync

A lightweight ERPNext / Frappe app that synchronizes Microsoft Entra (M365) security‑group membership with ERPNext roles.

## Features

* Set Tenant / Client / Secret in "M365 Role Sync Config"
* Map Azure group IDs → ERPNext roles
* Press **Run Sync Now** or let the daily scheduler handle it

## Installation

```bash
bench get-app https://github.com/ealecho/m365_role_sync.git
bench install-app m365_role_sync
```

## Setup

1. Go to Integrations → M365 Role Sync Config
2. Add Tenant ID, Client ID, and Client Secret
3. Add your group‑to‑role mappings
4. Click **Run Sync Now**

## License

MIT
