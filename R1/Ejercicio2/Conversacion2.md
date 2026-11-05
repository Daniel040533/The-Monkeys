# Historial Completo de la Conversación y Resolución (Caja Negra - Ejercicio B2)

---

## 1. Acceso a la Caja Negra en Windows

**Usuario:**
Actúa como un Senior Software Engineer y necesito acceder a la caja negra de windows ya que necesitamos resolver un problema.
*(Archivo adjunto: `LEEME_caja_negra.txt`)*

**Senior Software Engineer (IA):**
Para interactuar con la caja negra en Windows y descubrir las reglas de negocio no documentadas, debes ejecutar el binario proporcionado a través de tu terminal. Este programa resuelve el problema aplicando las reglas reales, lo que te permite probar entradas pequeñas para deducir la lógica antes de que tu solución final sea evaluada con entradas enormes.

De acuerdo con las especificaciones del archivo `LEEME_caja_negra.txt`, estos son los pasos para acceder a ella:

1. **Abre tu consola** (CMD o PowerShell) y navega hasta el directorio donde se encuentra el ejecutable y tus archivos de prueba (`dir`).
2. **Inyecta el archivo de prueba a la caja negra** usando el comando correspondiente a tu entorno:
   * **CMD:** `caja_windows.exe < ejemplo1.in`
   * **PowerShell:** `Get-Content ejemplo1.in | .\caja_windows.exe`
3. **Aplica ingeniería inversa con casos propios:** Escribe tus propias entradas pequeñas, guárdalas en archivos de texto y pásalas al ejecutable utilizando la misma sintaxis de tubería (`|`) para descubrir el comportamiento exacto del sistema.

---

## 2. Verificación de Salidas en Python (Ejercicio 1)

**Usuario:**
*(Comparte código de ventana deslizante circular con `deque` y `parse_scaled`)*
¿Ese código ya tiene las salidas?

**Senior Software Engineer (IA):**
**Sí, el código ya está preparado para generar y mostrar las salidas.**
1. **Almacenamiento en una lista (`out`):** Guarda cada resultado con `out.append(f"{best_L} {best_P}")`.
2. **Impresión por pantalla:** Al finalizar todos los casos de prueba, imprime todo de golpe en la salida estándar con `sys.stdout.write("\n".join(out) + "\n")`.

---

**Usuario:**
¿Cómo puedo comprobar mis salidas?

**Senior Software Engineer (IA):**
Puedes comprobarlas mediante redirección en terminal:
* **En PowerShell:**
  ```powershell
  Get-Content prueba.in | python tu_script.py
  ```
* **En CMD:**
  ```cmd
  python tu_script.py < prueba.in
  ```
* **Comparación automática en PowerShell:**
  ```powershell
  Get-Content prueba.in | python tu_script.py > mi_resultado.out
  Compare-Object (Get-Content mi_resultado.out) (Get-Content prueba.out)
  ```

---

## 3. Ejecución y Navegación de Directorios en PowerShell (VS Code)

**Usuario:**
`PS C:\Users\danie\OneDrive\Documentos\GitHub\The-Monkeys> & 'C:\Users\danie\AppData\Local\Python\pythoncore-3.14-64\python.exe' 'c:/Users/danie/OneDrive/Documentos/GitHub/The-Monkeys/R1/Ejercicio1/codigo1.py'`
Correr la prueba desde la terminal de Visual, mi ruta es `C:\Users\danie\OneDrive\Documentos\GitHub\The-Monkeys\R1\Ejercicio1`.

**Senior Software Engineer (IA):**
Para entrar a la carpeta desde la raíz de `The-Monkeys` y ejecutar la prueba:

```powershell
cd R1\Ejercicio1
Get-Content ejemplo1.in | & 'C:\Users\danie\AppData\Local\Python\pythoncore-3.14-64\python.exe' codigo1.py
```

---

## 4. Análisis y Pruebas de Caja Negra - Ejercicio B2 (Impresora con Prioridad)

**Usuario:**
Una impresora recibe trabajos con prioridad y procesa $Q$ órdenes en orden:
* `ADD id p`: agrega el trabajo `id` con prioridad `p` (los `id` nunca se repiten en `ADD`). No imprime nada.
* `BOOST id x`: si el trabajo está pendiente, su prioridad sube `x` e imprime `OK`; si no, `NO`.
* `CANCEL id`: si está pendiente, lo elimina e imprime `OK`; si no, `NO`.
* `PRINT k`: imprime, en una línea separados por espacio, hasta `k` trabajos pendientes, de mayor a menor prioridad, y los elimina. Si no hay ninguno imprime `VACIA`.

Lo que debes descubrir con la caja negra: cómo desempata la impresora cuando dos trabajos tienen la misma prioridad, si `BOOST` cambia algo más que la prioridad, y si las prioridades cambian con el tiempo.
* **Entrada:** línea 1: $Q$. Luego $Q$ líneas, una orden cada una.
* **Salida:** una línea por cada `BOOST`, `CANCEL` y `PRINT`.
* **Límites:** $Q \le 10^6$; $1 \le id \le 2 \cdot 10^6$; $1 \le p \le 10^9$; $1 \le x \le 10^{18}$; $1 \le k \le 10^6$.
* **Tiempo / memoria:** 10 s / 256 MB.

---

### Archivos de Prueba Generados para Descubrir Reglas

#### 1. `test1_empate.in` (Desempate de Prioridad)
```text
4
ADD 10 50
ADD 20 50
ADD 5 50
PRINT 3
```
* **Salida obtenida:** `10 20 5`
* **Regla descubierta:** Desempata por **FIFO** (orden cronológico de llegada).

#### 2. `test2_boost.in` (Efecto de BOOST y CANCEL)
```text
7
ADD 1 50
ADD 2 60
ADD 3 60
BOOST 1 10
BOOST 99 10
CANCEL 3
PRINT 3
```
* **Salida obtenida:**
  ```text
  OK
  NO
  OK
  1 2
  ```
* **Regla descubierta:** `BOOST` **conserva el tiempo de llegada original** del trabajo (`BOOST_RESETS_TIME = False`). Al subir el trabajo `1` a prioridad `60`, sale antes que el trabajo `2` porque llegó antes.

#### 3. `test3_tiempo.in` (Envejecimiento / Aging)
```text
6
ADD 1 10
ADD 2 100
PRINT 1
ADD 3 11
PRINT 2
PRINT 1
```
* **Salida obtenida:**
  ```text
  2
  3 1
  VACIA
  ```
* **Regla descubierta:** Las prioridades **no cambian automáticamente con el tiempo** (`AGING_MODE = 0`).

---

## 5. Código Final en Python (`Codigo2.py`)

Complejidad temporal $O(Q \log Q)$ y espacial $O(Q)$ empleando eliminación perezosa (*Lazy Deletion*) con `heapq` y diccionarios planos para cumplir con el límite de 256 MB de RAM y 10 segundos:

```python
import sys
import heapq

# =====================================================================
# CONFIGURACIÓN DE REGLAS VALIDADAS EN PRUEBAS
# =====================================================================
# 1. Criterio de desempate: "FIFO" (orden de llegada: 10 20 5)
TIE_BREAKER = "FIFO"

# 2. ¿BOOST reinicia el tiempo de llegada del trabajo? (False -> sale 1 2)
BOOST_RESETS_TIME = False

# 3. Envejecimiento (Aging): 0 = Sin cambio automático por turno
AGING_MODE = 0
AGING_RATE = 1
# =====================================================================


def solve():
    input_data = sys.stdin.read().splitlines()
    if not input_data:
        return

    Q = int(input_data[0].strip())

    # Estructuras planas para respetar el límite estricto de 256 MB en Python
    active_prio = {}  # id -> prioridad actual
    active_time = {}  # id -> orden de llegada / timestamp

    # Min-heap de Python (usamos valores negativos para simular Max-Heap)
    heap = []
    out = []

    global_time = 0
    aging_offset = 0

    for i in range(1, Q + 1):
        parts = input_data[i].split()
        if not parts:
            continue
        cmd = parts[0]

        if AGING_MODE == 1:
            aging_offset += AGING_RATE

        if cmd == "ADD":
            job_id = int(parts[1])
            p = int(parts[2])
            global_time += 1

            effective_p = p - aging_offset
            active_prio[job_id] = effective_p
            active_time[job_id] = global_time

            if TIE_BREAKER == "FIFO":
                tie = global_time
            elif TIE_BREAKER == "LIFO":
                tie = -global_time
            elif TIE_BREAKER == "MIN_ID":
                tie = job_id
            else:  # MAX_ID
                tie = -job_id

            heapq.heappush(heap, (-effective_p, tie, job_id, global_time))

        elif cmd == "BOOST":
            job_id = int(parts[1])
            x = int(parts[2])

            if job_id in active_prio:
                out.append("OK")
                new_p = active_prio[job_id] + x
                active_prio[job_id] = new_p

                if BOOST_RESETS_TIME:
                    global_time += 1
                    active_time[job_id] = global_time

                t_stamp = active_time[job_id]
                if TIE_BREAKER == "FIFO":
                    tie = t_stamp
                elif TIE_BREAKER == "LIFO":
                    tie = -t_stamp
                elif TIE_BREAKER == "MIN_ID":
                    tie = job_id
                else:
                    tie = -job_id

                heapq.heappush(heap, (-new_p, tie, job_id, t_stamp))
            else:
                out.append("NO")

        elif cmd == "CANCEL":
            job_id = int(parts[1])
            if job_id in active_prio:
                del active_prio[job_id]
                del active_time[job_id]
                out.append("OK")
            else:
                out.append("NO")

        elif cmd == "PRINT":
            if AGING_MODE == 2:
                aging_offset += AGING_RATE

            k = int(parts[1])
            printed = []

            # Eliminación perezosa (Lazy Deletion) en O(log Q)
            while len(printed) < k and heap:
                neg_p, tie, job_id, t_stamp = heapq.heappop(heap)

                if (
                    job_id in active_prio
                    and active_prio[job_id] == -neg_p
                    and active_time[job_id] == t_stamp
                ):
                    printed.append(str(job_id))
                    del active_prio[job_id]
                    del active_time[job_id]

            if printed:
                out.append(" ".join(printed))
            else:
                out.append("VACIA")

    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    solve()
```

---

## 6. Comandos de Ejecución en PowerShell

```powershell
# Posicionarse en la carpeta del ejercicio
cd "C:\Users\danie\OneDrive\Documentos\GitHub\The-Monkeys\R1\Ejercicio2"

# Ejecutar las pruebas con el script de Python
Get-Content test1_empate.in | python Codigo2.py
Get-Content test2_boost.in | python Codigo2.py
Get-Content test3_tiempo.in | python Codigo2.py
```