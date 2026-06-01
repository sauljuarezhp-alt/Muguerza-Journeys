import os, pathlib

BASE = pathlib.Path(os.path.expanduser("~")) / "Downloads" / "muguerza-journeys"

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
      <h2>Connect — CRM</h2>
      <p class="sub">Muguerza Connect · 5 flujos · Secretaria y Médico</p>
      <div class="flows">
        <span class="flow-tag">Bandeja WhatsApp</span>
        <span class="flow-tag">Gestión citas</span>
        <span class="flow-tag">Intake + Pre-auth</span>
        <span class="flow-tag">Resultados</span>
        <span class="flow-tag">Dashboard médico</span>
      </div>
    </a>

    <a href="clinica.html" class="card card-clinica">
      <div class="icon">🏥</div>
      <h2>Clínica — Operación</h2>
      <p class="sub">Journey del paciente · 3 variantes · Organic y Saltillo</p>
      <div class="flows">
        <span class="flow-tag">Journey genérico</span>
        <span class="flow-tag">Organic hospital</span>
        <span class="flow-tag">Spoke Saltillo</span>
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
  <h1>Muguerza Connect</h1>
  <div class="subtitle">CRM Journey · v1</div>
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
    <div class="eyebrow" style="color:#00857C;">Muguerza Connect · CRM</div>
    <h1>Journeys Secretaria &amp; Médico</h1>
    <p class="lead">Flows internos del CRM: cómo la secretaria gestiona la bandeja de WhatsApp, crea y edita citas, tramita pre-autorizaciones y entrega resultados. El médico ve su agenda y expedientes sin acceso a chats.</p>
    <div class="badges">
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
    <a href="#cl3"><span class="num">CL3</span> Inorganic — Saltillo</a>
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
    <p class="lead">Flujo end-to-end del paciente desde que agenda hasta que sale con su resultado. Tres variantes: el journey genérico de referencia, el modelo organic dentro de un hospital Muguerza existente y el spoke greenfield de Saltillo.</p>
    <div class="badges">
      <span class="badge">Organic: hub hospitalario</span>
      <span class="badge">Inorganic: spoke Saltillo</span>
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

  <!-- CL3 Inorganic Saltillo -->
  <section class="journey" id="cl3">
    <h2><span class="num special">CL3</span> Variante Inorganic — Spoke Saltillo</h2>
    <p class="purpose">Clínica ambulatoria greenfield en Saltillo. Espacio arrendado, diseñado desde cero, con Hospital Muguerza Saltillo como hub de escalación (traslado &lt;20 min). Modelo 100% asset-light.</p>

    <div class="diagram"><div class="mermaid">
flowchart TD
  A[Paciente de Saltillo agenda via WhatsApp] --> B[Confirmacion y pre-auth por equipo Connect]
  B --> C[Recordatorio T-24h con direccion del spoke Saltillo]
  C --> D[Paciente llega al Spoke Saltillo]
  D --> E[Check-in en recepcion o via WhatsApp]
  E --> F[Sala de espera - ambiente clinica de especialidad]
  F --> G[Servicio clinico en area dedicada]
  G --> H{Requiere escalacion clinica?}
  H -->|No| I[Alta ambulatoria y resultado por WhatsApp]
  H -->|Si| J[Protocolo traslado a Hospital Muguerza Saltillo]
  J --> K[Traslado coordinado - maximo 20 min]
  K --> L[Ingreso en hub con expediente disponible en Connect]
  I --> M[Paciente sale del spoke]
  style F fill:#FFF8EC,stroke:#E8A33D
  style J fill:#FDECEC,stroke:#D64545
    </div></div>

    <h3 style="margin:24px 0 8px;font-size:16px;">Protocolo de escalación clínica</h3>
    <div class="diagram"><div class="mermaid">
flowchart TD
  A[Evento clinico en spoke] --> B[Enfermero activa protocolo]
  B --> C[Llamada a Hospital Muguerza Saltillo - linea directa]
  C --> D[Preparar paciente para traslado]
  D --> E{Estabilidad del paciente}
  E -->|Estable| F[Traslado en vehiculo con acompanante clinico]
  E -->|Inestable| G[Llamar 911 y notificar hospital hub]
  F --> H[Llegada a hub en maximo 20 min]
  G --> H
  H --> I[Recepcion en urgencias con expediente de Connect]
  style G fill:#FDECEC,stroke:#D64545
  style H fill:#E8F4F3,stroke:#00857C
    </div></div>

    <div class="two-col">
      <table>
        <tr><th>Aspecto</th><th>Spoke Saltillo</th></tr>
        <tr><td>CAPEX</td><td>100% leasing — espacio, equipo, tecnología</td></tr>
        <tr><td>Mercado</td><td>Saltillo — nuevo mercado para CEI</td></tr>
        <tr><td>Servicios v1</td><td>Infusiones, laboratorio, imagen básica</td></tr>
        <tr><td>Escalación</td><td>Traslado externo al hub &lt;20 min</td></tr>
      </table>
      <table>
        <tr><th>Riesgo</th><th>Mitigación</th></tr>
        <tr><td>Mercado desconocido en Saltillo</td><td>Análisis de demanda + alianzas con médicos locales</td></tr>
        <tr><td>Escalación más lenta que organic</td><td>Protocolos de traslado pre-acordados, simulacros</td></tr>
        <tr><td>Bajo volumen inicial</td><td>Leasing permite ajustar capacidad</td></tr>
        <tr><td>Marca desconocida en Saltillo</td><td>Campaña local + red de médicos referentes</td></tr>
      </table>
    </div>

    <h3 style="margin:24px 0 8px;font-size:16px;">Hitos del modelo de negocio</h3>
    <table>
      <tr><th>Hito</th><th>Métrica</th><th>Plazo estimado</th></tr>
      <tr><td>Break-even operativo</td><td>60–70% de ocupación</td><td>6–12 meses post-apertura</td></tr>
      <tr><td>Volumen mínimo viable</td><td>25 pacientes / día</td><td>Mes 3</td></tr>
      <tr><td>NPS objetivo</td><td>&gt;80</td><td>Mes 6</td></tr>
      <tr><td>Expansión a segundo spoke</td><td>Según resultados Saltillo</td><td>Año 2</td></tr>
    </table>
  </section>"""

# ──────────────────────────────────────────────
# WRITE FILES
# ──────────────────────────────────────────────
index_path = BASE / "index.html"
connect_path = BASE / "connect.html"
clinica_path = BASE / "clinica.html"

index_path.write_text(INDEX_HTML, encoding="utf-8")
print(f"Created: {index_path}")

connect_html = page(
    "Muguerza Connect · CRM Journey v1",
    CONNECT_SIDEBAR,
    CONNECT_MAIN
)
connect_path.write_text(connect_html, encoding="utf-8")
print(f"Created: {connect_path}")

clinica_html = page(
    "CEI Ambulatoria · Clinica Journey v1",
    CLINICA_SIDEBAR,
    CLINICA_MAIN
)
clinica_path.write_text(clinica_html, encoding="utf-8")
print(f"Created: {clinica_path}")

print("Done.")
