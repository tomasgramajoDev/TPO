# Trazabilidad QA - Entrega 4

**Fecha de corte:** 2026-11-13

La matriz Excel del paquete es la fuente operativa para recorrer requisito -> criterio -> prueba -> resultado -> evidencia -> defecto. Este documento resume el estado y evita convertir pendientes externos en resultados aprobados.

## Estado consolidado

- Funciones internas principales: cubiertas por pruebas automatizadas y evidencia manual.
- M6-M3-Core: E2E confirmado.
- M1 approved: E2E confirmado.
- M1 rejected: pendiente de ejecucion externa.
- M2: pendiente prueba bilateral real.
- M7: pendiente prueba bilateral real.
- Resiliencia con caida real del broker compartido: pendiente de coordinacion con Core.
- Core sin clave data: pendiente de confirmacion HTTP 422 y ausencia de ingreso al hub/DLQ.
- IA: implementacion supervisada; falta consolidar evidencia final y firmas nominales de la declaracion.

## Regla de evidencia

Un test automatizado prueba el comportamiento del modulo, pero no acredita por si solo un circuito entre modulos. Para E2E se exigen eventId, correlationId, estado de enrutamiento, cola/DLQ y confirmacion funcional del receptor.

## Jira y Trello

Trello puede usarse como tablero diario. Jira no se descarta mientras el criterio G5 de la catedra lo exija. La forma minima de cumplir es mantener en Jira las historias, casos, defectos, responsables, estado y enlaces a evidencia; Trello puede referenciar los mismos IDs sin duplicar descripciones extensas.
