import pygame
from constantes import *
from ui.widgets import Boton
from ui.render import _osc


class EscenaClase:
    def __init__(self, j):
        self.j = j; cx = ANCHO//2
        self.b1 = Boton(cx-260, 280, 240, 240, "", C_AZUL)
        self.b2 = Boton(cx+20, 280, 240, 240, "", C_ROJO)
        self.bv = Boton(20, 20, 110, 38, "< Volver", C_GRIS, font_size=16)

    def manejar(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if self.b1.verificar_click(e.pos): self.j.clase = "heroe"; self.j.cambiar("estilo")
            elif self.b2.verificar_click(e.pos): self.j.clase = "villano"; self.j.cambiar("estilo")
            elif self.bv.verificar_click(e.pos): self.j.cambiar("nombre")

    def actualizar(self):
        pos = pygame.mouse.get_pos(); self.b1.verificar_hover(pos); self.b2.verificar_hover(pos); self.bv.verificar_hover(pos)

    def dibujar(self, p):
        self.bv.dibujar(p, self.j.f1)
        t = self.j.f3.render("Elige tu Clase", True, C_BLANCO); p.blit(t, (ANCHO//2 - t.get_width()//2, 100))
        s = self.j.f2.render(f"Jugador: {self.j.nombre}", True, C_GRIS_CLARO); p.blit(s, (ANCHO//2 - s.get_width()//2, 160))
        self._panel(p, self.b1.rect, "HEROE", C_AZUL, ["Mas ataque", "Menos defensa", "Golpe Fuerte", "Dano alto"])
        self._panel(p, self.b2.rect, "VILLANO", C_ROJO, ["Mas defensa", "Menos ataque", "Magia Ancestral", "Absorbe vida"])

    def _panel(self, p, r, t, c, stats):
        pygame.draw.rect(p, C_PANEL, r, border_radius=14); pygame.draw.rect(p, c, r, 3, border_radius=14)
        cx = r.centerx
        pygame.draw.circle(p, _osc(c,0.3), (cx, r.y+55), 32); pygame.draw.circle(p, c, (cx, r.y+55), 32, 3)
        sim = self.j.f3.render(t[0], True, C_BLANCO); p.blit(sim, (cx - sim.get_width()//2, r.y+35))
        tt = self.j.f2.render(t, True, c); p.blit(tt, (cx - tt.get_width()//2, r.y+100))
        y = r.y + 135
        for st in stats:
            s = self.j.f1.render(f"- {st}", True, C_BLANCO); p.blit(s, (r.x+25, y)); y += 24
