import pygame
from constantes import *
from ui.widgets import Boton


class EscenaCreditos:
    def __init__(self, j):
        self.j = j; self.bv = Boton(ANCHO//2-100, 500, 200, 50, "< Volver", C_GRIS, font_size=20)

    def manejar(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and self.bv.verificar_click(e.pos): self.j.cambiar("menu")

    def actualizar(self): self.bv.verificar_hover(pygame.mouse.get_pos())

    def dibujar(self, p):
        t = self.j.f3.render("CREDITOS", True, C_DORADO); p.blit(t, (ANCHO//2 - t.get_width()//2, 150))
        pygame.draw.line(p, C_DORADO, (300, 210), (700, 210), 2)
        d = self.j.f2.render("Desarrollado por:", True, C_GRIS_CLARO); p.blit(d, (ANCHO//2 - d.get_width()//2, 260))
        n = self.j.f3.render("Franklin Torres", True, C_BLANCO); p.blit(n, (ANCHO//2 - n.get_width()//2, 320))
        self.bv.dibujar(p, self.j.f2)


class EscenaPostCombate:
    def __init__(self, j):
        self.j = j; cx = ANCHO//2
        self.b1 = Boton(cx-130, 400, 260, 55, "NUEVA BATALLA", C_VERDE, font_size=22)
        self.b2 = Boton(cx-130, 480, 260, 55, "MENU PRINCIPAL", C_AZUL, font_size=22)

    def manejar(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if self.b1.verificar_click(e.pos): self.j.cambiar("clase")
            elif self.b2.verificar_click(e.pos): self.j.cambiar("menu")

    def actualizar(self):
        pos = pygame.mouse.get_pos(); self.b1.verificar_hover(pos); self.b2.verificar_hover(pos)

    def dibujar(self, p):
        t = self.j.f3.render("Fin del Combate", True, C_BLANCO); p.blit(t, (ANCHO//2 - t.get_width()//2, 200))
        if self.j.resultado_combate == "gano":
            r = self.j.f2.render(f"Puntaje Obtenido: {self.j.puntaje}", True, C_DORADO)
            p.blit(r, (ANCHO//2 - r.get_width()//2, 280))
        elif self.j.resultado_combate == "perdio":
            r = self.j.f2.render("Has sido derrotado...", True, C_ROJO)
            p.blit(r, (ANCHO//2 - r.get_width()//2, 280))
        else:
            r = self.j.f2.render("Te has rendido.", True, C_GRIS_CLARO)
            p.blit(r, (ANCHO//2 - r.get_width()//2, 280))
        self.b1.dibujar(p, self.j.f2); self.b2.dibujar(p, self.j.f2)
