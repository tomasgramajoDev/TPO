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
- CI Back: 117 pruebas, repetición anti-flakiness, Testcontainers PostgreSQL, PIT, SonarCloud, Gitleaks, Trivy y construcción de contenedor aprobados en los dos jobs del PR `#21`.
- CI Front: 61 pruebas, 85,66% de cobertura de líneas, lint, build y contenedor aprobados en el PR `#19`.
- Release `v2.0-entrega4`: arranque limpio en 138 segundos, ZAP con 0 hallazgos High/Critical y Gitleaks sobre el historial completo.
- k6: 50 usuarios durante 5 minutos, 14.911 iteraciones, p95 de 6,35 ms, 0% de solicitudes fallidas y 100% de checks.
- Azure Test: Terraform aplicó 2 actualizaciones in-place y 0 destrucciones; health público correcto y seis logins aprobados.

## Defectos encontrados durante esta preparación

| ID | Severidad | Hallazgo | Resolución |
| --- | --- | --- | --- |
| E4-01 | Bloqueante CI | tests de migración esperaban Flyway V10 tras agregar V11/V12 | corregido; suite local verde |
| E4-02 | Mayor | cobertura de ramas cayó a 69% por rutas nuevas | se agregaron pruebas; quedó 71,10% |
| E4-03 | Bloqueante CI | test Testcontainers de PostgreSQL seguía esperando V10 | corregido; CI y Testcontainers aprobados |
| E4-04 | Bloqueante integración | Sonar detectó una ruta nula en `EventDispatcher` | precondición explícita y prueba agregadas; SonarCloud verde |
| E4-05 | Bloqueante externo | Azure cambió la salida de `57.156.67.234` a `57.156.67.226`; AWS Core rechaza AMQPS | pendiente de allowlist de Core o salida estática administrada por Terraform |

## Pendientes de aceptación

1. Core debe permitir temporalmente `57.156.67.226/32` en TCP 5671 y confirmar `module_obras`/`q.obras`; como solución permanente, acordar salida estática en Azure.
2. Ejecutar en vivo los casos manuales BOLA/IDOR, BFLA, JWT inválido, mass assignment e inyecciones que el docente seleccione.
3. Configurar gateway real de IA y probar caída/recuperación contra el proveedor elegido.
4. Completar E2E M2, M7 y M1 `rejected`.
5. Verificar Jira y subir PDF/presentación a Teams.
6. Realizar la demo en vivo.

## Conclusión

El candidato quedó etiquetado, validado y desplegado. Front, Back, PostgreSQL y los seis logins están operativos. La aceptación integral sigue condicionada por la conectividad AMQPS de Core y por las actividades externas o presenciales listadas arriba. No se ocultan áreas no ejecutadas.
