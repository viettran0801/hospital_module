# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Assessment(models.Model):
    _name = 'hospital.assessment'
    _description = 'Assessment'
    _rec_name = 'name_seq'

    name_seq = fields.Char('ID', required=True, readonly=True, default=lambda self: 'New') 
    
    doctor_id = fields.Many2one('res.users', string="Doctor", required=True, default=lambda self: self.env.user, readonly=True)
    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)
    note = fields.Text('Notes', required=True)
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('seriuos', 'Serious'),
        ('critical', 'Critical'),
        ('dead', 'Dead')
    ], string='State determine', required=True)

    @api.model
    def create(self, vals):
        patient = self.env['hospital.patient'].browse(vals['patient_id'])
        patient.sudo().write({'state': vals['state']})

        if vals.get('name_seq', 'New') == 'New':
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.assessment.sequence') or 'New'
        return super(Assessment, self).create(vals)
    
 
    

        