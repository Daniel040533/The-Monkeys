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