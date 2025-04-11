{
    'name': 'Purchase Vendor Filter',
    'version': '1.0',
    'summary': 'Adds Vendor filter under Agreement in RFQ',
    'author': 'Prithvi',

    'depends': ['purchase'],  # Required for view inheritance
    'data': [
    'views/purchase_order_views.xml',
    'views/purchase_order_line_view.xml'# Ensure this matches exactly
],
    'installable': True,
    'application': False,
}
