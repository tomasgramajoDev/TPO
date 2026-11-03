# Bitácora QA — M3 Obras Públicas

## Estado resumido

- Frontend: 58 pruebas unitarias, cobertura de 86,05% en sentencias y 85,84% en líneas, 6 recorridos E2E en Chromium y control axe sin hallazgos serios o críticos.
- Backend: 108 pruebas aprobadas, 0 fallos, cobertura JaCoCo dentro de los umbrales definidos; la suite se repitió dos veces sin fallas.
- Mutación: 53 mutaciones generadas, 32 detectadas, score 60% y fuerza de tests 82%.
- PostgreSQL real: Testcontainers ejecutado en CI con PostgreSQL 17; Flyway aplicó V1–V10 y las dos pruebas aprobaron.
- Secretos: Gitleaks 8.30.1 ejecutado sobre la historia completa de Front, Back y TPO, con 0 hallazgos.
- Performance, ZAP y arranque limpio: pipeline preparado. Resultado pendiente de la corrida remota del PR/tag.

## Registro de trabajo

| Fecha | Actividad | Resultado | Evidencia |
|---|---|---|---|
| 03/11 08:00 | Auditoría de criterios eliminatorios G1–G9 | Se separaron cumplidos, preparados y pendientes | Documento QA Clase 15 |
| 03/11 08:30 | Escaneo completo de secretos | 0 hallazgos en los tres repositorios | Gitleaks 8.30.1 |
| 03/11 09:00 | Automatización Front | 58 unitarias y 6 E2E aprobadas | PR Front #15 y CI |
| 03/11 09:20 | Accesibilidad | 0 violaciones axe serias/críticas | E2E-06 |
| 03/11 09:30 | Integración PostgreSQL | 2 pruebas Testcontainers aprobadas con PostgreSQL 17 y Flyway V10 | PR Back #16 / CI |
| 03/11 09:53 | Cierre Back QA | 108 pruebas, repetición x2, PIT, Gitleaks, Trivy y Docker aprobados; PR fusionado | PR Back #16 |
| 03/11 09:37 | Mutation testing | 60% mutation score, 82% test strength | Reporte PIT |
| 03/11 09:40 | Release gates | Compose limpio, k6 y ZAP definidos | Workflow testing-release |
| 03/11 09:50 | Actividad IA Clase 14 | Feature, contrato, 20 evals y gobernanza preparados | Clase14_Grupo5_ObrasPublicas_IA.pdf |

## Hallazgos y correcciones

- El navegador encontró semántica incompleta en la barra de progreso. Se agregó `role=progressbar` y sus valores ARIA.
- Axe encontró contraste insuficiente en el estado de carga. Se corrigió el color y se repitió la prueba.
- El smoke PostgreSQL usaba una clase movida en Spring Boot 4. Se sustituyó por una verificación directa del controlador y la suite volvió a verde.
- PIT obtuvo inicialmente 57%. Se agregó una prueba que impide sobrescribir presupuesto y plazo aprobados; el resultado final llegó al umbral de 60%.

## Pendientes que no se deben ocultar

- Corrida remota final de Compose, k6 y ZAP.
- Sonar Quality Gate, que requiere proyecto y token de SonarCloud.
- Prueba bilateral real con Core/RabbitMQ y módulos externos.
- Carga final en Teams, Jira y la demo en vivo.
