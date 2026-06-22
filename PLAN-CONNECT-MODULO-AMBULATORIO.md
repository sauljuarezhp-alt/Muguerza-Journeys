# Plan — Ampliar Connect con el Módulo Ambulatorio (9 pantallas del PDF)

> **Estado:** Diseño aprobado. Implementación en curso.
> **Decisión final:** `connect.html` se **centra 100% en el módulo ambulatorio** (los 9 módulos
> del PDF). El **módulo de consultorio médico se deja de lado** — no es prioridad ahora.
> El trabajo de consultorio **no se borra**: se preserva archivado en `connect-consultorio.html`
> y sus fuentes `muguerza-connect/*.md` quedan intactas.
> **Fuente:** *Ambulatory Strategy Business Development.pdf* §6.1 "Muguerza Connect ambulatory module Features".

---

## 1. Punto de partida (qué hay hoy)

`connect.html` documenta **5 flujos del módulo de consultorio** (médico privado + su secretaria),
tal como aclara `NOTA-CONTEXTO.md`:

| Actual | Actor | Resuelve |
|---|---|---|
| C1 Bandeja WhatsApp CRM | Secretaria | Conversaciones que requieren humano |
| C2 Gestión de citas | Secretaria | Crear/editar/reagendar citas |
| C3 Intake y pre-autorización | Secretaria | Documentos + preauth con aseguradora |
| C4 Resultados y follow-up | Secretaria | Subir resultados, notificar paciente |
| C5 Dashboard del médico | Médico | Agenda del día y expedientes |

**Pivote (junio 2026):** el foco es 100% ambulatorio. Estos 5 flujos de consultorio **se dejan de
lado** (no es prioridad). No se borran: se mueven a `connect-consultorio.html` (archivo) y sus
fuentes `muguerza-connect/*.md` quedan intactas. `connect.html` pasa a ser el **CRM ambulatorio**.

---

## 2. Lo que vamos a agregar (los 9 módulos del PDF)

Actor del módulo ambulatorio = **equipo operativo de la clínica CEI** (recepción, enfermería,
coordinador clínico, administración), no la secretaria personal de un médico. Opera a escala de
**clínica / equipo / multi-recurso / multi-aseguradora**, no de un solo consultorio.

| # | Módulo (PDF) | Qué es | ¿Existe hoy? | Cómo se adapta al ambulatorio |
|---|---|---|---|---|
| A1 | **Dashboard** | Panel operativo diario de la clínica: citas de hoy, escalaciones activas, check-ins, procedimientos en curso, preauths, ocupación de recursos en vivo | Parcial — C5 es dashboard **del médico** | Reenfocado al **equipo de clínica**, no a un médico. Suma escalaciones, check-ins y ocupación de recursos |
| A2 | **Patients** | Registro de pacientes ambulatorios con seguro, póliza, historial, estado de tratamiento, próximas citas, alertas. Perfil → vista longitudinal | No (implícito en otros flujos) | **Nuevo** flujo dedicado de registro/expediente ambulatorio |
| A3 | **Calendar** | Workspace completo de citas: crear, filtrar por estado/servicio, estado de pago y preauth, asignar recursos, mover scheduled→check-in→in-progress→completed | Sí — **C2** | Misma lógica, re-escalada: agrega **asignación de recursos** y estados de flujo de clínica |
| A4 | **Pre-auth** | Cola de trabajo de pre-autorización por aseguradora: estatus, folios, pendientes, bloquea servicios sin autorización | Sí — **C3** | Misma lógica, vista de **cola/queue** a nivel clínica (no por paciente) |
| A5 | **Inbox** | Bandeja CRM ligada al journey del paciente: organiza por paciente, canal, intención, no-leídos, handoff humano | Sí — **C1** | Misma lógica, re-escalada al equipo de clínica |
| A6 | **Infrastructure** | Mapa de capacidad en vivo: sillones de infusión, estaciones de lab, salas de imagen, quirófanos, consultorios. Libre/ocupado/sobre-tiempo | **No** | **Nuevo** — específico de ambulatorio. Clave para throughput (lógica Salud Digna / USPI ~70% utilización) |
| A7 | **Results** | Seguimiento de resultados (lab, imagen, notas): críticos, notificados vs pendientes, ligados al expediente | Sí — **C4** | Misma lógica (incluida la regla dura de críticos), re-escalada a clínica |
| A8 | **Insurers** | Resumen de desempeño por aseguradora: citas, servicios completados, preauths pendientes/aprobadas | **No** | **Nuevo** — agrega visibilidad de cuellos de botella por pagador |
| A9 | **Performance** | Analítica financiera/operativa: ingreso cobrado, servicios, pacientes únicos, margen estimado, pipeline de aseguradoras, cancelaciones por preauth, tendencias, modelos de pago, desempeño por servicio | **No** | **Nuevo** — tablero de unit economics del modelo USPI |

### Resumen del mapeo
- **Lógica compartida, re-escalada a clínica (4):** Inbox (A5←C1), Calendar (A3←C2), Pre-auth (A4←C3), Results (A7←C4).
- **Existe pero cambia de actor (1):** Dashboard (A1) — de "agenda del médico" a "panel operativo del equipo".
- **Net-new, no tienen equivalente hoy (4):** Patients (A2), Infrastructure (A6), Insurers (A8), Performance (A9).

---

## 3. Estructura final de `connect.html` (ambulatorio)

`connect.html` se reconstruye **centrado en el módulo ambulatorio**. La lógica de consultorio
sale del foco y queda archivada en `connect-consultorio.html` (mismo estilo, fuera del flujo
principal). El paciente/operador ya no ve dos módulos compitiendo: ve el CRM ambulatorio.

### Navegación de connect.html (sidebar)

```text
Muguerza Connect — CRM Ambulatorio   (equipo de clínica CEI)

▸ OPERACIÓN DIARIA
    A1  Dashboard operativo
    A2  Patients (registro)
    A3  Calendar
    A5  Inbox

▸ AUTORIZACIÓN Y CLÍNICO
    A4  Pre-auth (cola)
    A6  Infrastructure (capacidad)
    A7  Results

▸ NEGOCIO
    A8  Insurers
    A9  Performance        [rol elevado]
```

> Consultorio (C1–C5) → archivado en `connect-consultorio.html`, enlazado discretamente desde el
> pie del sidebar como "Módulo consultorio (en pausa)". No se borra; no es el foco.

### Principios
1. **Actor único: equipo de clínica CEI** (recepción, enfermería, coordinador, administración).
   Roles tentativos a verificar contra el esquema real: `clinic_staff`, `clinic_coordinator`, `admin`.
2. **Reglas duras heredadas** que sí se conservan: resultados críticos no se notifican al paciente
   hasta autorización del médico (ver A7); aseguradoras solo las maneja el equipo, no el bot.
3. **A9 Performance con permiso elevado.** Datos financieros (margen, ingreso) solo para
   `clinic_coordinator` / `admin` — no para todo el equipo (CLAUDE.md: no exponer financiero).
4. **Sin UI sin dato real.** Los módulos net-new (A2, A6, A8, A9) se documentan como journeys, pero
   su implementación de UI depende de verificar/crear el esquema de datos (ver §4).

---

## 4. Arquitectura de datos — TASI vía API (NO Supabase)

**Decisión técnica (junio 2026):** el modelo ambulatorio **no usa Supabase**. La base de datos
operativa de las clínicas es **TASI**, el sistema que las clínicas ya usan. Muguerza Connect es
**solo la capa de UI**: toda lectura y escritura de datos de clínica ocurre **vía la API de TASI**.
Connect no posee una base de datos propia para datos de clínica — orquesta y presenta lo que TASI
expone.

```text
[ Muguerza Connect (UI) ]  <—— API de TASI ——>  [ TASI = sistema de registro / DB de clínicas ]
        9 módulos                                 pacientes · citas · recursos · pre-auths
        Concierge WhatsApp                         resultados · aseguradoras · métricas
```

Cada módulo nuevo **requiere dato real** (regla CLAUDE.md: sin UI sin fuente). Aquí la fuente es
siempre TASI; lo pendiente es **mapear qué endpoints/campos expone su API**:

| Módulo | Dato que consume de la API de TASI |
|---|---|
| A2 Patients | Registro de pacientes (póliza, aseguradora, estado de tratamiento, alertas) |
| A3 Calendar | Citas, slots, asignación de recursos, estados del flujo |
| A4 Pre-auth | Solicitudes de pre-autorización, folios y estatus por aseguradora |
| A6 Infrastructure | Catálogo de recursos (sillones, salas, quirófanos) + estado en tiempo real |
| A8 Insurers | Agregados por aseguradora (citas, servicios, pre-auths) |
| A9 Performance | Métricas financieras/operativas (ingreso, margen, pacientes únicos, cancelaciones) |

**Pendiente clave (terreno técnico/Codex):** obtener la **documentación de la API de TASI** y
mapear endpoints ↔ módulos. Si TASI no expone algún dato (p. ej. ocupación de recursos en vivo o
métricas financieras), se define cómo derivarlo o se levanta como gap de integración — **no se
inventa en la UI**.

---

## 5. Alcance de la implementación

- **connect.html → CRM ambulatorio:** los 9 módulos (A1–A9), cada uno con diagrama Mermaid,
  propósito, edge cases y permisos, en el mismo estilo visual.
- **Consultorio archivado:** `connect-consultorio.html` (mismo contenido C1–C5 de antes). Las
  fuentes `muguerza-connect/*.md` quedan intactas. Enlace discreto desde connect.html.
- **Generación:** todo vía `gen_html.py`. Se regeneran `connect.html` (ambulatorio) y
  `connect-consultorio.html` (archivo).
- **Index:** la card de Connect en `index.html` apunta al CRM ambulatorio (9 módulos) y menciona
  el consultorio en pausa.
- **Pendiente (siguiente pasada):** crear las fuentes `.md` de los 9 módulos en `connect-ambulatorio/`
  para mantener la convención de md-como-fuente del repo.

---

## 6. Preguntas abiertas antes de implementar

1. **Profundidad:** ¿los 9 módulos con el mismo nivel de detalle que C1–C5 (diagrama + edge cases
   + permisos + métricas), o primero una v0 más ligera (diagrama + descripción) para iterar?
2. **Roles ambulatorios:** ¿confirmamos nombres de rol (`clinic_staff`, `clinic_coordinator`) o
   los define el modelo de roles que exponga la API de TASI?
3. **A3/A4/A5/A7 (lógica compartida):** ¿documentar como flujo completo propio, o como
   "delta sobre C2/C3/C1/C4" para no repetir? (Recomiendo delta — menos mantenimiento.)
4. **API de TASI:** ¿tienes acceso a la documentación de la API (endpoints, auth, campos)? Es el
   insumo bloqueante para pasar de journeys a UI conectada. ¿Lectura/escritura o solo lectura?
