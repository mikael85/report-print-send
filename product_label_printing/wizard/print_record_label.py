# -*- coding: utf-8 -*-
# Copyright (C) 2016 SYLEAM (<http://www.syleam.fr>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields


class PrintProductLabel(models.TransientModel):
    _name = 'wizard.print.zpl2.product.label'
    _description = 'Imprimir Etiquetas de Productos'

    printer_id = fields.Many2one(
        comodel_name='printing.printer', string='Impresora', required=True,
        help='Impresora que será usada para la impresión de etiquetas.')
    label_id = fields.Many2one(
        comodel_name='printing.label.zpl2', string='Modelo de Etiquetas', required=True,
        domain=lambda self: [
            # ('model_id.model', '=', self.env.context.get('active_model'))],
            ('model_id.model', '=', 'product.product')],
        help='Modelo de etiquetas a utilizar.')
    line_ids = fields.Many2many(
        'wizard.print.zpl2.product.label.line',
        'wizardpzpl2',
        'wizard_id',
        'line_id',
         string=u'Líneas a imprimir')

    @api.model
    def default_get(self, fields_list):
        values = super(PrintProductLabel, self).default_get(fields_list)

        # Automatically select the printer and label, if only one is available
        printers = self.env['printing.printer'].search([])
        if len(printers) == 1:
            values['printer_id'] = printers.id

        labels = self.env['printing.label.zpl2'].search([
            ('model_id.model', '=', 'product.product'),
        ])
        if len(labels) == 1:
            values['label_id'] = labels.id

        active_ids = self._context.get('active_ids', [])
        active_model = self._context.get('active_model')

        # Itera sobre los hijos de cada template y los agrega con cantidad 1
        if active_model == 'product.template':
            products = self.env['product.template'].browse(
                active_ids).mapped('product_variant_ids')
        elif active_model == 'product.product':
            products = self.env['product.product'].browse(active_ids)
        line_ids = []
        for product in products:
            line_ids.append((0, False, {'product_id': product and product.id, 'qty': 1}))
        
        values['line_ids'] = line_ids
        return values

    @api.multi
    def print_label(self):
        """ Prints a label line.qty times per selected record """
        # record_model = self.env.context['active_model']
        record_model = 'product.product'
        for line in self.line_ids:
            # for i in range(line.qty):
            #     self.label_id.print_label(self.printer_id, line.product_id)            
            self.label_id.print_label(self.printer_id, line.product_id, page_count=line.qty)

class PrintProductLabelLine(models.TransientModel):
    _name = 'wizard.print.zpl2.product.label.line'

    product_id = fields.Many2one('product.product', string='Producto')
    qty = fields.Integer(
        string='Cantidad', help='Cantidad de etiquetas a imprimir de este producto.')
