import frappe
from m365_role_sync.m365_role_sync.utils import run_sync

def daily_sync():
    run_sync(silent=True)
