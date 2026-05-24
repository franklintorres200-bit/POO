import json
import os
from typing import Dict, Any

ARCHIVO_RANKING = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ranking.json")


def cargar_ranking() -> Dict[str, Any]:
    if os.path.exists(ARCHIVO_RANKING):
        with open(ARCHIVO_RANKING, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"habilidosos": [], "mejores": [], "dioses": []}

def guardar_ranking(ranking: Dict[str, Any]) -> None:
    with open(ARCHIVO_RANKING, "w", encoding="utf-8") as f:
        json.dump(ranking, f, ensure_ascii=False, indent=2)

def registrar_victoria(nombre: str, puntaje: int, dificultad: str, modo_jugado: str, clase_usada: str) -> None:
    ranking = cargar_ranking()
    if dificultad == "NORMAL":
        salon = ranking["habilidosos"]
        existente = next((e for e in salon if e["nombre"].lower() == nombre.lower()), None)
        if existente:
            if puntaje > existente["puntaje"]:
                existente["puntaje"] = puntaje
                existente["clase_usada"] = clase_usada
        else:
            salon.append({"nombre": nombre, "puntaje": puntaje, "clase_usada": clase_usada})
        ranking["habilidosos"] = sorted(salon, key=lambda x: x["puntaje"], reverse=True)[:10]
    elif dificultad == "DIFICIL":
        salon = ranking["mejores"]
        existente = next((e for e in salon if e["nombre"].lower() == nombre.lower()), None)
        if existente:
            if puntaje > existente["puntaje"]:
                existente["puntaje"] = puntaje
                existente["clase_usada"] = clase_usada
            modos = set(existente.get("modos_ganados", []))
            modos.add(modo_jugado)
            existente["modos_ganados"] = list(modos)
        else:
            salon.append({"nombre": nombre, "puntaje": puntaje, "clase_usada": clase_usada, "modos_ganados": [modo_jugado]})
        ranking["mejores"] = sorted(salon, key=lambda x: x["puntaje"], reverse=True)[:5]
        MODOS_REQUERIDOS = {"heroe_agresivo", "heroe_defensivo", "villano_agresivo", "villano_defensivo"}
        jugador_mejores = next((e for e in ranking["mejores"] if e["nombre"].lower() == nombre.lower()), None)
        if jugador_mejores:
            modos_logrados = set(jugador_mejores.get("modos_ganados", []))
            if MODOS_REQUERIDOS.issubset(modos_logrados):
                dioses = ranking["dioses"]
                dios_exist = next((d for d in dioses if d["nombre"].lower() == nombre.lower()), None)
                if dios_exist:
                    if puntaje > dios_exist["puntaje"]:
                        dios_exist["puntaje"] = puntaje
                        dios_exist["clase_usada"] = clase_usada
                else:
                    dioses.append({"nombre": nombre, "puntaje": jugador_mejores["puntaje"], "clase_usada": clase_usada})
                ranking["dioses"] = sorted(dioses, key=lambda x: x["puntaje"], reverse=True)[:3]
    guardar_ranking(ranking)
