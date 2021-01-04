# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Patient(models.Model):
    _name = 'hospital.patient'
    _description = 'Patient'
    _rec_name = 'name_seq'
    
    name = fields.Char('Name', required=True)
    name_seq = fields.Char('ID', required=True, readonly=True, default=lambda self: 'New')
    gender = fields.Selection([
        ('0', 'Male'),
        ('1', 'Female')
    ], string='Gender', required=True)
    age = fields.Integer('Age', required=True)
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'fair'),
        ('seriuos', 'Serious'),
        ('critical', 'Critical'),
        ('dead', 'Dead')
    ], string='State determine', readonly=True, default=lambda self: 'undetermined', required=True)
    description = fields.Text('Description')
    doctor_id = fields.Many2one('res.users', string="Doctor")
    assessments = fields.One2many('hospital.assessment', 'patient_id', string='Assessments')

    @api.model
    def create(self, vals):
        if vals.get('name_seq', 'New') == 'New':
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or 'New'
        return super(Patient, self).create(vals)

    @api.one
    @api.constrains('age')
    def _check_age(self):
        if self.age < 0:
            raise ValidationError('Age must be non nagative')

