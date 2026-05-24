import pygame
from constantes import *
from ui.widgets import Boton
from utils.ranking import cargar_ranking


class EscenaRanking:
    def __init__(self, j):
        self.j = j; self.bv = Boton(20, 20, 110, 38, "< Volver", C_GRIS, font_size=16); self.scroll = 0

    def manejar(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1 and self.bv.verificar_click(e.pos): self.j.cambiar("menu")
            elif e.button == 4: self.scroll = max(0, self.scroll - 20)
            elif e.button == 5: self.scroll += 20

    def actualizar(self): self.bv.verificar_hover(pygame.mouse.get_pos())

    def dibujar(self, p):
        self.bv.dibujar(p, self.j.f1)
        r = cargar_ranking(); y = 70 - self.scroll
        t1 = self.j.f2.render("SALON DE HABILIDOSOS (Normal - Top 10)", True, C_DORADO); p.blit(t1, (50, y)); y += 30
        if r["habilidosos"]:
            for i, e in enumerate(r["habilidosos"], 1):
                s = self.j.f1.render(f"{i}. {e['nombre']} - {e.get('clase_usada','?')} - Puntaje: {e['puntaje']}", True, C_BLANCO)
                p.blit(s, (60, y)); y += 22
        else: p.blit(self.j.f1.render("Vacio.", True, C_GRIS_CLARO), (60, y)); y += 22
        y += 20
        t2 = self.j.f2.render("SALON DE LOS MEJORES (Dificil - Top 5)", True, C_NARANJA); p.blit(t2, (50, y)); y += 30
        if r["mejores"]:
            for i, e in enumerate(r["mejores"], 1):
                m = len(e.get("modos_ganados", []))
                s = self.j.f1.render(f"{i}. {e['nombre']} - {e.get('clase_usada','?')} - Puntaje: {e['puntaje']} ({m}/4)", True, C_BLANCO)
                p.blit(s, (60, y)); y += 22
        else: p.blit(self.j.f1.render("Vacio.", True, C_GRIS_CLARO), (60, y)); y += 22
        y += 20
        t3 = self.j.f2.render("SALON DE LOS DIOSES (Top 3)", True, C_MORADO); p.blit(t3, (50, y)); y += 30
        if r["dioses"]:
            cols = [C_DORADO, C_PLATA, (205,127,50)]
            for i, e in enumerate(r["dioses"]):
                s = self.j.f1.render(f"{i+1}. {e['nombre']} - {e.get('clase_usada','?')} - Puntaje: {e['puntaje']}", True, cols[i])
                p.blit(s, (60, y)); y += 25
        else: p.blit(self.j.f1.render("Ningun mortal ha llegado aqui.", True, C_GRIS_CLARO), (60, y))
