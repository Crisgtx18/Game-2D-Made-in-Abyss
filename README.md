# Made in Abyss - prototipo 2D

Prototipo de juego de exploracion 2D inspirado en **Made in Abyss**, hecho en
**Python + Pygame**. Es la version temprana que despues evoluciono hasta
[UnderDown](https://github.com/Crisgtx18/UnderDown).

## Sistemas del prototipo

- **Mundo por chunks**: el mapa se carga por bloques mientras el jugador avanza
- **Iluminacion**: oscuridad con luz de la antorcha y zonas de descanso
- **Criaturas**: cada species con su propio comportamiento
- **Maldicion**: al bajar rapido al fondo se acumula pesadez y dano
- **Zonas de descanso** seguras
- **Inventario** y camara con seguimiento

## Como ejecutar

```bash
pip install pygame
python made_in_abyss/main.py
```

## Estructura

```
Game_2D/
  made_in_abyss/
    main.py         <- bucle del juego
    world.py        <- generacion por chunks
    chunks.py       <- carga de bloques
    lighting.py     <- oscuridad y luz
    creatures.py    <- bichos
    curse_system.py <- sistema de maldicion
    rest_zones.py   <- zonas seguras
    player.py  camera.py  inventory.py  ui.py  config.py
  abyss_system.py   <- nucleo del sistema
  player.py  screen.py  word.py
```

## Licencia

Codigo de uso educativo. Made in Abyss es una obra de Akihito Tsukushi;
este es un prototipo de aprendizaje, sin fines comerciales.
