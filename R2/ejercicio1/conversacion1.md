# Problema BF (Ventas masivas): conversación completa

Prompt & Code Challenge 2026, Ronda 2, Categoría Básica.

---

## 1. Usuario

> Necesito que actúes como un ingeniero en Ciencia de Datos para resolver el siguiente problema, te paso el enunciado del problema BF. Analiza los dos ejemplos y dime qué reglas se pueden deducir sobre las líneas inválidas, las ventas repetidas y qué productos se reportan. Indica qué reglas quedan ambiguas y no se pueden confirmar solo con los ejemplos.

*(Adjuntos: `Ronda2_Basica.pdf` y `Ronda2_Basica.zip`)*

## 1. Respuesta

Analicé los dos ejemplos línea por línea. Esto es lo que se puede deducir y lo que no.

### Ejemplo 1 (rango 2028-02-25 a 2028-03-03, salida `1 9 / 2 5 / 3 5`)

| # | Línea | id_venta | prod | cant | Qué pasa |
|---|---|---|---|---|---|
| L1 | 2028-02-27,4,3,5 | 4 | 3 | 5 | Cuenta → prod 3 = 5 |
| L2 | 2028-02-27,4,4,1,1 | 4 | – | – | 5 campos. No se ve en la salida (ver ambigüedades) |
| L3 | 2028-03-01,6,1,9 | 6 | 1 | 9 | Cuenta → prod 1 = 9 |
| L4 | 2028-02-26,6,2,-2 | 6 | 2 | -2 | **No cuenta**: si contara, prod 2 sería 3, no 5 |
| L5 | 2028-03-01,1,2,5 | 1 | 2 | 5 | Cuenta → prod 2 = 5 |
| L6 | 2028-03-03,9,4,5 | 9 | 4 | 5 | No se ve en la salida |
| L7 | 2028-02-26,9,3,5 | 9 | 3 | 5 | **No cuenta**: si contara, prod 3 sería 10 y saldría primero |
| L8 | 2028-02-23,4,4,8␠ | 4 | 4 | 8 | Fuera de rango (además tiene un espacio al final) |

### Ejemplo 2 (rango marzo 2026, salida `4 13 / 1 4`)

| # | Línea | Qué pasa |
|---|---|---|
| M1 | 2026-03-29,6,4,5 | Cuenta → prod 4 |
| M2 | *(vacía)* | Inválida, pero **sí cuenta dentro de las N líneas** (N=11 la incluye) |
| M3 | 2026-03-07,1,4,8 | Cuenta → prod 4 = 5+8 = **13** |
| M4 | 2026-03-25,5,1,4 | Cuenta → prod 1 = 4 |
| M5 | 2026-03-19,3,0,1 | `producto_id = 0`. **No se reporta**: tendría total 1 > 0 y saldría en la salida |
| M6 | 2026-03-29,6,4,5 | Copia exacta de M1. **No cuenta** (si contara, prod 4 = 18) |
| M7 | 2026-03-13,6,2,-5 | Mismo id 6 que M1. Lo más consistente es que no cuente |
| M8 | 2026-03-17,5,3,4 | Mismo id 5 que M4. **No cuenta**: si contara, prod 3 = 4 y aparecería |
| M9 | 2000-02-29,3,3,-2␠ | Fuera de rango (fecha bisiesta válida; espacio al final) |
| M10 | 2026-03-17,5,3,4 | Copia exacta de M8. No cuenta |
| M11 | 2026-04-02,6,3, | Cantidad vacía y fuera de rango |

### Reglas que sí se confirman

1. **El `id_venta` es global**, no depende del producto. Dos líneas con el mismo id y distinto producto también son repetidas (L1/L7 y M4/M8).
2. **De las ventas repetidas, cuenta solo una, y es la primera en aparecer, no la última.** Se ve en id 6 (Ej. 1), id 5 (Ej. 2) y en las copias exactas M6 y M10.
3. **Una línea con `producto_id = 0` se ignora.** Esto es consistente con el rango 1–100 000 del enunciado.
4. **Una línea vacía es inválida pero cuenta dentro de las N.** Para el parser, esto significa leer exactamente N líneas sin saltarse las vacías.
5. **Ordenamiento:** de mayor a menor total, y en empate gana el `producto_id` menor (`2 5` va antes que `3 5`).
6. **Se reportan hasta 3 productos.** Si hay menos con datos, se imprimen menos (Ej. 2 solo tiene 2).

### Reglas ambiguas (los ejemplos no las pueden confirmar)

**Ventas repetidas**
- **"Primera en aparecer" frente a otras reglas.** En todos los casos la línea que ganó era también la de **fecha más reciente** y la de **mayor cantidad (o positiva)**: 9 contra -2, 5 contra -5, 03-25 contra 03-17. Las tres reglas dan el mismo resultado en estos ejemplos.
- **Si la duplicación se resuelve antes o después de filtrar por fecha.** No hay ningún caso donde la primera aparición esté fuera de rango y una posterior dentro.
- **Si una línea inválida "ocupa" el `id_venta`.** L2 (inválida, id 4) aparece después de L1, así que no se nota. Falta un caso con la inválida primero.

**Líneas inválidas**
- **Más de 4 campos (L2) y cantidad vacía (M11):** no se puede saber si son inválidas. L2 se descarta de todos modos por ser repetida, y M11 está fuera de rango.
- **Espacios al final de la línea:** las dos líneas que los tienen (L8 y M9) están fuera de rango, así que no se sabe si invalidan la línea.
- **Fechas imposibles** (02-30, mes 13, 2027-02-29), `id_venta` fuera de 1–4 000 000, `producto_id` > 100 000, signos como `+5`, cantidades no enteras o cantidad 0: no aparece ningún caso.

**Productos reportados**
- **Productos con total ≤ 0:** en ningún ejemplo queda un producto con total negativo o cero que realmente cuente, porque las líneas negativas resultaron ser repetidas descartadas. No se sabe si se reportan.
- **Cuándo se imprime `SIN DATOS`:** ¿cuando no hay ventas válidas en el rango, o también cuando todos los totales son ≤ 0?
- **Si las fechas D1 y D2 se incluyen:** el enunciado dice "inclusive", pero los ejemplos no lo prueban. La única línea en un límite es L6 (2028-03-03), y su producto 4, aunque contara (total 5), quedaría oculto por el desempate contra el producto 3.

Todas estas son las preguntas que hay que hacerle a la caja negra con entradas pequeñas, una variable a la vez.

---

## 2. Usuario

> La caja negra solo acepta N ≤ 300 y solo muestra el top 3. Diseña archivos de prueba pequeños que respondan cada duda pendiente. Que cada salida distinga entre las posibles reglas: primera aparición o fecha más reciente; si el duplicado se descarta antes o después de filtrar por fecha; si una línea inválida ocupa el id; si se reportan totales ≤ 0. Dame los comandos para crear los archivos desde CMD de Windows y una tabla para interpretar cada resultado.

## 2. Respuesta

Son 5 archivos. Todos usan el rango `2026-03-01 2026-03-31`, y cada resultado posible da una salida distinta. No ejecuté la caja negra, así que estas son las salidas esperadas según cada regla, no resultados reales.

### Comandos para CMD

Abre CMD en la carpeta `BF` y pega cada bloque completo:

```bat
(
echo 2026-03-01 2026-03-31
echo 6
echo 2026-03-15,1,1,2
echo 2026-03-28,1,2,3
echo 2026-03-12,1,3,9
echo 2026-03-02,1,4,4
echo 2026-03-20,1,5,1
echo 2026-03-05,2,6,1
) > t1_repetidas.in
```

```bat
(
echo 2026-03-01 2026-03-31
echo 3
echo 2026-04-15,1,1,5
echo 2026-03-10,1,2,4
echo 2026-03-05,2,3,1
) > t2_filtro.in
```

```bat
(
echo 2026-03-01 2026-03-31
echo 6
echo 2026-03-20,1,0,9
echo 2026-03-10,1,1,5
echo 2026-03-20,2,7,9,9
echo 2026-03-10,2,2,4
echo 2026-03-20,3,8,
echo 2026-03-10,3,3,3
) > t3_invalida_id.in
```

```bat
(
echo 2026-03-01 2026-03-31
echo 2
echo 2026-03-10,1,1,-3
echo 2026-03-11,2,2,-1
) > t4_negativos.in
```

```bat
(
echo 2026-03-01 2026-03-31
echo 4
echo 2026-03-10,1,5,2
echo 2026-03-11,2,2,0
echo 2026-03-12,3,3,5
echo 2026-03-13,4,3,-5
) > t5_cero.in
```

Para correr todos de una vez:

```bat
for %f in (t*.in) do @(echo === %f & caja_windows.exe < %f)
```

No dejes espacios al final de las líneas `echo`, porque CMD los copia al archivo.

### Tablas de interpretación

**T1: ¿Qué venta repetida cuenta?** Las 5 líneas con id 1 se diferencian así: la primera es el prod 1, la de fecha más reciente el prod 2, la de mayor cantidad el prod 3, la de fecha más antigua el prod 4 y la última el prod 5. El prod 6 es un control con otro id.

| Salida | Regla |
|---|---|
| `1 2` / `6 1` | **Primera aparición** |
| `2 3` / `6 1` | **Fecha más reciente** |
| `3 9` / `6 1` | Mayor cantidad |
| `4 4` / `6 1` | Fecha más antigua |
| `5 1` / `6 1` | Última aparición (o menor cantidad) |
| `3 9` / `4 4` / `2 3` | No se descartan repetidos si cambia el producto |
| `6 1` | Si el id está repetido, no cuenta ninguna |

**T2: ¿Se descarta el repetido antes o después de filtrar por fecha?** La primera línea con id 1 está fuera de rango (abril) y además es la de fecha más reciente y la de mayor cantidad. Así la prueba sirve tanto si T1 sale "primera aparición" como si sale "fecha más reciente".

| Salida | Regla |
|---|---|
| `3 1` | **Antes**: la línea de abril "gana" el id y bloquea la de marzo |
| `2 4` / `3 1` | **Después**: primero se filtra por fecha y luego se busca el repetido |

**T3: ¿Una línea inválida ocupa el id?** Cada id tiene primero una línea dudosa (que además es la de fecha más reciente) y después una válida. Cada id se lee por separado:

| Id | Si aparece… | Significa |
|---|---|---|
| 1 (prod 0) | `1 5` | La línea con producto 0 **no ocupa** el id |
|  | no aparece prod 1 | La línea con producto 0 **sí ocupa** el id |
| 2 (5 campos) | `7 9` | La línea con 5 campos **es válida** (se ignora el campo extra) |
|  | `2 4` | Es inválida y **no ocupa** el id |
|  | ni 7 ni 2 | Es inválida y **sí ocupa** el id |
| 3 (cantidad vacía) | `3 3` | Es inválida y **no ocupa** el id |
|  | no aparece prod 3 | **Ocupa** el id (o se tomó como cantidad 0) |

**T4: ¿Se reportan totales negativos?**

| Salida | Regla |
|---|---|
| `SIN DATOS` | Solo se reportan totales > 0, y `SIN DATOS` sale cuando no hay ninguno positivo |
| `2 -1` / `1 -3` | Se reportan los negativos (ordenados de mayor a menor) |

**T5: ¿Se reportan totales iguales a 0?** El prod 2 tiene una venta con cantidad 0. El prod 3 suma 0 con dos ventas distintas (+5 y -5).

| Salida | Regla |
|---|---|
| `5 2` | Solo se reportan totales > 0 |
| `5 2` / `2 0` / `3 0` | Se reportan totales = 0, y la cantidad 0 es válida |
| `5 2` / `3 0` | Se reportan totales = 0, pero una línea con cantidad 0 es inválida |

Corre T1 antes que T2. Si T1 sale "fecha más antigua", T2 deja de servir, porque la línea de marzo ganaría en los dos casos. Si pasa eso, dímelo y la rediseño.

---

## 3. Usuario

> Diseña una sola prueba que revise muchas reglas de validez a la vez: años bisiestos, mes 13, fecha sin ceros, ceros a la izquierda, signo +, decimales, espacios, coma de más, id y producto fuera de rango, cantidad 0. Usa cantidades que sean potencias de 2 sobre el mismo producto, para que el total revele exactamente qué líneas aceptó la caja.

## 3. Respuesta

La prueba tiene 26 líneas. Todo el reporte cae en el **producto 1**, y cada regla dudosa tiene su propio bit. El rango de fechas, 1900 a 2100, cubre todas las fechas de la prueba. El total del producto 1 dice exactamente qué líneas aceptó la caja.

### Comandos para CMD

Cada línea lleva la redirección al principio (`>>archivo echo …`) para que CMD no quite ni agregue espacios. Pega todo en la carpeta `BF`:

```bat
>t6_validez.in echo 1900-01-01 2100-12-31
>>t6_validez.in echo 26
>>t6_validez.in echo 2024-03-10,101,1,1
>>t6_validez.in echo 2024-02-29,102,1,2
>>t6_validez.in echo 2023-02-29,103,1,4
>>t6_validez.in echo 2000-02-29,104,1,8
>>t6_validez.in echo 1900-02-29,105,1,16
>>t6_validez.in echo 2024-13-01,106,1,32
>>t6_validez.in echo 2024-00-10,107,1,64
>>t6_validez.in echo 2024-04-31,108,1,128
>>t6_validez.in echo 2024-3-5,109,1,256
>>t6_validez.in echo 2024-03-10,0110,1,512
>>t6_validez.in echo 2024-03-10,111,01,1024
>>t6_validez.in echo 2024-03-10,112,1,02048
>>t6_validez.in echo 2024-03-10,113,1,+4096
>>t6_validez.in echo 2024-03-10,114,1,8192.0
>>t6_validez.in echo  2024-03-10,115,1,16384
>>t6_validez.in echo 2024-03-10, 116,1,32768
>>t6_validez.in echo 2024-03-10,117,1,65536 
>>t6_validez.in echo 2024-03-10,118,1,131072,
>>t6_validez.in echo 2024-03-10,,119,1,262144
>>t6_validez.in echo 2024-03-10,0,1,524288
>>t6_validez.in echo 2024-03-10,4000001,1,1048576
>>t6_validez.in echo 2024-03-10,4000000,1,2097152
>>t6_validez.in echo 2024-03-20,123,1,0
>>t6_validez.in echo 2024-03-10,123,1,4194304
>>t6_validez.in echo 2024-03-10,125,100001,5
>>t6_validez.in echo 2024-03-10,126,100000,3
caja_windows.exe < t6_validez.in
```

Ojo con dos líneas de espacios. La del **16384** lleva **dos** espacios después de `echo`, y la del **65536** lleva un espacio al final. Algunos editores los borran al copiar. Para revisarlo:

```bat
findstr /n /r /c:"^ " /c:" $" t6_validez.in
```

Debe mostrar las líneas **17** y **19** del archivo.

### Tabla para leer el total del producto 1

| Bit | Cantidad | Qué prueba | Línea | Si se suma… |
|---|---|---|---|---|
| 0 | 1 | Control válido | `2024-03-10,101,1,1` | Debe sumarse siempre |
| 1 | 2 | Bisiesto normal | `2024-02-29` | Acepta el 29 de febrero bisiesto |
| 2 | 4 | 29 de febrero en año no bisiesto | `2023-02-29` | **No** revisa si el año es bisiesto |
| 3 | 8 | Bisiesto por la regla del 400 | `2000-02-29` | Acepta el 2000 |
| 4 | 16 | Siglo no bisiesto | `1900-02-29` | Usa solo "divisible entre 4" (regla incompleta) |
| 5 | 32 | Mes 13 | `2024-13-01` | **No** valida el mes |
| 6 | 64 | Mes 0 | `2024-00-10` | **No** valida el mes |
| 7 | 128 | 31 de abril | `2024-04-31` | **No** valida los días de cada mes |
| 8 | 256 | Fecha sin ceros | `2024-3-5` | Acepta la fecha sin el formato estricto AAAA-MM-DD |
| 9 | 512 | Cero a la izquierda en id | `0110` | Acepta ceros a la izquierda en el id |
| 10 | 1024 | Cero a la izquierda en producto | `01` | Acepta ceros a la izquierda en el producto |
| 11 | 2048 | Cero a la izquierda en cantidad | `02048` | Acepta ceros a la izquierda en la cantidad |
| 12 | 4096 | Signo + | `+4096` | Acepta el `+` |
| 13 | 8192 | Decimal | `8192.0` | Acepta decimales (o corta la parte decimal) |
| 14 | 16384 | Espacio al inicio | `␠2024-…` | Ignora los espacios iniciales |
| 15 | 32768 | Espacio después de una coma | `, 116` | Ignora los espacios entre campos |
| 16 | 65536 | Espacio al final | `…65536␠` | Ignora los espacios finales |
| 17 | 131072 | Coma al final | `…131072,` | Tolera una coma de más al final |
| 18 | 262144 | Coma doble | `,,119` | Tolera campos vacíos o comas repetidas |
| 19 | 524288 | id = 0 | `,0,` | **No** valida el id mínimo |
| 20 | 1048576 | id = 4 000 001 | `,4000001,` | **No** valida el id máximo |
| 21 | 2097152 | id = 4 000 000 (límite) | `,4000000,` | Acepta el límite superior (debería) |
| 22 | 4194304 | Cantidad 0 (ver nota) | par con id 123 | Bit **ausente**: la línea con cantidad 0 es válida y ocupó el id. Bit **presente**: es inválida |

**Las otras líneas de la salida (producto fuera de rango):**

| Si aparece | Significa |
|---|---|
| `100000 3` | Acepta el límite superior de producto (debería) |
| `100001 5` | **No** valida el producto máximo |

**Para decodificar el total**, pega esto en PowerShell y cambia `TOTAL` por el número que dio la caja:

```powershell
$t=TOTAL; 0..22 | % { if ($t -band (1 -shl $_)) { "bit $_ aceptada" } else { "bit $_ rechazada" } }
```

### Notas

- **El bit 0 también revisa el fin de línea.** CMD guarda los archivos con fin de línea de Windows (CRLF), y los ejemplos usan el de Linux (LF). Si la caja da `SIN DATOS` o el total es par, está rechazando el CRLF, y eso también afectaría las pruebas T1 a T5.
- **El bit 22 depende de T1 y T3.** La línea con cantidad 0 está primero y además es la de fecha más reciente, así que gana el id con cualquiera de las dos reglas de T1. Pero si T3 mostró que una línea inválida sí ocupa el id, este bit no sirve: saldría ausente en los dos casos.

---

## 4. Usuario

> Escribe la solución en Python con todas las reglas confirmadas. Debe procesar hasta 3 millones de líneas (~90 MB) en menos de 16 s y con menos de 64 MB de memoria. No uses sys.stdin.read() ni un set para los ids. Explica qué estructuras usas y por qué caben en memoria.

## 4. Respuesta

Primero corrí T1 a T6 en la caja negra (la versión Linux) y luego más pruebas para precisar límites. La solución (`bf.py`) da exactamente lo mismo que la caja en los dos ejemplos, en las 6 pruebas y en 1500 entradas aleatorias con líneas raras. Con 3 millones de líneas (87 MB) tardó **2.3 s** y usó **22 MB** de memoria en el pico.

### Resultados de la caja negra

| Prueba | Salida de la caja | Conclusión |
|---|---|---|
| T1 | `1 2` / `6 1` | Cuenta la primera aparición |
| T2 | `3 1` | El repetido se descarta antes de filtrar por fecha |
| T3 | `1 5` / `2 4` / `3 3` | Las líneas inválidas no ocupan el id; la línea con 5 campos es inválida |
| T4 | `SIN DATOS` | Los totales negativos no se reportan |
| T5 | `5 2` | Los totales iguales a 0 no se reportan |
| T6 | `1 3595` / `100000 3` | 3595 = bits 0, 1, 3, 9, 10 y 11 (ver correcciones abajo) |

### Reglas confirmadas con la caja

**Repetidas:**
- Cuenta la **primera línea válida** de cada `id_venta`.
- El id se ocupa **aunque esa línea esté fuera del rango de fechas**. Es decir, el repetido se descarta antes de filtrar por fecha.
- Una línea **inválida no ocupa** el id.

**Una línea es válida solo si cumple todo esto:**
- Tiene exactamente 4 campos separados por coma.
- No tiene ningún espacio. Sí se acepta el fin de línea de Windows (`\r\n`).
- La fecha va en formato estricto `AAAA-MM-DD`, es una fecha real (con bisiestos) y el año está entre **2000 y 2099**. Un año fuera de ese rango hace la línea inválida, no solo "fuera de rango".
- `id_venta` va de 1 a 4 000 000 y `producto_id` de 1 a 100 000. Solo se permiten dígitos (sin `+` ni decimales), se aceptan ceros a la izquierda y el número puede tener **como máximo 12 dígitos**. Por ejemplo, `0110` es el mismo id que `110`.
- `cantidad` lleva un `-` opcional y luego de 1 a 12 dígitos. Su valor debe estar entre **-10 000 y 10 000** y **no puede ser 0** (`-0` también es inválido).

**Reporte:**
- D1 y D2 se incluyen en el rango.
- Solo se reportan productos con **total > 0**, y si no hay ninguno se imprime `SIN DATOS`.

**Dos correcciones a la lectura de T6:**
- **Bits 21 y 22:** salieron ausentes porque esas cantidades pasan de 10 000, no por el id ni por la cantidad 0. El id 4 000 000 sí es válido.
- **Bit 4 (1900-02-29):** se rechazó por el año, no por la regla del bisiesto. Entre 2000 y 2099, "divisible entre 4" basta para saber si un año es bisiesto.

### Estructuras y por qué caben en 64 MB

| Estructura | Para qué | Memoria |
|---|---|---|
| `visto = bytearray(4_000_001)` | Marca de 1 byte por `id_venta`. Reemplaza al `set`, que con millones de ints usaría más de 200 MB | **4 MB** |
| `total = [0] * 100_001` | Venta neta de cada producto, usando el `producto_id` como índice directo | 0.8 MB de lista + ≤ 2.8 MB de enteros |
| `fechas`: diccionario con las 36 525 fechas válidas de 2000 a 2099 | Valida la fecha y dice si está en rango con una sola búsqueda. Es de tamaño fijo, así que la basura en la entrada no lo hace crecer | ~4 MB |
| Lectura `for linea in sys.stdin.buffer` | Lee línea por línea en binario, con búfer. Nunca tiene el archivo completo en memoria | Unos KB |

Lo demás es el propio intérprete de Python (~10 MB).

### Por qué es rápido

- Trabaja con `bytes`, sin decodificar a texto.
- Hace `split(b",")` una vez por línea y usa `isdigit()` e `int()` en lugar de expresiones regulares.
- **Descarta pronto:** después de validar la fecha y el id, si ese id ya estaba ocupado salta la línea sin revisar producto ni cantidad.
- El top 3 sale de `heapq.nsmallest(3, …)` sobre los productos con total positivo. Es un recorrido de 100 001 posiciones, que se hace una sola vez.

---

## 5. Usuario

> Mide tiempo y memoria del código con 3 millones de líneas. Prueba al menos dos alternativas de lectura y validación (regex por línea, split con isdigit, lectura por bloques). Elige la más rápida que siga respetando el límite de memoria. Después vuelve a verificarla contra la caja negra.

## 5. Respuesta

Me quedo con la **lectura por bloques + `split` con `isdigit`**: es la más rápida, usa 30 MB y coincide con la caja negra en todo lo que probé. La solución final es `bf_final.py` (código completo al final de este archivo).

### Medición (3 millones de líneas, 87 MB; mediana de 3 corridas)

| Variante | Tiempo | Memoria pico | ¿Misma salida? |
|---|---|---|---|
| A. Línea por línea + `split`/`isdigit` (la anterior) | 2.43 s | 22.4 MB | Sí |
| B. Línea por línea + regex | 2.61 s | 23.3 MB | Sí |
| **C. Bloques de 1 MB + `split`/`isdigit`** | **2.00 s** | **30.0 MB** | **Sí** |
| D. Bloques de 1 MB + regex | 2.53 s | 31.4 MB | Sí |

- **Por qué la regex sale más lenta:** valida el formato, pero aun así hay que convertir los números con `int()` y revisar sus rangos. Al final hace más trabajo por línea que `split`.
- **Por qué los bloques ganan:** se lee 1 MB a la vez y se parte con un solo `split(b"\n")`, en lugar de pedir cada línea por separado al iterador de Python. Los ~8 MB extra son el bloque y su lista de líneas, que se liberan en cada vuelta.

### Una protección que agregué

Un archivo con una línea enorme sin saltos de línea haría que la versión A guardara la línea completa en memoria. Con 90 MB en una sola línea, A llegó a **193 MB**. En C, si el pedazo pendiente pasa de 128 bytes, se reemplaza por una marca inválida, porque ninguna línea válida mide más de 53 bytes. Con ese mismo archivo, C se quedó en **22 MB**.

### Verificación contra la caja negra (versión Linux)

- Los 2 ejemplos y las pruebas T1 a T6: todo coincide.
- 2000 entradas aleatorias con líneas raras, fin de línea de Windows, archivos sin salto final y líneas sobrantes después de las N: todo coincide.
- 1000 entradas más con **bloques de 7 bytes**, para forzar cortes a media línea y entre `\r` y `\n`: todo coincide.
- Una línea de 2000 caracteres y un id con 500 ceros: coincide con la caja.

---

## Anexo: código final (`bf_final.py`)

```python
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
```
