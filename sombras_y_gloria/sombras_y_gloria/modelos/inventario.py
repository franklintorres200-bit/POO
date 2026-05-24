from typing import Optional, List


class Item:
    def __init__(self, nombre: str) -> None:
        self.nombre = nombre

class Inventario:
    def __init__(self, capacidad: int = 10) -> None:
        self._items: List[Item] = []
        self._capacidad = capacidad

    def agregar(self, item: Item) -> bool:
        if len(self._items) < self._capacidad:
            self._items.append(item)
            return True
        return False

    def usar_primero(self) -> Optional[Item]:
        if self._items: return self._items.pop(0)
        return None

    def __len__(self): return len(self._items)
