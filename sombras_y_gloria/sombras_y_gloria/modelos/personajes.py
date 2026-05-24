import random
from abc import ABC, abstractmethod
from modelos.inventario import Inventario


class SuperHeroe(ABC):
    VIDA_MAX = 100

    def __init__(self, nombre: str, vida: int, fuerza: int, defensa: int) -> None:
        self.nombre = nombre
        self.__vida = vida
        self.fuerza = fuerza
        self.defensa = defensa
        self.inventario = Inventario()

    @property
    def vida(self): return self.__vida

    @vida.setter
    def vida(self, valor): self.__vida = max(0, min(valor, self.VIDA_MAX))

    def recibir_dano_especial(self, dano, ignora_defensa, atacante):
        dano_real = dano if ignora_defensa else max(2, dano - self.defensa)
        self.vida -= dano_real
        return dano_real

    @abstractmethod
    def atacar(self, objetivo): pass

    @abstractmethod
    def habilidad_especial(self, objetivo): pass


class Heroe(SuperHeroe):
    RANGO_FUERZA = (10, 18)
    RANGO_DEFENSA = (1, 4)
    ESTILOS = {
        "agresivo": {"fuerza": (+4, +6), "defensa": (-1, 0), "personaje": "Saitama"},
        "defensivo": {"fuerza": (-3, -2), "defensa": (+3, +5), "personaje": "Capitan America"},
    }

    def __init__(self, nombre, estilo):
        mod = self.ESTILOS[estilo]
        f_min = max(1, self.RANGO_FUERZA[0] + mod["fuerza"][0])
        f_max = self.RANGO_FUERZA[1] + mod["fuerza"][1]
        d_min = max(0, self.RANGO_DEFENSA[0] + mod["defensa"][0])
        d_max = self.RANGO_DEFENSA[1] + mod["defensa"][1]
        fuerza = random.randint(f_min, f_max)
        defensa = random.randint(d_min, d_max)
        vida = random.randint(80, 100)
        super().__init__(nombre, vida, fuerza, defensa)
        self.estilo = estilo
        self.personaje = mod["personaje"]
        self.dano_min = max(1, fuerza - 1) if estilo == "agresivo" else max(1, fuerza - 3)
        self.dano_max = fuerza + 3 if estilo == "agresivo" else fuerza + 1

    def atacar(self, objetivo):
        dano = random.randint(max(1, self.fuerza - 1), self.fuerza + 3) if self.estilo == "agresivo" else random.randint(max(1, self.fuerza - 3), self.fuerza + 1)
        if random.randint(1, 100) <= 2: return {"dano": dano, "fallo": True, "dano_real": 0}
        dano_real = max(2, dano - objetivo.defensa)
        objetivo.vida -= dano_real
        return {"dano": dano, "fallo": False, "dano_real": dano_real}

    def habilidad_especial(self, objetivo):
        tirada = random.randint(1, 10)
        if tirada <= 1: return {"resultado": "fallo", "dano_real": 0, "mensaje": "El golpe falla!"}
        elif tirada == 10:
            dano_real = objetivo.recibir_dano_especial(30, True, self)
            return {"resultado": "critico", "dano_real": dano_real, "mensaje": "LUZ DIVINA! 30 dano imparable"}
        else:
            dano = random.randint(20, 25)
            dano_real = objetivo.recibir_dano_especial(dano, False, self)
            return {"resultado": "normal", "dano_real": dano_real, "mensaje": f"Golpe Fuerte: {dano_real} dano"}


class Villano(SuperHeroe):
    RANGO_FUERZA = (5, 12)
    RANGO_DEFENSA = (4, 8)
    ESTILOS = {
        "agresivo": {"fuerza": (+4, +6), "defensa": (-2, -1), "personaje": "El Guason"},
        "defensivo": {"fuerza": (-2, -1), "defensa": (+3, +5), "personaje": "Magneto"},
    }

    def __init__(self, nombre, estilo):
        mod = self.ESTILOS[estilo]
        f_min = max(1, self.RANGO_FUERZA[0] + mod["fuerza"][0])
        f_max = self.RANGO_FUERZA[1] + mod["fuerza"][1]
        d_min = max(0, self.RANGO_DEFENSA[0] + mod["defensa"][0])
        d_max = self.RANGO_DEFENSA[1] + mod["defensa"][1]
        fuerza = random.randint(f_min, f_max)
        defensa = random.randint(d_min, d_max)
        vida = random.randint(80, 100)
        super().__init__(nombre, vida, fuerza, defensa)
        self.estilo = estilo
        self.personaje = mod["personaje"]
        self.dano_min = fuerza if estilo == "agresivo" else max(1, fuerza - 2)
        self.dano_max = fuerza + 4 if estilo == "agresivo" else fuerza + 1

    def atacar(self, objetivo):
        if self.estilo == "agresivo": dano = random.randint(self.fuerza, self.fuerza + 4)
        else:
            dano = random.randint(max(1, self.fuerza - 2), self.fuerza + 1)
            self.vida = min(self.VIDA_MAX, self.vida + 1)
        if random.randint(1, 100) <= 2: return {"dano": dano, "fallo": True, "dano_real": 0, "absorbe": self.estilo == "defensivo"}
        dano_real = max(2, dano - objetivo.defensa)
        objetivo.vida -= dano_real
        return {"dano": dano, "fallo": False, "dano_real": dano_real, "absorbe": self.estilo == "defensivo"}

    def habilidad_especial(self, objetivo):
        tirada = random.randint(1, 10)
        if tirada <= 1: return {"resultado": "fallo", "dano_real": 0, "mensaje": "La magia se disipa!"}
        elif tirada == 10:
            dano_real = objetivo.recibir_dano_especial(30, True, self)
            return {"resultado": "critico", "dano_real": dano_real, "mensaje": "GOLPE DEVASTADOR! 30 dano imparable"}
        else:
            dano = random.randint(20, 25)
            dano_real = objetivo.recibir_dano_especial(dano, False, self)
            return {"resultado": "normal", "dano_real": dano_real, "mensaje": f"Magia Ancestral: {dano_real} dano"}
