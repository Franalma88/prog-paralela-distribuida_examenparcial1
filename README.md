# Sistema de Procesamiento de Imágenes Satelitales

# Descripción del problema

En este sistema, las imágenes llegan continuamente desde distintos satélites. Estas imágenes deben pasar por dos fases:

1. **Recepción y almacenamiento temporal**  
   Las imágenes llegan de forma impredecible, a veces muy rápido y otras veces lentamente. Por eso es necesario almacenarlas temporalmente.

2. **Procesamiento y análisis**  
   Las imágenes almacenadas son procesadas por analistas automáticos. Como el procesamiento puede tardar bastante, pueden acumularse varias imágenes en espera.

El objetivo es construir un sistema que permita:

- no perder ninguna imagen recibida,
- gestionar correctamente la espera,
- mantener un orden razonable de procesamiento,
- y soportar diferencias entre la velocidad de llegada y la velocidad de procesamiento.

---

##  Solución propuesta

La solución implementada sigue el modelo **productor-consumidor**:

- Los **satélites** actúan como **productores**.
- Los **analistas automáticos** actúan como **consumidores**.
- Se utiliza una **cola compartida** como almacenamiento temporal.

En Python se ha usado `queue.Queue`, que permite gestionar concurrencia de forma segura entre hilos.

---

## Por qué se ha usado una cola

Se ha elegido una **cola FIFO (First In, First Out)**:

- La primera imagen que entra es la primera en procesarse.
- Se mantiene el orden de llegada.
- Se evita que imágenes antiguas queden sin procesar.

Además:

- Si llegan muchas imágenes → se acumulan en la cola.
- Si llegan pocas → los analistas esperan.

---

#Funcionamiento general

El sistema crea varios hilos:

- **Satélites (productores)** → generan imágenes.
- **Analistas (consumidores)** → procesan imágenes.

### Flujo del sistema

1. Un satélite genera una imagen.
2. La imagen se añade a la cola.
3. Un analista toma una imagen de la cola.
4. El analista la procesa.
5. El proceso continúa hasta terminar todas las imágenes.

---

## Ventajas de esta solución

- ✔ No se pierden imágenes  
- ✔ Mantiene el orden de llegada (FIFO)  
- ✔ Maneja picos de carga  
- ✔ Permite espera controlada  
- ✔ Evita condiciones de carrera  
- ✔ Fácil de implementar y entender  

---

##  Por qué no he usado usar peer-to-peer (P2P)

Aunque se podría plantear una solución **peer-to-peer**, no es adecuada para este problema.

### 🔎 Qué es peer-to-peer

Es un modelo donde los nodos se comunican directamente entre sí, sin un sistema central.

---

### Problemas de usar P2P en este caso

#### 1. No hay almacenamiento central
El problema exige almacenar imágenes temporalmente.  
P2P no ofrece un punto claro de almacenamiento.

#### 2. Riesgo de pérdida de imágenes
Si los analistas están ocupados, las imágenes podrían perderse.  
Con una cola, siempre quedan almacenadas.

#### 3. Difícil control del orden
No es fácil mantener el orden de llegada en P2P.  
La cola FIFO sí lo garantiza.

#### 4. Mayor complejidad
La sincronización entre nodos es más complicada.  
El modelo productor-consumidor es más simple y robusto.

#### 5. No encaja con el enunciado
El sistema tiene roles claros:
- productores (satélites)
- almacenamiento (cola)
- consumidores (analistas)

Por lo que lo que parecia mas normal, ha sido muy dificil desde el codigo y creo que es mucho mas simple con este cambio
---

