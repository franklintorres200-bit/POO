import pygame
import random


class Particula:
    def __init__(self, x, y, color, vida=30, size=3):
        self.x, self.y, self.color, self.vida, self.vida_max, self.size = x, y, color, vida, vida, size
        self.vel_x, self.vel_y = random.uniform(-3, 3), random.uniform(-4, -1)

    def actualizar(self):
        self.x += self.vel_x; self.y += self.vel_y; self.vel_y += 0.15; self.vida -= 1

    def dibujar(self, p):
        s = max(1, int(self.size * (self.vida / self.vida_max)))
        pygame.draw.circle(p, self.color, (int(self.x), int(self.y)), s)

    @property
    def activo(self): return self.vida > 0


class TextoFlotante:
    def __init__(self, x, y, texto, color, duracion=45):
        self.x, self.y, self.texto, self.color, self.duracion, self.frame = x, y, texto, color, duracion, 0

    def actualizar(self): self.y -= 1.2; self.frame += 1

    def dibujar(self, p, f):
        alpha = max(0, 255 - int(255 * self.frame / self.duracion))
        surf = f.render(self.texto, True, self.color); surf.set_alpha(alpha)
        p.blit(surf, (int(self.x) - surf.get_width() // 2, int(self.y)))

    @property
    def activo(self): return self.frame < self.duracion
