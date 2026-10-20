# Sentinel AI India - Home page polish
# Version: v1.1 (no new version). Streamlit, built with Claude Code.
# Model: the AAROGYA X v1.1 Overview (brand.py, plain top, no HTML,
# Coming next in the sidebar). Updated 20 October 2026.

## Goal
The family home page, showing only what Sentinel does today - and a
Command Centre with no invented number.

## Tasks
1. src/brand.py: Brand(name="Sentinel AI India", vision="Unified AI
   security command centre", today_text="agent registry, priority
   queue, routing, links to CloudShield and AutoPilot - agents are
   Python classes; LLM agents arrive in v4", accent about #B45309);
   current_version() = newest "shipped" in docs/versions.json;
   today_line(version).
2. Top of Home: st.title(name); st.markdown("#### Vision: ...");
   the Today line as st.markdown(":orange[**<today line>**]").
   Sidebar on every page: the menu, then a closed st.expander
   "Coming next - 4 modules", then the foot line
   "<name> <version> · System healthy/unhealthy".
3. Navigation with st.navigation: Home, Command Centre, Evolution,
   About (their content kept).
4. Home, under the top:
   Row 1 - KPI cards, each from code, files or the database:
   Agents registered (the registry built at start) - Connected
   systems online, n of 2 (the REST clients) - Tasks recorded (the
   task history file) - Tests passing (versions.json).
   Row 2 - (left) Agent route map: st.graphviz_chart of the graph
   shortest_path uses, with its weights. (right) Connected systems:
   CloudShield and AutoPilot status from get_*_status - "online" or
   "not reachable", with the time checked. Caption: "These services
   run locally; on the live demo they show as not reachable."
   Row 3 - (left) Try the orchestrator: add a task with urgency 1-5
   and see the queue order (this session only, labelled "your test
   tasks - not live alerts"). (right) Task history table.
   Coming next (the sidebar expander of task 2, plain list, nothing
   clickable): Memory in PostgreSQL and a NumPy routing brain (v2) -
   SLA-breach prediction (v3) - LLM investigation agents and the
   human approval gate (v4) - the multi-agent SOC crew (v5).
   Footer on Home: "Every action will wait for a human - from v4."
5. Command Centre: remove every number typed into the code or drawn
   at random (queue_depths, tasks_per_agent, response_times,
   response_times_by_agent) and every chart built on them. Keep only
   charts whose data comes from the running system; where there is
   none, an empty state: "Telemetry appears as real tasks are
   recorded." Tasks created in code at start are labelled "example
   tasks".
6. No HTML anywhere: the Evolution version boxes are rebuilt with
   st.container(border=True), st.markdown and st.progress.
7. Home text: CloudShield is "log-based cloud security" - not
   "AI-powered" (it has no AI yet).
8. .streamlit/config.toml: base "light", primaryColor = the accent.
   Charts at a fixed small size (graphviz and any matplotlib figure),
   with a size test.
9. Tests: each KPI equals its source; the Today version equals
   versions.json; the Today line is orange bold Markdown; the Coming
   next expander is in the sidebar, closed, 4 "arrives in" lines, no
   st.metric, and not on Home; no "unsafe_allow_html" or "st.html"
   in any file; every page runs (AppTest). All earlier tests still
   pass.

## Must not
- Incidents, investigations, an "AI recommendation" or an Approve
  button - they arrive in v4-v5.
- The words "AI agent", "LLM" or "autonomous" for today's agents.
- A number without a source; "vs yesterday"; a login name.
- Any HTML; a new package; a logo or picture band.

## Verification
- Each KPI checked by hand against its source.
- The four removed lists are gone from the Command Centre file.
- Laptop 1366 x 768: title lines and KPI row visible, no scrolling.
- Live demo loads at its clean address; connected systems honestly
  "not reachable".