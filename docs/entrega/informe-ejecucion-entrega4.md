# Informe de ejecución — candidato Entrega 4

**Corte:** 10 de noviembre de 2026.  
**Regla:** solo se marca PASS con evidencia observada; pendiente no significa aprobado.

## Resultados comprobados

- Back local: 117 pruebas, 0 fallos, 0 errores y 2 omitidas porque Docker local no estaba disponible.
- JaCoCo Back: 90,43% de líneas y 71,10% de ramas.
- PIT: 53 mutaciones, mutation score 60% y test strength 82%.
- JAR de Back generado.
- Pruebas específicas: State, 409/412, idempotencia, Problem Details, 429, seguridad y fallback de IA aprobadas.
- M6–M3–Core: circuito funcional confirmado, colas sin pendientes y DLQ vacía al cierre observado.
- M1–M3–Core: escenario `approved` confirmado con correlación conservada y entrega en un intento.

## Defectos encontrados durante esta preparación

| ID | Severidad | Hallazgo | Resolución |
| --- | --- | --- | --- |
| E4-01 | Bloqueante CI | tests de migración esperaban Flyway V10 tras agregar V11/V12 | corregido; suite local verde |
| E4-02 | Mayor | cobertura de ramas cayó a 69% por rutas nuevas | se agregaron pruebas; quedó 71,10% |
| E4-03 | Bloqueante CI | test Testcontainers de PostgreSQL seguía esperando V10 | corregido en PR Back; revalidación CI pendiente |

## Pendientes de aceptación

1. CI verde y merge de los PR de Back, Front e infraestructura.
2. Crear `v2.0-entrega4` en `main` y comprobar el pipeline del tag.
3. Ejecutar k6 50 usuarios/5 minutos y guardar p95.
4. Ejecutar ZAP y pruebas manuales BOLA/IDOR, BFLA, JWT inválido, mass assignment e inyecciones.
5. Configurar gateway real de IA y probar caída/recuperación contra el proveedor elegido.
6. Completar E2E M2, M7 y M1 `rejected`.
7. Verificar Jira y subir PDF/presentación a Teams.
8. Realizar la demo en vivo.

## Conclusión

El candidato avanzó en código, pruebas y documentación, pero todavía no debe declararse listo ni etiquetarse mientras los pendientes anteriores no tengan evidencia. No se conoce un defecto crítico oculto; las áreas todavía no ejecutadas se informan explícitamente como riesgo.
