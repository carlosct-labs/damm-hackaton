# Plataforma de escucha activa · Estrella Damm (prototipo)

Prototipo para **UAB The Hack! 2026 · Reto Damm**. Es un prototipo navegable en HTML, CSS y JavaScript, sin servidor ni instalación.

## Cómo verlo

- Abre `index.html` en el navegador: es la plataforma para People/RRHH (inicio, encuestas, soluciones, informes, personas, escucha activa y avanzado).
- Abre `escucha.html`: es la página pública para el equipo. Un cuadro de texto, sin registro y sin nombre.
- La carpeta `pantallas/` es una versión antigua del prototipo en 20 archivos sueltos; ya no hace falta.

## Qué cubre del reto

El ciclo completo: necesidad, consulta adaptada con IA, validación humana, publicación (enlace, QR), participación sin saturar, análisis, visualización, acción y nueva consulta.

| Pieza | Dónde |
|---|---|
| Consulta adaptada con IA y preguntas neutras | Encuestas > Crear encuesta > Cuestionario |
| Validación humana: editar, reordenar, eliminar, aprobar y registro de quién aprobó | Cuestionario y Revisión |
| Participación representativa, puntos ciegos y fiabilidad | Inicio, Personas, Avanzado |
| Selección rotativa para no saturar | Crear encuesta > Audiencia |
| Escucha activa anónima y recordatorios (SMS, WhatsApp, correo) | Escucha activa y `escucha.html` |
| Soluciones, plan de acción y nueva encuesta de seguimiento | Soluciones |
| Informes con lo que sienten las personas | Informes |

## Privacidad y uso responsable

- **Solo datos sintéticos.** No hay datos reales de Damm ni de personas.
- **Siempre agregado.** Ningún segmento con menos de 5 respuestas se muestra, tampoco al combinar filtros.
- **Sin datos personales en comentarios.** Nombres, correos y teléfonos se ocultan automáticamente.
- **Formularios sospechosos.** Los enviados en menos de 4 segundos se descartan para no manchar los datos.
- **Control humano.** La IA propone, una persona aprueba antes de publicar y queda registrado.
- **Sin secretos.** No hay claves ni tokens en el código. Ver `.env.example`.

## Datos sintéticos

Script: `datos-sinteticos/generar_datos.py` (solo librería estándar de Python).

```
cd datos-sinteticos
python generar_datos.py                 # 720 respuestas, semilla 2026
python generar_datos.py --n 1000 --seed 7
```

Crea `respuestas_sinteticas.csv`, `respuestas_sinteticas.json` y `resumen_sintetico.json`.

| Campo | Ejemplo | Notas |
|---|---|---|
| id_resposta | r_00123 | Aleatorio, nunca ligado a una persona |
| periode | P1 / P2 | Septiembre y octubre de 2026 |
| data | 2026-10-15 | Para ver tendencias |
| col·lectiu | Planta, Logistica, Comercial, Oficina, Manager, Planta - Turno de noche | Categorías amplias |
| centre_tipus | Fabrica / Magatzem / Oficina | Sin centros concretos |
| canal | Movil-QR / Correu / Teams | Para analizar la participación por canal |
| benestar, carrega, comunicacio, reconeixement, descansos | 1 a 5 | Preguntas de escala |
| segons_resposta | 52 | Menos de 4 segundos se descarta |
| comentari_obert | texto libre | Con ruido y faltas |
| tema_real | descansos | Etiqueta oculta para validar la clasificación |
| conte_pii_fictici | 0 / 1 | Comentarios con nombres, correos o teléfonos ficticios |

Sesgos introducidos a propósito:

- Participación desigual: fábrica, logística y turno de noche responden menos.
- Tema emergente: "descansos entre turnos" y "comunicación de cambios" suben del periodo 1 al 2 en fábrica, logística y turno de noche.
- Respuestas demasiado rápidas y comentarios con datos personales ficticios, para probar que se detectan.

## Límites actuales

- La IA del prototipo es simulada: la generación de preguntas, la clasificación de comentarios y las respuestas de Estela usan reglas, no un modelo real.
- Los números de las pantallas son de ejemplo y no salen todavía del conjunto de datos generado.
- Los envíos por SMS, WhatsApp y correo son simulaciones.
