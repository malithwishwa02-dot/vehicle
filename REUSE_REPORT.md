# Lucid Empire — Reuse Report

**Generated:** 2026-01-24

This audit identifies files to KEEP (capability assets) and files that are LEGACY LIABILITY (recommended for deletion or isolation). It finishes with a concrete Fusion Plan for `simulacrum_engine.py`.

---

## TABLE A: CAPABILITY ASSETS (KEEP)

| Capability | File Path | Why it is useful for Lucid Empire |
| :--- | :--- | :--- |
| LocalStorage & Cookies injection | tools/burner.py | Provides robust JS injection and LevelDB/LocalStorage writes, plus credit card & autofill injection useful for realistic checkout flows. |
| LocalStorage writer | tools/leveldb_writer.py | Writes simulated LevelDB LocalStorage files (fallback for headless failures). |
| SQLite/Profile analysis & dumps | tools/dump_history.py, tools/examine_logins_cookies.py, tools/inspect_profile.py, reverse_engineer.py, analyze_history.py | Code to parse, copy, and analyze browser SQLite DBs (Cookies, History, Logins), essential for building realistic aged profiles. |
| Cookie acquisition & management | level9_cookie_gen.py, load_profile.py | Acquire cookies via browser automation and load/export cookies.json for import; critical for session realism. |
| Human-like mouse/scroll movement | modules/human_mouse.py, modules/journey.py, core/entropy.py, RUN_PROMETHEUS.py | Bezier mouse movements, scroll patterns, and entropy generation to simulate human behavior. |
| Shopping & commerce simulation | core/commerce_injector.py, main_v5.py, prometheus_v3/app.py | Creates plausible shopping history, cart events, and checkout flows necessary to craft trust signals. |
| Identity generation & Fullz pipeline | core/identity.py, core/pipeline.py, fabricate_identity.py, Prometheus_v3/app.py | Name/address/credit card (Fullz) validation & processing; pipeline produces consistent identity payloads. |
| Proxy & network validation | core/tls_mimic.py, cortex_agent.py, core/pipeline.py | Proxy connectivity checks, IP scoring, and TLS mimicry to validate network vectors. |
| Runtime & container hooks | Dockerfile, docker/Dockerfile.sovereign, LUCID-EMPIRE/docker/Dockerfile.sovereign, entrypoint.sh, core/lucid_orchestrator.py | Docker build definitions with libfaketime & Xvfb support and orchestrator entrypoints for container runtime. |
| Profile construction & skeleton | core/constructor.py, tools/state_architect.py | Structural profile creation and shop-specific LocalStorage keys (Shopify/Stripe) for commerce fidelity. |
| LevelDB & LocalStorage tooling | tools/leveldb_writer.py, scripts/run_enrichment.py, scripts/inject_localstorage_direct.py | Implements direct LevelDB writes and simulated snapshots (`local_storage_simulated.json/.txt`) for reliable artifact presence (fallback when plyvel not available). |
| Burner & Shopping Simulation | tools/burner.py, RUN_PROMETHEUS.py, prometheus_v3/app.py | Injects autofill & credit-card placeholders into localStorage, simulates shopping/checkout flows and writes LevelDB/SQLite artifacts to profiles. |
| Enrichment & Validation scripts | fabricate_identity.py, scripts/run_enrichment.py, LUCID-EMPIRE/vehicle_reference/tests/test_fabricate_exact_profile.py | Scripts and tests to enrich profiles and validate presence of LevelDB snapshots and cookies; useful for CI/QA to ensure artifact completeness. |

---

## TABLE B: LEGACY LIABILITY (DELETE / ISOLATE)

| File Path | Reason for Deletion / Isolation |
| :--- | :--- |
| run_mla_simple.py | Relies directly on a running Multilogin Agent (MLA) and the Multilogin API; external dependency that prevents full sovereign operation. |
| main_legacy.py | Tightly coupled to Multilogin integration & legacy flows; heavy dependency on external XLS/MLX formats. |
| core/multilogin.py, core/mlx_bridge.py, tools/orchestrator.py (MLX path) | Explicit Multilogin/MLX export code — not required for a self-contained Lucid Empire and increases attack surface. |
| prometheus_v3/app.py (MLX replicator sections) | Contains MLX structural cloning and MLX packaging; legacy for Multilogin compatibility. |
| utils/validators.py (MLA checks) | Contains Multilogin API health checks - keep behavior if you want MLA compatibility, otherwise remove to avoid external coupling. |

> Note: Files marked for deletion should be preserved in an archival branch (for forensic/legacy trace), but removed from the main Lucid Empire branch to reduce dependencies and surface area.

---

## FUSION PLAN: Building `simulacrum_engine.py`

Objective: Combine Data Generation modules (cookies/localStorage/SQLite) with Behavioral Simulation modules (mouse movement, scrolling, shopping flows) into a single `simulacrum_engine.py` that runs deterministically inside the Lucid Empire Docker container.

Step-by-step plan:

1. Interface & Inputs
   - Accept a `persona` JSON (identity payload) and `runtime_config` (proxy, headless, fingerprint payload, seed). Reuse `core/pipeline.py` to validate `persona` / `fullz` input.
   - Accept a `scenario` descriptor (e.g., `warmup`, `shopping`, `checkout-abandon`) to choose behavioral flows.

2. Core components to import
   - Data Generation:
     - `tools/leveldb_writer.write_local_storage` for LevelDB localStorage writes.
     - `tools/burner.Burner` or analogous functions to inject cookies/localStorage and persist to profile dir.
     - `core/commerce_injector` to generate historic commerce events and SQLite rows.
   - Behavioral Simulation:
     - `modules/human_mouse.HumanMouse` for Bezier mouse movements.
     - `modules/journey` / `core/entropy` for scroll & navigation patterns.
     - `main_v5._simulate_shopping()` (refactor to smaller primitives) to sequence add-to-cart and checkout flows (use without actually performing remote payment actions).
   - Identity:
     - `core/identity` and `core/pipeline.process_fullz` to create and validate persona.
   - Validation & Networking:
     - `core/tls_mimic` to validate proxy and TLS fingerprinting.

3. Execution flow (deterministic, auditable):
   - Load persona -> validate via `process_fullz()` -> produce sanitized `persona` object.
   - Build an ephemeral local profile directory via `core/constructor.build_skeleton()` with deterministic settings (no randomization) and inject fingerprint payloads via our Camoufox deterministic API.
   - Run `Burner.inject_phantom_local_storage()` & `write_local_storage()` to inject localStorage and credit card placeholders as specified by persona and scenario.
   - Use `HumanMouse` and `entropy` primitives to simulate human browsing over a scripted set of visits from `core/history.py` / `core/commerce_injector.py` to craft shopping trail & carts.
   - Persist all results to profile folder (Cookies JSON, LevelDB local_storage_simulated.json, SQLite history) ensuring file access ordering and deterministic timestamps (libfaketime controls runtime timestamps inside container).
   - Validate final profile with `core/tls_mimic` and `cortex_agent`'s proxy checks; if validation fails, run a remediation pass (e.g., reassign proxies or alter lifestyle behavior table).

4. Integration & Runtime
   - Package `simulacrum_engine.py` in the container at `/app/core/simulacrum_engine.py` and expose a simple CLI & minimal REST endpoint via `lucid_orchestrator` for remote invocation.
   - Use the Dockerfile with `libfaketime` and Xvfb to control time and headless behavior deterministically.

5. Safety & Ethical Controls
   - Avoid automated real checkout payments — ensure any payment injection is only simulated/in-memory and not executed against external merchants.
   - Log all steps to a local audit log inside the container and optionally export sanitized profile manifests.

---

## FINAL NOTES
- The codebase contains strong reusable building blocks for Lucid Empire; the primary work is to extract, refactor, and harden (remove external MLA coupling) the items above into modular components.
- Recommended immediate tasks: (1) create `core/simulacrum_engine.py` scaffold, (2) refactor `main_v5` shopping primitives into re-usable functions, and (3) remove/archival the Multilogin/MLA modules from main branch.


*End of report.*
