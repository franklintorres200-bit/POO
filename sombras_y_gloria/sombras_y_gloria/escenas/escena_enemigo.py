import pygame
from constantes import *
from ui.widgets import Boton
from ui.render import _osc


class EscenaEnemigo:
    def __init__(self, j):
        self.j = j; cx = ANCHO//2
        self.b1 = Boton(cx-260, 270, 240, 260, "", C_VERDE)
        self.b2 = Boton(cx+20, 270, 240, 260, "", C_ROJO)
        self.bv = Boton(20, 20, 110, 38, "< Volver", C_GRIS, font_size=16)

    def manejar(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if self.b1.verificar_click(e.pos): self.j.enemigo_e = "facil"; self.j.iniciar_combate()
            elif self.b2.verificar_click(e.pos): self.j.enemigo_e = "dificil"; self.j.iniciar_combate()
            elif self.bv.verificar_click(e.pos): self.j.cambiar("estilo")

    def actualizar(self):
        pos = pygame.mouse.get_pos(); self.b1.verificar_hover(pos); self.b2.verificar_hover(pos); self.bv.verificar_hover(pos)

    def dibujar(self, p):
        self.bv.dibujar(p, self.j.f1)
        t = self.j.f3.render("Elige tu Enemigo", True, C_BLANCO); p.blit(t, (ANCHO//2 - t.get_width()//2, 90))
        if self.j.clase == "heroe":
            i1 = ["Magneto", "Dificultad: FACIL", "Botiquin cada ronda", "Recoger: gratis"]
            i2 = ["El Guason", "Dificultad: NORMAL", "Botiquin cada 2 rondas", "Recoger: gratis"]
        else:
            i1 = ["Capitan America", "Dificultad: NORMAL", "Botiquin cada 2 rondas", "Recoger: gratis"]
            i2 = ["Saitama", "Dificultad: DIFICIL", "Botiquin cada 3 rondas", "Recoger: gasta turno"]
        self._panel(p, self.b1.rect, C_VERDE, i1); self._panel(p, self.b2.rect, C_ROJO, i2)

    def _panel(self, p, r, c, info):
        pygame.draw.rect(p, C_PANEL, r, border_radius=14); pygame.draw.rect(p, c, r, 3, border_radius=14)
        cx = r.centerx
        pygame.draw.circle(p, _osc(c,0.4), (cx, r.y+45), 25)
        pygame.draw.rect(p, _osc(c,0.4), (cx-18, r.y+70, 36, 25), border_radius=5)
        y = r.y + 110
        for l in info:
            s = self.j.f1.render(f"- {l}", True, C_BLANCO); p.blit(s, (r.x+20, y)); y += 26
