# Care Damm · Plataforma de escucha activa (prototipo)

Prototipo para **UAB The Hack! 2026 · Reto Damm**. Es un prototipo navegable en HTML, CSS y JavaScript, sin servidor ni instalación.

## Descripción

Care Damm es una plataforma de escucha activa para Damm que cierra el ciclo completo: necesidad, consulta, participación, análisis, acción y nueva consulta.

RRHH describe qué quiere saber y la IA propone una microconsulta breve (3-6 preguntas neutras, con tono y longitud adaptados a planta, logística, oficina o managers). Una persona la edita, reordena y aprueba antes de publicarla, y queda registrado quién lo hizo. Se comparte por enlace o QR, pensada para móvil y para quien no tiene ordenador, con selección rotativa para no saturar y recordatorios por SMS, WhatsApp o correo.

El panel muestra participación, representatividad y puntos ciegos por colectivo, temas emergentes entre periodos y alertas, siempre con tamaño de muestra, fiabilidad y límites del análisis, sin presentar correlaciones como causas. Después propone acciones y una encuesta de seguimiento.

La privacidad es de diseño: resultados agregados, ningún segmento con menos de 5 respuestas, datos personales ocultos y datos 100 % sintéticos. La publicación de formularios se apoya en Typeform y la evolución natural es la integración con Microsoft 365.

## Cómo verlo

- Abre `index.html` en el navegador: es la plataforma para People/RRHH (inicio, encuestas, soluciones, informes, personas, escucha activa y avanzado).
- Abre `escucha.html`: es la página pública para el equipo. Un cuadro de texto, sin registro y sin nombre.
- **Estela** es el asistente de la plataforma: responde dudas a RRHH dentro de `index.html`.

## Qué cubre del reto

El ciclo completo: necesidad, consulta adaptada con IA, validación humana, publicación (enlace, QR), participación sin saturar, análisis, visualización, acción y nueva consulta.

| Pieza | Dónde |
|---|---|
| Consulta adaptada con IA y preguntas neutras | Encuestas > Crear encuesta > Cuestionario |
| Validación humana: editar, reordenar, eliminar, aprobar y registro de quién aprobó | Cuestionario y Revisión |
| Publicación en Typeform y enlace / QR | Crear encuesta > Canales |
| Participación representativa, puntos ciegos y fiabilidad | Inicio, Personas, Avanzado |
| Selección rotativa para no saturar | Crear encuesta > Audiencia |
| Escucha activa anónima y recordatorios (SMS, WhatsApp, correo) | Escucha activa y `escucha.html` |
| Soluciones, plan de acción y nueva encuesta de seguimiento | Soluciones |
| Informes con lo que sienten las personas | Informes |

## Integración con Typeform

En este prototipo la conexión con Typeform es **visual**: aparece como canal conectado y como opción de publicación, pero no se hacen llamadas reales a su API.

La integración real (crear el formulario por API, obtener el enlace y leer las respuestas) ya se probó en otro proyecto del equipo y es el siguiente paso para conectarla a esta plataforma. Cuando se active:

- El token se guarda en una variable de entorno (`TYPEFORM_TOKEN`, ver `.env.example`) y nunca en el código ni en el repositorio.
- La IA no publica nada por su cuenta: el formulario solo se crea en Typeform después de la aprobación humana.
- Solo se leen respuestas agregadas y anónimas, y se aplica el mismo umbral mínimo de 5 respuestas.

## Privacidad y uso responsable

- **Solo datos sintéticos.** No hay datos reales de Damm ni de personas.
- **Siempre agregado.** Ningún segmento con menos de 5 respuestas se muestra, tampoco al combinar filtros.
- **Sin datos personales en comentarios.** Nombres, correos y teléfonos se ocultan automáticamente.
- **Formularios sospechosos.** Los enviados en menos de 4 segundos se descartan para no manchar los datos.
- **Control humano.** La IA propone, una persona aprueba antes de publicar y queda registrado.
- **Minimización y caducidad.** Se guarda solo lo necesario (sin identificadores personales) y durante el tiempo que dure la campaña y su seguimiento.
- **Sin secretos.** No hay claves ni tokens en el código. Ver `.env.example`.

## Datos sintéticos

Script: `datos-sinteticos/generar_datos.py` (solo librería estándar de Python).

```
cd datos-sinteticos
python generar_datos.py                 # 720 respuestas, semilla 2026
python generar_datos.py --n 1000 --seed 7
```

Crea `respuestas_sinteticas.csv`, `respuestas_sinteticas.json` y `resumen_sintetico.json`. Los nombres de campo siguen el esquema orientativo del reto, por eso mezclan catalán y castellano.

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
- La conexión con Typeform es visual: no se crea el formulario ni se leen respuestas por API (ver apartado anterior).
- Los números de las pantallas son de ejemplo y no salen todavía del conjunto de datos generado.
- Los envíos por SMS, WhatsApp y correo son simulaciones.
