from odoo import models, fields, api

class RealEstatePropertyType(models.Model):
    _name = 'real.estate.property.type'
    _description = 'Real Estate Property Type'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)
    property_ids = fields.One2many('real.estate', 'property_type_id', string='Properties')
    property_count = fields.Integer(string='Property Count', compute='_compute_property_count')

    def action_open_properties(self):
        return {
            'name': 'Properties',
            'type': 'ir.actions.act_window',
            'res_model': 'real.estate',
            'view_mode': 'list,form',
            'target': 'current',
            'domain': [('property_type_id', '=', self.id)],
            'context': {'default_property_type_id': self.id},
        }
    
    @api.depends('property_ids')
    def _compute_property_count(self):
        for record in self:
            record.property_count = len(record.property_ids)