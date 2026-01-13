# =========================
# AI Workflow Optimizer — Custom workflow input → AI-optimized workflow
# =========================

import json
import time
import streamlit as st
from openai import OpenAI
from openai import RateLimitError, APIError, APITimeoutError

from process_library import DOMAINS, TOOL_LIBRARY, get_default_steps


# -------------------------
# Page config
# -------------------------
st.set_page_config(
    page_title="AI Workflow Optimizer",
    page_icon="🧭",
    layout="centered"
)

# -------------------------
# Styles (mobile-safe + dark-mode-safe)
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
.badge-blue { background:#1d4ed8; color:#fff; padding:6px 10px; border-radius:10px; font-weight:800; display:inline-block; margin-bottom:10px; }

.small-muted { color: rgba(0,0,0,0.65); font-size: 0.92rem; }

.flow-vertical { display:flex; flex-direction:column; gap:10px; }
.step {
  border: 1px solid rgba(0,0,0,0.14);
  border-radius: 12px;
  padding: 10px 12px;
  background: rgba(255,255,255,0.98);
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
.step-label {
  font-size: 0.98rem;
  line-height: 1.2;
  max-width: 60%;
  word-break: break-word;
  overflow-wrap: anywhere;
}

.idpill {
  display:inline-block;
  font-size:0.72rem;
  padding:3px 7px;
  border-radius:999px;
  border:1px solid rgba(0,0,0,0.10);
  background: rgba(0,0,0,0.03);
  font-weight:900;
  margin-right:6px;
}

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

.mapping-row {
  display:flex;
  gap:10px;
  align-items:flex-start;
  padding:10px 12px;
  border-radius:12px;
  border:1px dashed rgba(0,0,0,0.18);
  margin-bottom:10px;
}
.mapping-left, .mapping-right { flex: 1; }
.mapping-title { font-weight:900; margin-bottom:4px; }

@media (prefers-color-scheme: dark) {
  .card { background: rgba(255,255,255,0.06); border-color: rgba(255,255,255,0.14); color: rgba(255,255,255,0.92); }
  .small-muted { color: rgba(255,255,255,0.72); }
  .step { background: rgba(17,24,39,0.65); border-color: rgba(255,255,255,0.18); color: rgba(255,255,255,0.92); }
  .tag, .idpill { color: rgba(255,255,255,0.78); background: rgba(255,255,255,0.06); border-color: rgba(255,255,255,0.14); }
  .arrow-down { color: rgba(255,255,255,0.35); }
  .chip { border-color: rgba(255,255,255,0.18); }
  .mapping-row { border-color: rgba(255,255,255,0.18); }
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# Header + description
# -------------------------
st.title("🧭 AI Workflow Optimizer")
st.write('A light-touch working demo built by "Prabodh & his AI Assistant".')
st.write(
    "Enter your current workflow and explore opportunities to optimize it using existing AI and automation tools. "
    "Please avoid entering any sensitive data. Outputs are indicative and high-level, and not a substitute for professional advice."
)
st.caption("Tip: Start with 6–12 steps. Keep labels short. You’ll get an indicative ‘before vs optimized’ view + a mapping between them.")

# -------------------------
# Session state (prevents blank page after reruns)
# -------------------------
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "last_error" not in st.session_state:
    st.session_state.last_error = None
if "last_raw" not in st.session_state:
    st.session_state.last_raw = None


# -------------------------
# Helpers
# -------------------------
def clean_lines(text: str) -> list[str]:
    lines = []
    for raw in (text or "").splitlines():
        s = raw.strip()
        if not s:
            continue
        s = s.replace("•", "-").strip()
        if len(s) > 140:
            s = s[:140]
        lines.append(s)
    return lines[:18]

def extract_json_object(text: str) -> str | None:
    """Extract the first complete top-level JSON object from a string."""
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

def parse_json_safely(raw: str) -> dict:
    raw = (raw or "").strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        extracted = extract_json_object(raw)
        if extracted:
            return json.loads(extracted)
        raise

def call_openai_with_retry(client: OpenAI, messages, max_retries: int = 3, max_tokens: int = 2000):
    last_err = None
    for attempt in range(max_retries):
        try:
            return client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=messages,
                temperature=0.10,
                max_tokens=max_tokens,
                response_format={"type": "json_object"},
            )
        except (RateLimitError, APITimeoutError, APIError) as e:
            last_err = e
            time.sleep(1.2 * (2 ** attempt))
    raise last_err

def try_repair_json(client: OpenAI, raw_partial: str) -> str:
    """If model output gets truncated, ask it to output the complete valid JSON object."""
    repair_prompt = f"""
You returned an incomplete/truncated JSON object. Return ONLY one complete valid JSON object.

Rules:
- Output must be a single JSON object (no markdown, no extra commentary).
- Preserve the same schema and keys.
- Complete any open arrays/objects and missing fields.
- Ensure JSON is valid.

PARTIAL_JSON_START:
{raw_partial}
PARTIAL_JSON_END
""".strip()

    messages = [
        {"role": "system", "content": "Return ONLY one valid JSON object. No markdown."},
        {"role": "user", "content": repair_prompt},
    ]
    resp = call_openai_with_retry(client, messages, max_retries=2, max_tokens=1800)
    return resp.choices[0].message.content or ""


ICON = {
    "HUMAN": "👤",
    "ERP": "🧾",
    "AI": "🤖",
    "AI+HUMAN": "🤖👤",
    "AI+ERP": "🤖🧾",
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
            return a2 if a2 in ICON else "AI+ERP+HUMAN"
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

def render_vertical_flow(steps, highlight_future: bool = False):
    if not isinstance(steps, list) or len(steps) == 0:
        st.info("No steps to display.")
        return

    blocks = []
    capped = steps[:12]
    for i, s in enumerate(capped):
        sid = (s.get("id") or "").strip()
        label = shorten_label((s.get("label") or "").strip())
        actor = normalize_actor(s.get("actor") or "HUMAN")
        intent = (s.get("intent") or "").strip()
        icon = ICON.get(actor, "👤")

        ai_step = ("AI" in actor)
        human_upshift = (intent in ("Decision", "Relationship"))

        step_classes = ["step"]
        if highlight_future and ai_step:
            step_classes.append("ai-highlight")
        if highlight_future and human_upshift:
            step_classes.append("human-upshift")

        id_html = f'<span class="idpill">{sid}</span>' if sid else ""
        tag_html = f'<span class="tag">{intent}</span>' if intent else ""

        blocks.append(f"""
          <div class="{' '.join(step_classes)}">
            <div class="step-row">
              <div class="step-label">{id_html}{tag_html}{label}</div>
              <div class="{chip_class(actor)}">{icon} {actor}</div>
            </div>
          </div>
        """)
        if i != len(capped) - 1:
            blocks.append('<div class="arrow-down">↓</div>')

    st.markdown(f'<div class="flow-vertical">{"".join(blocks)}</div>', unsafe_allow_html=True)


def safe_list(x):
    return x if isinstance(x, list) else []

def safe_str(x, fallback=""):
    return x if isinstance(x, str) and x.strip() else fallback


# -------------------------
# UI controls (renamed)
# -------------------------
functional_domain = st.selectbox("Functional Domain", list(DOMAINS.keys()))
process_workflows = list(DOMAINS[functional_domain].keys())
process_workflow = st.selectbox("Process Workflow", process_workflows)

sub_processes_dict = DOMAINS[functional_domain][process_workflow].get("sub_processes", {}) or {}
sub_process_options = list(sub_processes_dict.keys()) if isinstance(sub_processes_dict, dict) else []

sub_process = st.selectbox(
    "Sub Process (please select from the drop down)",
    sub_process_options if sub_process_options else ["(No sub-processes configured)"],
    disabled=(len(sub_process_options) == 0)
)

time_horizon = st.selectbox(
    "Optimization time horizon",
    [
        "Next 6–12 months (practical quick wins)",
        "1–2 years (scaled adoption)",
        "3–5 years (operating model shift)"
    ],
    index=0
)

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

maturity = st.selectbox(
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

workflow_goal = DOMAINS[functional_domain][process_workflow].get("goal", "")
sub_process_goal = ""
if isinstance(sub_processes_dict, dict) and sub_process in sub_processes_dict:
    sub_process_goal = sub_processes_dict[sub_process].get("goal", "")

prefill_steps = get_default_steps(functional_domain, process_workflow, sub_process)
prefill_text = "\n".join(prefill_steps) if prefill_steps else ""

st.markdown("### Your current workflow (editable)")
current_workflow_text = st.text_area(
    "Enter one step per line (you can edit the template below).",
    value=prefill_text,
    height=220,
)

extra_notes = st.text_area("Optional notes (1–2 lines)", height=70)

generate = st.button("Generate optimized workflow")


# -------------------------
# Generate (robust) → store in session_state
# -------------------------
if generate:
    st.session_state.last_error = None
    st.session_state.last_raw = None

    steps = clean_lines(current_workflow_text)
    if len(steps) < 4:
        st.warning("Please enter at least 4 workflow steps (one per line).")
        st.stop()

    if "OPENAI_API_KEY" not in st.secrets or not str(st.secrets["OPENAI_API_KEY"]).strip():
        st.error("Missing OPENAI_API_KEY in Streamlit Secrets.")
        st.stop()

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    tool_lib_json = json.dumps(TOOL_LIBRARY, ensure_ascii=False)

    prompt = f"""
Return ONLY one valid JSON object (no markdown, no extra text).

You are an evidence-minded operating model + process analyst.
Transform the user's CURRENT workflow into an optimized workflow for the selected time horizon.

Rules:
- Use the user's input steps as baseline.
- You may reorder, merge, rename, or add up to 2 missing control steps.
- Keep step labels short: 1–2 words (max 3).
- Include at least one explicit Control checkpoint.
- Prefer "assist/augment" over "replace".

Actors:
- today_steps actor: HUMAN or ERP only
- future_steps actor: HUMAN, ERP, AI, AI+HUMAN, AI+ERP, AI+ERP+HUMAN

Intent: Admin / Control / Decision / Relationship
- Today should skew more Admin.
- Future should increase Decision + Relationship for HUMAN-owned steps.

Mapping requirement:
- Every future step MUST include maps_to: array of TODAY step ids it replaces/absorbs.

Tools:
Use ONLY the provided TOOL_LIBRARY. Do NOT invent tools.
Return exactly 4 tool suggestions.

Terminology:
Provide a glossary of 6 terms used.

TOOL_LIBRARY (JSON):
{tool_lib_json}

JSON schema (exact keys):
functional_domain (string)
process_workflow (string)
sub_process (string)
time_horizon (string)
today_steps (array of 6–12 objects):
  id ("T1".."T12"), label, actor ("HUMAN"|"ERP"), intent
future_steps (array of 6–12 objects):
  id ("F1".."F12"), label, actor, intent, maps_to (array of today ids)
human_shift (array of 3 strings)
deltas (array of 4 strings)
glossary (array of 6 objects: term, definition)
tool_suggestions (array of 4 objects: tool_category, example_tools (1–3), use_in_workflow, fit_notes)
notes (array of 3 strings)

Context:
Functional Domain: {functional_domain}
Process Workflow: {process_workflow}
Sub Process: {sub_process}
Time horizon: {time_horizon}
Workflow goal: {workflow_goal}
Sub-process goal: {sub_process_goal if sub_process_goal else "None"}
Industry: {industry}
Today maturity: {maturity}
Constraints: {", ".join(constraints) if constraints else "None"}
User notes: {(extra_notes.strip() if extra_notes else "None")}

User CURRENT workflow steps (one per line):
{chr(10).join(steps)}
""".strip()

    messages = [
        {"role": "system", "content": "Return ONLY one valid JSON object. No markdown. No extra keys."},
        {"role": "user", "content": prompt}
    ]

    with st.spinner("Generating optimized workflow…"):
        try:
            resp = call_openai_with_retry(client, messages, max_retries=3, max_tokens=2000)
            raw = resp.choices[0].message.content or ""
            st.session_state.last_raw = raw

            # First parse attempt
            try:
                data = parse_json_safely(raw)
            except Exception:
                # If truncated, try repair once
                repaired = try_repair_json(client, raw)
                st.session_state.last_raw = repaired
                data = parse_json_safely(repaired)

            st.session_state.last_result = data

        except RateLimitError:
            st.session_state.last_error = "Rate limit/quota hit. Try again (or check billing/usage)."
        except Exception as e:
            st.session_state.last_error = f"Unexpected error: {e}"


# -------------------------
# Render last result (persists across reruns) — prevents blank page
# -------------------------
if st.session_state.last_error:
    st.error(st.session_state.last_error)

if st.session_state.last_raw:
    with st.expander("Debug: last raw model output"):
        st.code(st.session_state.last_raw)

data = st.session_state.last_result

if isinstance(data, dict):
    # Normalize fields defensively
    functional_domain_out = safe_str(data.get("functional_domain"), functional_domain)
    process_workflow_out = safe_str(data.get("process_workflow"), process_workflow)
    sub_process_out = safe_str(data.get("sub_process"), sub_process)
    time_horizon_out = safe_str(data.get("time_horizon"), time_horizon)

    today_steps = safe_list(data.get("today_steps"))
    future_steps = safe_list(data.get("future_steps"))
    human_shift = safe_list(data.get("human_shift"))
    deltas = safe_list(data.get("deltas"))
    glossary = safe_list(data.get("glossary"))
    tool_suggestions = safe_list(data.get("tool_suggestions"))
    notes = safe_list(data.get("notes"))

    st.markdown("## Workflow view (indicative)")

    st.markdown(f"""
    <div class="card">
      <div class="small-muted"><strong>Functional Domain:</strong> {functional_domain_out} •
      <strong>Process Workflow:</strong> {process_workflow_out} •
      <strong>Sub Process:</strong> {sub_process_out} •
      <strong>Horizon:</strong> {time_horizon_out}</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(f"""
        <div class="card">
          <div class="badge-red">Today (typical)</div>
          <div class="small-muted">Human + ERP handoffs, more admin + exception work.</div>
        </div>
        """, unsafe_allow_html=True)
        render_vertical_flow(today_steps, highlight_future=False)

    with c2:
        st.markdown(f"""
        <div class="card">
          <div class="badge-green">Optimized (AI-augmented)</div>
          <div class="small-muted">Fewer handoffs, more touchless processing, humans shifted to higher-value steps.</div>
        </div>
        """, unsafe_allow_html=True)
        render_vertical_flow(future_steps, highlight_future=True)

    # Mapping section
    st.markdown("### Step mapping (future → today)")
    if isinstance(future_steps, list) and len(future_steps) > 0:
        for fs in future_steps[:12]:
            fid = fs.get("id", "")
            flabel = fs.get("label", "")
            fmaps = fs.get("maps_to", [])
            if not isinstance(fmaps, list):
                fmaps = []
            left = f"<div class='mapping-title'>Future: {fid} — {flabel}</div>"
            right_ids = ", ".join(fmaps) if fmaps else "(no mapping provided)"
            right = f"<div class='mapping-title'>Replaces/absorbs: {right_ids}</div>"

            st.markdown(f"""
            <div class="mapping-row">
              <div class="mapping-left">{left}</div>
              <div class="mapping-right">{right}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No mapping available.")

    # Deltas + human shift
    d1, d2 = st.columns(2)
    with d1:
        st.markdown("<div class='card'><div class='badge-black'>Key deltas</div></div>", unsafe_allow_html=True)
        if deltas:
            st.write("\n".join([f"• {x}" for x in deltas[:6]]))
        else:
            st.write("• (No deltas provided)")

    with d2:
        st.markdown("<div class='card'><div class='badge-purple'>Human shift</div></div>", unsafe_allow_html=True)
        if human_shift:
            st.write("\n".join([f"• {x}" for x in human_shift[:6]]))
        else:
            st.write("• (No human shift provided)")

    # Tools
    st.markdown("### Tool suggestions (examples)")
    if tool_suggestions:
        for t in tool_suggestions[:4]:
            cat = safe_str(t.get("tool_category"), "Tool category")
            ex_tools = t.get("example_tools", [])
            if not isinstance(ex_tools, list):
                ex_tools = []
            use = safe_str(t.get("use_in_workflow"), "")
            fit = safe_str(t.get("fit_notes"), "")
            st.markdown(f"""
            <div class="card">
              <div class="badge-blue">{cat}</div>
              <div><strong>Example tools:</strong> {", ".join(ex_tools[:3]) if ex_tools else "—"}</div>
              <div><strong>Use:</strong> {use}</div>
              <div class="small-muted"><strong>Notes:</strong> {fit}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No tool suggestions available.")

    # Glossary
    st.markdown("### Glossary (terminology)")
    if glossary:
        for g in glossary[:8]:
            term = safe_str(g.get("term"), "")
            definition = safe_str(g.get("definition"), "")
            if term and definition:
                st.markdown(f"**{term}:** {definition}")
    else:
        st.write("—")

    # Notes
    if notes:
        st.markdown("### Notes")
        st.write("\n".join([f"• {x}" for x in notes[:6]]))

    st.caption("Tip: Don’t enter sensitive info. This is a demo/prototype for exploration, not professional advice.")
# ---- DEBUG (REMOVE FOR PROD) ----
# with st.expander("Debug"):
#     st.write("Last raw model output")
#     st.code(st.session_state.get("last_raw", ""))
