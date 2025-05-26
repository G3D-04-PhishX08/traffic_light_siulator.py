"""
Simulador de semáforo con tráfico usando Pygame
================================================

Requisitos:
-----------
- Python 3.9+
- Pygame 2.x  →  pip install pygame



Controles:
----------
• ESC  → Salir
• Barra espaciadora → Pausar / Reanudar la simulación

Descripción general:
--------------------
El programa simula una intersección simple con dos vías (horizontal y vertical).
Un semáforo controla el tráfico alternando los sentidos Norte‑Sur y Este‑Oeste.
Los coches se generan de forma pseudo‑aleatoria y respetan la luz roja.

Estructura principal de clases:
-------------------------------
TrafficLight → administra el estado (ROJO, VERDE, AMARILLO).
Car          → representa cada vehículo en pantalla.
Spawner      → genera coches en intervalos aleatorios.
Simulation   → bucle principal y orquestación.

El código está completamente comentado en español para facilitar el aprendizaje.
"""

import random
import sys
from enum import Enum, auto
from dataclasses import dataclass
from typing import Tuple, List
import pygame

# ============================ CONSTANTES GRÁFICAS ============================ #
ANCHO_PANTALLA: int = 900
ALTO_PANTALLA: int = 600
FPS: int = 60

COLOR_FONDO: Tuple[int, int, int] = (34, 40, 49)
COLOR_CARRETERA: Tuple[int, int, int] = (50, 50, 50)
COLOR_LINEA: Tuple[int, int, int] = (200, 200, 200)
COLOR_COCHE: Tuple[int, int, int] = (255, 165, 0)  # Naranja

# Semáforo
COLOR_ROJO: Tuple[int, int, int] = (220, 20, 60)
COLOR_AMARILLO: Tuple[int, int, int] = (255, 215, 0)
COLOR_VERDE: Tuple[int, int, int] = (0, 200, 0)
COLOR_CAJA_SEMAFORO: Tuple[int, int, int] = (20, 20, 20)

# ============================ ENUMERACIONES & DATAS ========================== #
class LightState(Enum):
    VERDE = auto()
    AMARILLO = auto()
    ROJO = auto()

# Direcciones cardinales simplificadas
class Direction(Enum):
    NORTE = auto()
    SUR = auto()
    ESTE = auto()
    OESTE = auto()

# Parámetros de ciclo del semáforo (en milisegundos)
TIEMPO_VERDE = 6000
TIEMPO_AMARILLO = 2000
# El rojo se calcula implícitamente cuando la otra vía está en verde/amarillo

@dataclass
class TrafficLight:
    """Controla el estado del semáforo para una dirección principal"""

    position: Tuple[int, int]
    orientation: Direction  # Indica qué sentido está en verde cuando este semáforo lo está
    last_change_ms: int = 0
    state: LightState = LightState.VERDE

    def update(self, current_ms: int):
        """Actualiza el estado según temporizador"""
        tiempo_en_estado = current_ms - self.last_change_ms
        if self.state == LightState.VERDE and tiempo_en_estado >= TIEMPO_VERDE:
            self.state = LightState.AMARILLO
            self.last_change_ms = current_ms
        elif self.state == LightState.AMARILLO and tiempo_en_estado >= TIEMPO_AMARILLO:
            self.state = LightState.ROJO
            self.last_change_ms = current_ms
        elif self.state == LightState.ROJO and tiempo_en_estado >= TIEMPO_VERDE + TIEMPO_AMARILLO:
            # Ciclo completo terminado -> volver a VERDE
            self.state = LightState.VERDE
            self.last_change_ms = current_ms

    def color(self) -> Tuple[int, int, int]:
        return {
            LightState.VERDE: COLOR_VERDE,
            LightState.AMARILLO: COLOR_AMARILLO,
            LightState.ROJO: COLOR_ROJO,
        }[self.state]

    def is_green_for(self, direction: Direction) -> bool:
        """Devuelve True si esta luz permite pasar al coche que viene en esa dirección"""
        if direction in (Direction.NORTE, Direction.SUR):
            mismo_eje = self.orientation in (Direction.NORTE, Direction.SUR)
        else:
            mismo_eje = self.orientation in (Direction.ESTE, Direction.OESTE)
        return mismo_eje and self.state == LightState.VERDE

@dataclass
class Car:
    """Representa un vehículo que se desplaza en línea recta"""

    direction: Direction
    position: pygame.Vector2
    speed: float = 120.0  # píxeles por segundo
    length: int = 25
    width: int = 15

    def update(self, dt: float, luces: List[TrafficLight]):
        """Mueve el coche si la luz se lo permite o si ya cruzó la intersección"""
        # Determinar eje y sentido
        dx, dy = 0.0, 0.0
        if self.direction == Direction.NORTE:
            dy = -self.speed * dt
        elif self.direction == Direction.SUR:
            dy = self.speed * dt
        elif self.direction == Direction.ESTE:
            dx = self.speed * dt
        elif self.direction == Direction.OESTE:
            dx = -self.speed * dt

        # Referencia: punto de detención antes de la intersección
        stop_line_y = ALTO_PANTALLA / 2 - 40
        stop_line_x = ANCHO_PANTALLA / 2 - 40

        # Verificar si debe detenerse en rojo
        for luz in luces:
            if not luz.is_green_for(self.direction):
                if self.direction == Direction.NORTE and self.position.y - self.length/2 <= stop_line_y:
                    if self.position.y - self.length/2 > stop_line_y - 5:
                        dy = 0  # Detener
                elif self.direction == Direction.SUR and self.position.y + self.length/2 >= stop_line_y + 80:
                    if self.position.y + self.length/2 < stop_line_y + 85:
                        dy = 0
                elif self.direction == Direction.OESTE and self.position.x - self.length/2 <= stop_line_x:
                    if self.position.x - self.length/2 > stop_line_x - 5:
                        dx = 0
                elif self.direction == Direction.ESTE and self.position.x + self.length/2 >= stop_line_x + 80:
                    if self.position.x + self.length/2 < stop_line_x + 85:
                        dx = 0
        # Actualizar posición
        self.position.x += dx
        self.position.y += dy

    def is_off_screen(self) -> bool:
        return (
            self.position.x < -50 or self.position.x > ANCHO_PANTALLA + 50 or
            self.position.y < -50 or self.position.y > ALTO_PANTALLA + 50
        )

    def rect(self) -> pygame.Rect:
        if self.direction in (Direction.NORTE, Direction.SUR):
            return pygame.Rect(self.position.x - self.width/2, self.position.y - self.length/2, self.width, self.length)
        else:
            return pygame.Rect(self.position.x - self.length/2, self.position.y - self.width/2, self.length, self.width)

class Spawner:
    """Crea coches nuevos en intervalos aleatorios"""

    def __init__(self, direction: Direction, spawn_pos: Tuple[int, int], interval_range=(1500, 4000)):
        self.direction = direction
        self.spawn_pos = spawn_pos
        self.interval_range = interval_range
        self.next_spawn_ms = 0

    def update(self, current_ms: int, cars: List[Car]):
        if current_ms >= self.next_spawn_ms:
            cars.append(Car(self.direction, pygame.Vector2(self.spawn_pos)))
            self.next_spawn_ms = current_ms + random.randint(*self.interval_range)

class Simulation:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        pygame.display.set_caption("Simulador de semáforo con tráfico")
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False

        # Semáforos en dos ejes⊕ simplificación: eje vertical está "gestionado" por traffic_light_ns
        self.traffic_light_ns = TrafficLight((ANCHO_PANTALLA/2 - 60, ALTO_PANTALLA/2 - 60), Direction.NORTE)
        self.traffic_light_ew = TrafficLight((ANCHO_PANTALLA/2 + 20, ALTO_PANTALLA/2 - 60), Direction.ESTE)
        # Desfase para que no sean verdes al mismo tiempo
        self.traffic_light_ew.state = LightState.ROJO
        self.traffic_light_ew.last_change_ms = 0
        self.traffic_light_ns.last_change_ms = 0

        self.cars: List[Car] = []
        # Spawners en los cuatro sentidos
        self.spawners = [
            Spawner(Direction.SUR, (ANCHO_PANTALLA/2 - 20, -30)),
            Spawner(Direction.NORTE, (ANCHO_PANTALLA/2 + 20, ALTO_PANTALLA + 30)),
            Spawner(Direction.ESTE, (-30, ALTO_PANTALLA/2 + 20)),
            Spawner(Direction.OESTE, (ANCHO_PANTALLA + 30, ALTO_PANTALLA/2 - 20)),
        ]

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000  # delta time en segundos
            current_ms = pygame.time.get_ticks()
            self.handle_events()
            if not self.paused:
                self.update(dt, current_ms)
            self.draw()
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused

    def update(self, dt: float, current_ms: int):
        # Actualizar semáforos
        self.traffic_light_ns.update(current_ms)
        # El semáforo EW cambia cuando NS termina verde+amarillo y viceversa
        ciclo_ns = (current_ms - self.traffic_light_ns.last_change_ms)
        if self.traffic_light_ns.state == LightState.ROJO:
            self.traffic_light_ew.update(current_ms)
        else:
            # Mantener semáforo EW en rojo cuando NS no está en rojo
            self.traffic_light_ew.state = LightState.ROJO
            self.traffic_light_ew.last_change_ms = current_ms

        # Spawners
        for spawner in self.spawners:
            spawner.update(current_ms, self.cars)

        # Coches
        for car in list(self.cars):
            car.update(dt, [self.traffic_light_ns, self.traffic_light_ew])
            if car.is_off_screen():
                self.cars.remove(car)

    def draw(self):
        self.screen.fill(COLOR_FONDO)
        self.draw_roads()
        self.draw_traffic_lights()
        self.draw_cars()
        pygame.display.flip()

    # --------------------------------------------------------------------- #
    def draw_roads(self):
        # Fondo de carretera horizontal
        pygame.draw.rect(
            self.screen, COLOR_CARRETERA,
            pygame.Rect(0, ALTO_PANTALLA/2 - 40, ANCHO_PANTALLA, 80))
        # Fondo de carretera vertical
        pygame.draw.rect(
            self.screen, COLOR_CARRETERA,
            pygame.Rect(ANCHO_PANTALLA/2 - 40, 0, 80, ALTO_PANTALLA))
        # Líneas divisoras
        for offset in range(-350, 350, 60):
            pygame.draw.line(
                self.screen, COLOR_LINEA,
                (ANCHO_PANTALLA/2, ALTO_PANTALLA/2 + offset),
                (ANCHO_PANTALLA/2, ALTO_PANTALLA/2 + offset + 30), 3)
            pygame.draw.line(
                self.screen, COLOR_LINEA,
                (ANCHO_PANTALLA/2 + offset, ALTO_PANTALLA/2),
                (ANCHO_PANTALLA/2 + offset + 30, ALTO_PANTALLA/2), 3)

    def draw_traffic_lights(self):
        for luz in (self.traffic_light_ns, self.traffic_light_ew):
            x, y = luz.position
            # Caja del semáforo
            pygame.draw.rect(self.screen, COLOR_CAJA_SEMAFORO, pygame.Rect(x, y, 40, 120), border_radius=4)
            # Luces
            for i, color in enumerate((COLOR_ROJO, COLOR_AMARILLO, COLOR_VERDE)):
                pygame.draw.circle(self.screen, color if luz.state == [LightState.ROJO, LightState.AMARILLO, LightState.VERDE][i] else (60, 60, 60), (x + 20, y + 20 + i*40), 12)

    def draw_cars(self):
        for car in self.cars:
            pygame.draw.rect(self.screen, COLOR_COCHE, car.rect(), border_radius=4)

# =============================== EJECUCIÓN =================================== #
if __name__ == "__main__":
    Simulation().run()
