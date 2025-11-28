# -*- coding: utf-8 -*-
{
    'name': 'Pritunl VPN Management',
    'version': '17.0.1.0.0',
    'category': 'Tools',
    'summary': 'Complete Pritunl VPN Server Management',
    'description': """
Pritunl VPN Management
======================
Complete management system for Pritunl VPN Server with:
* Dynamic API credentials configuration
* Organization management
* User management with subscription control
* Server management (create, start, stop, restart)
* Host management
* Site-to-site VPN links
* Automatic synchronization
* Subscription-based user activation/deactivation
* Full audit logging
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': [
        'base',
        'mail',
    ],
    'data': [
        # Security
        'security/security.xml',
        'security/ir.model.access.csv',

        # Data
        'data/cron.xml',

        # Views
        'views/pritunl_config_views.xml',
        'views/pritunl_organization_views.xml',
        'views/pritunl_user_views.xml',
        'views/pritunl_server_views.xml',
        'views/pritunl_host_views.xml',
        'views/pritunl_link_views.xml',
        'views/res_partner_views.xml',
        'views/pritunl_menu.xml',
    ],
    'external_dependencies': {
        'python': ['requests'],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
