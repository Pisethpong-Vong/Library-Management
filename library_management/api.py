import frappe
import math
import requests

doctype_books = 'Books'
doctype_transactions = 'Transactions'
doctype_cut_stock_book = 'Cut Stock Book'

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

    page = {
        "current_page": int(page_number),
        "last_page": math.ceil(total / per_page),
        "total": total
    }
    
    response = {
        'listdata': data_response,
        "pages": page
    }

    frappe.response["message"] = response

@frappe.whitelist()
def update_stock(type, title, docname, qty, rent_fee):
    book_stock = frappe.db.get_list(doctype_books, filters={'name': title}, pluck='book_stock', ignore_permissions=True)[0]

    if type == 'Issue':
        update = frappe.get_doc(doctype_books, title)
        update.book_stock = int(book_stock) - int(qty)
        update.save(ignore_permissions=True)
        
    else:
        returns = frappe.get_doc(doctype_transactions, docname)
        returns.type = type
        returns.rent_fee = rent_fee
        returns.save(ignore_permissions=True)

        if returns:
            update = frappe.get_doc(doctype_books, title)
            update.book_stock = int(book_stock) + int(qty)
            update.save(ignore_permissions=True)

            return "done"

@frappe.whitelist(allow_guest=True)
def create_book():
    data_url = requests.get(f"https://frappe.io/api/method/frappe-library?page=2&title=and").json()

    data = data_url.get('message')

    for i in data:
        doc = frappe.new_doc(doctype_books)
        doc.title = i.title
        doc.authors = i.authors
        doc.isbn = i.isbn
        doc.publisher = i.publisher
        doc.insert(ignore_permissions=True)

    frappe.response["message"] = "Saved Successfully"