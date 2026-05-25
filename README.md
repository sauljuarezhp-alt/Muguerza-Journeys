# Muguerza Connect · Journeys del Modelo Ambulatorio CEI

> **Proyecto:** CEI REACH 2030 — Ambulatory Strategy
> **Última actualización:** 2026-05-25

## Índice

### WhatsApp · Muguerza Concierge

| # | Journey | Resuelve |
|---|---|---|
| 00 | [Identificación y onboarding](whatsapp/00-identificacion-y-onboarding.md) | Primer contacto, alta automática por teléfono |
| 01 | [Agendar cita](whatsapp/01-agendar-cita.md) | Infusión / lab / imagen con disponibilidad real |
| 02 | [Cotizar servicio](whatsapp/02-cotizar-servicio.md) | Precio público sin aseguradora |
| 03 | [Reagendar / cancelar](whatsapp/03-reagendar-cancelar.md) | Cambio o cancelación de cita |
| 04 | [Recordatorio de cita](whatsapp/04-recordatorio-cita.md) | Outbound 24h y 2h antes |
| 05 | [Entrega de resultados](whatsapp/05-entrega-resultados.md) | Notificación + descarga de PDF |
| 06 | [Intake de documentos](whatsapp/06-intake-documentos.md) | PDF/imagen -> Supabase Storage |
| 07 | [Check-in de llegada](whatsapp/07-check-in-llegada.md) | Aviso de llegada desde WhatsApp |
| 08 | [FAQ](whatsapp/08-faq.md) | Ubicación, horarios, estacionamiento |
| 09 | [Derivar consulta especialidad](whatsapp/09-derivar-consulta-especialidad.md) | Handoff a secretaria |
| 10 | [Escalación a humano](whatsapp/10-escalacion-humano.md) | Fallback genérico |

### Muguerza Connect · CRM

| # | Journey | Actor |
|---|---|---|
| 01 | [Bandeja WhatsApp CRM](muguerza-connect/01-bandeja-whatsapp-crm.md) | Secretaria |
| 02 | [Gestión de citas](muguerza-connect/02-gestion-citas-desde-crm.md) | Secretaria |
| 03 | [Intake y pre-autorización](muguerza-connect/03-intake-y-preautorizacion.md) | Secretaria |
| 04 | [Resultados y follow-up](muguerza-connect/04-resultados-y-followup.md) | Secretaria |
| 05 | [Dashboard del médico](muguerza-connect/05-dashboard-medico.md) | Médico |

### Clínica · Journey físico

| # | Journey | Modelo |
|---|---|---|
| 01 | [Paciente ambulatorio genérico](clinica/01-journey-paciente-ambulatorio-generico.md) | Ambos |
| 02 | [Variante Organic](clinica/02-variante-organic-hospital.md) | Hospital existente |
| 03 | [Variante Inorganic – Saltillo](clinica/03-variante-inorganic-spoke-saltillo.md) | Greenfield |

## Convenciones

- **Idioma bot:** español MX, trato de tú, tono cálido y directo.
- **Identificador paciente:** número de teléfono E.164.
- **Horario operativo:** L–V 8:00–20:00, S 8:00–14:00 (configurable por clínica).
- **Servicios bot v1:** infusiones, laboratorio, imagen. Consultas y cirugías → secretaria.
- **Aseguradoras:** el bot NO las maneja. Cualquier mención → handoff.

## Template unificado

Cada journey usa estas secciones:

```text
1. Propósito
2. Precondiciones
3. Happy path  (diagrama Mermaid)
4. Mensajes del bot
5. Edge cases
6. Escalación a humano
7. Métricas de éxito
8. Pendientes / v2
```
