# -*- coding: utf-8 -*-
# Copyright (C) 2016 SYLEAM (<http://www.syleam.fr>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Impresión de etiquetas de productos ZPL II',
    'version': '9.0.1.1.0',
    'category': 'Printer',
    'author': 'Idea Software, Micael Gómez',
    'website': 'http://ideasoftware.com.ar',
    'license': 'AGPL-3',
    'depends': [
        'printer_zpl2',
    ],
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/printing_label_zpl2.xml',
        'wizard/print_record_label.xml',
    ],
    'installable': True,
}
