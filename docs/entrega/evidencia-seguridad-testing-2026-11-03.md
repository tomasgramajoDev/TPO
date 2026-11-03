# Evidencia de seguridad para Testing — 2026-11-03

Estado: `CONFIRMED` para los escaneos indicados.

Se ejecutó Gitleaks 8.30.1 con historial Git completo y salida redactada sobre los tres repositorios del Módulo 3:

| Repositorio | Commits escaneados | Resultado |
| --- | ---: | --- |
| Backend | 31 | 0 filtraciones |
| Frontend | 21 | 0 filtraciones |
| TPO / DevOps | 56 | 0 filtraciones |

El pipeline `Testing release gates` repite el escaneo completo sobre cada candidato y sobre el tag `v1.0-testing`. Ningún reporte debe contener valores de secretos. Las credenciales efímeras del entorno se generan en tiempo de ejecución, se enmascaran y no se versionan.

Esta evidencia cubre el control de secretos del historial. No sustituye las pruebas OWASP, de autorización ni el DAST sobre el ambiente controlado.
