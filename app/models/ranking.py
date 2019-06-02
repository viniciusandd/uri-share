from app.models.tables import Postagem

class Ranking:
    def __init__(self, postagens):
        self.postagens = postagens

    def montar_podium(self):        
        podium = []
        cont = 0
        for postagem in self.postagens:
            if cont == 3:
                break
            podium.append(postagem)
            cont = cont + 1
        return podium