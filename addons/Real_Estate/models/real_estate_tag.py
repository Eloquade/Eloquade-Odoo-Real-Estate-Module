from odoo import models, fields

class RealEstateTag(models.Model):
    _name = 'real.estate.tag'
    _description = 'Real Estate Tag'
    _sql_constraints = [
        ('unique_tag_name', 'unique(name)', 'The tag name must be unique.')
    ]
    
    name = fields.Char(string='Tag Name', required=True, unique=True)
    color = fields.Integer(string='Color')