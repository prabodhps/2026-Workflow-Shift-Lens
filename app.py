# =========================
# 2026 Workflow Shift Lens (Vertical + Side-by-side)
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
  margin-bottom: 14px;
  color: rgba(0,0,0,0.90);
}

/* Badges */
.badge-red { background:#b91c1c; color:#fff; padding:6px 10px; border-radius:10px; font-weight:700; display:inline-block; margin-bottom:10px; }
.badge-green { background:#15803d; color:#fff; padding:6px 10px; border-radius:10px; font-weight:700; display:inline-block; margin-bottom:10px; }
.badge-black { background:#111827; color:#fff; padding:6px 10px; border-radius:10px; font-weight:700; display:inline-block; margin-bottom:10px; }
.small-muted { color: rgba(0,0,0,0.65); font-size: 0.92rem; }

/* Vertical workflow container */
.flow-vertical {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* Step box */
.step {
  border: 1px solid rgba(0,0,0,0.14);
  border-radius: 12px;
  padding: 10px 12px;
  background: rgba(255,255,255,0.95);
  box-shadow: 0 1px 6px rgba(0,0,0,0.05);
  font-weight: 700;
}

/* Row inside step */
.step-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

/* Keep label readable on phone */
.step-label {
  font-size: 0.98rem;
  line-height: 1.2;
  max-width: 70%;
  word-wrap: break-word;
}

/* Actor chips */
.chip {
  display: inline-block;
  font-size: 0.82rem;
  padding: 4px 8px;
  border-radius: 999px;
  border: 1px solid rgba(0,0,0,0.12);
  font-weight: 750;
  white-space: nowrap;
}
.chip-human { background: rgba(37,99,235,0.10); }
.chip-erp   { background: rgba(2,132,199,0.10); }
.chip-ai    { background: rgba(22,163,74,0.12); }
.chip-mixed { background: rgba(124,58,237,0.12); }

/* Down arrow */
.arrow-down {
  text-align: center;
  font-size: 18px;
  font-weight: 900;
  color: rgba(0,0,0,0.35);
  line-height: 1;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .card { background: rgba(255,255,255,0.06); border-color: rgba(255,255,255,0.14); color: rgba(255,255,255,0.92); }
  .small-muted { color: rgba(255,255,255,0.72); }
  .step { background: rgba(17,24,39,0.65); border-color: rgba(255,255,255,0.18); color: rgba(255,255,255,0.92); }
  .arrow-down { color: rgba(255,255,255,0.35); }
  .chip { border-color: rgba(255,255,255,0.18); }
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# Header
# -------------------------
st.title(f"🧭 {YEAR} Workflow Shift Lens")
st.write("Select a domain + workflow to see an **indicative** shift from “today” to “2026 with AI”.")
st.caption("A lightweight AI experiment by Prabodh — built to visualize how work evolves step-by-step. No data is stored. Not professional advice.")

# -------------------------
# Inputs
# -------------------------
domain = st.selectbox("Domain", list(DOMAINS.keys()))
workflow = st.selectbox("Workflow", list(DOMAINS[domain].keys()))
focus_area = st.selectbox("Focus area (optional)", DOMAINS[domain][workflow])

# Better context (fixed options)
industry = st.selectbox(
    "Industry context",
    [
        "General / Cross-industry",
        "Technology / Software",
        "Telecom / ICT",
        "Financial Services",
        "Healthcare",
        "Manufacturing",
        "Retail / eCommerce",
        "Hospitality",
        "Energy / Utilities",
        "Government / Public sector"
    ],
    index=0
)

erp_maturity = st.selectbox(
    "Today’s ERP / automation maturity",
    [
        "Low (email + spreadsheets heavy)",
        "Medium (ERP exists, lots of exceptions & manual handoffs)",
        "High (standardized ERP workflows + reporting, limited manual touchpoints)"
    ],
    index=1
)

operating_model = st.selectbox(
    "Operating model",
    [
        "Single business unit",
        "Shared Services / SSC",
        "Multi-country / multi-entity",
        "Highly regulated / audit-heavy"
    ],
    index=0
)

constraints = st.multiselect(
    "Constraints (choose what applies)",
    [
        "Strict approvals & segregation of duties (SoD)",
        "Weak data quality / master data issues",
        "Legacy ERP / many point solutions",
        "Supplier/customer variability",
        "Strong compliance / audit requirements",
        "Cyber / privacy restrictions",
        "Heavy exception volumes"
    ],
    default=[]
)

extra_notes = st.text_area(
    "Optional notes (1–2 lines)",
    placeholder="e.g., high invoice volume, complex pricing, unionized workforce, long procurement cycles…",
    height=80
)

generate = st.button("Generate workflows")

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
                temperature=0.12,
                max_tokens=750,
                response_format={"type": "json_object"},
            )
        except (RateLimitError, APITimeoutError, APIError) as e:
            last_err = e
            time.sleep(1.5 * (2 ** attempt))
    raise last_err

# -------------------------
# Workflow rendering
# -------------------------
ICON = {
    "HUMAN": "👤",
    "ERP": "🧾",
    "AI": "🤖",
    "AI+HUMAN": "🤖👤",
    "HUMAN+AI": "🤖👤",
    "AI+ERP": "🤖🧾",
    "ERP+AI": "🤖🧾",
    "ERP+HUMAN": "🧾👤",
    "HUMAN+ERP": "🧾👤",
}

def chip_class(actor: str) -> str:
    a = (actor or "").upper().replace(" ", "")
    if "+" in a:
        return "chip chip-mixed"
    if a == "AI":
        return "chip chip-ai"
    if a == "ERP":
        return "chip chip-erp"
    return "chip chip-human"

def normalize_actor(actor: str) -> str:
    a = (actor or "HUMAN").upper().replace(" ", "")
    # normalize common variants
    if a in ("HUMAN", "PERSON"):
        return "HUMAN"
    if a in ("ERP", "SYSTEM"):
        return "ERP"
    if a in ("AI", "LLM"):
        return "AI"
    # allow combos
    if a in ICON:
        return a
    # allow unordered combos like "AI+HUMAN"
    if "+" in a:
        parts = [p for p in a.split("+") if p]
        parts = [p if p in ("AI", "ERP", "HUMAN") else None for p in parts]
        parts = [p for p in parts if p]
        if len(parts) >= 2:
            # keep stable ordering
            order = {"AI": 0, "ERP": 1, "HUMAN": 2}
            parts_sorted = sorted(set(parts), key=lambda x: order.get(x, 99))
            return "+".join(parts_sorted)
    return "HUMAN"

def shorten_label(label: str) -> str:
    """Keep diagram labels short: ideally 1–2 words, max 3."""
    if not label:
        return "Step"
    words = label.strip().split()
    if len(words) <= 3:
        return " ".join(words)
    return " ".join(words[:3])

def render_vertical_flow(steps):
    """
    steps: list of {label: str, actor: 'HUMAN'|'ERP'|'AI'|'AI+HUMAN'|'AI+ERP' ...}
    """
    if not isinstance(steps, list) or len(steps) == 0:
        st.info("No workflow steps generated.")
        return

    blocks = []
    for i, s in enumerate(steps[:10]):
        label = shorten_label((s.get("label") or "").strip())
        actor = normalize_actor(s.get("actor") or "HUMAN")
        icon = ICON.get(actor, "👤")

        blocks.append(f"""
          <div class="step">
            <div class="step-row">
              <div class="step-label">{label}</div>
              <div class="{chip_class(actor)}">{icon} {actor}</div>
            </div>
          </div>
        """)
        if i != min(len(steps), 10) - 1:
            blocks.append('<div class="arrow-down">↓</div>')

    st.markdown(f'<div class="flow-vertical">{"".join(blocks)}</div>', unsafe_allow_html=True)

# -------------------------
# Prompt (workflow lens, not rigid linear AI)
# -------------------------
PROMPT_TEMPLATE = f"""
You are an evidence-minded operating model + process analyst.

Return ONLY a single valid JSON object (no markdown, no extra text).

We are generating an INDICATIVE WORKFLOW LENS (not a perfect process map).
- Labels must be short: 1–2 words (max 3).
- Today workflow should include only: HUMAN or ERP (no AI).
- {YEAR} workflow may include: HUMAN, ERP, AI, AI+HUMAN, AI+ERP.
- Not every step must be “AI”—AI can be embedded as assist/augment in some steps.

Diagrams should be realistic and conservative:
- Prefer assist/augment over replace.
- Include at least one control point where it makes sense (e.g., Approval, Exception, Audit).
- Keep it generic (no company names, no vendor names).

JSON schema (exact keys):
domain (string)
workflow (string)
focus_area (string)
today_steps (array of 7–9 objects: label (string), actor (one of: "HUMAN","ERP"))
future_steps (array of 7–9 objects: label (string), actor (one of: "HUMAN","ERP","AI","AI+HUMAN","AI+ERP"))
notes (array of 3 strings) -> short assumptions/constraints reflecting context

Selection:
Domain: {{domain}}
Workflow: {{workflow}}
Focus area: {{focus_area}}

Context:
Industry: {{industry}}
ERP maturity today: {{erp_maturity}}
Operating model: {{operating_model}}
Constraints: {{constraints}}
Extra notes: {{extra_notes}}

Year: {YEAR}
"""

# -------------------------
# Generate
# -------------------------
if generate:
    if "OPENAI_API_KEY" not in st.secrets or not str(st.secrets["OPENAI_API_KEY"]).strip():
        st.error("Missing OPENAI_API_KEY in Streamlit Secrets.")
        st.stop()

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    messages = [
        {"role": "system", "content": "Return ONLY one valid JSON object. No markdown. No commentary. No extra keys."},
        {
            "role": "user",
            "content": PROMPT_TEMPLATE.format(
                domain=domain,
                workflow=workflow,
                focus_area=focus_area,
                industry=industry,
                erp_maturity=erp_maturity,
                operating_model=operating_model,
                constraints=(", ".join(constraints) if constraints else "None"),
                extra_notes=(extra_notes.strip() if extra_notes else "None"),
            )
        }
    ]

    with st.spinner("Generating workflow lens…"):
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

    today_steps = data.get("today_steps") or []
    future_steps = data.get("future_steps") or []
    notes = data.get("notes") or []

    # basic validation
    if not isinstance(today_steps, list) or len(today_steps) < 6:
        st.error("Today workflow was incomplete. Try again (or adjust context).")
        st.code(raw)
        st.stop()
    if not isinstance(future_steps, list) or len(future_steps) < 6:
        st.error(f"{YEAR} workflow was incomplete. Try again (or adjust context).")
        st.code(raw)
        st.stop()

    st.subheader("Workflow lens (indicative)")

    # Side-by-side columns
    left, right = st.columns(2)

    with left:
        st.markdown(f"""
        <div class="card">
          <div class="badge-red">Today (typical)</div>
          <div class="small-muted">{domain} • {workflow}</div>
        </div>
        """, unsafe_allow_html=True)
        render_vertical_flow(today_steps)

    with right:
        st.markdown(f"""
        <div class="card">
          <div class="badge-green">{YEAR} (with AI embedded)</div>
          <div class="small-muted">{industry} • {erp_maturity.split(' ')[0]} maturity</div>
        </div>
        """, unsafe_allow_html=True)
        render_vertical_flow(future_steps)

    # Notes + legend
    st.markdown(f"""
    <div class="card">
      <div class="badge-black">Notes, constraints & legend</div>
      <ul>
        {''.join([f"<li>{n}</li>" for n in notes[:3]])}
      </ul>
      <div class="small-muted">
        <strong>Legend:</strong>
        👤 HUMAN &nbsp; 🧾 ERP &nbsp; 🤖 AI &nbsp; 🤖👤 AI+HUMAN &nbsp; 🤖🧾 AI+ERP
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.caption("Tip: Screenshot & share. Avoid sensitive internal process details.")
