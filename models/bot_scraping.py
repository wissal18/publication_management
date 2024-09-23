# -*- coding: utf-8 -*-
from odoo import models, fields, api
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)

class BotScraping(models.Model):
    _name = 'bot.scraping'

    @api.model
    def executer_scrap(self):
        # fonction éxecuté à partir d'un cron
        configurations = self.env["configurations.postes"].search([("type_activité","=","actif")])
        for conf in configurations:
            source = conf.source
            mots_clés = conf.mots_clés.split(',')
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
                           'Referer':     'https://www.google.com/',
                           'Cookie':     '_ga=GA1.1.1029889206.1724514217; fpestid=EmL0LCXietd1qVpxjhhj89eliXIy0xK_YaV1HBJIURQryjx12_IK5ZY6P3owuC1E6Nq5cg; PHPSESSID=ico1tfdgikgrqjlid223chkktk; cf_clearance=SispSbYEuxUTZasBYhVAqYe8quoIRT5jW.GvhsEiBVk-1725535017-1.2.1.1-sOdwjK7WlMdthHZ35dW.CYuORA61ACPhes4n1gb.5quBpVr4PA20pTP8jrploShC3tZlDAhCSUe7Eg3GPN089I7mCf.pgjsARoYJZTXYtWZr_FWmBb4ZsrwBR1.1Ecebo8UBD.GVaBVgK_sqIcjiQj.ga7REkW8.gVSBtcOdkYfNzUjljUboqbJjT_uYCR3xUra4wY14_Pbx9mMn_U89PWh0Vp_RMHqXUYkhfdKPqf92aIlVnLSkjEeb8OlD94rcmTSAOzOQOJrZqrxEWmmx9_nj2uSe.f.aWfo1jAAvFdNi_lxVy5iUsacmHB_K2q7sjrFTA8t98RWV9ihUF608oq8kEuNcREpDUWDYpi4o1K6zffYQHqTNiq4hEoCCg9S5hPaMH_mj.ayKbPQKD2JpQ3hJTrKe2S9aaCVhBqkfcevEFv1YtK87Z5qOIy7DCBcV; _ga_ZL9LBW1J59=GS1.1.1725540114.16.0.1725540114.0.0.0'}
                rep = requests.get(source, headers=headers)
                if rep.status_code == 200:
                    soup = BeautifulSoup(rep.content, 'html.parser')
                    publications = soup.find_all('article', class_='media well listing-item listing-item__jobs')
                    for pub in publications:
                        # suposons qu'on travaille avec l'url : https://www.tanitjobs.com/jobs/
                        titre_tag = pub.find('div', class_='media-heading listing-item__title').find('a')
                        titre = pub.text.strip()
                        lien = titre_tag['href']
                        description = pub.find('div', class_='listing-item__desc hidden-sm hidden-xs').text.strip()
                        publicateur = pub.find('span', class_='listing-item__info--item listing-item__info--item-company').text.strip()
                        date = pub.find('div', class_='listing-item__date').text.strip()

                        for mot_clé in mots_clés:
                            mot_clé = mot_clé.lower()
                            if mot_clé in titre.lower() or mot_clé in description.lower() :
                                publication = {
                                    'nom': titre,
                                    'lien': lien,
                                    'publicateur': publicateur,
                                    'description': description,
                                    'date_publication': datetime.strptime(date, '%d/%m/%Y').date()
                                }
                                self.env['publications.postes'].create(publication)
                else:
                    print(f'Requète échoué avec le code: {rep.status_code}')
            except Exception as e:
                 _logger.error("Erreur lors du scraping du site: %s", str(e))
