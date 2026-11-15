# Informe de ejecución — candidato Entrega 4

**Corte:** 15 de noviembre de 2026.  
**Regla:** solo se marca PASS con evidencia observada; pendiente no significa aprobado.

## Resultados comprobados

- Back local sobre `1f2606e216ca6d9c59507b110a8f0647eee6e8a2`: 132 pruebas, 0 fallos, 0 errores y 2 omitidas porque Docker/WSL no está disponible en esta PC.
- JaCoCo Back: 90,56% de líneas y 72,24% de ramas; todos los umbrales del `pom.xml` aprobados.
- PIT: 53 mutaciones, mutation score 60% y test strength 82%.
- JAR de Back generado.
- Pruebas específicas: State, 409/412, idempotencia, Problem Details, 429, seguridad y fallback de IA aprobadas.
- M6–M3–Core: circuito funcional confirmado, colas sin pendientes y DLQ vacía al cierre observado.
- M1–M3–Core: escenario `approved` confirmado con correlación conservada y entrega en un intento.
- M1–M3–Core: escenario `rejected` confirmado, entregado a `q.obras` en un intento, sin DLQ y procesado por M3.
- M3–M7–Core: solicitud `streetClosureRequested` entregada y procesada por M7; respuesta y finalización pendientes por reconexión AMQPS de M7.
- CI Back: 117 pruebas, repetición anti-flakiness, Testcontainers PostgreSQL, PIT, SonarCloud, Gitleaks, Trivy y construcción de contenedor aprobados en los dos jobs del PR `#21`.
- Front local sobre `d472da55fa5dca8f6c351a01805d35495f611486`: 63 pruebas, 85,55% de líneas, 75,84% de ramas y build de producción aprobado. `npm audit` informa tres vulnerabilidades moderadas y ninguna crítica; deben quedar registradas como riesgo y no bloquean el umbral docente de CVE críticas.
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
| E4-05 | Bloqueante externo | Azure cambió la salida de `57.156.67.234` a `57.156.67.226`; AWS Core rechazaba AMQPS | resuelto al actualizar la allowlist; conexión `module_obras` observada en Azure |

## Pendientes de aceptación

1. Ejecutar en vivo los casos manuales BOLA/IDOR, BFLA, JWT inválido, mass assignment e inyecciones que el docente seleccione.
2. Incorporar al paquete la evidencia de Gemini activo y repetir los casos adversariales sobre la candidata final.
3. Completar E2E M2 y la respuesta/finalización de M7; obtener confirmación de los eventos secundarios de M6 y, si corresponde, `publicWorksProjectCompleted` de M1.
4. Verificar Jira y subir PDF/presentación a Teams.
5. Realizar la demo en vivo.
6. Evaluar salida estática de Azure para evitar depender de cambios de allowlist.

## Conclusión

Azure Test ejecuta Front `d472da55fa5dca8f6c351a01805d35495f611486` y Back `1f2606e216ca6d9c59507b110a8f0647eee6e8a2`. La auditoría del 15/11 detectó que el `compose.yaml` del tag remoto todavía fijaba revisiones anteriores; se prepara una candidata corregida y el gate debe repetirse antes de considerar congelada la entrega. La aceptación integral continúa condicionada por las actividades externas o presenciales listadas arriba.
