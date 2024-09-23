# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime


class PostesPublications(models.Model):
    _name = 'publications.postes'
    _description = 'Publications Postes'

    nom = fields.Char("Nom", required=True)
    lien = fields.Char("Lien")
    publicateur = fields.Char("Publicateur", default="Anonyme")
    description = fields.Text("Description")
    date_publication = fields.Date("Date de publication", default=datetime.today())
    user_id = fields.Many2one('res.users', string='Utilisateur')

    @api.model
    def create(self, vals):
        existing_record = self.env["publications.postes"].sudo().search([('nom', '=', vals.get('nom')),
                                                                        ('publicateur', '=', vals.get('publicateur')),
                                                                        ('date_publication', '=', vals.get('date_publication'))])

        if existing_record:
            return existing_record
        return super(PostesPublications, self).create(vals)