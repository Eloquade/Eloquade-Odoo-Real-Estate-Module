from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class RealEstateOffer(models.Model):
    _name = 'real.estate.offer'
    _description = 'Real Estate Offer'
    _order = 'price desc'

    name = fields.Char(required=True, copy=False, default='New')
    partner_id = fields.Many2one('res.partner', string='Buyer', required=True)
    property_id = fields.Many2one('real.estate', string='Property', required=True, ondelete='cascade')
    price = fields.Float(required=True)
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
        ('pending', 'Pending')
    ], default='pending')
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
        store=True,
        default=lambda self: fields.Date.today() + relativedelta(days=7)
    )
    create_date = fields.Datetime(readonly=True)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        """Compute deadline from create_date or fallback to today."""
        for offer in self:
            base = fields.Date.to_date(offer.create_date) if offer.create_date else fields.Date.today()
            offer.date_deadline = base + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        """Update validity when deadline is changed."""
        for offer in self:
            if offer.date_deadline:
                base = fields.Date.to_date(offer.create_date) if offer.create_date else fields.Date.today()
                offer.validity = (offer.date_deadline - base).days
