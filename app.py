# =========================
# 2026 Workflow Shift Lens (Vertical + Side-by-side + Visible Shift)
# =========================

YEAR = 2026

import json
import time
import streamlit as st
from openai import OpenAI
from openai import RateLimitError, APIError, APITimeoutError

from process_library import DOMAINS

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
.card {
  border: 1px solid rgba(0,0,0,0.12);
  border-radius: 14px;
  padding: 16px;
  background: #fff;
  box-shadow: 0 2px 10px rgba(0,0,0,0.06);
  margin-bottom: 14px;
  color: rgba(0,0,0,0.90);
}
.badge-red { background:#b91c1c; color:#fff; padding:6px 10px; border-radius:10px; font-weight:800; display:inline-block; margin-bottom:10px; }
.badge-green { background:#15803d; color:#fff; padding:6px 10px; border-radius:10px; font-weight:800; display:inline-block; margin-bottom:10px; }
.badge-black { background:#111827; color:#fff; padding:6px 10px; border-radius:10px; font-weight:800; display:inline-block; margin-bottom:10px; }
.badge-purple { background:#7c3aed; color:#fff; padding:6px 10px; border-radius:10px; font-weight:800; display:inline-block; margin-bottom:10px; }

.small-muted { color: rgba(0,0,0,0.65); font-size: 0.92rem; }

.flow-vertical { display:flex; flex-direction:column; gap:10px; }

.step {
  border: 1px solid rgba(0,0,0,0.14);
  border-radius: 12px;
  padding: 10px 12px;
  background: rgba(255,255,255,0.95);
  box-shadow: 0 1px 6px rgba(0,0,0,0.05);
  font-weight: 800;
}
.step.ai-highlight {
  border-color: rgba(22,163,74,0.55);
  box-shadow: 0 0 0 3px rgba(22,163,74,0.18), 0 1px 8px rgba(0,0,0,0.06);
}
.step.human-upshift {
  border-color: rgba(124,58,237,0.55);
  box-shadow: 0 0 0 3px rgba(124,58,237,0.16), 0 1px 8px rgba(0,0,0,0.06);
}

.step-row { display:flex; align-items:center; justify-content:space-between; gap:10px; }

.step-label { font-size: 0.98rem; line-height:1.2; max-width: 62%; word-wrap: break-word; }

.chip {
  display:inline-block; font-size:0.80rem; padding:4px 8px; border-radius:999px;
  border:1px solid rgba(0,0,0,0.12); font-weight:900; white-space:nowrap;
}
.chip-human { background: rgba(37,99,235,0.10); }
.chip-erp   { background: rgba(2,132,199,0.10); }
.chip-ai    { background: rgba(22,163,74,0.12); }
.chip-mixed { background: rgba(124,58,237,0.12); }

.tag {
  display:inline-block; font-size:0.72rem; padding:3px 7px; border-radius:999px;
  border:1px solid rgba(0,0,0,0.10); color: rgba(0,0,0,0.70);
  background: rgba(0,0,0,0.03); font-weight:800; margin-right:6px;
}

.arrow-down { text-align:center; font-size:18px; font-weight:900; color: rgba(0,0,0,0.35); line-height:1; }

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .card { background: rgba(255,255,255,0.06); border-color: rgba(255,255,255,0.14); color: rgba(255,255,255,0.92); }
  .small-muted { color: rgba(255,255,255,0.72); }
  .step { background: rgba(17,24,39,0.65); border-color: rgba(255,255,255,0.18); color: rgba(255,255,255,0.92); }
  .tag { color: rgba(255,255,255,0.75); background: rgba(255,255,255,0.06); border-color: rgba(255,255,255,0.14); }
  .arrow-down { color: rgba(255,255,255,0.35); }
  .chip { border-color: rgba(255,255,255,0.18); }
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# Header
# -------------------------
st.title(f"🧭 {YEAR} Workflow Shift Lens")
st.write("An indicative “before vs after” view of how workflows may evolve as AI gets embedded into systems and teams.")
st.caption("Built to visualize step-by-step change. No data is stored. Not professional advice.")

# -------------------------
# Inputs
# -------------------------
domain = st.selectbox("Domain", list(DOMAINS.keys()))
workflow = st.selectbox("Workflow", list(DOMAINS[domain].keys()))

focus_areas = DOMAINS[domain][workflow]["focus_areas"]
workflow_goal = DOMAINS[domain][workflow].get("goal", "")

focus_area = st.selectbox("Focus area (optional)", focus_areas)

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
    "Today’s automation maturity",
    [
        "Low (email + spreadsheets heavy)",
        "Medium (ERP exists, many manual handoffs/exceptions)",
        "High (standardized workflows + reporting, limited manual touchpoints)"
    ],
    index=1
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
    placeholder="What’s unique here? (volume, complexity, regulation, service levels, etc.)",
    height=70
)

generate = st.button("Generate workflows")

# -------------------------
# Helpers
# -------------------------
def extract_json_object(text: str) -> str | None:
    if not text:
        return None
    start = text.find("{")
    if start == -1:
        return None
    depth, in_str, escape = 0, False, False
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

def call_openai_with_retry(client: OpenAI, messages, max_retries: int = 3):
    last_err = None
    for attempt in range(max_retries):
        try:
            return client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=messages,
                temperature=0.12,
                max_tokens=900,
                response_format={"type": "json_object"},
            )
        except (RateLimitError, APITimeoutError, APIError) as e:
            last_err = e
            time.sleep(1.5 * (2 ** attempt))
    raise last_err

ICON = {
    "HUMAN": "👤",
    "ERP": "🧾",
    "AI": "🤖",
    "AI+HUMAN": "🤖👤",
    "AI+ERP": "🤖🧾",
    "ERP+HUMAN": "🧾👤",
    "AI+ERP+HUMAN": "🤖🧾👤"
}

def normalize_actor(actor: str) -> str:
    a = (actor or "HUMAN").upper().replace(" ", "")
    if a in ("HUMAN", "PERSON"):
        return "HUMAN"
    if a in ("ERP", "SYSTEM"):
        return "ERP"
    if a in ("AI", "LLM"):
        return "AI"
    if "+" in a:
        parts = [p for p in a.split("+") if p]
        allowed = [p for p in parts if p in ("AI", "ERP", "HUMAN")]
        if len(allowed) >= 2:
            order = {"AI": 0, "ERP": 1, "HUMAN": 2}
            allowed = sorted(set(allowed), key=lambda x: order.get(x, 99))
            a2 = "+".join(allowed)
            if a2 == "AI+ERP+HUMAN":
                return a2
            return a2
    return "HUMAN"

def chip_class(actor: str) -> str:
    a = (actor or "").upper().replace(" ", "")
    if "+" in a:
        return "chip chip-mixed"
    if a == "AI":
        return "chip chip-ai"
    if a == "ERP":
        return "chip chip-erp"
    return "chip chip-human"

def shorten_label(label: str) -> str:
    if not label:
        return "Step"
    words = label.strip().split()
    return " ".join(words[:3]) if len(words) > 3 else " ".join(words)

def render_vertical_flow(steps, highlight_ai: bool = False):
    if not isinstance(steps, list) or len(steps) == 0:
        st.info("No workflow steps generated.")
        return

    blocks = []
    for i, s in enumerate(steps[:10]):
        label = shorten_label((s.get("label") or "").strip())
        actor = normalize_actor(s.get("actor") or "HUMAN")
        intent = (s.get("intent") or "").strip()  # Admin / Control / Decision / Relationship
        icon = ICON.get(actor, "👤")

        ai_step = ("AI" in actor)  # AI or AI+...
        human_upshift = (intent in ("Decision", "Relationship", "Judgment", "Strategy"))

        step_classes = ["step"]
        if highlight_ai and ai_step:
            step_classes.append("ai-highlight")
        if highlight_ai and human_upshift:
            step_classes.append("human-upshift")

        tag_html = f'<span class="tag">{intent}</span>' if intent else ""

        blocks.append(f"""
          <div class="{' '.join(step_classes)}">
            <div class="step-row">
              <div class="step-label">{tag_html}{label}</div>
              <div class="{chip_class(actor)}">{icon} {actor}</div>
            </div>
          </div>
        """)
        if i != min(len(steps), 10) - 1:
            blocks.append('<div class="arrow-down">↓</div>')

    st.markdown(f'<div class="flow-vertical">{"".join(blocks)}</div>', unsafe_allow_html=True)

# -------------------------
# Prompt: FORCE visible difference + intent tagging
# -------------------------
PROMPT_TEMPLATE = f"""
You are an evidence-minded operating model + process analyst.

Return ONLY a single valid JSON object (no markdown, no extra text).

This is a WORKFLOW LENS (indicative), designed to VISUALLY show efficiency shift.
Make TODAY vs {YEAR} meaningfully different:
- TODAY: more handoffs, more manual checks, more admin.
- {YEAR}: fewer handoffs, more "touchless for clean cases", more automation embedded in ERP, more AI-assisted triage, and humans moved to review/validation/relationship/strategic decisions.

Labels must be short: 1–2 words (max 3).
Include at least one control point (Approval/Exception/Audit) where appropriate.

Actors allowed:
- today_steps actor: "HUMAN" or "ERP" only
- future_steps actor: "HUMAN", "ERP", "AI", "AI+HUMAN", "AI+ERP", "AI+ERP+HUMAN"

Add intent for each step to make the shift explicit:
intent must be ONE of: "Admin", "Control", "Decision", "Relationship"
- TODAY should contain more "Admin"
- {YEAR} should contain more "Decision" and "Relationship" for HUMAN-owned steps

JSON schema (exact keys):
domain (string)
workflow (string)
focus_area (string)
today_steps (array of 7–9 objects: label (string), actor, intent)
future_steps (array of 7–9 objects: label (string), actor, intent)
human_shift (array of 3 strings) -> "Humans move from X to Y" style, concrete
deltas (array of 4 strings) -> concrete differences that explain efficiency
notes (array of 3 strings) -> constraints/controls reflecting context

Selection:
Domain: {{domain}}
Workflow: {{workflow}}
Focus area: {{focus_area}}
Workflow goal: {{workflow_goal}}

Context:
Industry: {{industry}}
Today maturity: {{erp_maturity}}
Constraints: {{constraints}}
Notes: {{extra_notes}}

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
                workflow_goal=workflow_goal,
                industry=industry,
                erp_maturity=erp_maturity,
                constraints=(", ".join(constraints) if constraints else "None"),
                extra_notes=(extra_notes.strip() if extra_notes else "None"),
            )
        }
    ]

    with st.spinner("Generating workflow lens…"):
        try:
            resp = call_openai_with_retry(client, messages)
        except RateLimitError:
            st.error("Rate limit/quota hit. Try again (or check billing/usage).")
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
    deltas = data.get("deltas") or []
    human_shift = data.get("human_shift") or []
    notes = data.get("notes") or []

    if not isinstance(today_steps, list) or len(today_steps) < 6:
        st.error("Today workflow incomplete. Try again (or refine context).")
        st.code(raw)
        st.stop()
    if not isinstance(future_steps, list) or len(future_steps) < 6:
        st.error(f"{YEAR} workflow incomplete. Try again (or refine context).")
        st.code(raw)
        st.stop()

    st.subheader("Workflow lens (indicative)")

    # Deltas + shift summary FIRST (so readers see the “why”)
    st.markdown(f"""
    <div class="card">
      <div class="badge-purple">What changes (in plain terms)</div>
      <ul>
        {''.join([f"<li>{d}</li>" for d in deltas[:4]])}
      </ul>
      <div style="margin-top:10px;">
        <strong>Human shift:</strong>
        <ul>
          {''.join([f"<li>{h}</li>" for h in human_shift[:3]])}
        </ul>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Side-by-side workflows with SAME titles
    left, right = st.columns(2)

    with left:
        st.markdown(f"""
        <div class="card">
          <div class="badge-red">Workflow today</div>
          <div class="small-muted">{domain} • {workflow}</div>
        </div>
        """, unsafe_allow_html=True)
        render_vertical_flow(today_steps, highlight_ai=False)

    with right:
        st.markdown(f"""
        <div class="card">
          <div class="badge-green">Workflow in {YEAR}</div>
          <div class="small-muted">{domain} • {workflow}</div>
        </div>
        """, unsafe_allow_html=True)
        render_vertical_flow(future_steps, highlight_ai=True)

    # Notes + legend
    st.markdown(f"""
    <div class="card">
      <div class="badge-black">Controls, constraints & legend</div>
      <ul>
        {''.join([f"<li>{n}</li>" for n in notes[:3]])}
      </ul>
      <div class="small-muted">
        <strong>Legend:</strong>
        👤 HUMAN &nbsp; 🧾 ERP &nbsp; 🤖 AI &nbsp; 🤖👤 AI+HUMAN &nbsp; 🤖🧾 AI+ERP &nbsp; 🤖🧾👤 AI+ERP+HUMAN<br/>
        <strong>Intent tags:</strong> Admin / Control / Decision / Relationship
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.caption("Tip: Screenshot & share. Avoid sensitive internal process details.")
