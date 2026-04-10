import threading
import queue
import time
import random

# Cola compartida para almacenar imágenes temporalmente
almacen = queue.Queue()

# Número total de imágenes a simular por cada satélite
IMAGENES_POR_SATELITE = 5

# Número de satélites y analistas
NUM_SATELITES = 2
NUM_ANALISTAS = 2


def satelite(id_satelite):
    """Productor: genera imágenes y las mete en la cola."""
    for i in range(IMAGENES_POR_SATELITE):
        # Simula llegada impredecible de imágenes
        time.sleep(random.uniform(0.5, 2.0))

        imagen = f"Imagen_{id_satelite}_{i}"
        almacen.put(imagen)  # Añade la imagen a la cola

        print(f"[SATÉLITE {id_satelite}] Recibida y almacenada: {imagen}")

    print(f"[SATÉLITE {id_satelite}] Ha terminado de enviar imágenes.")


def analista(id_analista):
    """Consumidor: saca imágenes de la cola y las procesa."""
    while True:
        imagen = almacen.get()  # Espera si no hay imágenes

        # Señal especial para terminar
        if imagen is None:
            almacen.task_done()
            print(f"[ANALISTA {id_analista}] Finaliza su trabajo.")
            break

        print(f"[ANALISTA {id_analista}] Procesando {imagen}...")
        time.sleep(random.uniform(1.0, 3.0))  # Simula procesamiento costoso
        print(f"[ANALISTA {id_analista}] Procesamiento completado: {imagen}")

        almacen.task_done()


# Crear hilos de satélites
hilos_satelites = []
for i in range(NUM_SATELITES):
    t = threading.Thread(target=satelite, args=(i,))
    hilos_satelites.append(t)
    t.start()

# Crear hilos de analistas
hilos_analistas = []
for i in range(NUM_ANALISTAS):
    t = threading.Thread(target=analista, args=(i,))
    hilos_analistas.append(t)
    t.start()

# Esperar a que terminen los satélites
for t in hilos_satelites:
    t.join()

# Esperar a que se procesen todas las imágenes almacenadas
almacen.join()

# Enviar señal de finalización a los analistas
for _ in range(NUM_ANALISTAS):
    almacen.put(None)

# Esperar a que terminen los analistas
for t in hilos_analistas:
    t.join()

print("Sistema finalizado correctamente.")