# =========================
# 2026 Workflow Shift Lens (Diagram View)
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
# Styles
# -------------------------
st.markdown("""
<style>
/* Card base */
.card {
  border: 1px solid rgba(0,0,0,0.12);
  border-radius: 14px;
  padding: 16px;
  background: #fff;
  box-shadow: 0 2px 10px rgba(0,0,0,0.06);
  margin-bottom: 16px;
  color: rgba(0,0,0,0.90);
}

/* Badges */
.badge-red { background:#b91c1c; color:#fff; padding:6px 10px; border-radius:10px; font-weight:700; display:inline-block; margin-bottom:10px; }
.badge-green { background:#15803d; color:#fff; padding:6px 10px; border-radius:10px; font-weight:700; display:inline-block; margin-bottom:10px; }
.badge-black { background:#111827; color:#fff; padding:6px 10px; border-radius:10px; font-weight:700; display:inline-block; margin-bottom:10px; }
.small-muted { color: rgba(0,0,0,0.65); font-size: 0.92rem; }

/* Diagram container */
.flow {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px;
  line-height: 1.2;
}

/* Step box */
.step {
  border: 1px solid rgba(0,0,0,0.14);
  border-radius: 12px;
  padding: 10px 12px;
  background: rgba(255,255,255,0.95);
  min-width: 120px;
  max-width: 180px;
  text-align: center;
  box-shadow: 0 1px 6px rgba(0,0,0,0.05);
  font-weight: 650;
}

/* Actor chips */
.chip {
  display: inline-block;
  margin-top: 6px;
  font-size: 0.85rem;
  padding: 4px 8px;
  border-radius: 999px;
  border: 1px solid rgba(0,0,0,0.12);
  font-weight: 650;
}
.chip-human { background: rgba(37,99,235,0.08); }
.chip-erp   { background: rgba(2,132,199,0.08); }
.chip-ai    { background: rgba(22,163,74,0.10); }

/* Arrow */
.arrow {
  font-size: 18px;
  color: rgba(0,0,0,0.45);
  font-weight: 700;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .card { background: rgba(255,255,255,0.06); border-color: rgba(255,255,255,0.14); color: rgba(255,255,255,0.92); }
  .small-muted { color: rgba(255,255,255,0.72); }
  .step { background: rgba(17,24,39,0.65); border-color: rgba(255,255,255,0.18); color: rgba(255,255,255,0.92); }
  .arrow { color: rgba(255,255,255,0.35); }
  .chip { border-color: rgba(255,255,255,0.18); }
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# Header
# -------------------------
st.title(f"🧭 {YEAR} Workflow Shift Lens")
st.write("Pick a process to visualize a simple **before vs after** workflow diagram for 2026.")
st.caption("A lightweight AI experiment by Prabodh — built to visualize how work evolves step-by-step. No data is stored. Not professional advice.")

# -------------------------
# Dropdowns
# -------------------------
domain = st.selectbox("Domain", list(DOMAINS.keys()))
process = st.selectbox("Process", list(DOMAINS[domain].keys()))
sub_process = st.selectbox("Focus area (sub-process)", DOMAINS[domain][process])

context = st.text_area(
    "Optional context (scale, ERP maturity, constraints)",
    placeholder="e.g., shared services, heavy approvals, regulated environment, multi-country operations…",
    height=80
)

generate = st.button("Generate diagram")

# -------------------------
# JSON helpers
# -------------------------
def extract_json_object(text: str) -> str | None:
    """Extract first top-level JSON object even if model adds extra text."""
    if not text:
        return None
    start = text.find("{")
    if start == -1:
        return None

    depth = 0
    in_str = False
    escape = False

    for i in range(start, len(text)):
        ch = text[i]
        if in_str:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_str = False
        else:
            if ch == '"':
                in_str = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return text[start:i+1]
    return None

def parse_json_safely(raw: str):
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        extracted = extract_json_object(raw)
        if extracted:
            return json.loads(extracted)
        raise

# -------------------------
# OpenAI helper
# -------------------------
def call_openai_with_retry(client: OpenAI, messages, max_retries: int = 3):
    last_err = None
    for attempt in range(max_retries):
        try:
            return client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=messages,
                temperature=0.15,
                max_tokens=650,
                response_format={"type": "json_object"},
            )
        except (RateLimitError, APITimeoutError, APIError) as e:
            last_err = e
            time.sleep(1.5 * (2 ** attempt))
    raise last_err

# -------------------------
# Diagram rendering
# -------------------------
ICON = {"HUMAN": "👤", "ERP": "🧾", "AI": "🤖"}

def chip_class(actor: str) -> str:
    a = (actor or "").upper()
    if a == "AI":
        return "chip chip-ai"
    if a == "ERP":
        return "chip chip-erp"
    return "chip chip-human"

def render_flow(steps):
    """
    steps: list of {label: str, actor: 'HUMAN'|'ERP'|'AI'}
    """
    items = []
    for idx, s in enumerate(steps):
        label = (s.get("label") or "").strip()
        actor = (s.get("actor") or "HUMAN").strip().upper()

        # safety: keep labels short so diagram looks clean
        if len(label.split()) > 3:
            label = " ".join(label.split()[:3])

        icon = ICON.get(actor, "👤")
        items.append(f"""
          <div class="step">
            {label}
            <div class="{chip_class(actor)}">{icon} {actor.title()}</div>
          </div>
        """)
        if idx != len(steps) - 1:
            items.append('<div class="arrow">→</div>')

    html = f'<div class="flow">{"".join(items)}</div>'
    st.markdown(html, unsafe_allow_html=True)

# -------------------------
# Prompt (diagram-first)
# -------------------------
PROMPT_TEMPLATE = f"""
You are an evidence-minded operating model + process analyst.

Return ONLY a single valid JSON object (no markdown, no extra text).
Make the output DIAGRAM-FRIENDLY:
- Each step label must be 1–2 words (max 3).
- Steps must be high-level, realistic, not "sci-fi".
- Today has NO AI steps (only HUMAN, ERP).
- 2026 includes AI steps (AI, HUMAN, ERP).
- 7 to 9 steps per diagram.

JSON schema (exact keys):
domain (string)
process (string)
sub_process (string)
today_steps (array of objects: label (string), actor (one of: "HUMAN","ERP"))
future_steps (array of objects: label (string), actor (one of: "HUMAN","ERP","AI"))
notes (array of 3 strings) -> short, realistic assumptions/controls (e.g., "audit trail", "exceptions", "human sign-off for high risk")

Rules:
- Prefer "assist/augment" over "replace".
- Include at least one "Exception" or "Approval" control step where appropriate.
- Keep it generic (no company names, no vendor names).

Selection:
Domain: {{domain}}
Process: {{process}}
Focus area: {{sub_process}}
Context: {{context}}

Year: {YEAR}
"""

# -------------------------
# Generate logic
# -------------------------
if generate:
    if "OPENAI_API_KEY" not in st.secrets or not str(st.secrets["OPENAI_API_KEY"]).strip():
        st.error("Missing OPENAI_API_KEY in Streamlit Secrets.")
        st.stop()

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    messages = [
        {
            "role": "system",
            "content": "Return ONLY one valid JSON object. No markdown. No commentary. No extra keys."
        },
        {
            "role": "user",
            "content": PROMPT_TEMPLATE.format(
                domain=domain,
                process=process,
                sub_process=sub_process,
                context=(context.strip() if context else "None")
            )
        }
    ]

    with st.spinner("Generating diagrams…"):
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
        data = parse_json_safely(raw)
    except Exception:
        st.error("Model returned non-JSON output. Raw response below:")
        st.code(raw)
        st.stop()

    # Defensive fallbacks
    today_steps = data.get("today_steps") or []
    future_steps = data.get("future_steps") or []
    notes = data.get("notes") or []

    # Basic validation to avoid blank diagram
    if not isinstance(today_steps, list) or len(today_steps) < 5:
        st.error("Output was incomplete. Try again (or add a bit of context).")
        st.code(raw)
        st.stop()

    if not isinstance(future_steps, list) or len(future_steps) < 5:
        st.error("Future diagram was incomplete. Try again (or add a bit of context).")
        st.code(raw)
        st.stop()

    # -------------------------
    # Render
    # -------------------------
    st.subheader("Process diagram (Before vs After)")

    st.markdown(f"""
    <div class="card">
      <div class="badge-red">Today (typical)</div>
    </div>
    """, unsafe_allow_html=True)
    render_flow(today_steps[:9])

    st.markdown(f"""
    <div class="card">
      <div class="badge-green">{YEAR} (with AI)</div>
    </div>
    """, unsafe_allow_html=True)
    render_flow(future_steps[:9])

    # Notes + legend
    st.markdown(f"""
    <div class="card">
      <div class="badge-black">Notes & controls</div>
      <ul>
        {''.join([f"<li>{n}</li>" for n in notes[:3]])}
      </ul>
      <div class="small-muted"><strong>Legend:</strong> 👤 Human &nbsp;&nbsp; 🧾 ERP/System &nbsp;&nbsp; 🤖 AI</div>
    </div>
    """, unsafe_allow_html=True)

    st.caption("Tip: Screenshot & share. Avoid sensitive internal process details.")
