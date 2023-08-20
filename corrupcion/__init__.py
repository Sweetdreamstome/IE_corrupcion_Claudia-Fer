from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'corrupcion'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 5
    dotacion = 50
    Ciudadano1_ROLE = 'Ciudadano1'
    Ciudadano2_ROLE = 'Ciudadano2'
    Oficial_ROLE = 'Oficial'
    Monitor_ROLE = 'Monitor'

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    soborno = models.BooleanField()
    soborno_aceptado = models.BooleanField()


class Player(BasePlayer):
    ofrecer_soborno = models.BooleanField(
        choices = [
            [False, 'No ofrecer soborno'],
            [True, 'Ofrecer soborno']
        ]
    )

    aceptar_soborno = models.BooleanField(
        choices=[
            [False, 'No aceptar soborno'],
            [True, 'Aceptar soborno']
        ]
    )

    castigar_soborno = models.BooleanField()
    no_castigar_soborno = models.BooleanField()

    castigar_soborno_ambos = models.BooleanField()
    no_castigar_soborno_ambos = models.BooleanField()
    castigar_soborno_ciudadano = models.BooleanField()
    castigar_soborno_oficial = models.BooleanField()

    monto_ciudadano_sinSoborno = models.IntegerField(min=1, max=10, blank=True)
    ambos_monto_ciudadano_conSoborno = models.IntegerField(min=1, max=10, blank=True)
    ambos_monto_oficial_conSoborno = models.IntegerField(min=1, max=10, blank=True)
    monto_ciudadano_conSoborno = models.IntegerField(min=1, max=10, blank=True)
    monto_oficial_conSoborno = models.IntegerField(min=1, max=10, blank=True)




# PAGES
class Instrucciones(Page):
    pass

class Instrucciones_roles(Page):
    pass

class Preguntas_control(Page):
    form_model = 'player'
    form_fields = []
    #5 variables.
    #2 tipos de pregunta


class WaitPage_Ciudadano1(WaitPage):
    @staticmethod
    def is_displayed(player):
        return player.role == 'Ciudadano1'


class WaitPage_Ciudadano2(WaitPage):
    @staticmethod
    def is_displayed(player):
        return player.role == 'Ciudadano2'

class WaitPage_Oficial(WaitPage):
    @staticmethod
    def is_displayed(player):
        return player.role == 'Oficial'

class WaitPage_Monitor(WaitPage):
    @staticmethod
    def is_displayed(player):
        return player.role == 'Monitor'

class Ciudadano1(Page):
    form_model = 'player'
    form_fields = ['ofrecer_soborno']

    @staticmethod
    def is_displayed(player):
        return player.role == 'Ciudadano1'

class WaitPageSoborno(WaitPage):
    def after_all_players_arrive(group:Group):
        for p in group.get_players():
            if p.id_in_group == 1:
                group.soborno = p.ofrecer_soborno

class Oficial(Page):
    form_model = 'player'
    form_fields = ['aceptar_soborno']

    @staticmethod
    def is_displayed(player):
        return player.group.soborno and player.role == 'Oficial'

class WaitPageAceptarSoborno(WaitPage):
    def is_displayed(player):
        group = player.group
        return group.soborno

    def after_all_players_arrive(group:Group):
        for p in group.get_players():
            if p.id_in_group == 3:
                group.soborno_aceptado = p.aceptar_soborno

class MonitorsinSoborno(Page):

    form_model = 'player'
    form_fields = ['castigar_soborno', 'no_castigar_soborno', 'monto_ciudadano_sinSoborno']

    @staticmethod
    def is_displayed(player):
        group = player.group
        return (not player.group.soborno_aceptado) and player.role == 'Monitor' and group.soborno

class MonitorconSoborno(Page):

    form_model = 'player'
    form_fields = ['castigar_soborno_ambos', 'no_castigar_soborno_ambos', 'castigar_soborno_ciudadano', 'castigar_soborno_oficial', 'ambos_monto_ciudadano_conSoborno', 'ambos_monto_oficial_conSoborno', 'monto_oficial_conSoborno', 'monto_ciudadano_conSoborno' ]

    @staticmethod
    def is_displayed(player):
        group = player.group
        return player.group.soborno_aceptado and player.role == 'Monitor' and group.soborno

class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(group:Group):
        pass

class Resultados(Page):
    pass


page_sequence = [Instrucciones,
                 Instrucciones_roles,
                 Preguntas_control,
                 WaitPage_Ciudadano2,
                 WaitPage_Oficial,
                 WaitPage_Monitor,
                 Ciudadano1,
                 WaitPageSoborno,
                 WaitPage_Ciudadano1,
                 WaitPage_Ciudadano2,
                 WaitPage_Monitor,
                 Oficial,
                 WaitPageAceptarSoborno,
                 WaitPage_Ciudadano1,
                 WaitPage_Ciudadano2,
                 WaitPage_Oficial,
                 MonitorsinSoborno,
                 MonitorconSoborno,
                 ResultsWaitPage,
                 Resultados]
