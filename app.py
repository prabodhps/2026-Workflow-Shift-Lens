# =========================
# 2026 Workflow Shift Lens
# =========================

YEAR = 2026

import json
import time
import streamlit as st
from openai import OpenAI
from openai import RateLimitError, APIError, APITimeoutError

from process_library import DOMAINS

# -------------------------
# Page config
# -------------------------
st.set_page_config(
    page_title=f"{YEAR} Workflow Shift Lens",
    page_icon="🧭",
    layout="centered"
)

# -------------------------
# Styles (Cards / Boxes)
# -------------------------
st.markdown("""
<style>
.card {
  border: 1px solid rgba(0,0,0,0.12);
  border-radius: 14px;
  padding: 16px;
  background: white;
  box-shadow: 0 2px 10px rgba(0,0,0,0.06);
  margin-bottom: 16px;
  color: rgba(0,0,0,0.88);
}
.badge-red { background:#b91c1c; color:white; padding:6px 10px; border-radius:10px; font-weight:600; margin-bottom:10px; display:inline-block; }
.badge-green { background:#15803d; color:white; padding:6px 10px; border-radius:10px; font-weight:600; margin-bottom:10px; display:inline-block; }
.badge-black { background:#111827; color:white; padding:6px 10px; border-radius:10px; font-weight:600; margin-bottom:10px; display:inline-block; }
.badge-blue { background:#1d4ed8; color:white; padding:6px 10px; border-radius:10px; font-weight:600; margin-bottom:10px; display:inline-block; }

.small-muted { color: rgba(0,0,0,0.65); font-size: 0.92rem; }
ul { margin-top: 6px; }
li { margin-bottom: 6px; }
a { color: #1d4ed8; }
@media (prefers-color-scheme: dark) {
  .card { background: rgba(255,255,255,0.06); border-color: rgba(255,255,255,0.14); color: rgba(255,255,255,0.92); }
  .small-muted { color: rgba(255,255,255,0.7); }
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# Header
# -------------------------
st.title(f"🧭 {YEAR} Workflow Shift Lens")
st.write("Select a business process to see a grounded 'before vs after' workflow view for 2026.")
st.caption(
    "A lightweight AI experiment by Prabodh—built to visualize how work evolves, one step at a time. "
    "No data is stored. Not a substitute for professional advice."
)

# -------------------------
# Dropdowns
# -------------------------
domain = st.selectbox("Domain", list(DOMAINS.keys()))
process = st.selectbox("Process", list(DOMAINS[domain].keys()))
sub_process = st.selectbox("Sub-process focus", DOMAINS[domain][process])


context = st.text_area(
    "Optional context (ERP, scale, constraints, industry, region)",
    placeholder="e.g., SAP/Oracle ERP, regulated industry, shared services model, high approval thresholds…",
    height=90
)

generate = st.button("Generate workflow shift")

# -------------------------
# Prompt
# -------------------------
PROMPT_TEMPLATE = f"""
You are an evidence-minded operating model + process improvement analyst.

Goal: Provide a grounded, high-level workflow shift view for {YEAR} for the selected process.
Be conservative: prefer assist/augment over replace. Avoid sci-fi or fully autonomous claims.
Assume typical enterprise systems exist (ERP/workflow), but do NOT name specific companies in workflow steps.

Return STRICT JSON (no markdown) with EXACTLY these keys:
domain (string)
process (string)
sub_process (string)
assumptions (array of 3-5 strings)
workflow_today (array of 6-10 objects with: step (int), name (string), human (string), system (string), friction (string))
workflow_2026_ai (array of 6-10 objects with: step (int), name (string), ai (string), human (string), system (string), control (string))
ai_automation_opportunities (array of 6-10 objects with: activity (string), ai_can_do (string), risk (string), guardrail (string))
tools_examples (object with: categories (array of strings), notes (string))
impact_summary (object with: where_time_is_saved (array 3-6 strings), kpis_to_watch (array 4-8 strings))

Rules:
- Keep steps high level and realistic.
- Ensure workflow_today vs workflow_2026_ai clearly differ (fewer handoffs, auto-drafting, exception-based review).
- Always include controls: audit trail, access control, policy checks, exception handling.

Selection:
Domain: {{domain}}
Process: {{process}}
Sub-process: {{sub_process}}
Context: {{context}}
"""

# -------------------------
# Helper: retry wrapper
# -------------------------
def call_openai_with_retry(client: OpenAI, messages, max_retries: int = 3):
    last_err = None
    for attempt in range(max_retries):
        try:
            return client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=messages,
                temperature=0.25,
                max_tokens=900,
                response_format={"type": "json_object"},
            )
        except (RateLimitError, APITimeoutError, APIError) as e:
            last_err = e
            time.sleep(1.5 * (2 ** attempt))
    raise last_err

# -------------------------
# Render helpers
# -------------------------
def render_workflow_card(title, badge_class, steps, mode="today"):
    rows = []
    for s in steps:
        if mode == "today":
            rows.append(
                f"<li><strong>{s.get('name','')}</strong><br/>"
                f"<span class='small-muted'>Human:</span> {s.get('human','')}<br/>"
                f"<span class='small-muted'>System:</span> {s.get('system','')}<br/>"
                f"<span class='small-muted'>Friction:</span> {s.get('friction','')}</li>"
            )
        else:
            rows.append(
                f"<li><strong>{s.get('name','')}</strong><br/>"
                f"<span class='small-muted'>AI:</span> {s.get('ai','')}<br/>"
                f"<span class='small-muted'>Human:</span> {s.get('human','')}<br/>"
                f"<span class='small-muted'>System:</span> {s.get('system','')}<br/>"
                f"<span class='small-muted'>Control:</span> {s.get('control','')}</li>"
            )
    st.markdown(f"""
    <div class="card">
      <div class="{badge_class}">{title}</div>
      <ul>{''.join(rows)}</ul>
    </div>
    """, unsafe_allow_html=True)

# -------------------------
# Generate
# -------------------------
if generate:
    if "OPENAI_API_KEY" not in st.secrets or not str(st.secrets["OPENAI_API_KEY"]).strip():
        st.error("Missing OPENAI_API_KEY in Streamlit Secrets.")
        st.stop()

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    messages = [
        {"role": "system", "content": "Return strictly valid JSON only. No markdown. No extra keys."},
        {"role": "user", "content": PROMPT_TEMPLATE.format(
            domain=domain,
            process=process,
            sub_process=sub_process,
            context=(context.strip() if context else "None")
        )}
    ]

    with st.spinner("Thinking…"):
        try:
            resp = call_openai_with_retry(client, messages)
        except RateLimitError:
            st.error("Rate limit/quota hit. Try again in a minute (or check billing/usage).")
            st.stop()
        except Exception as e:
            st.error(f"Unexpected error calling OpenAI: {e}")
            st.stop()

    raw = resp.choices[0].message.content

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        st.error("Model returned non-JSON output. Raw response below:")
        st.code(raw)
        st.stop()

    st.subheader("Workflow shift (before vs after)")

    # Two columns: Today vs 2026
    col1, col2 = st.columns(2)

    with col1:
        render_workflow_card(
            title=f"Typical workflow today (high level)",
            badge_class="badge-red",
            steps=(data.get("workflow_today") or [])[:10],
            mode="today"
        )

    with col2:
        render_workflow_card(
            title=f"Workflow in {YEAR} with AI (target state)",
            badge_class="badge-green",
            steps=(data.get("workflow_2026_ai") or [])[:10],
            mode="ai"
        )

    # Opportunities
    st.markdown("### AI automation opportunities")
    opps = data.get("ai_automation_opportunities") or []
    if opps:
        for o in opps[:10]:
            st.markdown(f"""
            <div class="card">
              <div class="badge-blue">{o.get('activity','Activity')}</div>
              <div><strong>AI can help:</strong> {o.get('ai_can_do','')}</div>
              <div class="small-muted"><strong>Risk:</strong> {o.get('risk','')}</div>
              <div class="small-muted"><strong>Guardrail:</strong> {o.get('guardrail','')}</div>
            </div>
            """, unsafe_allow_html=True)

    # Tools examples
    st.markdown("### Tool examples (illustrative)")
    tools = data.get("tools_examples") or {}
    cats = tools.get("categories") or []
    notes = tools.get("notes") or ""
    st.markdown(f"""
    <div class="card">
      <div class="badge-black">Tool categories</div>
      <ul>{''.join([f"<li>{c}</li>" for c in cats])}</ul>
      <div class="small-muted">{notes}</div>
    </div>
    """, unsafe_allow_html=True)

    # Impact summary
    impact = data.get("impact_summary") or {}
    st.markdown("### What to measure")
    st.markdown(f"""
    <div class="card">
      <div class="badge-black">Impact summary</div>
      <div><strong>Where time is saved:</strong></div>
      <ul>{''.join([f"<li>{x}</li>" for x in (impact.get("where_time_is_saved") or [])])}</ul>
      <div><strong>KPIs to watch:</strong></div>
      <ul>{''.join([f"<li>{x}</li>" for x in (impact.get("kpis_to_watch") or [])])}</ul>
    </div>
    """, unsafe_allow_html=True)

    st.caption("Tip: Screenshot & share. Avoid sensitive process details.")
