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
    frac_str = parts[1][:6]
    frac_str = frac_str.ljust(6, "0")
    frac_part = int(frac_str)
  else:
    frac_part = 0

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

    raw_vals = []
    for _ in range(N):
      raw_vals.append(parse_scaled(next(iterator)))

    # Duplicamos el arreglo para manejar la estructura circular
    val = raw_vals + raw_vals
    is_q = [v is None for v in val]

    max_dq = deque()
    min_dq = deque()

    best_L = 0
    best_P = 1
    r = 0

    for l in range(N):
        # r avanza mientras sea posible mantener la condición de tolerancia K
      while r + 1 < l + N:
        next_r = r + 1
        if not is_q[next_r]:
          # Verificamos si al agregar next_r se rompe la tolerancia K
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
        best_P = l + 1  # Base 1

      # Limpiamos los elementos que van a salir de la ventana deslizante
      if max_dq and max_dq[0] == l:
        max_dq.popleft()
      if min_dq and min_dq[0] == l:
        min_dq.popleft()

    out.append(f"{best_L} {best_P}")

  sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
  solve()