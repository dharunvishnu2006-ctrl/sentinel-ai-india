# Build log

One entry per batch: what Claude Code built, what I changed, caught or
rejected, what I learned, and the time it took.

### Home page polish (v1.1) - 20 Oct 2026

- **What Claude Code built:** src/brand.py, src/home_data.py, the
  views/ pages with st.navigation, the sidebar "Coming next", 20 new
  tests; removed the typed/random Command Centre charts and all HTML.
- **What I changed, caught or rejected:** rejected Dijkstra with
  typed-in latencies and a duplicate route finder on Home; caught
  "degraded" shown as a status, the "Security Breach!" history row
  without a label, views/shared.py not in the plan, the inch-based
  size test that let an ~800 px chart through, Black reformatting 4
  untouched files (reverted), stale test count 54 (real: 77), and the
  false Dijkstra and LLM claims in versions.json and About. By hand:
  amber telemetry bars, About text, versions.json.
- **What I learned:** patch the name where it is looked up -
  patching src.retry.time.sleep froze AppTest because it replaced
  time.sleep for the whole process. BFS counts hops; Dijkstra adds
  costs.
- **Time:** about 3.5 hours (12:30-17:25, with a break).