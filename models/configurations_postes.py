# -*- coding: utf-8 -*-
from odoo import models, fields

class ConfigurationsPostes(models.Model):
    _name = 'configurations.postes'
    _description = 'configurations des postes'

    nom = fields.Char("Nom du poste")
    type_activité = fields.Selection([("actif",     "Actif"),
                                      ("inactif",   "Inactif"),
                                      ("en_attente","En Attente")], string="Etat", required=True, default="actif")
    mots_clés = fields.Char("Mots clés", help="les mots clés doivent être séparés par des virgules.")
    source = fields.Char("Site source")