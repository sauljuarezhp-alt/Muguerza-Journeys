# Nota de contexto — mayo 2026

Los flujos de Muguerza Connect documentados en esta carpeta (`muguerza-connect/`) fueron diseñados bajo el enfoque de **consultorio privado**: un médico, su secretaria personal y sus pacientes dentro de Muguerza.

En mayo 2026 el enfoque del proyecto se clarificó: Muguerza Connect tiene dos módulos distintos con lógicas separadas.

1. **Módulo de consultorio** (existente, no tocar) — portal doctor + portal secretaria, centrado en el médico privado dentro de Muguerza. Los journeys de esta carpeta aplican aquí.

2. **Módulo de clínicas ambulatorias** (nuevo) — portal del equipo operativo de cada clínica CEI ambulatoria. Tiene su propia interfaz, su propia lógica de BD y sus propios flujos. Los journeys de la carpeta `clinica/` son la referencia correcta para este módulo.

Los journeys `muguerza-connect/01` a `05` siguen siendo válidos para el módulo de consultorio. No reflejan el flujo del módulo ambulatorio.
