from odoo import models, fields

class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many('real.estate', 'salesman_id', string='Properties')
