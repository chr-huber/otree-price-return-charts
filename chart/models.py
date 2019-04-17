from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import csv
import random

author = """
Christoph Huber

Christoph.huber@uibk.ac.as
www.chr-huber.com

"""

doc = """
otree-price-return-chart
"""


class Constants(BaseConstants):
    name_in_url = 'chart'
    players_per_group = 2
    num_rounds = 6

    time_per_return = 500

    riskfree = 0.9

    initial_wealth = 5000


class Subsession(BaseSubsession):

    def creating_session(self):
        if self.round_number == 1:
            for p in self.get_players():
                p.participant.vars['count'] = []

                month = [0]
                init_wealth = [Constants.initial_wealth]
                percentage = [0]
                end_wealth = [Constants.initial_wealth]
                history = list(zip(month, init_wealth, percentage, end_wealth))
                p.participant.vars['history'] = history

                p.random_data = random.randint(1, 6)

                # --- Load Data from .csv ---
                with open("chart/static/chart/data" + str(p.random_data) + ".csv") as datacsv:
                    prices = []
                    returns = []
                    reader = csv.reader(datacsv, delimiter=';')
                    next(reader)
                    for row in reader:
                        prices.append(row[0])
                        returns.append(row[1])

                #    prices = [i[0] for i in prices]
                prices = [float(i) for i in prices]

                #    returns = [i[0] for i in returns]
                returns = [float(i) for i in returns]

                p.participant.vars['returns'] = returns
                p.participant.vars['prices'] = prices

                # --- Load Monthly Returns from .csv ---
                with open("chart/static/chart/mreturns.csv") as datacsv:
                    mreturns = []
                    reader = csv.reader(datacsv, delimiter=';')
                    next(reader)
                    for row in reader:
                        mreturns.append(row)

                mreturns = [i[p.random_data-1] for i in mreturns]
                mreturns = [float(i) for i in mreturns]

                p.participant.vars['returns'] = returns
                p.participant.vars['prices'] = prices
                p.participant.vars['mreturns'] = mreturns

                p.participant.vars['returns1'] = returns


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    random_data = models.IntegerField(blank=True)

    investment = models.FloatField(blank=True)
    rate = models.IntegerField(blank=True)
    risk = models.IntegerField(blank=True)
    fc = models.FloatField(blank=True)
    fc_p05 = models.FloatField(blank=True)
    fc_p95 = models.FloatField(blank=True)

    monthly_return = models.FloatField(blank=True)

    def write_variables(self):
        if self.round_number < Constants.num_rounds:
            self.monthly_return = self.participant.vars['mreturns'][self.round_number - 1]
