import frappe
import requests

def get_context(context):
    data = requests.get(f"https://frappe.io/api/method/frappe-library?page=2&title=and").json()

    test = data.get('message')

    context.data = test

    return context