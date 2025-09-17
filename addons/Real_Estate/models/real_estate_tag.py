from odoo import models, fields

class RealEstateTag(models.Model):
    _name = 'real.estate.tag'
    _description = 'Real Estate Tag'

    name = fields.Char(string='Tag Name', required=True, unique=True)
    color = fields.Integer(string='Color')