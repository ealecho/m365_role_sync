app_name = "m365_role_sync"
app_title = "M365 Role Sync"
app_publisher = "Your Name"
app_description = "Sync Microsoft 365 / Entra groups to ERPNext roles"
app_email = "you@example.com"
app_license = "MIT"

scheduler_events = {
    "daily": [
        "m365_role_sync.m365_role_sync.tasks.daily_sync"
    ]
}
