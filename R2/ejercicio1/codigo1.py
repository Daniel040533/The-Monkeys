import sys
from heapq import nsmallest

BLOQUE = 1 << 20

def main():
    entrada = sys.stdin.buffer
    d1, d2 = entrada.readline().split()
    n = int(entrada.readline())
    dias_mes = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    fechas = {}
    for a in range(2000, 2100):
        for m in range(1, 13):
            ult = 29 if (m == 2 and a % 4 == 0) else dias_mes[m - 1]
            for d in range(1, ult + 1):
                f = b"%04d-%02d-%02d" % (a, m, d)
                fechas[f] = d1 <= f <= d2
    visto = bytearray(4_000_001)
    total = [0] * 100_001
    get_fecha = fechas.get

    faltan = n
    resto = b""
    fin = False
    while faltan > 0 and not fin:
        bloque = entrada.read(BLOQUE)
        if not bloque:
            fin = True
            if not resto:
                break
            lineas = [resto]
        else:
            lineas = (resto + bloque).split(b"\n")
            resto = lineas.pop()          # la última puede estar incompleta
            if len(resto) > 128:          # ninguna línea válida mide más de 53 bytes
                resto = b"#"              # se conserva como línea inválida sin guardar su texto
        if len(lineas) > faltan:
            del lineas[faltan:]
        faltan -= len(lineas)
        for linea in lineas:
            if linea[-1:] == b"\r":
                linea = linea[:-1]
            campos = linea.split(b",")
            if len(campos) != 4:
                continue
            f, s_id, s_prod, s_cant = campos
            en_rango = get_fecha(f)
            if en_rango is None:
                continue
            if not s_id.isdigit() or len(s_id) > 12:
                continue
            id_v = int(s_id)
            if id_v < 1 or id_v > 4_000_000 or visto[id_v]:
                continue
            if not s_prod.isdigit() or len(s_prod) > 12:
                continue
            prod = int(s_prod)
            if prod < 1 or prod > 100_000:
                continue
            cuerpo = s_cant[1:] if s_cant[:1] == b"-" else s_cant
            if not cuerpo.isdigit() or len(cuerpo) > 12:
                continue
            cant = int(s_cant)
            if cant == 0 or cant > 10_000 or cant < -10_000:
                continue
            visto[id_v] = 1
            if en_rango:
                total[prod] += cant
    top = nsmallest(3, ((-t, p) for p, t in enumerate(total) if t > 0))
    sys.stdout.write("SIN DATOS\n" if not top else "".join("%d %d\n" % (p, -t) for t, p in top))

main()
