import frappe
import math

doctype_books = 'Books'

@frappe.whitelist(allow_guest=True)
def library_book(**kwargs):
    '''
    function api response pagination for books.
    param : kwargs
    '''
    
    kwargs = frappe._dict(kwargs)

    page_number = int(kwargs.get('current_page', 1))

    per_page = 20
    
    all_book = frappe.db.get_list(doctype_books, fields=['name'], ignore_permissions=True)
    
    total = len(all_book)

    all_book = [all_book[i:i+per_page] for i in range(0, total, per_page)]

    if 0 <= page_number and page_number <= math.ceil(total / per_page):
        all_book = all_book[page_number - 1]

    else:
        all_book = []

    datalist = []

    for s in all_book:
        datalist.append(s.name)

    data_response = frappe.db.get_list(doctype_books, fields=['name', 'title', 'authors', 'isbn', 'publisher', 'page'], filters={'name': ['in', datalist]}, ignore_permissions=True)

    meta = {
        "current_page": int(page_number),
        "last_page": math.ceil(total / per_page),
        "total": total
    }
    
    response = {
        'listdata': data_response,
        "meta": meta
    }

    frappe.response["message"] = response
