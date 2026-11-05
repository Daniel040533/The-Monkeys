# Registro de Sesión: Ingeniería Inversa de la Caja Negra (Problema B1)

## Contexto Inicial
El usuario consulta cómo acceder y utilizar el ejecutable de la caja negra para Windows (`caja_windows.exe`) correspondiente al Reto 1, Categoría Básica (Problema B1).

### Comandos de Ejecución en Windows
Para interactuar con la caja negra localmente:
- **CMD:** `caja_windows.exe < ejemplo1.in`
- **PowerShell:** `Get-Content ejemplo1.in | .\caja_windows.exe`

---

## Hallazgos y Análisis del Problema B1

A partir de los casos de prueba ejecutados y los ejemplos del documento oficial, se descubrieron las reglas clave que rigen el comportamiento del sistema:

1. **Arreglo Circular:** Los sensores se disponen en un anillo circular (después del sensor $N$ sigue el sensor $1$), y la longitud máxima de la racha está limitada a $N$.
2. **Tolerancia $K$ Estricta:** La condición de estabilidad exige que en todo el tramo se cumpla $\max(\text{lecturas}) - \min(\text{lecturas}) \le K$.
3. **Precisión Numérica:** Debido a que las lecturas alcanzan magnitudes de hasta $9 \cdot 10^{12}$ con 6 decimales, los cálculos en punto flotante (`double`) fallan por errores de precisión. Es obligatorio escalar las entradas multiplicándolas por $10^6$ para tratarlas como enteros exactos.
4. **Comportamiento de las Interrogaciones (`?`):** Actúan como comodines libres que simplemente se ignoran al evaluar la diferencia máxima y mínima dentro de la ventana de estabilidad.

---

## Solución Optimizada en Python ($O(N)$)

Dado que la suma de $N \le 10^6$ y se trabaja en Python con un límite de tiempo estricto de $8$ segundos, se diseñó una solución basada en una **ventana deslizante circular** utilizando colas doblemente terminadas (`collections.deque`) y lectura masiva de buffers (`sys.stdin.read`):

```python
import sys
from collections import deque

def parse_scaled(s):
    """Convierte un string decimal de hasta 6 decimales a un entero escalado por 10^6."""
    if s == "?":
        return None
    neg = False
    if s[0] == "-":
        neg = True
        s = s[1:]
    
    parts = s.split(".")
    int_part = int(parts[0])
    frac_part = 0
    if len(parts) > 1:
        frac_str = parts[1][:6].ljust(6, '0')
        frac_part = int(frac_str)
        
    val = int_part * 1000000 + frac_part
    return -val if neg else val

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    T = int(next(iterator))
    
    out = []
    for _ in range(T):
        N = int(next(iterator))
        k_str = next(iterator)
        K = parse_scaled(k_str)
        
        raw_vals = [parse_scaled(next(iterator)) for _ in range(N)]
        
        # Duplicamos el arreglo para manejar la estructura circular
        val = raw_vals + raw_vals
        is_q = [v is None for v in val]
        
        max_dq = deque()
        min_dq = deque()
        
        best_L = 0
        best_P = 1
        r = 0
        
        for l in range(N):
            while r + 1 < l + N:
                next_r = r + 1
                if not is_q[next_r]:
                    cur_max = val[next_r]
                    if max_dq and val[max_dq[0]] > cur_max:
                        cur_max = val[max_dq[0]]
                    
                    cur_min = val[next_r]
                    if min_dq and val[min_dq[0]] < cur_min:
                        cur_min = val[min_dq[0]]
                    
                    if cur_max - cur_min > K:
                        break
                r = next_r
                if not is_q[r]:
                    while max_dq and val[max_dq[-1]] <= val[r]:
                        max_dq.pop()
                    max_dq.append(r)
                    while min_dq and val[min_dq[-1]] >= val[r]:
                        min_dq.pop()
                    min_dq.append(r)
            
            cur_L = r - l + 1
            if cur_L > best_L:
                best_L = cur_L
                best_P = l + 1 # Base 1
            
            if max_dq and max_dq[0] == l:
                max_dq.popleft()
            if min_dq and min_dq[0] == l:
                min_dq.popleft()
                
        out.append(f"{best_L} {best_P}")
        
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    solve()
```