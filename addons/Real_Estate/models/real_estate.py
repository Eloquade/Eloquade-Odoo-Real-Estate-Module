from odoo import models, fields, api
from odoo.exceptions import ValidationError

class RealEstate(models.Model):
    _name = 'real.estate'
    _description = 'Real Estate Property'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _sql_constraints = [
    # 1. Unique property name (no two properties with the same name)
    ('unique_property_name', 'unique(name)', 'The property name must be unique.'),

    # 2. Price must be greater than 0
    ('check_price_positive', 'CHECK(price > 0)', 'The price must be greater than zero.'),

    # 3. Selling price must be positive if set
    ('check_selling_price_positive', 'CHECK(selling_price >= 0)', 'The selling price must be zero or positive.'),

    # 4. Living area must be positive
    ('check_living_area_positive', 'CHECK(living_area >= 0)', 'The living area must be zero or positive.'),

    # 5. Garden area must be positive
    ('check_garden_area_positive', 'CHECK(garden_area >= 0)', 'The garden area must be zero or positive.'),

    # 6. Bedrooms cannot be negative
    ('check_bedrooms_non_negative', 'CHECK(bedrooms >= 0)', 'The number of bedrooms cannot be negative.'),

    # 7. Bathrooms cannot be negative
    ('check_bathrooms_non_negative', 'CHECK(bathrooms >= 0)', 'The number of bathrooms cannot be negative.'),

    # 8. Available date must be in the future (or today)
    ('check_available_date_future', "CHECK(date_available IS NULL OR date_available >= CURRENT_DATE)", 
     'The available date must be today or in the future.'),

    # 9. Selling price cannot be higher than listed price
    ('check_selling_price_less_than_price', 
     'CHECK(selling_price <= price)', 
     'The selling price cannot be greater than the listed price.'),

    # 10. Area consistency check (optional)
    ('check_area_consistency',
     'CHECK(area >= 0)',
     'The total area must be zero or positive.')
    ]

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
    
    @api.constrains('area')
    def _check_area(self):
        for record in self:
            if record.area < 10:
                raise models.ValidationError("The total area must be at least 10 sqm.")

    def action_mark_sold(self):
        for record in self:
            if record.state != 'sold':
                record.state = 'sold'
                record.selling_price = record.price
            else:
                raise models.ValidationError("The property is already marked as sold.")
    
    def action_mark_cancelled(self):
        for record in self:
            if record.state != 'cancelled':
                record.state = 'cancelled'
            else:
                raise models.ValidationError("The property is already marked as cancelled.")
            