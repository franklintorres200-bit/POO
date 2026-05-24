import pygame
import random
from constantes import *
from ui.widgets import Boton, BarraVida, PanelLog
from ui.efectos import Particula, TextoFlotante
from ui.render import dibujar_personaje
from modelos.inventario import Item
from utils.ranking import registrar_victoria


class EscenaCombate:
    def __init__(self, j):
        self.j = j; jj = j.jugador; ee = j.enemigo
        self.bj = BarraVida(40, 60, 300, 28, jj.VIDA_MAX)
        self.be = BarraVida(ANCHO-340, 60, 300, 28, ee.VIDA_MAX)
        self.log = PanelLog(20, 490, ANCHO-40, 150)
        yb = 660
        self.ba = Boton(20, yb, 150, 45, "Atacar [A]", C_ROJO, font_size=16)
        self.br = Boton(180, yb, 160, 45, "Recoger [R]", C_VERDE, font_size=16)
        self.bu = Boton(350, yb, 160, 45, "Usar [B]", C_CYAN, font_size=16)
        self.bg = Boton(520, yb, 180, 45, "Especial [G]", C_MORADO, font_size=16)
        self.bq = Boton(710, yb, 150, 45, "Rendirse [Q]", C_GRIS, font_size=16)
        self.bc = Boton(ANCHO//2-120, 620, 240, 50, "CONTINUAR", C_AZUL, font_size=22); self.bc.habilitado = False
        self.ronda = 0; self.golpes = 0; self.boti = False; self.res = None
        self.te = False; self.timer = 0; self.parts = []; self.textos = []
        self.anim = None; self.fj = 0; self.fe = 0; self.shake = 0
        self.log.agregar(f"Comienza el combate! Ronda 1", C_DORADO)
        self.log.agregar(f"{jj.nombre} ({jj.personaje}) vs {ee.nombre} ({ee.personaje})", C_BLANCO)
        self._nueva_ronda()

    def _nueva_ronda(self):
        self.ronda += 1
        if self.ronda > 1: self.log.agregar(f"-- Ronda {self.ronda} --", C_DORADO)
        if self.ronda % self.j.rondas_b == 0:
            self.boti = True; self.log.agregar("Aparecio un botiquin!", C_VERDE)

    def _cp(self, x, y, c, n=12):
        for _ in range(n): self.parts.append(Particula(x, y, c, vida=25, size=random.randint(2,5)))

    def manejar(self, e):
        if self.res:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and self.bc.verificar_click(e.pos): self.j.cambiar("post")
            return
        if self.te or self.anim: return
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if self.ba.verificar_click(e.pos): self._atacar()
            elif self.br.verificar_click(e.pos): self._recoger()
            elif self.bu.verificar_click(e.pos): self._usar()
            elif self.bg.verificar_click(e.pos): self._esp()
            elif self.bq.verificar_click(e.pos): self._rendir()
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_a: self._atacar()
            elif e.key == pygame.K_r: self._recoger()
            elif e.key == pygame.K_b: self._usar()
            elif e.key == pygame.K_g: self._esp()
            elif e.key == pygame.K_q: self._rendir()

    def _atacar(self):
        if self.res or self.te or self.anim: return
        jj, ee = self.j.jugador, self.j.enemigo; self.golpes += 1
        r = jj.atacar(ee)
        if r["fallo"]:
            self.log.agregar(f"{jj.nombre} ataca... y falla!", C_AMARILLO)
            self.textos.append(TextoFlotante(700, 200, "FALLA!", C_AMARILLO))
        else:
            self.log.agregar(f"{jj.nombre} golpea: {r['dano_real']} dano", C_ROJO)
            self.textos.append(TextoFlotante(700, 180, f"-{r['dano_real']}", C_ROJO))
            self._cp(700, 250, C_ROJO); self.fe = 10; self.shake = 5
        self.anim = {"t": "j", "f": 0, "m": 18}
        if ee.vida <= 0: self._victoria()
        else: self.te = True; self.timer = 35

    def _recoger(self):
        if self.res or self.te or self.anim: return
        if not self.boti: self.log.agregar("No hay botiquin.", C_GRIS_CLARO); return
        self.j.jugador.inventario.agregar(Item("Botiquin")); self.boti = False
        self.log.agregar(f"Recogiste un botiquin. Tienes {len(self.j.jugador.inventario)}", C_VERDE)
        self.textos.append(TextoFlotante(250, 200, "+Botiquin", C_VERDE))
        if self.j.boti_gasta:
            self.log.agregar("Recoger gasto tu turno!", C_AMARILLO); self.te = True; self.timer = 35

    def _usar(self):
        if self.res or self.te or self.anim: return
        jj = self.j.jugador
        if len(jj.inventario) == 0: self.log.agregar("No tienes botiquines.", C_GRIS_CLARO); return
        c = random.randint(10, 15); jj.vida += c; jj.inventario.usar_primero()
        self.log.agregar(f"Recuperaste {c} de vida. Actual: {jj.vida}/{jj.VIDA_MAX}", C_VERDE)
        self.textos.append(TextoFlotante(250, 180, f"+{c}", C_VERDE)); self._cp(250, 250, C_VERDE, 8)

    def _esp(self):
        if self.res or self.te or self.anim: return
        jj, ee = self.j.jugador, self.j.enemigo
        if jj.vida > 10: self.log.agregar(f"Solo con vida <= 10. Tienes {jj.vida}", C_AMARILLO); return
        self.golpes += 1; r = jj.habilidad_especial(ee)
        if r["resultado"] == "fallo":
            self.log.agregar(r["mensaje"], C_GRIS_CLARO); self.textos.append(TextoFlotante(700, 200, "FALLA!", C_AMARILLO))
        elif r["resultado"] == "critico":
            self.log.agregar(f"CRITICO! {r['mensaje']}", C_DORADO)
            self.textos.append(TextoFlotante(700, 160, f"-{r['dano_real']}!!", C_DORADO, 60))
            self._cp(700, 250, C_DORADO, 25); self.fe = 15; self.shake = 10
        else:
            self.log.agregar(r["mensaje"], C_MORADO)
            self.textos.append(TextoFlotante(700, 180, f"-{r['dano_real']}", C_MORADO))
            self._cp(700, 250, C_MORADO, 15); self.fe = 12; self.shake = 7
        self.anim = {"t": "j", "f": 0, "m": 20}
        if ee.vida <= 0: self._victoria()
        else: self.te = True; self.timer = 35

    def _rendir(self):
        if self.res: return
        self.res = "rindio"; self.j.resultado_combate = "rindio"
        self.log.agregar("Te rendiste.", C_ROJO); self.bc.habilitado = True

    def _victoria(self):
        self.res = "gano"; self.j.resultado_combate = "gano"
        self.log.agregar("GANASTE!", C_DORADO); self.bc.habilitado = True
        if self.j.dificultad in ("NORMAL", "DIFICIL"):
            p = max(0, self.j.jugador.vida - self.golpes); self.j.puntaje = p
            self.log.agregar(f"Puntaje: {self.j.jugador.vida} - {self.golpes} = {p}", C_CYAN)
            registrar_victoria(self.j.nombre, p, self.j.dificultad, self.j.modo, self.j.clase_usada)

    def _derrota(self):
        self.res = "perdio"; self.j.resultado_combate = "perdio"
        self.log.agregar("PERDISTE...", C_ROJO); self.bc.habilitado = True

    def _turno_e(self):
        ee, jj = self.j.enemigo, self.j.jugador; r = ee.atacar(jj)
        if r["fallo"]:
            self.log.agregar(f"{ee.nombre} ataca... y falla!", C_AMARILLO)
        else:
            msg = f"{ee.nombre} ataca: {r['dano_real']} dano"
            if r.get("absorbe"): msg += " (+1 vida)"
            self.log.agregar(msg, C_NARANJA)
            self.textos.append(TextoFlotante(250, 200, f"-{r['dano_real']}", C_NARANJA))
            self._cp(250, 250, C_NARANJA); self.fj = 10; self.shake = 5
        self.anim = {"t": "e", "f": 0, "m": 18}
        if jj.vida <= 0: self._derrota()
        else: self._nueva_ronda()

    def actualizar(self):
        pos = pygame.mouse.get_pos()
        for b in [self.ba, self.br, self.bu, self.bg, self.bq, self.bc]: b.verificar_hover(pos)
        if self.j.jugador and self.j.enemigo:
            self.bj.actualizar(self.j.jugador.vida); self.be.actualizar(self.j.enemigo.vida)
        if self.anim:
            self.anim["f"] += 1
            if self.anim["f"] >= self.anim["m"]: self.anim = None
        for p in self.parts: p.actualizar()
        self.parts = [p for p in self.parts if p.activo]
        for t in self.textos: t.actualizar()
        self.textos = [t for t in self.textos if t.activo]
        if self.fj > 0: self.fj -= 1
        if self.fe > 0: self.fe -= 1
        if self.shake > 0: self.shake -= 1
        if self.te and not self.res:
            self.timer -= 1
            if self.timer <= 0: self.te = False; self._turno_e()
        self.br.habilitado = self.boti and not self.te and not self.res
        self.bu.habilitado = len(self.j.jugador.inventario) > 0 and not self.te and not self.res
        self.bg.habilitado = self.j.jugador.vida <= 10 and not self.te and not self.res
        self.ba.habilitado = not self.te and not self.res
        self.bq.habilitado = not self.res

    def dibujar(self, p):
        sx = random.randint(-self.shake, self.shake) if self.shake > 0 else 0
        sy = random.randint(-self.shake, self.shake) if self.shake > 0 else 0
        pygame.draw.rect(p, (20,20,35), (sx, sy, ANCHO, 470))
        pygame.draw.line(p, C_BORDE, (0, 470), (ANCHO, 470), 2)
        jj, ee = self.j.jugador, self.j.enemigo
        if not jj or not ee: return
        a_j = 0; a_e = 0
        if self.anim:
            prog = self.anim["f"] / self.anim["m"]
            if self.anim["t"] == "j": a_j = int(40 * (1 - abs(prog - 0.5) * 2))
            else: a_e = int(-40 * (1 - abs(prog - 0.5) * 2))
        dibujar_personaje(p, jj, 250 + sx, 280 + sy, True, a_j, self.fj > 5, self.j.f1)
        dibujar_personaje(p, ee, 750 + sx, 280 + sy, False, a_e, self.fe > 5, self.j.f1)
        self.bj.dibujar(p, self.j.f1, jj.nombre, jj.personaje, True)
        self.be.dibujar(p, self.j.f1, ee.nombre, ee.personaje, False)
        inv = self.j.f1.render(f"Botiquines: {len(jj.inventario)}", True, C_VERDE)
        p.blit(inv, (20 + sx, 450 + sy))
        rd = self.j.f1.render(f"Ronda: {self.ronda} | Dificultad: {self.j.dificultad}", True, C_GRIS_CLARO)
        p.blit(rd, (ANCHO - rd.get_width() - 20 + sx, 450 + sy))
        if self.boti:
            bt = self.j.f1.render("Botiquin disponible!", True, C_VERDE)
            p.blit(bt, (ANCHO//2 - bt.get_width()//2 + sx, 450 + sy))
        for t in self.textos: t.dibujar(p, self.j.f2)
        for pt in self.parts: pt.dibujar(p)
        self.log.dibujar(p, self.j.f1)
        if self.res:
            if self.res == "gano": rt = self.j.f3.render("VICTORIA!", True, C_DORADO)
            elif self.res == "perdio": rt = self.j.f3.render("DERROTA", True, C_ROJO)
            else: rt = self.j.f3.render("RENDICION", True, C_GRIS_CLARO)
            p.blit(rt, (ANCHO//2 - rt.get_width()//2, 560))
            self.bc.dibujar(p, self.j.f2)
        else:
            self.ba.dibujar(p, self.j.f1); self.br.dibujar(p, self.j.f1)
            self.bu.dibujar(p, self.j.f1); self.bg.dibujar(p, self.j.f1); self.bq.dibujar(p, self.j.f1)
            if self.te:
                tt = self.j.f1.render("Turno del enemigo...", True, C_AMARILLO)
                p.blit(tt, (ANCHO//2 - tt.get_width()//2, 615))
