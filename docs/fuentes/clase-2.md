# Fuente — Clase 2

- Archivo recibido: `Clase 2 (1).pdf`.
- Fecha del material: 2026-08-11 según los metadatos del PDF.
- Tipo: material docente.
- Estado: `RECEIVED` como contexto académico; no constituye por sí solo una decisión del proyecto.

## Sistemas orientados a eventos

La clase compara sistemas distribuidos con comportamientos naturales descentralizados: cada servicio es independiente, publica eventos y reacciona de forma asíncrona a lo que recibe. El flujo emerge de productores y suscriptores sin requerir un orquestador central.

Este contenido refuerza la integración asíncrona exigida por la consigna, pero no define tecnología de mensajería, contratos ni topología para M3.

## Roles ágiles

Se describen Scrum Master, Product Owner, backend developer, tester, analista funcional y frontend developer. La lista no incluye DevOps en esas diapositivas, pero no contradice la asignación del usuario: la Clase 1 y la decisión explícita del equipo ya establecen el rol DevOps.

## Metodologías y seguimiento

La clase presenta:

- Kanban, visualización del trabajo y límites de WIP;
- Scrum, backlog, sprint y métricas;
- Trello como ejemplo de tablero;
- velocidad, burndown, cambios de alcance, defectos y satisfacción como métricas posibles.

No se indica que el proyecto deba adoptar una metodología o herramienta específica.

## Definition of Done

La Definition of Done general incluye:

- pruebas unitarias y funcionales aprobadas;
- código revisado;
- criterios de aceptación cumplidos;
- requisitos no funcionales cumplidos;
- aceptación de la historia por el Product Owner.

La variante estricta agrega:

- despliegue en producción con la funcionalidad desactivada mediante feature toggle;
- al menos un caso de prueba por criterio de aceptación;
- documentación técnica y de usuario;
- revisión por pares;
- pruebas de integración;
- registro de configuraciones manuales posteriores al despliegue;
- release notes;
- correspondencia de la UI con el diseño y comunicación de cambios.

Se adoptan como insumos para definir la DoD del equipo, no como requisitos confirmados. Producción y feature flags siguen pendientes.

## Historias de usuario

Se presenta el formato:

> Como tipo de usuario, quiero realizar una tarea, para lograr un objetivo.

Los criterios de aceptación siguen la estructura Dado/Cuando/Entonces. El material también solicita título, prioridad y estimación.

## Git

Git se presenta como control de versiones distribuido para conservar historial y permitir trabajo simultáneo. La diapositiva utiliza la expresión “GitHub merge request”; para este repositorio se mantiene la terminología oficial de GitHub: **pull request**.

## Escalado ágil

Se explican tres familias de organización:

- Nexus: backlog único, varios Scrum Teams, Nexus Integration Team e incremento integrado.
- SAFe: niveles Portfolio, Program/ART y Team, con variantes Essential y Large Solution.
- Modelo Spotify: squads, tribes, chapters y guilds; se menciona expresamente una guild de DevOps o seguridad.

El contexto de nueve módulos vuelve relevante la coordinación de dependencias y entregas integradas, pero el material no selecciona un framework para el TPO.

## Impacto en DevOps

- Mantener pipelines compatibles con revisión por pares y pruebas bloqueantes.
- Conservar documentación y release notes junto con cada promoción.
- Coordinar dependencias de integración entre módulos antes de un incremento integrado.
- Evitar asumir que una historia desplegada equivale automáticamente a una historia terminada: debe satisfacer la DoD acordada.
