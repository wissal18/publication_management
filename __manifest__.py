{
    'name': 'Publications Postes',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',

        'data/scraping_cron.xml',

        'views/publications_postes_views.xml',
        'views/configurations_postes_views.xml'
    ],
    'installable': True,
    'application': True
}
