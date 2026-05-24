import pygame
import random
import sys
import os
from constantes import *
from ui.render import dibujar_fondo
from modelos.personajes import Heroe, Villano
from escenas.escena_menu import EscenaMenu
from escenas.escena_nombre import EscenaNombre
from escenas.escena_clase import EscenaClase
from escenas.escena_estilo import EscenaEstilo
from escenas.escena_enemigo import EscenaEnemigo
from escenas.escena_combate import EscenaCombate
from escenas.escena_ranking import EscenaRanking
from escenas.escena_fin import EscenaCreditos, EscenaPostCombate

class Juego:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.FULLSCREEN | pygame.SCALED)
        pygame.display.set_caption("Sombras y Gloria - Combate Epico")
        self.reloj = pygame.time.Clock()
        self.corriendo = True
        fd = None
        for fp in ["C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/segoeui.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/System/Library/Fonts/Helvetica.ttc"]:
            if os.path.exists(fp): fd = fp; break
        self.f1 = pygame.font.Font(fd, 16); self.f2 = pygame.font.Font(fd, 20)
        self.f3 = pygame.font.Font(fd, 32); self.f4 = pygame.font.Font(fd, 48)
        self.nombre = ""; self.clase = ""; self.estilo = ""; self.enemigo_e = ""
        self.jugador = None; self.enemigo = None; self.dificultad = ""
        self.modo = ""; self.clase_usada = ""; self.puntaje = 0
        self.rondas_b = 1; self.boti_gasta = False
        self.resultado_combate = None
        self.escena = EscenaMenu(self)
        self.particulas_f = [{"x": random.randint(0,ANCHO), "y": random.randint(0,ALTO), "v": random.uniform(0.2,0.8), "s": random.randint(1,3), "a": random.randint(30,120)} for _ in range(40)]

    def cambiar(self, n):
        if n == "menu": self.escena = EscenaMenu(self)
        elif n == "nombre": self.escena = EscenaNombre(self)
        elif n == "clase": self.escena = EscenaClase(self)
        elif n == "estilo": self.escena = EscenaEstilo(self)
        elif n == "enemigo": self.escena = EscenaEnemigo(self)
        elif n == "combate": self.escena = EscenaCombate(self)
        elif n == "ranking": self.escena = EscenaRanking(self)
        elif n == "creditos": self.escena = EscenaCreditos(self)
        elif n == "post": self.escena = EscenaPostCombate(self)

    def iniciar_combate(self):
        e = self.estilo
        if self.clase == "heroe":
            self.jugador = Heroe(self.nombre, e); self.modo = f"heroe_{e}"; self.clase_usada = f"Heroe - {self.jugador.personaje}"
            if self.enemigo_e == "facil": self.enemigo = Villano("Villano", "defensivo"); self.dificultad = "FACIL"; self.rondas_b = 1; self.boti_gasta = False
            else: self.enemigo = Villano("Villano", "agresivo"); self.dificultad = "NORMAL"; self.rondas_b = 2; self.boti_gasta = False
        else:
            self.jugador = Villano(self.nombre, e); self.modo = f"villano_{e}"; self.clase_usada = f"Villano - {self.jugador.personaje}"
            if self.enemigo_e == "facil": self.enemigo = Heroe("Heroe", "defensivo"); self.dificultad = "NORMAL"; self.rondas_b = 2; self.boti_gasta = False
            else: self.enemigo = Heroe("Heroe", "agresivo"); self.dificultad = "DIFICIL"; self.rondas_b = 3; self.boti_gasta = True
        self.cambiar("combate")

    def ejecutar(self):
        while self.corriendo:
            for e in pygame.event.get():
                if e.type == pygame.QUIT: self.corriendo = False
                elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    if self.escena.__class__.__name__ not in ["EscenaCombate", "EscenaMenu"]: self.cambiar("menu")
                    elif self.escena.__class__.__name__ == "EscenaMenu": self.corriendo = False
                self.escena.manejar(e)
            self.escena.actualizar()
            dibujar_fondo(self.pantalla)
            for p in self.particulas_f:
                p["y"] -= p["v"]
                if p["y"] < -5: p["y"] = ALTO + 5; p["x"] = random.randint(0, ANCHO)
                pygame.draw.circle(self.pantalla, (p["a"]//4, p["a"]//4, p["a"]), (int(p["x"]), int(p["y"])), p["s"])
            self.escena.dibujar(self.pantalla)
            pygame.display.flip(); self.reloj.tick(FPS)
        pygame.quit(); sys.exit()


if __name__ == "__main__":
    Juego().ejecutar()
