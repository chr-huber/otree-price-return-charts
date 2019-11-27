from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from django.utils.translation import ugettext as _

class Chart(Page):

    form_model = 'player'
    form_fields = [
        'investment',
        'rate',
        'risk',
        'fc',
        'fc_p05',
        'fc_p95'
    ]

    def is_displayed(self):
        return self.player.id_in_group == 3

    def vars_for_template(self):
        return {
            'prices': self.player.participant.vars['prices'],
            'returns': self.player.participant.vars['returns'],
            'page': self.subsession.round_number,
            'num_pages': Constants.num_rounds - 1,
            'mreturns': self.player.participant.vars['mreturns'],
            'mreturn': self.player.participant.vars['mreturns'][self.subsession.round_number - 2] * 100
        }

    def before_next_page(self):
        self.player.write_variables()


class Chart1(Page):

    form_model = 'player'
    form_fields = [
        'investment',
        'rate',
        'risk',
        'fc',
        'fc_p05',
        'fc_p95'
    ]

    def is_displayed(self):
        return self.player.id_in_group == 1 or self.player.id_in_group == 2

    def vars_for_template(self):
        return {
            'prices': self.player.participant.vars['prices'],
            'returns': self.player.participant.vars['returns'],
            'page': self.subsession.round_number,
            'num_pages': Constants.num_rounds - 1,
            'mreturns': self.player.participant.vars['mreturns'],
            'mreturn': self.player.participant.vars['mreturns'][self.subsession.round_number - 2] * 100
        }

    def before_next_page(self):
        self.player.write_variables()




class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


class Results(Page):
    pass


page_sequence = [
    Chart,
    Chart1
]
