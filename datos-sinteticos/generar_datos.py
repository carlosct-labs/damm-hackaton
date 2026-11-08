#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera respuestas 100 % SINTETICAS para probar la plataforma de escucha activa.

- No contiene ningun dato real de Damm ni de personas.
- Entre 300 y 1.000 respuestas, repartidas en DOS periodos y en 6 colectivos
  con participacion desigual (fabrica, logistica y turno de noche responden menos).
- Tema emergente: "descansos entre turnos" y "comunicacion de cambios" crecen del
  periodo 1 al periodo 2 en fabrica, logistica y turno de noche.
- Sesgos intencionados para validar que la plataforma los detecta:
    * colectivos con poca participacion
    * respuestas demasiado rapidas (menos de 4 segundos) que deben descartarse
    * algunos comentarios con datos personales FICTICIOS que deben ocultarse

Uso:
    python generar_datos.py                 # 720 respuestas, semilla 2026
    python generar_datos.py --n 1000 --seed 7
"""
import argparse, csv, json, math, random
from collections import Counter, defaultdict
from datetime import date, timedelta

# colectivo: personas, participacion P1, participacion P2, centro, canal (qr, correo, teams),
#            medias 1-5 (bienestar, carga, comunicacion, reconocimiento, descansos)
COLECTIVOS = {
    "Planta":                  (1240, .38, .41, "Fabrica",  (.65, .30, .05), (3.6, 3.0, 3.1, 3.3, 2.8)),
    "Logistica":               (860,  .36, .38, "Magatzem", (.60, .33, .07), (3.5, 3.1, 3.2, 3.3, 3.0)),
    "Comercial":               (420,  .52, .55, "Oficina",  (.50, .40, .10), (3.9, 3.4, 3.6, 3.7, 3.6)),
    "Oficina":                 (380,  .65, .67, "Oficina",  (.15, .50, .35), (4.0, 3.6, 3.7, 3.8, 3.8)),
    "Manager":                 (150,  .69, .71, "Oficina",  (.10, .50, .40), (4.1, 3.5, 3.8, 3.9, 3.7)),
    "Planta - Turno de noche": (310,  .15, .19, "Fabrica",  (.70, .28, .02), (3.3, 2.8, 2.9, 3.0, 2.4)),
}
FABRICA = {"Planta", "Logistica", "Planta - Turno de noche"}

PERIODOS = {"P1": (date(2026, 9, 1), date(2026, 9, 30)), "P2": (date(2026, 10, 1), date(2026, 10, 31))}
CANALES = ["Movil-QR", "Correu", "Teams"]

TEMAS = {
    "descansos": ["Entre un turno y otro casi no descanso", "Descansamos muy poco al cambiar de tarde a manana",
                  "Els descansos entre torns son massa curts", "Con tan poco descanso llego cansado/a al siguiente turno"],
    "comunicacion": ["Los cambios de turno nos llegan tarde", "No sabemos que ha cambiado hasta el ultimo momento",
                     "Falta informacion clara cuando cambia algo", "Avisen antes de los cambios, por favor"],
    "turnos": ["La rotacion de turnos no esta clara", "Me gustaria poder elegir mejor mis turnos",
               "El calendario de turnos sale muy tarde"],
    "herramientas": ["El sistema de reservas va muy lento", "La aplicacion se cuelga a menudo",
                     "Faltan herramientas para trabajar mas rapido"],
    "ambiente": ["Muy buen ambiente en el equipo", "Me gusta trabajar con mis companeros",
                 "Se nota companerismo en el dia a dia"],
    "reconocimiento": ["Se agradece que se reconozca el trabajo bien hecho", "A veces cuesta que se valore lo que hacemos"],
    "horarios": ["Seria genial tener mas flexibilidad horaria", "Me vendria bien poder teletrabajar algun dia"],
    "formacion": ["Echo en falta mas formacion", "Me gustaria aprender cosas nuevas aqui"],
    "otros": ["Todo bien, sin comentarios", "No tengo nada que anadir", "Ok", "En general bien"],
}

NOMBRES_FICTICIOS = ["Pedro Gomez", "Laia Soler", "Marc Vidal", "Nuria Pons", "Jordi Ferrer"]


def pesos_tema(colectivo, periodo):
    w = {"descansos": .08, "comunicacion": .10, "turnos": .08, "herramientas": .12, "ambiente": .18,
         "reconocimiento": .08, "horarios": .08, "formacion": .06, "otros": .22}
    if colectivo in FABRICA:
        w["turnos"] = .14
        w["descansos"] = .10 if periodo == "P1" else .30      # tema emergente
        w["comunicacion"] = .14 if periodo == "P1" else .22   # tema emergente
        w["horarios"] = .04
        w["herramientas"] = .08
    else:
        w["descansos"] = .03
        w["herramientas"] = .16
        w["horarios"] = .12
    t = sum(w.values())
    return {k: v / t for k, v in w.items()}


def ruido(texto, rnd):
    if rnd.random() < .30:
        texto = texto[0].lower() + texto[1:]
    if rnd.random() < .20 and len(texto) > 8:
        i = rnd.randrange(2, len(texto) - 2)
        texto = texto[:i] + texto[i] + texto[i:]          # letra repetida
    if rnd.random() < .15:
        texto += rnd.choice([".", "...", "!!", " :("])
    return texto


def puntuacion(media, rnd):
    return max(1, min(5, int(round(rnd.gauss(media, .9)))))


def generar(n, seed):
    rnd = random.Random(seed)
    pesos = {(c, p): v[0] * (v[1] if p == "P1" else v[2]) for c, v in COLECTIVOS.items() for p in PERIODOS}
    total = sum(pesos.values())
    cuotas = {k: max(5, round(n * w / total)) for k, w in pesos.items()}   # nunca menos de 5 por segmento
    filas = []
    for (c, p), cuota in cuotas.items():
        pers, p1, p2, centro, canales, medias = COLECTIVOS[c]
        ini, fin = PERIODOS[p]
        pt = pesos_tema(c, p)
        for _ in range(cuota):
            dias = (fin - ini).days
            tema = rnd.choices(list(pt), weights=list(pt.values()))[0]
            texto = ruido(rnd.choice(TEMAS[tema]), rnd)
            pii = 0
            if rnd.random() < .02:   # datos personales FICTICIOS para probar la deteccion
                nom = rnd.choice(NOMBRES_FICTICIOS)
                texto += rnd.choice([" Hablad con " + nom, " Escribidme a " + nom.lower().replace(" ", ".") + "@correo.example",
                                     " Mi movil es 600 00" + str(rnd.randint(1000, 9999))])
                pii = 1
            seg = rnd.randint(1, 3) if rnd.random() < .015 else int(min(400, max(8, rnd.lognormvariate(math.log(70), .5))))
            esc = [puntuacion(m - (.5 if (p == "P2" and i == 4 and c in FABRICA) else 0), rnd) for i, m in enumerate(medias)]
            filas.append({
                "periode": p,
                "data": (ini + timedelta(days=rnd.randint(0, dias))).isoformat(),
                "col·lectiu": c,
                "centre_tipus": centro,
                "canal": rnd.choices(CANALES, weights=canales)[0],
                "benestar": esc[0], "carrega": esc[1], "comunicacio": esc[2], "reconeixement": esc[3], "descansos": esc[4],
                "segons_resposta": seg,
                "comentari_obert": texto,
                "tema_real": tema,
                "conte_pii_fictici": pii,
            })
    rnd.shuffle(filas)
    for i, f in enumerate(filas, 1):
        f["id_resposta"] = "r_%05d" % i
    cols = ["id_resposta", "periode", "data", "col·lectiu", "centre_tipus", "canal", "benestar", "carrega",
            "comunicacio", "reconeixement", "descansos", "segons_resposta", "comentari_obert", "tema_real", "conte_pii_fictici"]
    return cols, filas


def resumen(filas):
    por = defaultdict(Counter)
    for f in filas:
        por[f["periode"]][f["col·lectiu"]] += 1
    temas = {p: Counter(f["tema_real"] for f in filas if f["periode"] == p) for p in PERIODOS}
    return {
        "respuestas": len(filas),
        "por_periodo_y_colectivo": {p: dict(c) for p, c in por.items()},
        "temas_por_periodo_pct": {p: {t: round(100 * v / sum(c.values()), 1) for t, v in c.most_common()} for p, c in temas.items()},
        "respuestas_menos_de_4_segundos": sum(1 for f in filas if f["segons_resposta"] < 4),
        "comentarios_con_dato_personal_ficticio": sum(f["conte_pii_fictici"] for f in filas),
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Genera respuestas sinteticas (sin datos reales).")
    ap.add_argument("--n", type=int, default=720, help="numero de respuestas (300-1000)")
    ap.add_argument("--seed", type=int, default=2026)
    a = ap.parse_args()
    n = max(300, min(1000, a.n))
    cols, filas = generar(n, a.seed)
    with open("respuestas_sinteticas.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(filas)
    with open("respuestas_sinteticas.json", "w", encoding="utf-8") as fh:
        json.dump(filas, fh, ensure_ascii=False, indent=1)
    r = resumen(filas)
    with open("resumen_sintetico.json", "w", encoding="utf-8") as fh:
        json.dump(r, fh, ensure_ascii=False, indent=1)
    print(json.dumps(r, ensure_ascii=False, indent=1))
