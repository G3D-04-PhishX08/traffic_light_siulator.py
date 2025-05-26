# Simulador de Semáforo con Tráfico 🚦

Este repositorio contiene un **simulador interactivo de un semáforo** y el flujo de vehículos en una intersección simple, construido con **Python 3** y **Pygame 2**.

![Vista previa del simulador](docs/screenshot.gif)

---

## Tabla de Contenidos
1. [Características](#características)
2. [Instalación](#instalación)
3. [Uso](#uso)
4. [Controles](#controles)
5. [Estructura del Código](#estructura-del-código)
6. [Personalización](#personalización)
7. [Contribuciones](#contribuciones)
8. [Licencia](#licencia)

---

## Características

- **Ciclo completo de semáforo** (verde → amarillo → rojo) con tiempos configurables.
- Generación aleatoria de vehículos que **respetan la luz** antes de cruzar.
- **Pausa / Reanudación** de la simulación con la barra espaciadora.
- Código **totalmente comentado** y organizado en clases para fácil mantenimiento.
- Preparado para **extensión a múltiples carriles o intersecciones**.

---

## Instalación

```bash
# Clona el repositorio
git clone https://github.com/G3D-04-PhishX08/traffic-light-simulator.git
cd traffic-light-simulator

# Crea un entorno virtual (opcional)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instala dependencias
pip install -r requirements.txt
```

> **Nota:** El único requisito externo es `pygame>=2.5`.

---

## Uso

```bash
python traffic_light_simulator.py
```

---

## Controles

| Tecla               | Acción                          |
|---------------------|---------------------------------|
| **Barra espaciadora** | Pausar / Reanudar simulación    |
| **Esc**             | Salir del programa              |

---

## Estructura del Código

```
traffic_light_simulator.py   # Programa principal
docs/
└─ screenshot.gif            # Gif de demostración (opcional)
README.md                    # Este archivo
requirements.txt             # Dependencias
```

### Módulos principales

- **TrafficLight**: Gestiona el ciclo de luces y sus tiempos.
- **Vehicle**: Representa vehículos con movimiento y detección de luz.
- **Simulation**: Configura la ventana, crea objetos y ejecuta el bucle principal.

---

## Personalización

Todos los parámetros clave se encuentran en la cabecera de `traffic_light_simulator.py`:

```python
GREEN_TIME   = 6   # seg
YELLOW_TIME  = 2   # seg
RED_TIME     = 6   # seg
SPAWN_RATE   = 1.5 # vehículos/seg
VEHICLE_SPEED= 2.5 # px/frame
```

- **Cambiar tiempos de luz:** Ajusta `GREEN_TIME`, `YELLOW_TIME`, `RED_TIME`.
- **Densidad de tráfico:** Reduce / incrementa `SPAWN_RATE`.
- **Velocidad de vehículos:** Modifica `VEHICLE_SPEED`.
- **Colores:** Edita la constante `COLORS` en el archivo para cambiar la paleta.

---

## Contribuciones

¡Las PR son bienvenidas! Abre un *Issue* para sugerencias o reportar bugs y crea una *Pull Request* con tus mejoras.

1. Haz un *fork* del proyecto.
2. Crea tu rama de características (`git checkout -b feature/nueva-funcionalidad`).
3. *Commitea* tus cambios (`git commit -m 'feat: añade nueva funcionalidad'`).
4. Empuja la rama (`git push origin feature/nueva-funcionalidad`).
5. Crea la PR.

---

## Licencia

Distribuido bajo la **Licencia MIT**. Consulta el archivo `LICENSE` para más información.
