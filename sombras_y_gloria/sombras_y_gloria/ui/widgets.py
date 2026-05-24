import pygame
from constantes import *


class Boton:
    def __init__(self, x, y, w, h, texto, color_base, color_hover=None, font_size=20):
        self.rect = pygame.Rect(x, y, w, h); self.texto = texto; self.color_base = color_base
        self.color_hover = color_hover or tuple(min(255, c + 40) for c in color_base)
        self.font_size = font_size; self.hover = False; self.habilitado = True; self.escala = 1.0

    def verificar_hover(self, pos): self.hover = self.rect.collidepoint(pos) and self.habilitado

    def verificar_click(self, pos): return self.habilitado and self.rect.collidepoint(pos)

    def dibujar(self, p, f):
        self.escala += ((1.05 if self.hover else 1.0) - self.escala) * 0.2
        color = self.color_hover if self.hover else self.color_base
        if not self.habilitado: color = C_GRIS
        w, h = max(1, int(self.rect.width * self.escala)), max(1, int(self.rect.height * self.escala))
        cx, cy = self.rect.centerx, self.rect.centery
        r = pygame.Rect(cx - w//2, cy - h//2, w, h)
        pygame.draw.rect(p, (0,0,0), r.move(3,3), border_radius=10)
        pygame.draw.rect(p, color, r, border_radius=10)
        pygame.draw.rect(p, tuple(min(255, c+60) for c in color), r, 2, border_radius=10)
        txt = f.render(self.texto, True, C_BLANCO if self.habilitado else C_GRIS_CLARO)
        p.blit(txt, txt.get_rect(center=r.center))


class BarraVida:
    def __init__(self, x, y, w, h, vida_max=100):
        self.rect = pygame.Rect(x, y, w, h)
        self.vida_max = vida_max
        self.vida_actual = float(vida_max)

    def actualizar(self, vida):
        self.vida_actual = float(vida)

    def dibujar(self, p, f, nombre, personaje, es_jugador=True):
        c = C_CYAN if es_jugador else C_ROJO
        p.blit(f.render(f"{nombre} ({personaje})", True, c), (self.rect.x, self.rect.y - 22))
        pygame.draw.rect(p, C_GRIS_OSCURO, self.rect, border_radius=5)
        r = max(0, self.vida_actual / self.vida_max)
        color = C_VERDE if r > 0.5 else (C_AMARILLO if r > 0.25 else C_ROJO)
        w = max(0, int(self.rect.width * r))
        if w > 0:
            pygame.draw.rect(p, color, (self.rect.x, self.rect.y, w, self.rect.height), border_radius=5)
        pygame.draw.rect(p, C_BLANCO, self.rect, 2, border_radius=5)
        txt = f.render(f"{int(self.vida_actual)}/{self.vida_max}", True, C_BLANCO)
        p.blit(txt, txt.get_rect(center=self.rect.center))


class PanelLog:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h); self.lineas = []

    def agregar(self, texto, color=C_BLANCO):
        self.lineas.append((texto, color))
        if len(self.lineas) > 50: self.lineas = self.lineas[-50:]

    def dibujar(self, p, f):
        pygame.draw.rect(p, C_PANEL, self.rect, border_radius=8)
        pygame.draw.rect(p, C_BORDE, self.rect, 2, border_radius=8)
        p.blit(f.render("Registro de Combate", True, C_DORADO), (self.rect.x + 10, self.rect.y + 5))
        y = self.rect.y + 28
        for i, (t, c) in enumerate(self.lineas[-6:]):
            alpha = int(255 * (i + 1) / 6)
            s = f.render(t[:75], True, c); s.set_alpha(alpha); p.blit(s, (self.rect.x + 10, y)); y += 20


class CampoTexto:
    def __init__(self, x, y, w, h, ph=""):
        self.rect = pygame.Rect(x, y, w, h); self.texto = ""; self.ph = ph; self.activo = False; self.ct = 0

    def manejar(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN: self.activo = self.rect.collidepoint(e.pos)
        elif e.type == pygame.KEYDOWN and self.activo:
            if e.key == pygame.K_BACKSPACE: self.texto = self.texto[:-1]
            elif e.key == pygame.K_RETURN: return self.texto
            elif len(e.unicode) == 1 and e.unicode.isprintable() and len(self.texto) < 20: self.texto += e.unicode
        return None

    def dibujar(self, p, f):
        c = C_CYAN if self.activo else C_GRIS_CLARO
        pygame.draw.rect(p, C_PANEL, self.rect, border_radius=8)
        pygame.draw.rect(p, c, self.rect, 2, border_radius=8)
        txt = self.texto if self.texto else self.ph
        col = C_BLANCO if self.texto else C_GRIS_CLARO
        p.blit(f.render(txt, True, col), (self.rect.x + 12, self.rect.y + 10))
        if self.activo:
            self.ct += 1
            if self.ct % 40 < 20:
                x_c = self.rect.x + 12 + f.size(self.texto)[0]
                pygame.draw.line(p, C_BLANCO, (x_c, self.rect.y+6), (x_c, self.rect.y+self.rect.height-6), 2)
