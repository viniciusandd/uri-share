from datetime import datetime

class Funcoes(object):
    def retornar_data_atual():
        data_e_hora_atuais = datetime.now()
        data_e_hora_em_texto = data_e_hora_atuais.strftime('%Y-%m-%d')
        return data_e_hora_em_texto

    def retornar_hora_atual():
        data_e_hora_atuais = datetime.now()
        data_e_hora_em_texto = data_e_hora_atuais.strftime('%H:%M:%S')
        return data_e_hora_em_texto



