from odoo import models, fields, api

class RealEstate(models.Model):
    _name = 'real.estate'
    _description = 'Real Estate Property'

    name = fields.Char(string='Property Name', required=True)
    description = fields.Text(string='Description')
    address = fields.Char(string='Address')
    price = fields.Float(string='Price', required=True)
    bedrooms = fields.Integer(string='Bedrooms')
    bathrooms = fields.Integer(string='Bathrooms')
    living_area = fields.Float(string='Living Area (sqm)')
    garden_area = fields.Float(string='Garden Area (sqm)')
    area = fields.Float(string='Area (sqm)', compute='_compute_area', store=True)
    active = fields.Boolean(string='Active', default=True)
    date_available = fields.Date(string='Available From')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft')
    tag_ids = fields.Many2many('real.estate.tag', string='Tags')
    property_type_id = fields.Many2one('real.estate.property.type', string='Property Type')

    @api.depends('living_area', 'garden_area')
    def _compute_area(self):
        for record in self:
            record.area = record.living_area * record.garden_area