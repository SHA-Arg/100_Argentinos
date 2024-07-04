class Comodin:

    def init(self):
        self.disponible = True

    def activar(self):
        if self.disponible:
            print("El comodín ya ha sido usado en esta partida.")
            return False
        else:
            self.disponible = True
            print("El comodín ha sido activado.")
            return True

    def reiniciar(self):
        self.disponible = True
        print("El comodín está disponible para la siguiente partida.")
