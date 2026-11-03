import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const workspaceDir = "C:/Users/torik/Documents/Codex/2026-08-11/si-testing";
const buildDir = path.join(workspaceDir, ".pptx-build");
const outputDir = path.join(workspaceDir, "output/testing");
const finalPath = path.join(outputDir, "Bitacora_QA_Grupo5_ObrasPublicas.pptx");
const skillDir = "C:/Users/torik/.codex/plugins/cache/openai-primary-runtime/presentations/26.1026.10807/skills/presentations";
const python = "C:/Users/torik/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe";

await fs.mkdir(buildDir, { recursive: true });
await fs.mkdir(outputDir, { recursive: true });

const deck = Presentation.create({ slideSize: { width: 1280, height: 720 } });
const C = { navy: "#0f2f3a", teal: "#0f766e", aqua: "#2dd4bf", blue: "#2563eb", ink: "#111827", gray: "#64748b", pale: "#f1f5f9", white: "#ffffff", green: "#15803d", amber: "#b45309", red: "#b91c1c" };
const font = "Aptos";

function textbox(slide, text, left, top, width, height, size=24, color=C.ink, bold=false, align="left") {
  const box = slide.shapes.add({ geometry: "textbox", position: { left, top, width, height }, fill: "none", line: { fill: "none", width: 0 } });
  box.text = text;
  box.text.style = { fontFamily: font, fontSize: size, color, bold, alignment: align, verticalAlignment: "middle" };
  return box;
}

function base(title, number) {
  const slide = deck.slides.add();
  slide.background.fill = C.white;
  textbox(slide, "M3 · OBRAS PÚBLICAS", 64, 34, 430, 28, 14, C.teal, true);
  textbox(slide, title, 64, 72, 1090, 64, 32, C.navy, true);
  textbox(slide, String(number).padStart(2, "0"), 1170, 36, 48, 28, 13, C.gray, true, "right");
  const line = slide.shapes.add({ geometry: "rect", position: { left: 64, top: 144, width: 1152, height: 3 }, fill: C.aqua, line: { fill: "none", width: 0 } });
  return slide;
}

function bulletList(slide, items, left, top, width, size=21, color=C.ink, gap=54) {
  items.forEach((item, index) => {
    textbox(slide, "•", left, top + index * gap, 28, 34, size, C.teal, true);
    textbox(slide, item, left + 34, top + index * gap, width - 34, 42, size, color, false);
  });
}

// 1. Cover
{
  const s = deck.slides.add();
  s.background.fill = C.navy;
  textbox(s, "BITÁCORA DE QA", 72, 82, 620, 48, 18, C.aqua, true);
  textbox(s, "Testing del TP\nObras Públicas", 72, 154, 760, 190, 52, C.white, true);
  textbox(s, "Evidencia, resultados y pendientes sin ocultar", 76, 370, 720, 52, 24, "#cbd5e1", false);
  textbox(s, "Grupo 5 · Desarrollo de Aplicaciones II · 3 de noviembre de 2026", 76, 618, 1000, 34, 18, C.white, false);
  const accent = s.shapes.add({ geometry: "rect", position: { left: 1060, top: 0, width: 220, height: 720 }, fill: C.teal, line: { fill: "none", width: 0 } });
  textbox(s, "19", 1090, 180, 160, 86, 58, C.white, true, "center");
  textbox(s, "casos con\nevidencia PASS", 1090, 270, 160, 82, 20, C.white, true, "center");
  textbox(s, "60%", 1090, 410, 160, 76, 46, C.white, true, "center");
  textbox(s, "mutation score", 1090, 486, 160, 36, 17, C.white, false, "center");
}

// 2. Scope
{
  const s = base("Qué verificamos", 2);
  bulletList(s, [
    "Flujos funcionales de proyectos, órdenes, recursos y cortes de calle",
    "Roles, autenticación, respuestas negativas y protección de datos",
    "Contratos de eventos, deduplicación y comportamiento ante fallas",
    "Arranque desde cero, calidad del código, performance y seguridad"
  ], 96, 195, 1070, 23, C.ink, 82);
  textbox(s, "La regla de la bitácora", 96, 554, 330, 36, 19, C.teal, true);
  textbox(s, "PASS solo aparece cuando existe una prueba o evidencia reproducible.", 96, 595, 1040, 46, 24, C.navy, true);
}

// 3. Automation
{
  const s = base("Automatización ejecutada", 3);
  textbox(s, "FRONTEND", 84, 188, 250, 30, 16, C.teal, true);
  textbox(s, "58", 84, 222, 190, 74, 54, C.navy, true);
  textbox(s, "pruebas unitarias", 84, 296, 270, 34, 20, C.gray);
  textbox(s, "6", 84, 370, 190, 74, 54, C.blue, true);
  textbox(s, "recorridos E2E reales", 84, 444, 300, 34, 20, C.gray);
  textbox(s, "BACKEND", 470, 188, 250, 30, 16, C.teal, true);
  textbox(s, "108", 470, 222, 220, 74, 54, C.navy, true);
  textbox(s, "pruebas aprobadas", 470, 296, 280, 34, 20, C.gray);
  textbox(s, "V10", 470, 370, 220, 74, 54, C.blue, true);
  textbox(s, "Flyway sobre PostgreSQL real en CI", 470, 444, 370, 54, 20, C.gray);
  textbox(s, "CALIDAD", 860, 188, 250, 30, 16, C.teal, true);
  textbox(s, "86%", 860, 222, 240, 74, 54, C.navy, true);
  textbox(s, "cobertura del Front", 860, 296, 300, 34, 20, C.gray);
  textbox(s, "82%", 860, 370, 240, 74, 54, C.blue, true);
  textbox(s, "fuerza de los tests de mutación", 860, 444, 330, 54, 20, C.gray);
  textbox(s, "Todos los valores provienen de ejecuciones locales o CI. No son estimaciones.", 84, 604, 1080, 34, 18, C.gray);
}

// 4. Execution chart
{
  const s = base("Estado de los 34 casos", 4);
  s.charts.add("bar", {
    position: { left: 90, top: 205, width: 720, height: 350 },
    categories: ["PASS", "Preparados", "No aplica"],
    series: [{ name: "Casos", values: [19, 14, 1], fill: C.teal }],
    hasLegend: false,
    dataLabels: { showValue: true, position: "outEnd" },
    xAxis: { majorGridlines: { style: "solid", fill: "#e2e8f0", width: 1 } },
    yAxis: {}
  });
  textbox(s, "19", 900, 218, 200, 74, 54, C.green, true);
  textbox(s, "con evidencia", 900, 288, 250, 32, 20, C.gray);
  textbox(s, "14", 900, 355, 200, 74, 54, C.amber, true);
  textbox(s, "esperan ambiente o prueba compartida", 900, 425, 285, 60, 20, C.gray);
  textbox(s, "1", 900, 512, 200, 62, 46, C.gray, true);
  textbox(s, "XXE no aplica: la API expuesta usa JSON", 900, 570, 300, 54, 18, C.gray);
}

// 5. Findings
{
  const s = base("Defectos encontrados por las pruebas", 5);
  const rows = [
    ["Accesibilidad", "Barra de progreso sin semántica ARIA", "Corregido y repetido"],
    ["Contraste", "Estado de carga con contraste insuficiente", "Corregido; axe sin críticos"],
    ["Compatibilidad", "TestRestTemplate movido en Spring Boot 4", "Smoke adaptado; build verde"],
    ["Calidad", "Mutation score inicial de 57%", "Nueva prueba; resultado final 60%"]
  ];
  rows.forEach((r, i) => {
    const y = 190 + i * 102;
    textbox(s, r[0], 84, y, 190, 34, 18, C.teal, true);
    textbox(s, r[1], 290, y, 520, 54, 21, C.ink);
    textbox(s, r[2], 860, y, 330, 54, 20, C.green, true);
  });
  textbox(s, "Las pruebas generaron cambios concretos en el producto y en la suite.", 84, 620, 1080, 36, 23, C.navy, true);
}

// 6. Security
{
  const s = base("Seguridad y protección de la entrega", 6);
  bulletList(s, [
    "Gitleaks 8.30.1 revisó toda la historia de Front, Back y TPO: 0 hallazgos",
    "Los roles y JWT tienen casos positivos y negativos automatizados",
    "El pipeline ejecuta auditoría de dependencias y ZAP sobre el stack limpio",
    "Las credenciales viven en secretos o .env local y nunca aparecen en logs ni evidencias"
  ], 88, 190, 1090, 22, C.ink, 82);
  textbox(s, "Pendiente de la corrida final", 88, 540, 360, 34, 18, C.amber, true);
  textbox(s, "Confirmar 0 vulnerabilidades High/Critical en ZAP y conservar el artefacto del job.", 88, 580, 1060, 56, 23, C.navy, true);
}

// 7. Resilience
{
  const s = base("Resiliencia e integración", 7);
  bulletList(s, [
    "Inbox deduplica por eventId y Outbox conserva el identificador durante reintentos",
    "El caso de duplicado ya pasó en pruebas automatizadas",
    "El pipeline prepara la prueba de broker caído, recuperación y arranque limpio",
    "Las pruebas bilaterales con Core, M2, M6 y M7 requieren el ambiente compartido"
  ], 88, 190, 1090, 22, C.ink, 82);
  textbox(s, "Criterio de salida", 88, 548, 280, 34, 18, C.teal, true);
  textbox(s, "No se puede declarar integración completa hasta observar publicación, ruteo y consumo del mismo eventId.", 88, 588, 1080, 58, 23, C.navy, true);
}

// 8. AI declaration
{
  const s = base("Uso responsable de Claude y Codex", 8);
  bulletList(s, [
    "Claude y Codex ayudaron a analizar, proponer código, preparar pruebas y redactar documentación",
    "Una persona revisa cada diff y conserva la autoridad sobre merges, tags y despliegues",
    "CI, pruebas, escaneo de secretos y revisión de contratos validan las sugerencias",
    "Ninguna salida de IA convierte una prueba pendiente en aprobada ni reemplaza evidencia"
  ], 88, 190, 1090, 22, C.ink, 82);
  textbox(s, "Ejemplo", 88, 546, 180, 32, 18, C.teal, true);
  textbox(s, "Se rechazó la idea de que “muchas pruebas” alcanzaban. Se agregaron mutación, E2E, seguridad y trazabilidad.", 88, 585, 1080, 60, 23, C.navy, true);
}

// 9. Pending actions
{
  const s = base("Qué falta para cerrar la entrega", 9);
  bulletList(s, [
    "Ejecutar y guardar el job final de Compose, k6 y ZAP",
    "Configurar SonarCloud y obtener Quality Gate Approved",
    "Completar la prueba bilateral con Core y módulos externos",
    "Cargar evidencias en Jira, Trello y Teams antes del límite",
    "Crear v1.0-testing solo cuando el commit candidato tenga todos los gates verdes"
  ], 88, 180, 1090, 22, C.ink, 72);
  textbox(s, "La demo se realiza en vivo sobre el mismo tag y cada integrante defiende su parte.", 88, 590, 1080, 54, 25, C.navy, true);
}

for (const [i, slide] of deck.slides.items.entries()) {
  const png = await deck.export({ slide, format: "png", scale: 1 });
  await fs.writeFile(path.join(buildDir, `qa-slide-${String(i + 1).padStart(2, "0")}.png`), new Uint8Array(await png.arrayBuffer()));
}
const montage = await deck.export({ format: "webp", montage: true });
await fs.writeFile(path.join(buildDir, "qa-montage.webp"), new Uint8Array(await montage.arrayBuffer()));

const { finalizePresentation } = await import(pathToFileURL(path.join(skillDir, "container_tools/artifact_tool_utils.mjs")).href);
const staging = path.join(buildDir, "finalizer");
await fs.mkdir(staging, { recursive: true });
const candidate = path.join(staging, "candidate.pptx");
await (await PresentationFile.exportPptx(deck)).save(candidate);
await finalizePresentation({
  workspaceDir,
  candidatePath: candidate,
  finalPath,
  pythonExecutable: python,
  integrityValidatorPath: path.join(skillDir, "container_tools/inspect_presentation_package_integrity.py"),
  layoutValidatorPath: path.join(skillDir, "container_tools/inspect_presentation_layout_geometry.py"),
  layoutArgs: ["--expected-slide-size-emu", "12192000,6858000", "--validate-heading-fit"],
  explicitTotalSlideCount: 9,
  requiredNativeTableOwnerSlides: [],
  requiredNativeChartOwnerSlides: [4],
  materializeLiteralChartWorkbooks: true,
  fontPolicy: { basis: "design", families: [font] },
  verifyArtifactToolImport: true,
  receiptPath: path.join(staging, "Bitacora_QA.validation.json")
});

console.log(finalPath);
