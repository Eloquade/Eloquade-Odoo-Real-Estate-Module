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
    selling_price = fields.Float(string='Selling Price', readonly=True)
    offer_ids = fields.One2many('real.estate.offer', 'property_id', string='Offers')
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
            
    
    @api.onchange('date_available')
    def _onchange_date_available(self):
        if self.date_available and self.date_available < fields.Date.today():
            self.date_available = fields.Date.today()
            return {
                'warning': {
                    'title': "Invalid Date",
                    'message': "The available date cannot be in the past. It has been reset to today.",
                }
            }