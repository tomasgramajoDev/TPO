# Importación de seguimiento QA

Este paquete contiene 34 casos de prueba preparados a partir de los criterios de la Clase 15.

## Jira

Importar `Jira_Import_Casos_QA.csv` con el importador CSV de Jira. La columna `Issue Type` usa `Task`; si el proyecto emplea un tipo llamado `Test`, reemplazar ese valor durante el mapeo.

## Trello

Importar `Trello_Import_Casos_QA.csv` con un importador CSV o crear las tarjetas usando `Name`, `Description`, `List`, `Labels` y `Due Date`.

## Fuente de verdad

`Matriz_Ejecucion_QA.csv` conserva identificador, criterio, resultado esperado, estado y evidencia. Los estados significan:

- `PASS`: existe evidencia ejecutada.
- `PREPARADO`: caso definido y listo, todavía requiere ejecución en el ambiente indicado.
- `NO_APLICA`: el caso no corresponde al alcance actual y tiene justificación.

No cambiar un caso a `PASS` sin adjuntar evidencia verificable.
