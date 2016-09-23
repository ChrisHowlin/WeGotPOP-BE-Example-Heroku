# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, lurl
from tg import request, redirect, tmpl_context
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.exceptions import HTTPFound
from tg import predicates
from wegotpopbeexample import model
from wegotpopbeexample.controllers.secure import SecureController
from wegotpopbeexample.model import DBSession
from tgext.admin.tgadminconfig import BootstrapTGAdminConfig as TGAdminConfig
from tgext.admin.controller import AdminController

from wegotpopbeexample.lib.base import BaseController
from wegotpopbeexample.controllers.error import ErrorController

from wegotpopbeexample.controllers import ArtistFileService
from wegotpopbeexample.controllers import BasicRelevanceStrategy,\
                                          RelaxedRelevanceStrategy,\
                                          BlendedRelevanceStrategy,\
                                          ArtistFileService
from wegotpopbeexample.controllers.validators import AgeValidation,\
                                                     LocationValidation,\
                                                     RateValidation,\
                                                     GenderValidation

__all__ = ['RootController']

strategy_dict = { 'basic' : BasicRelevanceStrategy.BasicRelevanceStrategy,
                  'relaxed' : RelaxedRelevanceStrategy.RelaxedRelevanceStrategy,
                  'blended' : BlendedRelevanceStrategy.BlendedRelevanceStrategy }

class RootController(BaseController):
    """
    The root controller for the WeGotPOP-BE-Example application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::

        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.

    """
    secc = SecureController()
    admin = AdminController(model, DBSession, config_type=TGAdminConfig)

    error = ErrorController()

    def _before(self, *args, **kw):
        tmpl_context.project_name = "wegotpopbeexample"

    @expose('wegotpopbeexample.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict(page='index')

    @expose('json')
    def artists(self, age_min=None, age_max=None, age_wgt=None,
                      loc_lat=None, loc_lon=None, loc_rad=None, loc_wgt=None,
                      rate_max=None, rate_wgt=None,
                      gender=None, gender_wgt=None,
                      relevance='basic'):
        service = ArtistFileService.ArtistFileService('wegotpopbeexample/controllers/artists.json')

        validated_age = AgeValidation.validate_age(age_min, age_max, age_wgt)
        validated_location = LocationValidation.validate_location(loc_lat,
                                                                  loc_lon,
                                                                  loc_rad,
                                                                  loc_wgt)
        validated_rate = RateValidation.validate_rate(rate_max, rate_wgt)
        validated_gender = GenderValidation.validate_gender(gender, gender_wgt)

        # Use service 
        artists = service.get_artists()

        strategy = strategy_dict[relevance]
        filtered_artists = strategy().apply(artists,
                                            validated_age,
                                            validated_location,
                                            validated_rate, 
                                            validated_gender)

        return filtered_artists
        # return '{}'

    @expose('wegotpopbeexample.templates.about')
    def about(self):
        """Handle the 'about' page."""
        return dict(page='about')
