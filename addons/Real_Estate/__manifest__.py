{
    'name': 'Real Estate',
    'version': '18.0.1.0.0',
    'summary': 'Manage real estate properties, offers, and sales',
    'description': 'A module to manage real estate properties, offers, and sales in Odoo.',
    'author': 'Your Name or Company',
    'website': 'https://yourcompany.com',
    'category': 'Real Estate',
    'depends': ['base'],
    'data': [
        'views/real_estate_property_views.xml',
        'views/real_estate_property_type_views.xml',
        'views/real_estate_tag_views.xml',
        'security/ir.model.access.csv',
        
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}