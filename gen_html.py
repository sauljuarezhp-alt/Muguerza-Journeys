import os, pathlib

# Genera los HTML en la misma carpeta donde vive este script (robusto al checkout).
BASE = pathlib.Path(__file__).resolve().parent

# ──────────────────────────────────────────────
# SHARED HELPERS
# ──────────────────────────────────────────────
MERMAID_CDN = '<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>'
MERMAID_INIT = """<script>
  mermaid.initialize({
    startOnLoad: true,
    theme: 'base',
    themeVariables: {
      primaryColor: '#E8F4F3',
      primaryTextColor: '#1A2E2C',
      primaryBorderColor: '#00857C',
      lineColor: '#5C6F6D',
      secondaryColor: '#FFF8EC',
      tertiaryColor: '#FAFCFB',
      fontSize: '14px',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
    },
    flowchart: { curve: 'basis', padding: 18, nodeSpacing: 50, rankSpacing: 55 }
  });
</script>"""

BASE_CSS = """
  :root {
    --primary: #00857C;
    --primary-dark: #005A54;
    --primary-light: #E8F4F3;
    --accent: #F4B942;
    --bg: #F7F9FA;
    --surface: #FFFFFF;
    --text: #1A2E2C;
    --text-muted: #5C6F6D;
    --border: #E1E8E7;
    --whatsapp: #25D366;
    --whatsapp-bg: #DCF8C6;
    --bot-bg: #FFFFFF;
    --danger: #D64545;
    --warning: #E8A33D;
    --success: #2DA771;
    --shadow: 0 2px 8px rgba(0,0,0,0.06);
    --shadow-lg: 0 8px 24px rgba(0,0,0,0.08);
  }
  * { box-sizing: border-box; }
  html { scroll-behavior: smooth; }
  body {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.55;
    font-size: 15px;
  }
  .app { display: grid; grid-template-columns: 280px 1fr; min-height: 100vh; }
  .sidebar {
    position: sticky; top: 0; align-self: start; height: 100vh;
    background: linear-gradient(180deg, var(--sidebar-dark, var(--primary-dark)), var(--sidebar, var(--primary)));
    color: white; padding: 28px 22px; overflow-y: auto;
  }
  .sidebar h1 { margin: 0 0 4px; font-size: 18px; font-weight: 700; letter-spacing: -0.2px; }
  .sidebar .subtitle { font-size: 12px; opacity: 0.75; margin-bottom: 28px; text-transform: uppercase; letter-spacing: 0.6px; }
  .sidebar nav { display: flex; flex-direction: column; gap: 2px; }
  .sidebar nav a {
    color: white; text-decoration: none; padding: 9px 12px; border-radius: 8px;
    font-size: 13.5px; opacity: 0.85; transition: all 0.15s; border-left: 3px solid transparent;
  }
  .sidebar nav a:hover { background: rgba(255,255,255,0.1); opacity: 1; }
  .sidebar nav a .num { display: inline-block; width: 28px; font-variant-numeric: tabular-nums; opacity: 0.6; font-weight: 600; }
  .nav-group { font-size: 10px; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; color: rgba(255,255,255,0.45); padding: 14px 12px 4px; }
  .sidebar .meta { margin-top: 32px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.15); font-size: 12px; opacity: 0.75; line-height: 1.7; }
  .sidebar .meta strong { display: block; margin-top: 8px; color: #fff; opacity: 1; }
  .sidebar .back { display: inline-block; margin-bottom: 18px; color: white; opacity: 0.7; text-decoration: none; font-size: 12px; }
  .sidebar .back:hover { opacity: 1; }
  main { padding: 48px 60px 80px; max-width: 1100px; }
  .hero {
    background: var(--surface); border-radius: 16px; padding: 40px 44px;
    margin-bottom: 36px; box-shadow: var(--shadow); border-left: 6px solid var(--hero-accent, var(--primary));
  }
  .hero .eyebrow { text-transform: uppercase; letter-spacing: 1.2px; font-size: 11px; font-weight: 700; color: var(--hero-accent, var(--primary)); margin-bottom: 10px; }
  .hero h1 { margin: 0 0 12px; font-size: 34px; line-height: 1.15; letter-spacing: -0.5px; }
  .hero p.lead { font-size: 16px; color: var(--text-muted); margin: 0; max-width: 720px; }
  .hero .badges { margin-top: 20px; display: flex; gap: 8px; flex-wrap: wrap; }
  .badge { display: inline-flex; align-items: center; gap: 6px; padding: 4px 10px; background: var(--primary-light); color: var(--primary-dark); border-radius: 20px; font-size: 12px; font-weight: 600; }
  .badge.warn { background: #FFF3DD; color: #8A5A00; }
  .badge.danger { background: #FCE8E8; color: var(--danger); }
  .badge.green { background: #DCF8C6; color: #075E54; }
  section.journey { background: var(--surface); border-radius: 14px; padding: 32px 36px; margin-bottom: 24px; box-shadow: var(--shadow); scroll-margin-top: 20px; }
  section.journey h2 { display: flex; align-items: center; gap: 14px; margin: 0 0 8px; font-size: 22px; letter-spacing: -0.3px; }
  section.journey h2 .num { display: inline-flex; align-items: center; justify-content: center; width: 36px; height: 36px; background: var(--primary); color: white; border-radius: 50%; font-size: 14px; font-weight: 700; }
  section.journey h2 .num.doctor { background: #4A6FA5; }
  section.journey h2 .num.special { background: var(--accent); color: var(--text); }
  section.journey > p.purpose { color: var(--text-muted); margin: 0 0 24px; font-size: 14.5px; padding-left: 50px; }
  .diagram { background: linear-gradient(135deg, #FAFCFB, #F2F7F6); border: 1px solid var(--border); border-radius: 10px; padding: 22px; margin: 18px 0 22px; overflow-x: auto; text-align: center; }
  .mermaid { font-family: inherit !important; min-width: 100%; }
  .chat-preview { background: #ECE5DD; border-radius: 10px; padding: 18px; margin: 16px 0; border: 1px solid var(--border); }
  .chat-preview .label { font-size: 11px; text-transform: uppercase; letter-spacing: 0.8px; color: var(--text-muted); font-weight: 600; margin-bottom: 10px; }
  .bubble { max-width: 80%; padding: 8px 12px; border-radius: 8px; margin-bottom: 6px; font-size: 14px; line-height: 1.45; box-shadow: 0 1px 0.5px rgba(0,0,0,0.13); word-wrap: break-word; white-space: pre-wrap; }
  .bubble.bot { background: var(--bot-bg); border-top-left-radius: 0; margin-right: auto; }
  .bubble.patient { background: var(--whatsapp-bg); border-top-right-radius: 0; margin-left: auto; text-align: left; }
  .bubble.secretary { background: #E3EAF7; border-top-right-radius: 0; margin-left: auto; text-align: left; }
  .bubble .author { display: block; font-size: 11px; color: var(--primary); font-weight: 700; margin-bottom: 2px; }
  .bubble.patient .author { color: #075E54; }
  .bubble.secretary .author { color: #4A6FA5; }
  .screen-mock { background: #1E1E2E; color: #CDD6F4; border-radius: 10px; padding: 20px 24px; margin: 16px 0; font-family: "Consolas", "Fira Code", monospace; font-size: 12.5px; line-height: 1.6; overflow-x: auto; }
  .screen-mock .bar { background: #313244; border-radius: 6px; padding: 6px 12px; margin-bottom: 12px; font-size: 11px; color: #6C7086; }
  details { background: #FAFCFB; border: 1px solid var(--border); border-radius: 8px; padding: 12px 16px; margin: 12px 0; }
  details summary { cursor: pointer; font-weight: 600; color: var(--primary-dark); font-size: 14px; user-select: none; }
  details[open] summary { margin-bottom: 10px; }
  table { width: 100%; border-collapse: collapse; margin: 14px 0; font-size: 13.5px; }
  th, td { text-align: left; padding: 10px 12px; border-bottom: 1px solid var(--border); }
  th { background: var(--primary-light); color: var(--primary-dark); font-weight: 600; font-size: 12px; text-transform: uppercase; letter-spacing: 0.4px; }
  td code { background: #F1F5F4; padding: 1px 6px; border-radius: 4px; font-size: 12.5px; color: var(--primary-dark); }
  .callout { border-left: 4px solid var(--primary); background: var(--primary-light); padding: 12px 16px; border-radius: 6px; margin: 14px 0; font-size: 14px; }
  .callout.warn { border-color: var(--warning); background: #FFF8EC; }
  .callout.danger { border-color: var(--danger); background: #FDECEC; }
  .callout strong { color: var(--primary-dark); }
  .callout.warn strong { color: #8A5A00; }
  .callout.danger strong { color: var(--danger); }
  .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 18px 0; }
  .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 14px; margin: 16px 0; }
  .stat { background: var(--primary-light); border-radius: 10px; padding: 14px 16px; }
  .stat .val { font-size: 22px; font-weight: 700; color: var(--primary-dark); }
  .stat .lbl { font-size: 12px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; margin-top: 2px; }
  ul.actions { list-style: none; padding: 0; margin: 12px 0; display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
  ul.actions li { background: var(--primary-light); border-radius: 8px; padding: 10px 14px; font-size: 13.5px; }
  ul.actions li strong { display: block; color: var(--primary-dark); font-size: 12px; text-transform: uppercase; letter-spacing: 0.4px; margin-bottom: 2px; }
  footer { text-align: center; color: var(--text-muted); font-size: 12px; padding: 30px 0 10px; }
  @media (max-width: 800px) {
    .app { grid-template-columns: 1fr; }
    .sidebar { position: relative; height: auto; }
    main { padding: 24px 20px; }
    .two-col { grid-template-columns: 1fr; }
  }
"""

def page(title, sidebar_html, main_html, extra_vars=""):
    return f"""<!DOCTYPE html>
<html lang="es-MX">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
{MERMAID_CDN}
<style>{BASE_CSS}{extra_vars}</style>
</head>
<body>
<div class="app">
{sidebar_html}
<main>
{main_html}
<footer>Muguerza Connect · CEI Ambulatory Strategy · v1 · 2026-05-25</footer>
</main>
</div>
{MERMAID_INIT}
</body>
</html>"""

# ──────────────────────────────────────────────
# INDEX.HTML
# ──────────────────────────────────────────────
INDEX_CSS = """
  :root { --hero-accent: #00857C; }
  body { display: flex; align-items: center; justify-content: center; min-height: 100vh; background: var(--bg); }
  .index-wrap { max-width: 900px; width: 100%; padding: 48px 24px; }
  .index-logo { font-size: 13px; text-transform: uppercase; letter-spacing: 1.5px; color: var(--text-muted); font-weight: 700; margin-bottom: 8px; }
  .index-title { font-size: 42px; font-weight: 800; letter-spacing: -1px; color: var(--text); margin: 0 0 8px; }
  .index-sub { font-size: 17px; color: var(--text-muted); margin: 0 0 40px; }
  .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 20px; }
  .card { background: var(--surface); border-radius: 16px; padding: 32px 28px; box-shadow: var(--shadow-lg); text-decoration: none; color: var(--text); border-top: 5px solid var(--card-color, var(--primary)); transition: transform 0.15s, box-shadow 0.15s; display: block; }
  .card:hover { transform: translateY(-3px); box-shadow: 0 12px 32px rgba(0,0,0,0.11); }
  .card .icon { font-size: 36px; margin-bottom: 14px; }
  .card h2 { margin: 0 0 6px; font-size: 20px; letter-spacing: -0.3px; }
  .card .sub { font-size: 13px; color: var(--text-muted); margin: 0 0 16px; }
  .card .flows { display: flex; flex-wrap: wrap; gap: 6px; }
  .card .flow-tag { background: #F0F4F3; color: var(--text-muted); border-radius: 20px; padding: 3px 10px; font-size: 12px; }
  .card-wa { --card-color: #25D366; }
  .card-connect { --card-color: #00857C; }
  .card-clinica { --card-color: #F4B942; }
  .index-footer { text-align: center; color: var(--text-muted); font-size: 12px; margin-top: 48px; }
"""

INDEX_HTML = """<!DOCTYPE html>
<html lang="es-MX">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Muguerza Journeys · CEI Ambulatory v1</title>
<style>""" + BASE_CSS + INDEX_CSS + """</style>
</head>
<body>
<div class="index-wrap">
  <div class="index-logo">CEI Ambulatory Strategy</div>
  <h1 class="index-title">Muguerza Journeys</h1>
  <p class="index-sub">Flujos de experiencia del modelo ambulatorio — bot WhatsApp, CRM Connect y operación de clínica.</p>

  <div class="cards">
    <a href="whatsapp.html" class="card card-wa">
      <div class="icon">💬</div>
      <h2>WhatsApp — Paciente</h2>
      <p class="sub">Bot Muguerza Concierge · 12 flujos · Paciente como único actor</p>
      <div class="flows">
        <span class="flow-tag">Contacto inicial</span>
        <span class="flow-tag">Agendamiento</span>
        <span class="flow-tag">Cotización</span>
        <span class="flow-tag">Recordatorios</span>
        <span class="flow-tag">Check-in</span>
        <span class="flow-tag">Resultados</span>
        <span class="flow-tag">Intake docs</span>
        <span class="flow-tag">Escalación</span>
      </div>
    </a>

    <a href="connect.html" class="card card-connect">
      <div class="icon">🖥️</div>
      <h2>Connect — CRM Ambulatorio</h2>
      <p class="sub">Muguerza Connect · 9 módulos · Equipo de clínica CEI</p>
      <div class="flows">
        <span class="flow-tag">Dashboard</span>
        <span class="flow-tag">Patients</span>
        <span class="flow-tag">Calendar</span>
        <span class="flow-tag">Pre-auth</span>
        <span class="flow-tag">Inbox</span>
        <span class="flow-tag">Infrastructure</span>
        <span class="flow-tag">Results</span>
        <span class="flow-tag">Insurers</span>
        <span class="flow-tag">Performance</span>
      </div>
    </a>

    <a href="clinica.html" class="card card-clinica">
      <div class="icon">🏥</div>
      <h2>Clínica — Operación</h2>
      <p class="sub">Journey del paciente · 3 variantes · Organic y San Pedro</p>
      <div class="flows">
        <span class="flow-tag">Journey genérico</span>
        <span class="flow-tag">Organic hospital</span>
        <span class="flow-tag">Spoke San Pedro</span>
        <span class="flow-tag">Escalación clínica</span>
      </div>
    </a>
  </div>

  <p class="index-footer">Muguerza Connect · CEI Ambulatory Strategy · v1 · 2026-05-25</p>
</div>
</body>
</html>"""

# ──────────────────────────────────────────────
# CONNECT.HTML
# ──────────────────────────────────────────────
CONNECT_SIDEBAR = """<aside class="sidebar" style="--sidebar-dark:#005A54;--sidebar:#00857C;">
  <a href="index.html" class="back">&#8592; Volver al índice</a>
  <a href="connect.html" class="back">&#8592; Ir al CRM Ambulatorio</a>
  <h1>Muguerza Connect</h1>
  <div class="subtitle">CRM Consultorio · en pausa</div>
  <nav>
    <div class="nav-group">Secretaria</div>
    <a href="#c1"><span class="num">C1</span> Bandeja WhatsApp CRM</a>
    <a href="#c2"><span class="num">C2</span> Gestión de citas</a>
    <a href="#c3"><span class="num">C3</span> Intake y pre-autorización</a>
    <a href="#c4"><span class="num">C4</span> Resultados y follow-up</a>
    <div class="nav-group">Médico</div>
    <a href="#c5"><span class="num">C5</span> Dashboard del médico</a>
  </nav>
  <div class="meta">
    <strong>Proyecto</strong> CEI Ambulatory Strategy
    <strong>Actores</strong> Secretaria · Médico
    <strong>Versión</strong> v1 · 2026-05-25
  </div>
</aside>"""

CONNECT_MAIN = """  <div class="hero" style="border-left-color:#00857C;">
    <div class="eyebrow" style="color:#00857C;">Muguerza Connect · CRM Consultorio</div>
    <h1>Journeys Secretaria &amp; Médico</h1>
    <div class="callout warn"><strong>Módulo en pausa.</strong> El foco actual es el <a href="connect.html">CRM Ambulatorio</a>. Este módulo de consultorio médico se preserva como referencia pero no es prioridad. Sus fuentes viven en <code>muguerza-connect/*.md</code>.</div>
    <p class="lead">Flows internos del CRM: cómo la secretaria gestiona la bandeja de WhatsApp, crea y edita citas, tramita pre-autorizaciones y entrega resultados. El médico ve su agenda y expedientes sin acceso a chats.</p>
    <div class="badges">
      <span class="badge warn">Módulo en pausa</span>
      <span class="badge">Secretaria: 4 flows</span>
      <span class="badge">Médico: 1 flow</span>
      <span class="badge warn">Médico: sin acceso a WhatsApp</span>
      <span class="badge warn">Aseguradoras: solo equipo clínico</span>
    </div>
  </div>

  <!-- C1 Bandeja WhatsApp CRM -->
  <section class="journey" id="c1">
    <h2><span class="num">C1</span> Bandeja WhatsApp CRM</h2>
    <p class="purpose">Vista exclusiva de secretaria en Connect conectada vía WhatsApp Business API. Gestiona conversaciones que requieren intervención humana — el médico no tiene acceso a esta sección.</p>

    <div class="diagram"><div class="mermaid">
flowchart TD
  A[Secretaria abre Bandeja WhatsApp] --> B[Lista filtrable por prioridad y motivo]
  B --> C[Seleccionar conversacion con needs-human marcado]
  C --> D[Sistema asigna la conversacion a la secretaria]
  D --> E[Panel lateral carga citas y documentos del paciente]
  E --> F[Secretaria lee historial completo del chat]
  F --> G[Responde manualmente o usa plantilla rapida]
  G --> H[Mensaje sale via API como outbound-humano]
  H --> I{Caso resuelto?}
  I -->|Si| J[Marcar resuelto y cerrar conversacion]
  I -->|Requiere otra area| K[Reasignar con nota interna]
  style D fill:#E8F4F3,stroke:#00857C
  style J fill:#DCF8C6,stroke:#25D366
    </div></div>

    <div class="chat-preview">
      <div class="label">Secretaria responde desde Connect</div>
      <div class="bubble bot"><span class="author">Bot Concierge</span>Hola Ana, te paso con el equipo para ayudarte con lo de tu aseguradora.</div>
      <div class="bubble patient"><span class="author">Ana López</span>gracias, es que GNP me dijo que necesito carta de referencia</div>
      <div class="bubble secretary"><span class="author">María (Secretaria)</span>Hola Ana, ya vi tu caso. Déjame revisar con el Dr. García y te confirmo hoy en la tarde. 👍</div>
    </div>

    <details><summary>Acciones disponibles para la secretaria</summary>
    <ul class="actions">
      <li><strong>Tomar conversación</strong>Asignarse el chat, visible para el equipo</li>
      <li><strong>Responder</strong>Enviar mensaje vía WhatsApp Business API</li>
      <li><strong>Plantilla rápida</strong>Insertar texto predefinido</li>
      <li><strong>Crear cita</strong>Modal sin salir del chat</li>
      <li><strong>Adjuntar archivo</strong>PDF o imagen al paciente</li>
      <li><strong>Nota interna</strong>Solo visible en CRM, no al paciente</li>
      <li><strong>Reasignar</strong>A otra secretaria o supervisor</li>
      <li><strong>Devolver al bot</strong>Bot retoma con needs_human=false</li>
    </ul>
    </details>

    <details><summary>Edge cases &amp; manejo</summary>
    <table>
      <tr><th>#</th><th>Caso</th><th>Manejo</th></tr>
      <tr><td>E1</td><td>Dos secretarias abren el mismo chat</td><td>Lock: la primera en tomar asigna; la segunda ve aviso</td></tr>
      <tr><td>E2</td><td>Paciente escribe mientras secretaria redacta</td><td>Notificación de nuevo mensaje sin perder el borrador</td></tr>
      <tr><td>E3</td><td>Ventana 24h cerrada sin mensaje del paciente</td><td>Forzar plantilla HSM pre-aprobada</td></tr>
      <tr><td>E4</td><td>Mensaje saliente falla (número bloqueado)</td><td>Error visible en chat, marcar whatsapp_blocked en paciente</td></tr>
      <tr><td>E5</td><td>Secretaria acaba turno con chats abiertos</td><td>Sistema sugiere reasignar; supervisor ve huérfanos</td></tr>
    </table>
    </details>

    <div class="callout warn"><strong>Permisos:</strong> <code>secretary</code> ve su clínica · <code>secretary_supervisor</code> ve todas · <code>doctor</code> sin acceso · <code>admin</code> solo lectura de auditoría</div>
  </section>

  <!-- C2 Gestión de citas -->
  <section class="journey" id="c2">
    <h2><span class="num">C2</span> Gestión de citas desde CRM</h2>
    <p class="purpose">Crear, editar, reagendar o cancelar citas manualmente. Aplica a citas originadas por llamada, handoff del bot, walk-in o consulta de especialidad.</p>

    <div class="diagram"><div class="mermaid">
flowchart TD
  A[Secretaria abre modal nueva cita] --> B[Buscar paciente por telefono o nombre]
  B --> C{Existe en sistema?}
  C -->|No| D[Crear paciente con datos minimos]
  C -->|Si| E[Cargar perfil del paciente]
  D --> E
  E --> F[Elegir servicio del catalogo]
  F --> G{Tipo de servicio}
  G -->|Infusion Lab o Imagen| H[Mostrar slots disponibles]
  G -->|Consulta especialidad| I[Mostrar agenda del medico]
  H --> J[Seleccionar slot]
  I --> J
  J --> K[Capturar notas y origen de la cita]
  K --> L[Crear cita y reservar slot]
  L --> M[Enviar confirmacion al paciente por WhatsApp]
  style L fill:#DCF8C6,stroke:#25D366
  style M fill:#25D366,stroke:#075E54,color:#fff
    </div></div>

    <details><summary>Acciones sobre cita existente</summary>
    <table>
      <tr><th>Acción</th><th>Descripción</th></tr>
      <tr><td>Editar</td><td>Hora, clínica o servicio — queda en audit log</td></tr>
      <tr><td>Reagendar</td><td>Libera slot, reserva nuevo, notifica al paciente</td></tr>
      <tr><td>Cancelar</td><td>Motivo obligatorio, notifica al paciente</td></tr>
      <tr><td>Marcar no-show</td><td>Al cierre del día</td></tr>
      <tr><td>Convertir a recurrente</td><td>Series de infusión cada X días</td></tr>
      <tr><td>Adjuntar documentos</td><td>Receta u orden médica</td></tr>
    </table>
    </details>

    <details><summary>Edge cases &amp; manejo</summary>
    <table>
      <tr><th>#</th><th>Caso</th><th>Manejo</th></tr>
      <tr><td>E1</td><td>Paciente sin nombre completo o sin INE</td><td>Permitir con datos mínimos, perfil marcado incompleto</td></tr>
      <tr><td>E2</td><td>Slot tomado al confirmar</td><td>Recargar disponibilidad automáticamente</td></tr>
      <tr><td>E3</td><td>Fuera de horario operativo</td><td>Bloquear con mensaje claro</td></tr>
      <tr><td>E4</td><td>Servicio requiere referencia sin documento</td><td>Crear cita con flag pendiente de referencia</td></tr>
      <tr><td>E5</td><td>Cita con aseguradora sin póliza validada</td><td>Crear cita y generar tarea de preauth</td></tr>
      <tr><td>E6</td><td>Dos citas el mismo día para el paciente</td><td>Advertir pero permitir</td></tr>
      <tr><td>E7</td><td>Edición de cita ya confirmada por paciente</td><td>Notificar el cambio al paciente por WhatsApp</td></tr>
    </table>
    </details>
  </section>

  <!-- C3 Intake y pre-autorización -->
  <section class="journey" id="c3">
    <h2><span class="num">C3</span> Intake de documentos y pre-autorización</h2>
    <p class="purpose">Gestionar documentos del paciente que llegaron vía WhatsApp o que la secretaria sube manualmente, y tramitar la pre-autorización con la aseguradora antes de la cita.</p>

    <div class="diagram"><div class="mermaid">
flowchart TD
  A[Secretaria abre seccion Documentos del paciente] --> B[Ver documentos pendientes de revision]
  B --> C[Abrir documento y verificar legibilidad]
  C --> D{Documento valido?}
  D -->|No| E[Notificar al paciente que reenvie via WhatsApp]
  D -->|Si| F[Categorizar y asociar a la cita]
  F --> G[Iniciar tramite de preautorizacion con aseguradora]
  G --> H[Registrar numero de caso o folio]
  H --> I{Preauth aprobada?}
  I -->|Si| J[Actualizar cita como autorizada y notificar al paciente]
  I -->|Pendiente| K[Registrar seguimiento y fecha limite]
  I -->|Rechazada| L[Notificar al medico y al paciente con opciones]
  style J fill:#DCF8C6,stroke:#25D366
  style L fill:#FDECEC,stroke:#D64545
    </div></div>

    <div class="chat-preview">
      <div class="label">Mensajes desde la bandeja CRM al paciente</div>
      <div class="bubble secretary"><span class="author">María (Secretaria)</span>Hola Ana, revisé tu póliza. Tu cita del mié 27 ya está <b>autorizada</b> por GNP. ✅ Llega con tu credencial de asegurado.</div>
      <div class="bubble secretary"><span class="author">María (Secretaria)</span>Hola Ana, necesitamos que reenvíes la receta del Dr. García, la foto está borrosa. ¿La tienes en PDF?</div>
    </div>

    <details><summary>Edge cases &amp; manejo</summary>
    <table>
      <tr><th>#</th><th>Caso</th><th>Manejo</th></tr>
      <tr><td>E1</td><td>Aseguradora tarda más de 48h</td><td>Recordatorio automático, registrar en seguimiento</td></tr>
      <tr><td>E2</td><td>Paciente no tiene documento requerido</td><td>Secretaria coordina con médico tratante</td></tr>
      <tr><td>E3</td><td>Preauth rechazada por cobertura</td><td>Dar al paciente opción de pago privado</td></tr>
      <tr><td>E4</td><td>Cita urgente sin tiempo de preauth</td><td>Marcar pago privado con posible reembolso posterior</td></tr>
      <tr><td>E5</td><td>Póliza vencida</td><td>Notificar al paciente de inmediato</td></tr>
    </table>
    </details>

    <div class="stats">
      <div class="stat"><div class="val">&lt;24h</div><div class="lbl">Tramitación de preauth</div></div>
      <div class="stat"><div class="val">&gt;90%</div><div class="lbl">Citas autorizadas antes de fecha</div></div>
      <div class="stat"><div class="val">&gt;85%</div><div class="lbl">Docs validados en &lt;4h hábiles</div></div>
    </div>
  </section>

  <!-- C4 Resultados y follow-up -->
  <section class="journey" id="c4">
    <h2><span class="num">C4</span> Resultados y follow-up</h2>
    <p class="purpose">Subir resultados de laboratorio o imagen al expediente del paciente y disparar la notificación automática vía WhatsApp. Resultados críticos van al médico antes de llegar al paciente.</p>

    <div class="diagram"><div class="mermaid">
flowchart TD
  A[Secretaria recibe resultado de lab o imagen] --> B[Abrir expediente del paciente en Connect]
  B --> C[Ir a seccion Resultados de la cita]
  C --> D[Subir PDF o imagen al Storage]
  D --> E{Resultado tiene valor critico?}
  E -->|Si| F[Escalar al medico antes de notificar al paciente]
  E -->|No| G[Marcar notify-patient como verdadero]
  F --> H[Medico revisa y autoriza entrega]
  H --> G
  G --> I[Sistema dispara notificacion WhatsApp al paciente]
  I --> J[Registrar notificacion enviada y enlace generado]
  style F fill:#FDECEC,stroke:#D64545
  style I fill:#25D366,stroke:#075E54,color:#fff
    </div></div>

    <div class="callout danger"><strong>Regla dura:</strong> resultados marcados como críticos no se notifican al paciente hasta que el médico los autoriza explícitamente. Sin excepción.</div>

    <details><summary>Criterios de resultado crítico</summary>
    <table>
      <tr><th>Criterio</th><th>Acción</th></tr>
      <tr><td>Valores fuera de rango marcados por el laboratorio</td><td>Escalar al médico antes de liberar</td></tr>
      <tr><td>Hallazgos de imagen con nota de urgencia del radiólogo</td><td>Escalar al médico antes de liberar</td></tr>
      <tr><td>Cualquier duda por parte de la secretaria</td><td>Consultar al médico antes de liberar</td></tr>
    </table>
    </details>

    <details><summary>Edge cases &amp; manejo</summary>
    <table>
      <tr><th>#</th><th>Caso</th><th>Manejo</th></tr>
      <tr><td>E1</td><td>Resultado de imagen como DICOM</td><td>v1: subir PDF del reporte, no el DICOM bruto</td></tr>
      <tr><td>E2</td><td>Archivo mayor a 16 MB</td><td>Comprimir o dividir antes de subir</td></tr>
      <tr><td>E3</td><td>Paciente bloqueó el bot</td><td>Notificar por llamada o email (datos en expediente)</td></tr>
      <tr><td>E4</td><td>Médico no disponible para revisar crítico</td><td>Escalar a médico de guardia o supervisor</td></tr>
      <tr><td>E5</td><td>Resultado llega a la clínica equivocada</td><td>Reasignar al expediente correcto</td></tr>
    </table>
    </details>

    <div class="stats">
      <div class="stat"><div class="val">&gt;90%</div><div class="lbl">Notificados al paciente mismo día</div></div>
      <div class="stat"><div class="val">&lt;5 min</div><div class="lbl">Resultado en sistema a WhatsApp</div></div>
      <div class="stat"><div class="val">100%</div><div class="lbl">Críticos escalados antes de entregar</div></div>
    </div>
  </section>

  <!-- C5 Dashboard médico -->
  <section class="journey" id="c5">
    <h2><span class="num doctor">C5</span> Dashboard del médico</h2>
    <p class="purpose">Vista principal del médico: agenda del día, expedientes de sus pacientes y acceso a historial clínico. Sin acceso a la bandeja de WhatsApp ni a información financiera.</p>

    <div class="diagram"><div class="mermaid">
flowchart TD
  A[Medico inicia sesion en Connect] --> B[Dashboard con agenda del dia]
  B --> C[Ver lista de citas ordenadas por hora]
  C --> D[Seleccionar cita para ver detalle]
  D --> E[Ver perfil del paciente y documentos adjuntos]
  E --> F{Accion del medico}
  F -->|Ver historial| G[Expediente completo del paciente]
  F -->|Agregar nota| H[Nota clinica en la cita]
  F -->|Marcar completada| I[Status cambia a completado]
  F -->|Ver resultados| J[Resultados subidos por secretaria]
  style B fill:#E8F4F3,stroke:#00857C
    </div></div>

    <div class="screen-mock">
      <div class="bar">Muguerza Connect · Dr. García &nbsp;·&nbsp; Mi agenda &nbsp;·&nbsp; Expedientes &nbsp;·&nbsp; Resultados</div>
HOY · Miércoles 27 de mayo                                   📅 Filtrar fecha

  07:30  Ana López           Química 27          ✅ Confirmada
  08:00  Carlos Ruiz         Resonancia rodilla  🕐 En espera
  09:00  María Treviño       Infusión Herceptin  ✅ Confirmada
  10:30  [slot disponible]

────────────────────────────────────────────────────────────────
EXPEDIENTE: Ana López
Última visita: 15 may · Próxima: hoy 7:30
Documentos: receta.pdf · póliza GNP · resultado_abr.pdf
[Agregar nota]  [Ver historial completo]
    </div>

    <div class="callout warn"><strong>El médico NO tiene acceso en v1:</strong> bandeja de WhatsApp · información financiera o de seguros · conversaciones internas del equipo · comunicación directa con el paciente.</div>

    <details><summary>Edge cases &amp; manejo</summary>
    <table>
      <tr><th>#</th><th>Caso</th><th>Manejo</th></tr>
      <tr><td>E1</td><td>Médico sin citas hoy</td><td>Dashboard vacío con mensaje claro</td></tr>
      <tr><td>E2</td><td>Paciente llega sin confirmar</td><td>Secretaria marca desde su vista; médico ve el status actualizado</td></tr>
      <tr><td>E3</td><td>Médico quiere ver citas de otra fecha</td><td>Filtro de fecha en agenda</td></tr>
      <tr><td>E4</td><td>Resultado crítico mientras médico está en consulta</td><td>Badge de notificación en pestaña Resultados</td></tr>
      <tr><td>E5</td><td>Médico de guardia ve pacientes de otro médico</td><td>Solo si tiene permiso de guardia habilitado por admin</td></tr>
    </table>
    </details>
  </section>"""

# ──────────────────────────────────────────────
# CLINICA.HTML
# ──────────────────────────────────────────────
CLINICA_SIDEBAR = """<aside class="sidebar" style="--sidebar-dark:#7A5B00;--sidebar:#B17B00;">
  <a href="index.html" class="back">&#8592; Volver al índice</a>
  <h1>CEI Ambulatoria</h1>
  <div class="subtitle">Operación Clínica · v1</div>
  <nav>
    <div class="nav-group">Journeys de clínica</div>
    <a href="#cl1"><span class="num">CL1</span> Journey paciente</a>
    <a href="#cl2"><span class="num">CL2</span> Organic — hospital</a>
    <a href="#cl3"><span class="num">CL3</span> Inorganic — San Pedro</a>
  </nav>
  <div class="meta">
    <strong>Proyecto</strong> CEI Ambulatory Strategy
    <strong>Actor</strong> Paciente
    <strong>Modelos</strong> Organic · Inorganic
    <strong>Versión</strong> v1 · 2026-05-25
  </div>
</aside>"""

CLINICA_MAIN = """  <div class="hero" style="border-left-color:#F4B942;">
    <div class="eyebrow" style="color:#B17B00;">CEI Ambulatoria · Operación</div>
    <h1>Journeys de Clínica</h1>
    <p class="lead">Flujo end-to-end del paciente desde que agenda hasta que sale con su resultado. Tres variantes: el journey genérico de referencia, el modelo organic dentro de un hospital Muguerza existente y el spoke inorgánico en sitio arrendado en San Pedro (Monterrey).</p>
    <div class="badges">
      <span class="badge">Organic: hub hospitalario</span>
      <span class="badge">Inorganic: spoke San Pedro (leasing)</span>
      <span class="badge warn">Escalación clínica: protocolos distintos</span>
    </div>
  </div>

  <!-- CL1 Journey paciente genérico -->
  <section class="journey" id="cl1">
    <h2><span class="num special">CL1</span> Journey del paciente ambulatorio</h2>
    <p class="purpose">Flujo end-to-end de referencia. Aplica a ambos modelos (organic e inorganic). Las variantes específicas están en CL2 y CL3.</p>

    <div class="diagram"><div class="mermaid">
flowchart TD
  A[Paciente agenda cita via WhatsApp o llamada] --> B[Recibe confirmacion con indicaciones]
  B --> C[Recibe recordatorio T-24h y T-2h]
  C --> D[Hace check-in via WhatsApp al llegar]
  D --> E[Llega a la clinica y da su nombre en recepcion]
  E --> F[Recepcion valida en Connect y confirma registro]
  F --> G[Paciente espera en sala]
  G --> H{Tipo de servicio}
  H -->|Laboratorio| I[Extraccion de muestra]
  H -->|Imagen| J[Sala de estudio con tecnico]
  H -->|Infusion| K[Sillon de infusion con enfermero]
  I --> L[Muestra procesada en laboratorio]
  J --> M[Estudio realizado y enviado a PACS]
  K --> N[Infusion completada - alta ambulatoria]
  L --> O[Resultado disponible en sistema]
  M --> O
  O --> Q[Secretaria sube resultado a Connect]
  Q --> R[Paciente recibe resultado por WhatsApp]
  N --> S[Paciente sale de la clinica]
  R --> S
  style F fill:#E8F4F3,stroke:#00857C
  style R fill:#DCF8C6,stroke:#25D366
    </div></div>

    <table>
      <tr><th>Etapa</th><th>Responsable</th><th>Herramienta</th><th>Duración esperada</th></tr>
      <tr><td>Agendado</td><td>Bot / Secretaria</td><td>WhatsApp / Connect</td><td>2–5 min</td></tr>
      <tr><td>Pre-autorización</td><td>Secretaria</td><td>Connect + aseguradora</td><td>&lt;24 h antes</td></tr>
      <tr><td>Recordatorio</td><td>Bot automático</td><td>WhatsApp HSM</td><td>T-24h y T-2h</td></tr>
      <tr><td>Check-in</td><td>Paciente / Bot</td><td>WhatsApp</td><td>&lt;30 s</td></tr>
      <tr><td>Recepción clínica</td><td>Recepcionista</td><td>Connect</td><td>&lt;3 min</td></tr>
      <tr><td>Espera en sala</td><td>—</td><td>—</td><td>&lt;15 min (meta)</td></tr>
      <tr><td>Servicio clínico</td><td>Técnico / Enfermero</td><td>Equipo clínico</td><td>Variable</td></tr>
      <tr><td>Resultado / Alta</td><td>Secretaria + Bot</td><td>Connect + WhatsApp</td><td>&lt;5 min post-servicio</td></tr>
    </table>

    <div class="callout"><strong>Principios de experiencia no negociables:</strong><br>
    1. El paciente no espera más de 15 min antes de ser atendido.<br>
    2. El paciente nunca gestiona papelería de aseguradora — la absorbe la clínica.<br>
    3. El resultado llega por WhatsApp sin que el paciente lo solicite.<br>
    4. El ambiente no debe sentirse como hospital: luz natural, silencio controlado, sillones cómodos.<br>
    5. En caso de complicación, el protocolo de escalación al hub toma menos de 10 min.
    </div>

    <details><summary>Edge cases &amp; manejo</summary>
    <table>
      <tr><th>#</th><th>Caso</th><th>Manejo</th></tr>
      <tr><td>E1</td><td>Paciente llega sin cita (walk-in)</td><td>Secretaria verifica disponibilidad y crea cita en el momento</td></tr>
      <tr><td>E2</td><td>Paciente llega sin ayuno o preparación</td><td>Informar y ofrecer reagendar mismo día si hay slot</td></tr>
      <tr><td>E3</td><td>Complicación durante infusión</td><td>Activar protocolo de escalación al hub hospitalario</td></tr>
      <tr><td>E4</td><td>Equipo no disponible (falla técnica de imagen)</td><td>Reagendar con disculpa + prioridad en próximo slot</td></tr>
      <tr><td>E5</td><td>Resultado del lab tarda más de lo previsto</td><td>Notificar al paciente el retraso por WhatsApp</td></tr>
      <tr><td>E6</td><td>Paciente quiere resultados impresos</td><td>Recepción imprime en el momento</td></tr>
    </table>
    </details>

    <div class="stats">
      <div class="stat"><div class="val">&gt;80</div><div class="lbl">NPS objetivo al salir</div></div>
      <div class="stat"><div class="val">&lt;15 min</div><div class="lbl">Espera en sala (p90)</div></div>
      <div class="stat"><div class="val">&lt;2 h</div><div class="lbl">Resultado lab por WhatsApp</div></div>
      <div class="stat"><div class="val">&lt;10%</div><div class="lbl">No-show rate objetivo</div></div>
    </div>
  </section>

  <!-- CL2 Organic -->
  <section class="journey" id="cl2">
    <h2><span class="num special">CL2</span> Variante Organic — dentro del hospital</h2>
    <p class="purpose">Zona ambulatoria dedicada dentro de un Hospital Muguerza existente. Entrada independiente, diseño interior diferenciado, personal propio. Escalación clínica sin ambulancia: traslado interno directo.</p>

    <div class="diagram"><div class="mermaid">
flowchart TD
  A[Paciente llega al hospital Muguerza] --> B{Ambulatorio o hospital general?}
  B -->|Ambulatorio| C[Toma entrada independiente senalizada]
  B -->|Hospital general| D[Recepcion general redirige a ambulatorio]
  C --> E[Check-in en recepcion o via WhatsApp previo]
  D --> E
  E --> F[Validacion de cita y pre-auth en Connect]
  F --> G[Sala de espera - ambiente clinica no hospital]
  G --> H[Servicio clinico en area dedicada]
  H --> I{Requiere escalacion?}
  I -->|No| J[Alta ambulatoria y resultado por WhatsApp]
  I -->|Si| K[Traslado directo al piso hospitalario]
  K --> L[Atencion hospitalaria sin re-ingreso administrativo]
  J --> M[Paciente sale por salida ambulatoria]
  style G fill:#E8F4F3,stroke:#00857C
  style K fill:#FFF3DD,stroke:#E8A33D
    </div></div>

    <div class="two-col">
      <table>
        <tr><th>Aspecto</th><th>Variante Organic</th></tr>
        <tr><td>Capex</td><td>Bajo — solo adaptación de área existente</td></tr>
        <tr><td>Escalación clínica</td><td>Traslado interno &lt;10 min, sin ambulancia</td></tr>
        <tr><td>Identidad visual</td><td>Muguerza Ambulatorio — [Hospital]</td></tr>
        <tr><td>Personal</td><td>Propio, acceso a servicios del hospital en emergencia</td></tr>
      </table>
      <table>
        <tr><th>Riesgo</th><th>Mitigación</th></tr>
        <tr><td>Flujos mezclados con hospitalario</td><td>Señalización estricta, entradas separadas</td></tr>
        <tr><td>Se siente como hospital</td><td>Diseño interior radicalmente distinto</td></tr>
        <tr><td>Demoras por recursos compartidos</td><td>Equipos dedicados al ambulatorio en horario operativo</td></tr>
      </table>
    </div>

    <div class="stats">
      <div class="stat"><div class="val">&lt;10 min</div><div class="lbl">Escalación a hospitalización</div></div>
      <div class="stat"><div class="val">&gt;70%</div><div class="lbl">Utilización área en horario operativo</div></div>
    </div>
  </section>

  <!-- CL3 Inorganic San Pedro -->
  <section class="journey" id="cl3">
    <h2><span class="num special">CL3</span> Variante Inorganic — Spoke arrendado en San Pedro</h2>
    <p class="purpose">Clínica ambulatoria en sitio arrendado <b>move-in-ready</b> en San Pedro Garza García (Monterrey), adaptado por fit-out — no greenfield. Hospital Muguerza Alta Especialidad como hub de escalación cercano. Modelo 100% asset-light (espacio, equipo y tecnología arrendados).</p>

    <div class="diagram"><div class="mermaid">
flowchart TD
  A[Paciente de Monterrey agenda via WhatsApp] --> B[Confirmacion y pre-auth por equipo Connect]
  B --> C[Recordatorio T-24h con direccion del spoke San Pedro]
  C --> D[Paciente llega al Spoke San Pedro]
  D --> E[Check-in en recepcion o via WhatsApp]
  E --> F[Sala de espera - ambiente clinica de especialidad]
  F --> G[Servicio clinico en area dedicada]
  G --> H{Requiere escalacion clinica?}
  H -->|No| I[Alta ambulatoria y resultado por WhatsApp]
  H -->|Si| J[Protocolo traslado a Hospital Muguerza Alta Especialidad]
  J --> K[Traslado coordinado - hub a corta distancia]
  K --> L[Ingreso en hub con expediente disponible en Connect]
  I --> M[Paciente sale del spoke]
  style F fill:#FFF8EC,stroke:#E8A33D
  style J fill:#FDECEC,stroke:#D64545
    </div></div>

    <h3 style="margin:24px 0 8px;font-size:16px;">Protocolo de escalación clínica</h3>
    <div class="diagram"><div class="mermaid">
flowchart TD
  A[Evento clinico en spoke] --> B[Enfermero activa protocolo]
  B --> C[Llamada a Hospital Muguerza Alta Especialidad - linea directa]
  C --> D[Preparar paciente para traslado]
  D --> E{Estabilidad del paciente}
  E -->|Estable| F[Traslado en vehiculo con acompanante clinico]
  E -->|Inestable| G[Llamar 911 y notificar hospital hub]
  F --> H[Llegada a hub cercano]
  G --> H
  H --> I[Recepcion en urgencias con expediente de Connect]
  style G fill:#FDECEC,stroke:#D64545
  style H fill:#E8F4F3,stroke:#00857C
    </div></div>

    <div class="two-col">
      <table>
        <tr><th>Aspecto</th><th>Spoke San Pedro</th></tr>
        <tr><td>CAPEX</td><td>100% leasing — espacio, equipo, tecnología</td></tr>
        <tr><td>Mercado</td><td>Monterrey / San Pedro — mercado core de Muguerza</td></tr>
        <tr><td>Servicios v1</td><td>Especialidad única: infusiones / oncología</td></tr>
        <tr><td>Escalación</td><td>Traslado externo a hub cercano, coordinado</td></tr>
      </table>
      <table>
        <tr><th>Riesgo</th><th>Mitigación</th></tr>
        <tr><td>Volumen ya capturado por Alivia / Oncare</td><td>Concierge de aseguradora, médicos referentes, precio bundled</td></tr>
        <tr><td>Fit-out del sitio no listo a tiempo</td><td>Propiedad move-in-ready, obra acotada, hitos con penalización</td></tr>
        <tr><td>Bajo volumen inicial</td><td>Leasing permite ajustar capacidad y salir del sitio</td></tr>
        <tr><td>Escalación depende de distancia al hub</td><td>Sitio a corta distancia de Muguerza, traslado pre-acordado</td></tr>
      </table>
    </div>

    <h3 style="margin:24px 0 8px;font-size:16px;">Hitos del modelo de negocio</h3>
    <table>
      <tr><th>Hito</th><th>Métrica</th><th>Plazo estimado</th></tr>
      <tr><td>Sitio live y COFEPRIS-compliant</td><td>Apertura del primer spoke</td><td>≤ 6 meses</td></tr>
      <tr><td>Primera ruta de pago con aseguradora (PHI)</td><td>Bundle / preferente con pagador ancla (vía Sekura)</td><td>A la apertura</td></tr>
      <tr><td>Break-even operativo</td><td>~70% de ocupación</td><td>6–12 meses post-apertura</td></tr>
      <tr><td>Médicos ancla refiriendo</td><td>3–5 especialistas</td><td>Mes 6</td></tr>
      <tr><td>Decisión de escalar</td><td>Playbook + segundo pagador en proceso</td><td>Mes 12</td></tr>
    </table>
  </section>"""

# ──────────────────────────────────────────────
# CONNECT.HTML — CRM AMBULATORIO (9 módulos, foco actual)
# ──────────────────────────────────────────────
CONNECT_AMB_SIDEBAR = """<aside class="sidebar" style="--sidebar-dark:#005A54;--sidebar:#00857C;">
  <a href="index.html" class="back">&#8592; Volver al índice</a>
  <h1>Muguerza Connect</h1>
  <div class="subtitle">CRM Ambulatorio · v1</div>
  <nav>
    <div class="nav-group">Módulo ambulatorio</div>
    <a href="#a1"><span class="num">A1</span> Dashboard operativo</a>
    <a href="#a2"><span class="num">A2</span> Patients · Registro</a>
    <a href="#a3"><span class="num">A3</span> Calendar</a>
    <a href="#a4"><span class="num">A4</span> Pre-auth · Cola</a>
    <a href="#a5"><span class="num">A5</span> Inbox</a>
    <a href="#a6"><span class="num">A6</span> Infrastructure</a>
    <a href="#a7"><span class="num">A7</span> Results</a>
    <a href="#a8"><span class="num">A8</span> Insurers</a>
    <a href="#a9"><span class="num">A9</span> Performance</a>
  </nav>
  <div class="meta">
    <strong>Proyecto</strong> CEI Ambulatory Strategy
    <strong>Actor</strong> Equipo de clínica CEI
    <strong>Versión</strong> v1 · 2026-06-22
    <a href="connect-consultorio.html" class="back" style="margin-top:14px;display:inline-block;">Módulo consultorio (en pausa) &#8594;</a>
  </div>
</aside>"""

CONNECT_AMB_MAIN = """  <div class="hero" style="border-left-color:#00857C;">
    <div class="eyebrow" style="color:#00857C;">Muguerza Connect · CRM Ambulatorio</div>
    <h1>Operación de la Clínica Ambulatoria CEI</h1>
    <p class="lead">El backbone operativo del modelo ambulatorio: nueve módulos que conectan al equipo de clínica, al paciente, al médico referente y a la aseguradora en un solo sistema. Es el primer pilar a lanzar de la estrategia ambulatoria.</p>
    <div class="badges">
      <span class="badge">9 módulos</span>
      <span class="badge">Actor: equipo de clínica CEI</span>
      <span class="badge warn">Performance: rol elevado</span>
      <span class="badge green">En beta avanzada</span>
    </div>
  </div>

  <div class="callout"><strong>Arquitectura técnica:</strong> Muguerza Connect es la <strong>capa de UI</strong>. El sistema de registro de las clínicas es <strong>TASI</strong> — la base de datos operativa que las clínicas ya usan. Toda lectura y escritura de datos de clínica (pacientes, citas, recursos, pre-auths, resultados, métricas) ocurre <strong>vía la API de TASI</strong>. Connect no mantiene una base de datos propia para los datos de clínica: orquesta y presenta lo que expone TASI.</div>

  <!-- A1 Dashboard operativo -->
  <section class="journey" id="a1">
    <h2><span class="num">A1</span> Dashboard operativo</h2>
    <p class="purpose">Panel de control diario del equipo de la clínica. Centraliza el estado de la clínica de un vistazo: citas de hoy, check-ins, procedimientos en curso, escalaciones activas, pre-autorizaciones pendientes y ocupación de recursos en vivo.</p>

    <div class="diagram"><div class="mermaid">
flowchart TD
  A[Equipo abre Connect e inicia sesion] --> B[Dashboard operativo del dia]
  B --> C[Tarjetas de estado en vivo]
  C --> D[Citas de hoy y check-ins]
  C --> E[Procedimientos en progreso]
  C --> F[Escalaciones activas]
  C --> G[Preauths pendientes]
  C --> H[Ocupacion de recursos en vivo]
  D --> I{Accion requerida?}
  F --> I
  G --> I
  I -->|Si| J[Click lleva al modulo correspondiente]
  I -->|No| K[Monitoreo continuo del turno]
  style B fill:#E8F4F3,stroke:#00857C
  style F fill:#FDECEC,stroke:#D64545
    </div></div>

    <div class="callout"><strong>Tarjetas en vivo:</strong> citas de hoy · check-ins · procedimientos en progreso · escalaciones activas · pre-auths pendientes · ocupación de recursos. Cada tarjeta es un acceso directo al módulo correspondiente.</div>

    <div class="callout warn"><strong>Permisos:</strong> <code>clinic_staff</code> ve operación de su clínica · <code>clinic_coordinator</code> ve además negocio (A8, A9) · <code>admin</code> solo lectura de auditoría. <em>Roles tentativos — verificar contra el modelo de roles real que exponga la API de TASI.</em></div>
  </section>

  <!-- A2 Patients -->
  <section class="journey" id="a2">
    <h2><span class="num">A2</span> Patients · Registro ambulatorio</h2>
    <p class="purpose">Registro buscable de pacientes ambulatorios con aseguradora, póliza, historial de visitas, estado de tratamiento, próximas citas y alertas. Cada perfil abre una vista longitudinal del paciente.</p>

    <div class="diagram"><div class="mermaid">
flowchart TD
  A[Equipo abre Patients] --> B[Buscar por telefono nombre o poliza]
  B --> C{Paciente existe?}
  C -->|No| D[Crear paciente ambulatorio con datos minimos]
  C -->|Si| E[Abrir perfil longitudinal]
  D --> E
  E --> F[Ver citas preauths resultados y conversaciones]
  F --> G[Ver recursos asignados y timeline]
  G --> H{Accion}
  H -->|Nueva cita| I[Abrir Calendar con paciente cargado]
  H -->|Ver resultados| J[Abrir Results del paciente]
  H -->|Atender alerta| K[Resolver alerta activa]
  style E fill:#E8F4F3,stroke:#00857C
    </div></div>

    <details><summary>Qué contiene el perfil longitudinal</summary>
    <ul class="actions">
      <li><strong>Citas</strong>Historial y próximas, con estado</li>
      <li><strong>Pre-auths</strong>Estatus por aseguradora y folio</li>
      <li><strong>Resultados</strong>Lab e imagen ligados a cada visita</li>
      <li><strong>Conversaciones</strong>Hilo de Inbox del paciente</li>
      <li><strong>Recursos</strong>Sillón o sala asignada por visita</li>
      <li><strong>Timeline</strong>Línea de tiempo de toda la relación</li>
    </ul>
    </details>

    <details><summary>Edge cases &amp; manejo</summary>
    <table>
      <tr><th>#</th><th>Caso</th><th>Manejo</th></tr>
      <tr><td>E1</td><td>Paciente sin INE o datos completos</td><td>Crear con datos mínimos, perfil marcado incompleto</td></tr>
      <tr><td>E2</td><td>Duplicado por dos teléfonos</td><td>Sugerir fusión de expedientes al coordinador</td></tr>
      <tr><td>E3</td><td>Paciente recurrente de infusión</td><td>Mostrar serie de tratamiento y adherencia</td></tr>
    </table>
    </details>
  </section>

  <!-- A3 Calendar -->
  <section class="journey" id="a3">
    <h2><span class="num">A3</span> Calendar</h2>
    <p class="purpose">Workspace completo de citas ambulatorias. Crear visitas, filtrar por estado o tipo de servicio, ver estado de pago y pre-auth, asignar recursos operativos y mover al paciente por los estados agendado, check-in, en progreso y completado.</p>

    <div class="diagram"><div class="mermaid">
flowchart TD
  A[Equipo abre Calendar] --> B[Filtrar por estado o tipo de servicio]
  B --> C[Crear nueva visita]
  C --> D[Elegir servicio del catalogo]
  D --> E[Asignar recurso sillon sala o quirofano]
  E --> F[Verificar estado de pago y preauth]
  F --> G[Reservar slot y crear cita]
  G --> H[Mover por estados del flujo]
  H --> I[Scheduled luego Check-in]
  I --> J[In-progress luego Completed]
  J --> K[Liberar recurso al completar]
  style G fill:#DCF8C6,stroke:#25D366
  style K fill:#E8F4F3,stroke:#00857C
    </div></div>

    <div class="callout"><strong>Diferencia clave vs consultorio:</strong> el Calendar ambulatorio <strong>asigna recursos físicos</strong> (sillón de infusión, sala de imagen, quirófano) y libera la capacidad al completar — alimenta directamente al módulo Infrastructure (A6).</div>

    <details><summary>Edge cases &amp; manejo</summary>
    <table>
      <tr><th>#</th><th>Caso</th><th>Manejo</th></tr>
      <tr><td>E1</td><td>Slot o recurso tomado al confirmar</td><td>Recargar disponibilidad de slots y recursos</td></tr>
      <tr><td>E2</td><td>Cita con aseguradora sin pre-auth</td><td>Crear cita y generar tarea en la cola de Pre-auth (A4)</td></tr>
      <tr><td>E3</td><td>Servicio requiere recurso no disponible</td><td>Bloquear y sugerir siguiente slot con recurso libre</td></tr>
      <tr><td>E4</td><td>Infusión recurrente</td><td>Crear serie cada X días con recurso reservado</td></tr>
    </table>
    </details>
  </section>

  <!-- A4 Pre-auth -->
  <section class="journey" id="a4">
    <h2><span class="num">A4</span> Pre-auth · Cola de autorización</h2>
    <p class="purpose">Cola de trabajo de pre-autorización para servicios con aseguradora. Permite seguir solicitudes por estatus, revisar folios del pagador, identificar aprobaciones pendientes y evitar que un servicio avance sin la autorización requerida.</p>

    <div class="diagram"><div class="mermaid">
flowchart TD
  A[Equipo abre cola de Pre-auth] --> B[Filtrar por estatus]
  B --> C[Abrir caso de preauth]
  C --> D[Registrar folio de la aseguradora]
  D --> E{Estatus del caso}
  E -->|Pendiente| F[Dar seguimiento y fecha limite]
  E -->|Aprobada| G[Marcar cita como autorizada]
  E -->|Rechazada| H[Notificar opciones de pago privado]
  F --> I{Servicio listo para avanzar?}
  I -->|Sin autorizacion| J[Bloquear servicio en Calendar]
  G --> K[Liberar servicio para ejecucion]
  style J fill:#FDECEC,stroke:#D64545
  style K fill:#DCF8C6,stroke:#25D366
    </div></div>

    <div class="callout danger"><strong>Regla dura:</strong> un servicio con cobertura de aseguradora <strong>no avanza</strong> si la pre-autorización no está aprobada. La cola bloquea la ejecución en Calendar hasta limpiar el folio (o convertir a pago privado con consentimiento).</div>

    <div class="stats">
      <div class="stat"><div class="val">&lt;24h</div><div class="lbl">Tramitación de preauth</div></div>
      <div class="stat"><div class="val">&gt;90%</div><div class="lbl">Citas autorizadas antes de fecha</div></div>
      <div class="stat"><div class="val">0</div><div class="lbl">Servicios ejecutados sin folio</div></div>
    </div>
  </section>

  <!-- A5 Inbox -->
  <section class="journey" id="a5">
    <h2><span class="num">A5</span> Inbox</h2>
    <p class="purpose">Bandeja de comunicación estilo CRM conectada al journey del paciente. Organiza conversaciones por paciente, canal, intención, estado de no-leído y handoff humano, para dar seguimiento a citas, pre-autorizaciones, resultados, escalaciones y solicitudes generales.</p>

    <div class="diagram"><div class="mermaid">
flowchart TD
  A[Equipo abre Inbox del CRM] --> B[Conversaciones ligadas al journey del paciente]
  B --> C[Organizar por paciente canal intencion y no leidos]
  C --> D[Seleccionar conversacion con handoff humano]
  D --> E[Panel lateral con citas y documentos del paciente]
  E --> F[Responder o usar plantilla rapida]
  F --> G{Caso resuelto?}
  G -->|Si| H[Marcar resuelto y devolver al bot]
  G -->|Otra area| I[Reasignar con nota interna]
  style D fill:#E8F4F3,stroke:#00857C
  style H fill:#DCF8C6,stroke:#25D366
    </div></div>

    <div class="chat-preview">
      <div class="label">El equipo de clínica responde desde el Inbox</div>
      <div class="bubble bot"><span class="author">Bot Concierge</span>Te paso con el equipo de la clínica para confirmar tu infusión del jueves.</div>
      <div class="bubble patient"><span class="author">Ana López</span>gracias, ¿necesito algo de mi aseguradora?</div>
      <div class="bubble secretary"><span class="author">Equipo Clínica</span>Hola Ana, tu pre-autorización con GNP ya está aprobada ✅. Solo llega 15 min antes con tu credencial.</div>
    </div>

    <div class="callout warn"><strong>Aseguradoras:</strong> el bot nunca las gestiona; cualquier mención hace handoff al equipo. La autorización se trabaja en la cola de Pre-auth (A4).</div>
  </section>

  <!-- A6 Infrastructure -->
  <section class="journey" id="a6">
    <h2><span class="num">A6</span> Infrastructure · Capacidad en vivo</h2>
    <p class="purpose">Mapa de capacidad en tiempo real de los recursos de la clínica: sillones de infusión, estaciones de laboratorio, salas de imagen, quirófanos y consultorios. Muestra qué recursos están libres, ocupados o sobre-tiempo para coordinar throughput y liberar capacidad al completar servicios.</p>

    <div class="diagram"><div class="mermaid">
flowchart TD
  A[Equipo abre Infrastructure] --> B[Mapa de capacidad en vivo]
  B --> C[Sillones de infusion]
  B --> D[Estaciones de laboratorio]
  B --> E[Salas de imagen]
  B --> F[Quirofanos y consultorios]
  C --> G{Estado del recurso}
  G -->|Libre| H[Asignar a la siguiente cita]
  G -->|Ocupado| I[Ver tiempo restante estimado]
  G -->|Sobre tiempo| J[Alerta al coordinador]
  H --> K[Throughput coordinado meta 70 por ciento]
  style J fill:#FDECEC,stroke:#D64545
  style K fill:#E8F4F3,stroke:#00857C
    </div></div>

    <div class="callout"><strong>Por qué importa:</strong> la utilización de recursos es la palanca de margen del modelo USPI / Salud Digna. El breakeven operativo se ubica cerca del <strong>70% de utilización</strong>; este módulo es la herramienta que hace visible y accionable esa disciplina.</div>

    <div class="stats">
      <div class="stat"><div class="val">~70%</div><div class="lbl">Utilización objetivo (breakeven)</div></div>
      <div class="stat"><div class="val">En vivo</div><div class="lbl">Estado libre / ocupado / sobre-tiempo</div></div>
    </div>
  </section>

  <!-- A7 Results -->
  <section class="journey" id="a7">
    <h2><span class="num">A7</span> Results</h2>
    <p class="purpose">Seguimiento de resultados de laboratorio, imagen y notas de procedimiento. Destaca hallazgos críticos, separa notificados de pendientes y liga cada resultado al expediente del paciente para que el follow-up no dependa de seguimiento manual.</p>

    <div class="diagram"><div class="mermaid">
flowchart TD
  A[Llega resultado de lab o imagen] --> B[Abrir expediente en Patients]
  B --> C[Subir PDF al Storage]
  C --> D{Resultado critico?}
  D -->|Si| E[Escalar al medico antes de notificar]
  D -->|No| F[Marcar para notificar al paciente]
  E --> G[Medico revisa y autoriza entrega]
  G --> F
  F --> H[Disparar notificacion por WhatsApp]
  H --> I[Registrar entrega y enlace generado]
  style E fill:#FDECEC,stroke:#D64545
  style H fill:#25D366,stroke:#075E54,color:#fff
    </div></div>

    <div class="callout danger"><strong>Regla dura heredada:</strong> los resultados marcados como críticos no se notifican al paciente hasta que el médico los autoriza explícitamente. Sin excepción.</div>

    <div class="stats">
      <div class="stat"><div class="val">&gt;90%</div><div class="lbl">Notificados el mismo día</div></div>
      <div class="stat"><div class="val">&lt;5 min</div><div class="lbl">Resultado en sistema a WhatsApp</div></div>
      <div class="stat"><div class="val">100%</div><div class="lbl">Críticos escalados antes de entregar</div></div>
    </div>
  </section>

  <!-- A8 Insurers -->
  <section class="journey" id="a8">
    <h2><span class="num">A8</span> Insurers</h2>
    <p class="purpose">Resumen de desempeño de la clínica agrupado por aseguradora. Muestra total de citas, servicios completados, pre-autorizaciones pendientes y autorizaciones aprobadas, dando visibilidad de los cuellos de botella relacionados con cada pagador.</p>

    <div class="diagram"><div class="mermaid">
flowchart TD
  A[Coordinador abre Insurers] --> B[Actividad agrupada por aseguradora]
  B --> C[Citas y servicios completados]
  B --> D[Preauths pendientes y aprobadas]
  C --> E{Cuello de botella por pagador?}
  D --> E
  E -->|Si| F[Drill-down a casos pendientes]
  F --> G[Coordinar con el pagador via equipo]
  E -->|No| H[Monitoreo de desempeno por pagador]
  style B fill:#E8F4F3,stroke:#00857C
    </div></div>

    <details><summary>Métricas por aseguradora</summary>
    <table>
      <tr><th>Métrica</th><th>Para qué</th></tr>
      <tr><td>Citas totales</td><td>Peso del pagador en el volumen de la clínica</td></tr>
      <tr><td>Servicios completados</td><td>Conversión real de cita a servicio</td></tr>
      <tr><td>Pre-auths pendientes</td><td>Riesgo de servicios bloqueados</td></tr>
      <tr><td>Autorizaciones aprobadas</td><td>Salud de la relación con el pagador</td></tr>
    </table>
    </details>

    <div class="callout"><strong>Conexión estratégica:</strong> este módulo sostiene la negociación de paquetes <em>bundled</em> con pagadores ancla (canal Sekura) — el mecanismo de margen del modelo USPI tropicalizado.</div>
  </section>

  <!-- A9 Performance -->
  <section class="journey" id="a9">
    <h2><span class="num">A9</span> Performance</h2>
    <p class="purpose">Módulo de analítica financiera y operativa de la clínica ambulatoria. Sigue ingreso cobrado, servicios completados, pacientes únicos, margen estimado, pipeline de aseguradoras, cancelaciones por pre-auth, tendencias mensuales, modelos de pago y desempeño por servicio.</p>

    <div class="diagram"><div class="mermaid">
flowchart TD
  A[Coordinador o admin abre Performance] --> B[Tablero de unit economics]
  B --> C[Ingreso cobrado y servicios completados]
  B --> D[Pacientes unicos y margen estimado]
  B --> E[Pipeline de aseguradoras]
  B --> F[Cancelaciones por preauth]
  B --> G[Tendencias mensuales y modelos de pago]
  C --> H{Desviacion vs meta?}
  D --> H
  H -->|Si| I[Identificar servicio o pagador a corregir]
  H -->|No| J[Validar disciplina de margen]
  style B fill:#E8F4F3,stroke:#00857C
  style I fill:#FFF8EC,stroke:#E8A33D
    </div></div>

    <div class="callout danger"><strong>Permiso elevado:</strong> Performance expone datos financieros (ingreso, margen). Solo accesible a <code>clinic_coordinator</code> y <code>admin</code> — no al equipo operativo general. <em>Rol a verificar contra el esquema real.</em></div>

    <div class="callout warn"><strong>Sin UI sin dato real:</strong> las métricas de este módulo (margen, ingreso, cancelaciones) deben venir de la <strong>API de TASI</strong> — verificar qué endpoints/campos financieros expone antes de implementar la vista. No se renderizan números inventados.</div>
  </section>"""

# ──────────────────────────────────────────────
# WRITE FILES
# ──────────────────────────────────────────────
index_path = BASE / "index.html"
connect_path = BASE / "connect.html"
connect_cons_path = BASE / "connect-consultorio.html"
clinica_path = BASE / "clinica.html"

index_path.write_text(INDEX_HTML, encoding="utf-8")
print(f"Created: {index_path}")

connect_html = page(
    "Muguerza Connect · CRM Ambulatorio v1",
    CONNECT_AMB_SIDEBAR,
    CONNECT_AMB_MAIN
)
connect_path.write_text(connect_html, encoding="utf-8")
print(f"Created: {connect_path}")

# Consultorio: módulo en pausa, preservado como archivo (no es el foco actual).
connect_cons_html = page(
    "Muguerza Connect · CRM Consultorio (en pausa)",
    CONNECT_SIDEBAR,
    CONNECT_MAIN
)
connect_cons_path.write_text(connect_cons_html, encoding="utf-8")
print(f"Created: {connect_cons_path}")

clinica_html = page(
    "CEI Ambulatoria · Clinica Journey v1",
    CLINICA_SIDEBAR,
    CLINICA_MAIN
)
clinica_path.write_text(clinica_html, encoding="utf-8")
print(f"Created: {clinica_path}")

print("Done.")
