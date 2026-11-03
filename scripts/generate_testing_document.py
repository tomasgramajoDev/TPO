from pathlib import Path
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.shared import Cm, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "testing"
OUT.mkdir(parents=True, exist_ok=True)
DOCX = OUT / "Clase15_Grupo5_ObrasPublicas_Testing.docx"

NAVY = "16324F"
TEAL = "0E7C7B"
LIGHT = "EAF2F5"
RED = "A61B1B"
AMBER = "9A6700"
GREEN = "1B6E3B"
GREY = "5F6B73"


def shade(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def set_cell_text(cell, text, bold=False, color=None, size=8):
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(str(text))
    r.bold = bold
    r.font.name = "Aptos"
    r.font.size = Pt(size)
    if color:
        r.font.color.rgb = RGBColor.from_string(color)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER


def add_table(doc, headers, rows, widths=None, font_size=7.5):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"
    for i, h in enumerate(headers):
        set_cell_text(table.rows[0].cells[i], h, True, "FFFFFF", 8)
        shade(table.rows[0].cells[i], NAVY)
    for row in rows:
        cells = table.add_row().cells
        for i, value in enumerate(row):
            set_cell_text(cells[i], value, False, None, font_size)
            if len(table.rows) % 2 == 1:
                shade(cells[i], "F6F8FA")
    if widths:
        for row in table.rows:
            for i, width in enumerate(widths):
                row.cells[i].width = Cm(width)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return table


def heading(doc, text, level=1):
    p = doc.add_heading(text, level=level)
    p.paragraph_format.keep_with_next = True
    return p


def bullet(doc, text, level=0):
    p = doc.add_paragraph(style="List Bullet" if level == 0 else "List Bullet 2")
    p.add_run(text)
    return p


def status_box(doc, title, text, color):
    t = doc.add_table(rows=1, cols=1)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = t.cell(0, 0)
    shade(c, color)
    c.text = ""
    p = c.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(f"{title}: ")
    r.bold = True
    r.font.color.rgb = RGBColor(255, 255, 255)
    r2 = p.add_run(text)
    r2.font.color.rgb = RGBColor(255, 255, 255)
    return t


doc = Document()
sec = doc.sections[0]
sec.top_margin = Cm(1.6)
sec.bottom_margin = Cm(1.5)
sec.left_margin = Cm(1.6)
sec.right_margin = Cm(1.6)

styles = doc.styles
styles["Normal"].font.name = "Aptos"
styles["Normal"].font.size = Pt(9.5)
styles["Normal"].paragraph_format.space_after = Pt(5)
styles["Title"].font.name = "Aptos Display"
styles["Title"].font.size = Pt(28)
styles["Title"].font.bold = True
styles["Title"].font.color.rgb = RGBColor.from_string(NAVY)
for name, size, color in [("Heading 1", 17, NAVY), ("Heading 2", 13, TEAL), ("Heading 3", 10.5, NAVY)]:
    styles[name].font.name = "Aptos Display"
    styles[name].font.size = Pt(size)
    styles[name].font.bold = True
    styles[name].font.color.rgb = RGBColor.from_string(color)

header = sec.header.paragraphs[0]
header.text = "Municipalidad UADE · Grupo 5 · Obras Públicas · Clase 15"
header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
header.runs[0].font.size = Pt(8)
header.runs[0].font.color.rgb = RGBColor.from_string(GREY)
footer = sec.footer.paragraphs[0]
footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = footer.add_run("Documento de trabajo QA · Estado al 03/11/2026 · Evidencia requerida antes de entregar")
run.font.size = Pt(8)
run.font.color.rgb = RGBColor.from_string(GREY)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(34)
r = p.add_run("ASEGURAMIENTO DE CALIDAD")
r.bold = True
r.font.size = Pt(11)
r.font.color.rgb = RGBColor.from_string(TEAL)
title = doc.add_paragraph(style="Title")
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
title.add_run("Prueba del TP Obligatorio")
sub = doc.add_paragraph()
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
rr = sub.add_run("Plan, trazabilidad, ejecución, defectos, seguridad y uso de IA")
rr.font.size = Pt(14)
rr.font.color.rgb = RGBColor.from_string(GREY)
doc.add_paragraph()
add_table(doc, ["Dato", "Valor"], [
    ("Grupo / dominio", "Grupo 5 · Obras Públicas, Infraestructura y Mantenimiento Urbano"),
    ("Versión candidata", "v1.0-testing (tag pendiente de crear sobre main luego de cerrar todos los gates)"),
    ("Fecha límite documental", "10/11/2026, 13:30 — carga en Teams por QA"),
    ("Repositorios", "TPO / DesarrolloDeAplicacionesIIBack / DesarrolloAppsII_Front"),
    ("Ambientes", "Local reproducible; Azure Test para demo; Core compartido para integración bilateral"),
    ("Responsables", "QA: completar · DevOps: Tomás Gramajo · Front/Back: completar nombres"),
], widths=[4, 13], font_size=9)
doc.add_paragraph()
status_box(doc, "Estado global", "NO APTO TODAVÍA PARA ETIQUETAR. Hay evidencia local favorable, pero quedan condiciones eliminatorias que deben cerrarse y registrarse.", RED)
doc.add_paragraph()
note = doc.add_paragraph()
note.alignment = WD_ALIGN_PARAGRAPH.CENTER
note.add_run("Este informe no reemplaza Jira, Teams ni la demo en vivo. Los campos “pendiente” deben completarse con enlaces y capturas reales antes de la entrega.").italic = True
doc.add_page_break()

heading(doc, "1. Dictamen ejecutivo y condiciones eliminatorias", 1)
doc.add_paragraph("La regla operativa es binaria: si una condición G1–G9 no tiene evidencia válida, la instancia puede quedar desaprobada. La tabla distingue hechos verificados de tareas preparadas o pendientes.")
gates = [
    ("G1", "Clon limpio + un comando ≤15 min", "PREPARADO / NO EJECUTADO", "compose.yaml y .env.example creados; falta corrida cronometrada desde clon limpio con Docker Desktop."),
    ("G2", "Tag v1.0-testing en main antes de 13:30", "PENDIENTE", "Crear únicamente después de fusionar y comprobar CI; capturar URL, SHA y hora."),
    ("G3", "CI completo en verde sobre el tag", "PENDIENTE", "Gates locales aprobados; falta CI remoto del commit final, análisis estático y evidencia del tag."),
    ("G4", "Entregables QA en Teams", "PENDIENTE", "Este documento integra los mínimos; QA debe completar enlaces/evidencias y cargarlo antes del límite."),
    ("G5", "Jira actualizado", "PENDIENTE", "Crear/actualizar casos y defectos con HU, dueño, severidad, estado y evidencia."),
    ("G6", "Cero secretos en toda la historia", "PENDIENTE", "CI propuesto con Gitleaks; falta resultado remoto y escaneo histórico del tag."),
    ("G7", "Demo E2E en vivo", "PENDIENTE", "Existe recorrido histórico en Azure; debe repetirse en vivo sobre v1.0-testing."),
    ("G8", "Declaración de IA completa", "BORRADOR", "Sección 10 preparada; cada integrante debe validar, completar herramientas/prompts y firmar revisión."),
    ("G9", "Informe honesto", "CUMPLE EN BORRADOR", "Las brechas se mantienen visibles; no se declaran aprobadas pruebas sin evidencia."),
]
add_table(doc, ["Gate", "Criterio", "Estado", "Evidencia / acción"], gates, widths=[1.2, 4, 3.2, 9], font_size=7.5)
heading(doc, "Decisión de salida", 2)
bullet(doc, "No crear el tag mientras G1, G3 y G6 no hayan pasado sobre el commit candidato.")
bullet(doc, "No cargar el PDF en Teams sin enlaces de Jira, CI, Quality Gate, seguridad y evidencias de ejecución.")
bullet(doc, "No ocultar defectos: 0 Blocker, 0 Critical y máximo 3 Major con workaround es el umbral de aceptación.")

heading(doc, "2. Estrategia y plan de pruebas", 1)
heading(doc, "2.1 Alcance", 2)
bullet(doc, "Incluido: autenticación multirol; proyectos; órdenes de trabajo; recursos; cortes; persistencia PostgreSQL; API REST; proxy /api; seguridad por roles; eventos M2/M6/M7/M1; Outbox/Inbox y tolerancia de mensajería.")
bullet(doc, "Incluido: Front responsivo a 360, 768 y 1280 px; manejo de errores; accesibilidad; performance; análisis de dependencias y secretos.")
bullet(doc, "Fuera del resultado ejecutado actual: integración bilateral real con todos los módulos, pruebas k6, ZAP, mutación PIT, Sonar y Testcontainers, hasta producir evidencia.")
heading(doc, "2.2 Niveles, ambientes y datos", 2)
add_table(doc, ["Nivel", "Ambiente", "Objetivo", "Datos"], [
    ("Unitario", "CI / local", "Reglas, estados, validadores, componentes y clientes", "Factories y fixtures sin datos personales"),
    ("Integración", "Docker local", "PostgreSQL, API, proxy y broker disponible", "Seed reproducible y cuentas demo"),
    ("Contrato", "CI / Core", "Envelope y data contra JSON Schema/OpenAPI", "UUID v4 y payloads ficticios"),
    ("E2E", "Azure Test", "Cinco recorridos automatizados + demo manual", "Proyecto, OT y corte QA identificables"),
    ("Resiliencia", "Docker / Core coordinado", "Broker/externo caído, duplicados, DLQ y recuperación", "eventId/correlationId registrados"),
    ("Seguridad", "CI / Test", "OWASP API, authn/authz, ZAP, SCA y secretos", "Tokens efímeros; nunca se adjuntan"),
    ("Performance", "Test controlado", "50 usuarios, 5 min, 3 endpoints críticos", "Datos precreados; sin mutar producción"),
], widths=[2, 3, 6, 6], font_size=7.7)
heading(doc, "2.3 Entrada y salida", 2)
add_table(doc, ["Entrada", "Salida"], [
    ("Código fusionado en main; .env local válido; Docker/CI disponibles; schemas versionados; datos ficticios; defectos conocidos cargados.", "G1–G9 aprobados; 100% HU ejecutadas; ≥95% CA aprobados; 0 Blocker/Critical; ≤3 Major con workaround; CI verde; evidencias enlazadas; demo ensayada."),
], widths=[8.5, 8.5], font_size=8.5)
heading(doc, "2.4 Matriz de riesgos priorizada", 2)
risks = [
    ("R-01", "Arranque no reproducible", "Alta", "Alta", "Crítico", "Clon limpio cronometrado; fail-fast de .env"),
    ("R-02", "Autorización horizontal/vertical", "Alta", "Alta", "Crítico", "BOLA/BFLA multirol + 401/403"),
    ("R-03", "Pérdida/duplicado de eventos", "Alta", "Alta", "Crítico", "Inbox/Outbox, eventId, ACK/NACK, DLQ"),
    ("R-04", "Transición de estado inválida", "Media", "Alta", "Alto", "Tabla de estados y respuesta 409"),
    ("R-05", "Corte o módulo externo caído", "Media", "Alta", "Alto", "Timeout, circuit breaker/fallback, recuperación"),
    ("R-06", "Secreto en Git/log", "Media", "Alta", "Crítico", "Gitleaks histórico y revisión de logs"),
    ("R-07", "UI no usable/accesible", "Media", "Media", "Medio", "Viewport + axe/Lighthouse"),
    ("R-08", "Degradación de rendimiento", "Media", "Media", "Medio", "k6 y límites p95/error"),
]
add_table(doc, ["ID", "Riesgo", "Prob.", "Impacto", "Nivel", "Tratamiento"], risks, widths=[1.2, 4, 1.4, 1.5, 1.6, 7], font_size=7.5)

heading(doc, "3. Matriz de trazabilidad", 1)
trace = [
    ("HU-01 Login", "CA-01 happy / CA-02 inválido / CA-03 rol", "TC-001/002/003", "Front App.test + Back AuthController", "Local: PASS", "coverage + surefire", "—"),
    ("HU-02 Proyecto", "CA-04 crear / CA-05 aprobar / CA-06 rechazar", "TC-004/005/006", "ProjectController/Service tests", "Local: PASS parcial", "JaCoCo", "DEF-PEND"),
    ("HU-03 Orden", "CA-07 crear / CA-08 transición / CA-09 error", "TC-007..011", "WorkOrder tests", "Local: PASS", "JaCoCo", "—"),
    ("HU-04 Recursos", "CA-10 asignar / CA-11 stock / CA-12 conflicto", "TC-012/013/014", "Resource tests", "Local: PASS parcial", "Surefire", "DEF-PEND"),
    ("HU-05 Corte", "CA-13 solicitar / CA-14 aprobar / CA-15 vencer", "TC-015/016/017", "StreetClosure tests", "Local: PASS parcial", "JaCoCo", "INT-M7"),
    ("HU-06 M2", "CA-16 ROUTED / CA-17 RESOLVED / CA-18 inválido", "TC-018/019/020", "Message consumer tests", "Local: PASS parcial", "Surefire", "INT-M2"),
    ("HU-07 M6", "CA-19 request / CA-20 schedule / CA-21 complete", "TC-021/022", "Schema + handlers", "Pendiente E2E", "Core event log", "INT-M6"),
    ("HU-08 Resiliencia", "CA-22 broker down / CA-23 duplicate / CA-24 DLQ", "TC-023/024", "Inbox/Outbox tests", "Local: PASS parcial", "logs/DB", "INT-CORE"),
]
add_table(doc, ["HU", "Criterios", "Casos", "Automatización", "Resultado", "Evidencia", "Defecto"], trace, widths=[2, 4, 2, 4, 2.5, 2, 1.5], font_size=6.9)
doc.add_paragraph("Antes de entregar: reemplazar “parcial/pendiente” por el resultado real y una URL o ruta exacta. El profesor debe poder recorrer HU → CA → caso → automatización → resultado → evidencia → defecto.")

heading(doc, "4. Especificación de casos", 1)
cases = [
    ("TC-001", "Login válido por cada rol", "Usuarios seed", "Usuario + DEMO_PASSWORD", "Ingresar; verificar menú y permisos", "200, token y UI del rol", "P0", "F+S", "Sí"),
    ("TC-002", "Password incorrecta", "Usuario existente", "Password inválida", "Intentar login", "401 sin filtrar detalles", "P0", "N", "Sí"),
    ("TC-003", "JWT expirado/manipulado/alg none", "Token preparado", "3 tokens inválidos", "Invocar endpoint protegido", "401 en los tres", "P0", "N+S", "Pend."),
    ("TC-004", "Crear y presentar proyecto", "PERSONAL_OBRAS", "Proyecto QA", "Crear; editar; presentar", "Estado pendiente y datos persistidos", "P0", "F", "Sí"),
    ("TC-005", "Presupuesto negativo", "Sesión válida", "-1", "Crear proyecto", "400 Problem Details; sin alta", "P0", "N", "Sí"),
    ("TC-006", "Aprobar sin rol", "OPERARIO", "projectId válido", "Aprobar", "403; estado intacto", "P0", "N+S", "Sí"),
    ("TC-007", "Crear OT desde proyecto", "Proyecto aprobado", "UUID + número visible", "Crear OT", "OT vinculada una vez", "P0", "F", "Sí"),
    ("TC-008", "Proyecto inexistente", "Sesión válida", "UUID inexistente", "Crear OT", "404; sin alta", "P0", "N", "Sí"),
    ("TC-009", "Transición programar→iniciar→completar", "OT creada", "Fechas válidas", "Ejecutar flujo por roles", "Estados y auditoría correctos", "P0", "F", "Sí"),
    ("TC-010", "Transición inválida", "OT completada", "Acción start", "Intentar iniciar", "409 Problem Details", "P0", "N+B", "Pend."),
    ("TC-011", "Reabrir y validar", "OT completada", "Motivo + evidencia", "Inspector reabre; se completa; valida", "Historial íntegro", "P0", "F", "Sí"),
    ("TC-012", "Asignar recurso disponible", "OT programada", "Cuadrilla", "Asignar", "Carga y vínculo actualizados", "P1", "F", "Parcial"),
    ("TC-013", "Stock insuficiente", "Material bajo", "Cantidad > stock", "Asignar", "409; sin stock negativo", "P0", "N+B", "Pend."),
    ("TC-014", "Concurrencia/ETag obsoleto", "Dos clientes", "ETag viejo", "Actualizar desde ambos", "Segundo recibe 412", "P1", "N+R", "Pend."),
    ("TC-015", "Solicitar corte estructurado", "OT válida", "affectedSections", "Solicitar", "Evento v1.0 válido", "P0", "F+I", "Parcial"),
    ("TC-016", "Corte rechazado", "Solicitud emitida", "streetClosureRejected", "Consumir evento", "Estado rechazo y motivo", "P0", "A+I", "Parcial"),
    ("TC-017", "Corte vence", "ACTIVE/APROVED", "endDate vencido", "Avanzar reloj", "ACTIVE ended; APPROVED expired", "P1", "B+I", "Pend."),
    ("TC-018", "ticketUpdated no M3", "Consumidor activo", "responsibleAreaId M4", "Consumir", "ACK e ignorar sin mutación", "P0", "A+N", "Parcial"),
    ("TC-019", "STARTED antes de PROGRESS", "Ticket ROUTED", "Dos eventos", "Publicar en orden", "M2 acepta ambos", "P0", "A+I", "Pend."),
    ("TC-020", "PROGRESS fuera de orden", "Ticket ROUTED", "PROGRESS", "Publicar", "NACK/DLQ según Core; sin inconsistencia", "P0", "A+N", "Pend."),
    ("TC-021", "requestId→sourceRequestId", "M6/Core activos", "UUID", "Consumir request; emitir schedule/complete", "Correlación preservada", "P0", "A+I", "Pend."),
    ("TC-022", "data omitido", "Core disponible", "Envelope sin data", "POST /events", "422 y no ingresa al hub", "P0", "N+C", "Sí código"),
    ("TC-023", "Duplicado exacto", "Inbox activa", "Mismo eventId dos veces", "Entregar dos veces", "Una sola mutación; ACK seguro", "P0", "N+R", "Parcial"),
    ("TC-024", "Broker caído y recuperación", "Stack activo", "Corte de broker", "Detener; operar; reiniciar", "Sin pérdida; Outbox reintenta", "P0", "N+R", "Pend."),
]
add_table(doc, ["ID", "Caso", "Precond.", "Datos", "Pasos", "Esperado", "Prio", "Tipo", "Auto"], cases, widths=[1.2, 3.2, 2.3, 2.3, 3, 3.4, 1, 1.1, 1.1], font_size=6.1)
doc.add_paragraph("Cobertura negativa/borde: 11 de 24 casos (45,8%), superior al mínimo de 40%. Leyenda: F funcional, N negativo, B borde, S seguridad, I integración, A asíncrono, R resiliencia, C contrato.")

heading(doc, "5. Informe de ejecución", 1)
status_box(doc, "Corte de evidencia", "Resultados locales del 03/11/2026. No equivalen a CI remoto, Test, Core bilateral ni demo en vivo.", AMBER)
heading(doc, "5.1 Resultados verificados", 2)
add_table(doc, ["Componente", "Comando", "Resultado", "Cobertura / observación"], [
    ("Back", "mvnw clean verify", "105 tests PASS; JAR generado", "Líneas 90,83%; ramas 70,67%; gate 80/70"),
    ("Front", "npm run test:coverage", "58 tests PASS", "Sent. 86,05%; ramas 77,81%; func. 84,09%; líneas 85,84%"),
    ("Front", "npm run lint / build", "PASS", "TypeScript/Vite y contenedor pendientes de CI final"),
    ("Front SCA", "npm audit --audit-level=high", "Sin High/Critical", "3 Moderate del tooling de desarrollo"),
    ("Compose", "docker compose config/up", "NO EJECUTADO", "Docker CLI no disponible en la estación de esta auditoría"),
], widths=[2.5, 4, 3.5, 7], font_size=8)
heading(doc, "5.2 Métricas obligatorias aún pendientes", 2)
add_table(doc, ["Métrica", "Umbral", "Resultado", "Evidencia requerida"], [
    ("Mutación dominio", "≥60%", "Pendiente", "Reporte PIT/Stryker del commit etiquetado"),
    ("Sonar Quality Gate", "Approved", "Pendiente", "URL/captura; 0 blocker/critical; A; dup ≤3%; hotspots 100%"),
    ("E2E pipeline", "≥5", "Pendiente", "Job CI y artefactos Playwright/Cypress"),
    ("Accesibilidad", "≥90; 0 críticos", "Pendiente", "Lighthouse + axe 360/768/1280"),
    ("Performance", "p95 <500 ms; error <1%", "Pendiente", "k6 50 VU, 5 min, 3 endpoints"),
    ("Flakiness", "3 corridas idénticas", "Preparado", "CI modificado; falta enlace verde final"),
    ("Testcontainers", "DB y broker reales", "Pendiente", "Pruebas CI con PostgreSQL/RabbitMQ containers"),
], widths=[4, 4, 3, 6], font_size=8)

heading(doc, "6. Registro de defectos", 1)
defects = [
    ("DEF-001", "G1 no ejecutado desde clon limpio", "Major", "Preparado", "QA/DevOps", "Ejecutar y cronometrar; adjuntar log y captura", "Pendiente Jira"),
    ("DEF-002", "Sin E2E automatizado en pipeline", "Major", "Abierto", "Front/QA", "Implementar ≥5 recorridos Playwright", "Pendiente Jira"),
    ("DEF-003", "Sin mutación ni Sonar final", "Major", "Abierto", "Back/DevOps", "Configurar y conservar reportes", "Pendiente Jira"),
    ("DEF-004", "Sin evidencia k6/ZAP/axe", "Major", "Abierto", "QA", "Ejecutar contra Test controlado", "Pendiente Jira"),
    ("DEF-005", "Integración Core bilateral no acreditada", "Major", "Abierto", "Back/DevOps", "Coordinar eventId y registro de punta a punta", "Pendiente Jira"),
]
add_table(doc, ["ID", "Descripción", "Sev.", "Estado", "Dueño", "Reproducción / corrección", "Jira"], defects, widths=[1.4, 4.4, 1.5, 2, 2, 5, 2], font_size=7.4)
doc.add_paragraph("El número de defectos Major abiertos excede el umbral de salida. Deben corregirse o reclasificarse únicamente con evidencia; no se deben ocultar para cumplir el máximo.")

heading(doc, "7. Seguridad", 1)
sec_rows = [
    ("SEC-01", "BOLA", "Cambiar UUID de proyecto/OT entre usuarios", "403/404 sin filtración", "Pendiente"),
    ("SEC-02", "BFLA", "Operario intenta aprobar/rechazar", "403 y sin mutación", "Parcial"),
    ("SEC-03", "JWT", "Expirado, firma alterada, alg none, issuer incorrecto", "401 uniforme", "Pendiente"),
    ("SEC-04", "Mass assignment", "Campos role/status/owner adicionales", "Ignorados o 400", "Pendiente"),
    ("SEC-05", "Injection/XSS", "SQL/meta/caracteres y scripts", "Sin ejecución/reflejo", "Pendiente"),
    ("SEC-06", "XXE", "XML con entidad externa si aplica", "Rechazo seguro/no aplicable justificado", "Pendiente"),
    ("SEC-07", "Brute force", "Intentos repetidos de login", "429 y política documentada", "Pendiente"),
    ("SEC-08", "Headers/CORS", "Origins y headers", "CSP/HSTS/XCTO; CORS restrictivo", "Pendiente"),
    ("SEC-09", "Secrets/logs", "Gitleaks + inspección logs", "0 secretos; 0 token/PII/stack trace", "Pendiente CI"),
    ("SEC-10", "SCA/ZAP", "Escaneo dependencia y DAST", "0 High; Medium justificado", "Pendiente"),
]
add_table(doc, ["ID", "Control", "Prueba", "Esperado", "Estado"], sec_rows, widths=[1.4, 2.5, 5.5, 5.5, 2.2], font_size=7.4)
heading(doc, "Tratamiento de credenciales", 2)
bullet(doc, ".env está ignorado; .env.example enumera variables sin valores reales.")
bullet(doc, "Compose corta con mensaje explícito si faltan DB_PASSWORD, JWT_SECRET, DEMO_PASSWORD o RABBITMQ_PASSWORD.")
bullet(doc, "Contraseñas/tokens no se imprimen, no se incluyen en capturas y no se adjuntan como evidencia.")
bullet(doc, "La prueba G6 debe escanear toda la historia, no solo el árbol actual.")

heading(doc, "8. Resiliencia e integración", 1)
add_table(doc, ["Escenario", "Procedimiento", "Criterio de aprobación", "Evidencia"], [
    ("Broker caído", "Detener broker; ejecutar operación; restaurar", "Operación consistente; Outbox conserva y reintenta; sin pérdida", "DB outbox + logs sin secretos"),
    ("Servicio externo caído", "Simular timeout >5 s", "Timeout 5 s, retry acotado/circuit breaker/fallback", "Métricas + respuesta"),
    ("Duplicado", "Entregar mismo eventId dos veces", "Una mutación; Inbox deduplica", "Inbox + entidad"),
    ("Mensaje inválido", "data fuera de schema", "NACK requeue=false; reintentos Core; DLQ", "eventId + panel"),
    ("Transacción fallida", "Fallar persistencia después del cambio", "Rollback total o compensación; Outbox coherente", "DB antes/después"),
    ("Idempotency-Key", "Repetir POST con misma clave", "Un recurso y misma respuesta", "HTTP + DB"),
    ("ETag", "Actualizar con versión obsoleta", "412 Precondition Failed", "HTTP"),
], widths=[3, 5, 6, 3], font_size=7.5)
doc.add_paragraph("Core informado: maxAttempts=4 cuenta entregas; con el default hay entrega original + 3 reintentos, esperas 5 s, 30 s y 2 min (ventana 2 min 35 s). Verificar siempre la topología real antes de la prueba.")

heading(doc, "9. Guion de prueba en vivo", 1)
steps = [
    ("00:00–02:00", "Mostrar tag/CI/secret scan y arrancar desde clon limpio con un comando."),
    ("02:00–04:00", "Login por rol; crear/presentar/aprobar proyecto."),
    ("04:00–07:00", "Crear OT; programar; iniciar; completar; reabrir; completar; validar."),
    ("07:00–09:00", "Caso negativo aleatorio: 401/403/400/404/409; demostrar ausencia de mutación."),
    ("09:00–12:00", "Detener broker/externo; ejecutar escenario; restaurar; mostrar Outbox/Inbox y recuperación."),
    ("12:00–14:00", "Duplicado y mensaje inválido → DLQ/reproceso; registrar eventId."),
    ("14:00–16:00", "Mostrar Sonar, JaCoCo, mutación, E2E, k6, ZAP, SCA, axe/Lighthouse."),
    ("16:00–18:00", "Caso al azar del profesor y defensa individual de decisiones."),
]
add_table(doc, ["Tiempo", "Acción"], steps, widths=[3, 14], font_size=8.3)
heading(doc, "Plan B permitido", 2)
doc.add_paragraph("El plan B solo conserva evidencia para diagnosticar; no reemplaza la demo en vivo. Si falla un servicio, se muestra el fallo, el comportamiento resiliente y la recuperación. Nunca se cambia de versión ni se oculta el incidente durante la defensa.")

heading(doc, "10. Declaración de uso de IA", 1)
add_table(doc, ["Herramienta/versión", "Uso", "Prompt o referencia", "Aceptado/corregido", "Verificación humana"], [
    ("Codex (modelo de la sesión)", "Auditoría, propuesta de CI, casos y documento", "Historial de trabajo del 03/11/2026", "Se aceptaron estructuras; resultados se verificaron por comandos", "QA/DevOps revisa líneas, métricas y enlaces"),
    ("Completar por integrante", "Código/tests/documentación", "URL o extracto", "Detallar cambios", "Firma/revisor"),
], widths=[3.5, 4, 4, 3.5, 3], font_size=7.8)
heading(doc, "Ejemplo de sugerencia incorrecta de IA", 2)
doc.add_paragraph("La IA podría afirmar que “tener 105 pruebas implica cumplir Testing”. Se rechazó: el criterio exige además cobertura, mutación, integración real, E2E, seguridad, resiliencia, performance, trazabilidad y evidencia. La corrección fue separar resultados locales de pendientes eliminatorios.")
heading(doc, "Reglas de revisión", 2)
bullet(doc, "Todo test o código generado por IA tiene autor/revisor humano y resultado reproducible.")
bullet(doc, "No se aceptan resultados narrados sin reporte o comando verificable.")
bullet(doc, "No se suministran secretos, tokens ni datos personales a herramientas de IA.")

heading(doc, "11. Lecciones aprendidas", 1)
add_table(doc, ["Defecto tardío", "Por qué no se detectó antes", "Prueba preventiva"], [
    ("CORS bloqueó login desde el Front aunque API directa daba 200", "Smoke API sin header Origin", "E2E por proxy con Origin real en CI/Test"),
    ("Flujo de OT dependía de window.prompt y no era automatizable/usable", "Pruebas centradas en endpoints y navegador parcial", "E2E completo por rol + accesibilidad"),
    ("Contratos de eventos divergieron en nombres/UUID/schema", "No había validación cruzada ni Core bilateral", "Contract tests + registro schema + prueba eventId E2E"),
], widths=[5.5, 6, 5.5], font_size=8)

heading(doc, "12. Checklist final del QA", 1)
for item in [
    "Ejecutar clon limpio cronometrado y guardar salida completa.",
    "Fusionar PR finales; confirmar CI verde; escanear historia; crear tag v1.0-testing sobre main.",
    "Completar Jira: casos, defectos, HU, responsables, severidad, estado y evidencia.",
    "Ejecutar/adjuntar Sonar, mutación, Testcontainers, E2E, k6, ZAP, SCA, Gitleaks, axe y Lighthouse.",
    "Actualizar resultados de este PDF sin ocultar fallos; verificar 0 Blocker/Critical y ≤3 Major con workaround.",
    "Completar y firmar declaración de IA por integrante.",
    "Cargar un solo PDF Clase15_Grupo5_ObrasPublicas_Testing.pdf y sus links en Teams antes de 13:30.",
    "Ensayar defensa individual y demo en vivo; preparar caso al azar y recuperación de fallos.",
]:
    bullet(doc, "☐ " + item)

heading(doc, "13. Índice de evidencias a completar", 1)
add_table(doc, ["Evidencia", "Enlace / ruta", "Responsable", "Estado"], [
    ("Tag y commit", "COMPLETAR", "DevOps", "Pendiente"),
    ("CI Front/Back/TPO", "COMPLETAR", "DevOps", "Pendiente"),
    ("Jira", "COMPLETAR", "QA/PM", "Pendiente"),
    ("Sonar/JaCoCo/Mutación", "COMPLETAR", "Back", "Pendiente parcial"),
    ("E2E/axe/Lighthouse", "COMPLETAR", "Front/QA", "Pendiente"),
    ("k6/ZAP/SCA/Gitleaks", "COMPLETAR", "QA/DevOps", "Pendiente"),
    ("Core/RabbitMQ bilateral", "COMPLETAR eventId/correlationId", "Back/DevOps", "Pendiente"),
    ("Video/capturas/logs", "COMPLETAR", "QA", "Pendiente"),
], widths=[4, 7, 3, 3], font_size=8)

doc.add_paragraph()
status_box(doc, "Conclusión", "El equipo tiene una base verificable de tests y cobertura, pero aún no satisface todos los criterios eliminatorios. La entrega se considera lista únicamente cuando este checklist quede respaldado por evidencias del commit etiquetado.", NAVY)

doc.save(DOCX)
print(DOCX)
