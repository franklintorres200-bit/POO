# Sombras y Gloria

Juego de combate por turnos hecho en Python con Pygame.

## De qué se trata

El jugador elige si quiere ser héroe o villano, escoge su estilo de pelea (agresivo o defensivo) y se enfrenta a un enemigo. Cada combinación da un personaje distinto: Saitama, Capitán América, El Guasón o Magneto. El combate es por turnos, hay botiquines que se pueden recoger y usar, y una habilidad especial que solo se activa cuando la vida baja de 10.

Al ganar se registra el puntaje en un salón de la fama. Hay tres categorías según la dificultad: Habilidosos, Los Mejores y Los Dioses (esta última requiere ganar con los 4 modos en difícil).

## Tecnologías

- Python 3.10+ - 3.12.10-
- Pygame 2.6.1

## Cómo correrlo

Crear el entorno virtual e instalar dependencias:

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
python main.py
```

## Estructura

```
sombras_y_gloria/
├── main.py
├── constantes.py
├── requirements.txt
├── modelos/
│   ├── inventario.py
│   └── personajes.py
├── ui/
│   ├── widgets.py
│   ├── efectos.py
│   └── render.py
├── escenas/
│   ├── escena_menu.py
│   ├── escena_nombre.py
│   ├── escena_clase.py
│   ├── escena_estilo.py
│   ├── escena_enemigo.py
│   ├── escena_combate.py
│   ├── escena_ranking.py
│   └── escena_fin.py
└── utils/
    └── ranking.py
```

## Controles

- `A` — Atacar
- `R` — Recoger botiquín
- `B` — Usar botiquín
- `G` — Habilidad especial (vida <= 10)
- `Q` — Rendirse
- `ESC` — Menú principal

## Autor

Franklin Torres
