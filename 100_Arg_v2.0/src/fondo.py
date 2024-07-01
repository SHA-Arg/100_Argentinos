from .utils import cargar_imagen


class Fondo:
    def __init__(self, imagen_path, pantalla):
        self.imagen = cargar_imagen(imagen_path, 800, 600)
        self.pantalla = pantalla

    def dibujar(self):
        self.pantalla.blit(self.imagen, (0, 0))
