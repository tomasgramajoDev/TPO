from __future__ import annotations

import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "docs/ia/evals/incident-triage-v1.json"
OUTPUT = ROOT / "output/pdf/Clase14_Grupo5_ObrasPublicas_IA.pdf"

NAVY = colors.HexColor("#123142")
TEAL = colors.HexColor("#138A86")
MINT = colors.HexColor("#D9F4EF")
BLUE = colors.HexColor("#2563EB")
PALE = colors.HexColor("#F4F7FA")
INK = colors.HexColor("#17202A")
MUTED = colors.HexColor("#5B6770")
AMBER = colors.HexColor("#F3B61F")
RED = colors.HexColor("#C2413B")


def register_fonts() -> tuple[str, str]:
    regular = Path(r"C:\Windows\Fonts\arial.ttf")
    bold = Path(r"C:\Windows\Fonts\arialbd.ttf")
    if regular.exists() and bold.exists():
        pdfmetrics.registerFont(TTFont("ActivitySans", str(regular)))
        pdfmetrics.registerFont(TTFont("ActivitySans-Bold", str(bold)))
        return "ActivitySans", "ActivitySans-Bold"
    return "Helvetica", "Helvetica-Bold"


FONT, FONT_BOLD = register_fonts()


def p(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(text, style)


def build_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="CoverKicker", fontName=FONT_BOLD, fontSize=10, leading=13, textColor=TEAL, spaceAfter=8))
    styles.add(ParagraphStyle(name="CoverTitle", fontName=FONT_BOLD, fontSize=28, leading=31, textColor=NAVY, spaceAfter=12))
    styles.add(ParagraphStyle(name="CoverSub", fontName=FONT, fontSize=12, leading=17, textColor=MUTED, spaceAfter=14))
    styles.add(ParagraphStyle(name="H1x", fontName=FONT_BOLD, fontSize=18, leading=22, textColor=NAVY, spaceBefore=3, spaceAfter=9))
    styles.add(ParagraphStyle(name="H2x", fontName=FONT_BOLD, fontSize=12, leading=15, textColor=TEAL, spaceBefore=6, spaceAfter=5))
    styles.add(ParagraphStyle(name="Bodyx", fontName=FONT, fontSize=9.2, leading=13.4, textColor=INK, spaceAfter=6))
    styles.add(ParagraphStyle(name="Smallx", fontName=FONT, fontSize=7.7, leading=10.3, textColor=INK))
    styles.add(ParagraphStyle(name="Tinyx", fontName=FONT, fontSize=6.9, leading=8.6, textColor=INK))
    styles.add(ParagraphStyle(name="TableHeader", fontName=FONT_BOLD, fontSize=7.5, leading=9.5, textColor=colors.white))
    styles.add(ParagraphStyle(name="BoxTitle", fontName=FONT_BOLD, fontSize=10, leading=12, textColor=NAVY, spaceAfter=3))
    styles.add(ParagraphStyle(name="BoxBody", fontName=FONT, fontSize=8.3, leading=11.5, textColor=INK))
    styles.add(ParagraphStyle(name="Metric", fontName=FONT_BOLD, fontSize=15, leading=18, textColor=BLUE, alignment=TA_CENTER))
    styles.add(ParagraphStyle(name="MetricLabel", fontName=FONT, fontSize=7.5, leading=9.5, textColor=MUTED, alignment=TA_CENTER))
    return styles


ST = build_styles()


def page_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#D7E0E5"))
    canvas.line(18 * mm, 14 * mm, 192 * mm, 14 * mm)
    canvas.setFont(FONT, 7)
    canvas.setFillColor(MUTED)
    canvas.drawString(18 * mm, 9 * mm, "Grupo 5 · M3 Obras Públicas · Actividad IA Clase 14")
    canvas.drawRightString(192 * mm, 9 * mm, f"Página {doc.page}")
    canvas.restoreState()


def box(title: str, body: str, width: float, accent=TEAL):
    content = [p(title, ST["BoxTitle"]), p(body, ST["BoxBody"])]
    table = Table([[content]], colWidths=[width], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALE),
        ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#C8D6DC")),
        ("LINEBEFORE", (0, 0), (0, -1), 4, accent),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return table


def section(title: str, subtitle: str | None = None):
    items = [p(title, ST["H1x"])]
    if subtitle:
        items.append(p(subtitle, ST["Bodyx"]))
    return items


def bullet(text: str):
    return p(f"• {text}", ST["Bodyx"])


def architecture_table():
    labels = [
        ("Frontend", "Operador revisa"),
        ("SuggestionService", "Orquesta"),
        ("AIGateway", "Facade + contrato"),
        ("OpenAIAdapter", "Proveedor aislado"),
        ("Responses API", "gpt-6-luna"),
    ]
    row = []
    for idx, (title, sub) in enumerate(labels):
        row.append([p(title, ST["BoxTitle"]), p(sub, ST["Tinyx"])])
        if idx < len(labels) - 1:
            row.append(p("→", ParagraphStyle(name=f"arrow{idx}", parent=ST["BoxTitle"], alignment=TA_CENTER, textColor=TEAL)))
    widths = [31 * mm, 7 * mm, 33 * mm, 7 * mm, 31 * mm, 7 * mm, 31 * mm, 7 * mm, 31 * mm]
    table = Table([row], colWidths=widths, hAlign="LEFT")
    style = [("VALIGN", (0, 0), (-1, -1), "MIDDLE")]
    for col in range(0, len(row), 2):
        style += [
            ("BACKGROUND", (col, 0), (col, 0), MINT),
            ("BOX", (col, 0), (col, 0), 0.7, TEAL),
            ("LEFTPADDING", (col, 0), (col, 0), 6),
            ("RIGHTPADDING", (col, 0), (col, 0), 6),
            ("TOPPADDING", (col, 0), (col, 0), 8),
            ("BOTTOMPADDING", (col, 0), (col, 0), 8),
        ]
    table.setStyle(TableStyle(style))
    return table


def metrics_table():
    metrics = [
        ("100%", "schema válido"),
        ("≥90%", "categoría"),
        ("≥85%", "prioridad"),
        ("0", "fugas de PII"),
        ("100%", "adversariales"),
        ("≤5 s", "latencia p95"),
    ]
    cells = [[p(value, ST["Metric"]), p(label, ST["MetricLabel"])] for value, label in metrics]
    table = Table([cells], colWidths=[29 * mm] * 6)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALE),
        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#CFD9DF")),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#DDE5E9")),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return table


def eval_table(cases):
    header = [p("ID", ST["TableHeader"]), p("Tipo", ST["TableHeader"]), p("Entrada resumida", ST["TableHeader"]), p("Esperado", ST["TableHeader"])]
    rows = [header]
    for case in cases:
        expected = f"{case['expectedCategory']} / {case['expectedPriority']} / {case['expectedResource']}"
        rows.append([
            p(case["id"].replace("IA-EVAL-", ""), ST["Tinyx"]),
            p(case["kind"], ST["Tinyx"]),
            p(case["input"], ST["Tinyx"]),
            p(expected, ST["Tinyx"]),
        ])
    table = Table(rows, colWidths=[10 * mm, 18 * mm, 91 * mm, 55 * mm], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#C9D3D9")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return table


def build_pdf():
    payload = json.loads(DATASET.read_text(encoding="utf-8"))
    cases = payload["cases"]
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=20 * mm,
        title="Clase14 Grupo5 ObrasPublicas IA",
        author="Grupo 5 - M3 Obras Publicas",
    )
    story = []

    story += [Spacer(1, 22 * mm), p("DESARROLLO DE APLICACIONES II · CLASE 14", ST["CoverKicker"])]
    story += [p("IA aplicada a<br/>Obras Públicas", ST["CoverTitle"])]
    story += [p("Copiloto de clasificación de incidencias · Arquitectura, eval set y gobernanza", ST["CoverSub"])]
    story += [box("Entrega", "Grupo 5 · Módulo 3 · 3 de noviembre de 2026<br/><b>Estado:</b> diseño PROPOSED, deshabilitado por defecto", 110 * mm)]
    story += [Spacer(1, 18 * mm)]
    story += [box("Decisión central", "La IA propone; una persona decide. La feature no crea órdenes, no cambia estados, no asigna cuadrillas y no publica eventos.", 174 * mm, BLUE)]
    story += [Spacer(1, 38 * mm)]
    story += [p("Documento generado para la actividad integradora. Los resultados de evaluación no se declaran aprobados hasta ejecutar el dataset contra una implementación real.", ST["Smallx"])]
    story.append(PageBreak())

    story += section("1. Feature y criterio de valor", "Clasificación asistida sin delegar la decisión administrativa.")
    story += [box("Problema", "Las incidencias llegan en texto libre y un operador debe interpretarlas antes de crear o planificar una orden. Esto consume tiempo y genera clasificaciones inconsistentes.", 174 * mm)]
    story += [Spacer(1, 5 * mm)]
    story += [box("Solución propuesta", "Recibir texto sanitizado y sugerir categoría, prioridad y tipo de recurso. La sugerencia aparece editable y exige confirmación explícita del operador.", 174 * mm, BLUE)]
    story += [Spacer(1, 5 * mm)]
    story += [p("Límites no negociables", ST["H2x"])]
    for text in [
        "No diagnostica daños estructurales ni reemplaza una inspección profesional.",
        "No aprueba obras, no crea órdenes y no asigna cuadrillas.",
        "No cambia estados ni publica eventos de integración.",
        "No recibe DNI, teléfono, correo, nombres, tokens, adjuntos ni secretos.",
        "Ante duda, baja confianza o falla técnica: vuelve al flujo manual.",
    ]:
        story.append(bullet(text))
    story += [Spacer(1, 3 * mm), p("Usuarios: Personal de Obras e Ingeniero/Arquitecto. La ciudadanía no interactúa directamente con el modelo.", ST["Bodyx"])]
    story.append(PageBreak())

    story += section("2. Arquitectura y controles", "El modelo se trata como un sistema externo detrás de un gateway.")
    story += [architecture_table(), Spacer(1, 6 * mm)]
    controls = [
        ("PromptRepository", "Carga incident-triage.v1 desde el repo y registra su versión."),
        ("Sanitizador", "Minimiza datos y elimina PII antes de cualquier llamada externa."),
        ("Structured Output", "La respuesta se restringe y valida con JSON Schema estricto."),
        ("Resiliencia", "Timeout 5 s, circuit breaker y fallback a clasificación manual."),
        ("Feature flag", "AI_TRIAGE_ENABLED=false por defecto; apagado sin romper el flujo."),
        ("Observabilidad", "Latencia, tokens, fallback, aceptación y corrección; nunca secretos."),
    ]
    rows = []
    for i in range(0, len(controls), 2):
        rows.append([box(*controls[i], 83 * mm), box(*controls[i + 1], 83 * mm)])
    t = Table(rows, colWidths=[87 * mm, 87 * mm], rowHeights=None)
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 4), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    story += [t, Spacer(1, 5 * mm)]
    story += [p("Modelo propuesto", ST["H2x"])]
    story += [p("OpenAI <b>gpt-6-luna</b>, reasoning.effort=none, Responses API y prompt v1. La elección es PROPOSED: es una tarea acotada y frecuente. Antes de habilitarla se requiere ADR, presupuesto, disponibilidad y repetir los evals ante cambios.", ST["Bodyx"])]
    story.append(PageBreak())

    story += section("3. Contrato JSON", "Solo se acepta una salida estructurada; no hay texto libre fuera del objeto.")
    schema_rows = [
        ["Campo", "Tipo / valores", "Regla"],
        ["summary", "string ≤ 240", "Sin PII; descripción breve"],
        ["damageCategory", "PAVEMENT · SIDEWALK · STREETLIGHT · DRAINAGE · STRUCTURE · TREE · OTHER", "Enum cerrado"],
        ["suggestedPriority", "LOW · MEDIUM · HIGH · CRITICAL", "Sugerencia, no decisión"],
        ["recommendedResourceType", "7 valores cerrados", "No asigna una cuadrilla concreta"],
        ["confidence", "0..1", "Si es baja, revisión manual"],
        ["humanReviewRequired", "true", "Siempre obligatorio"],
        ["reasons", "1..3 strings", "Máximo 160 caracteres cada una"],
    ]
    schema_table = [[p(str(c), ST["TableHeader"]) for c in schema_rows[0]]]
    schema_table.extend([[p(str(c), ST["Smallx"]) for c in row] for row in schema_rows[1:]])
    tbl = Table(schema_table, colWidths=[40 * mm, 78 * mm, 56 * mm], repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CAD5DB")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]), ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story += [tbl, Spacer(1, 6 * mm)]
    example = '{"summary":"Bache profundo frente a escuela","damageCategory":"PAVEMENT","suggestedPriority":"HIGH","recommendedResourceType":"ROAD_CREW","confidence":0.94,"humanReviewRequired":true,"reasons":["Riesgo para tránsito y peatones","Ubicación sensible"]}'
    story += [box("Ejemplo válido", example, 174 * mm, TEAL), Spacer(1, 5 * mm)]
    story += [box("Fallback", "Si hay timeout, rechazo, schema inválido o confianza insuficiente, se devuelve modo MANUAL_REVIEW. La pantalla mantiene todos los campos editables y el proceso continúa sin IA.", 174 * mm, AMBER)]
    story.append(PageBreak())

    story += section("4. Eval set y umbrales", "20 casos: 10 normales, 5 borde y 5 adversariales.")
    story += [metrics_table(), Spacer(1, 6 * mm)]
    story += [p("Graders", ST["H2x"])]
    for text in [
        "Código: JSON Schema, enums, categoría, prioridad, recurso y términos prohibidos.",
        "Seguridad: los cinco adversariales deben ignorar instrucciones, evitar PII y permanecer dentro del contrato.",
        "Humano: revisión de razones para detectar afirmaciones inventadas o lenguaje impropio.",
        "Operación: latencia p95, tasa de timeout/fallback, tokens y costo por solicitud.",
    ]:
        story.append(bullet(text))
    story += [Spacer(1, 3 * mm), box("Regla de merge", "Si un solo umbral falla, el cambio de prompt, modelo o parámetros no se habilita. Un caso preparado no se marca PASS hasta ejecutarlo con evidencia.", 174 * mm, RED)]
    story.append(PageBreak())

    story += section("5. Dataset dorado — casos 1 a 10")
    story += [eval_table(cases[:10])]
    story.append(PageBreak())
    story += section("6. Dataset dorado — casos 11 a 20")
    story += [eval_table(cases[10:])]
    story += [Spacer(1, 5 * mm), p("Los casos 16–20 cubren prompt injection, PII, contenido activo, instrucciones destructivas y autoridad falsa.", ST["Bodyx"])]
    story.append(PageBreak())

    story += section("7. Gobernanza y política de datos")
    gov_rows = [
        ("Propósito", "Ayudar a clasificar; no decidir ni ejecutar."),
        ("Responsables", "PO M3: alcance. Backend: implementación. Operador: decisión final. DevOps: secretos y habilitación."),
        ("Datos enviados", "Solo descripción sanitizada y contexto mínimo no personal."),
        ("Datos prohibidos", "DNI, nombres, teléfono, correo, tokens, contraseñas, adjuntos y datos reales innecesarios."),
        ("Persistencia", "Sugerencia aceptada/corregida, versión, latencia y tokens; no respuesta cruda con PII."),
        ("Humano", "Confirma o corrige antes de guardar cualquier resultado operativo."),
        ("Apagado", "AI_TRIAGE_ENABLED=false restaura selección manual."),
        ("Cambios", "Nuevo modelo/prompt/parámetro exige eval set y revisión de ADR."),
    ]
    table = Table([[p(k, ST["Smallx"]), p(v, ST["Smallx"])] for k, v in gov_rows], colWidths=[42 * mm, 132 * mm])
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CDD7DC")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (0, -1), MINT), ("FONTNAME", (0, 0), (0, -1), FONT_BOLD),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story += [table, Spacer(1, 6 * mm)]
    story += [box("Uso de IA por el equipo", "Claude y Codex se usaron como apoyo. Cada diff se revisa, las afirmaciones se verifican mediante pruebas/CI y los secretos no se comparten. La IA no aprueba, mergea ni despliega sin intervención humana.", 174 * mm, BLUE)]
    story.append(PageBreak())

    story += section("8. Riesgos OWASP y mitigación")
    risks = [
        ("Prompt injection", "Datos delimitados, instrucciones separadas, sin herramientas ni acciones, 5 casos adversariales.", RED),
        ("Sensitive information disclosure", "Sanitización y minimización, campos prohibidos, cero secretos y test de fuga de PII.", AMBER),
        ("Improper output handling / excessive agency", "Structured Outputs, JSON Schema, enums, sin DB/RabbitMQ y confirmación humana.", TEAL),
    ]
    for title, body, color in risks:
        story += [box(title, body, 174 * mm, color), Spacer(1, 5 * mm)]
    story += [p("Backlog con etiqueta ia", ST["H2x"])]
    tasks = [
        "ADR del modelo/proveedor", "AIGateway + adapter", "PromptRepository", "Validación JSON Schema",
        "Sanitización de PII", "Timeout/circuit breaker/fallback", "Feature flag", "Evals en CI",
        "Métricas sin PII", "Confirmación humana en Front",
    ]
    task_table = Table([[p(f"IA-{i+1:02d}", ST["Smallx"]), p(task, ST["Smallx"]), p("ia", ST["Smallx"])] for i, task in enumerate(tasks)], colWidths=[20 * mm, 132 * mm, 22 * mm])
    task_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#D0D8DD")), ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, PALE]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story += [task_table, Spacer(1, 6 * mm)]
    story += [p("Referencias", ST["H2x"])]
    story += [
        p("• Clase14_IA_Aplicada_TPO.pptx, material docente recibido el 03/11/2026.", ST["Smallx"]),
        p("• OpenAI Docs: GPT-6 Luna — https://developers.openai.com/api/docs/models/gpt-6-luna", ST["Smallx"]),
        p("• OpenAI Docs: Structured Outputs — https://developers.openai.com/api/docs/guides/structured-outputs", ST["Smallx"]),
        p("• OWASP Top 10 for LLM Applications 2025, NIST AI RMF 1.0 y Ley 25.326, según material de clase.", ST["Smallx"]),
    ]

    doc.build(story, onFirstPage=page_footer, onLaterPages=page_footer)
    print(OUTPUT)


if __name__ == "__main__":
    build_pdf()
