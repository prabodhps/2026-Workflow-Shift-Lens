# =========================
# 2026 Workflow Shift Lens — Custom workflow input → AI-optimized workflow
# Fixes: truncated JSON / "non-JSON" errors by auto-repairing partial outputs
# =========================

YEAR = 2026

import json
import time
import csv
import os
from datetime import datetime, timezone

import streamlit as st
from openai import OpenAI
from openai import RateLimitError, APIError, APITimeoutError

from process_library import DOMAINS, TOOL_LIBRARY, get_default_steps

# Optional (persistent logging via webhook). If requests isn't installed, app still works.
try:
    import requests
except Exception:
    requests = None


# -------------------------
# Page config
# -------------------------
st.set_page_config(
    page_title=f"{YEAR} Workflow Shift Lens",
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
.kv { margin: 6px 0; }

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
# Header
# -------------------------
st.title(f"🧭 {YEAR} Workflow Shift Lens — Custom")
st.write("Pick a functional area, paste your *current* workflow steps, and generate an optimized 2026 workflow with AI embedded.")
st.caption("Please avoid sensitive data. This is an indicative workflow lens, not implementation advice.")


# -------------------------
# Inputs
# -------------------------
domain = st.selectbox("Functional area", list(DOMAINS.keys()))
workflow = st.selectbox("Workflow template", list(DOMAINS[domain].keys()))

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

workflow_goal = DOMAINS[domain][workflow].get("goal", "")

prefill = "\n".join(get_default_steps(domain, workflow)) or ""
st.markdown("### Your current workflow (editable)")
current_workflow_text = st.text_area(
    "Enter one step per line (you can edit the template below).",
    value=prefill,
    height=220,
)

extra_notes = st.text_area("Optional notes (1–2 lines)", height=70)

generate = st.button("Generate optimized workflow")


# -------------------------
# Helpers
# -------------------------
def clean_lines(text: str) -> list[str]:
    lines = []
    for raw in (text or "").splitlines():
        s = raw.strip()
        if not s:
            continue
        if len(s) > 140:
            s = s[:140]
        lines.append(s)
    return lines[:18]  # allow a bit more

def extract_json_object(text: str) -> str | None:
    """Extract first complete JSON object { ... } even if the model adds extra text around it."""
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
    raw = (raw or "").strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        extracted = extract_json_object(raw)
        if extracted:
            return json.loads(extracted)
        raise

def call_openai_with_retry(client: OpenAI, messages, max_retries: int = 3, max_tokens: int = 2200):
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
            time.sleep(1.5 * (2 ** attempt))
    raise last_err

def try_repair_json(client: OpenAI, raw_partial: str, max_tokens: int = 1600) -> str:
    """
    If model returned truncated JSON, ask it to continue and return ONLY the completed JSON.
    We pass the partial content and ask for a valid final object.
    """
    repair_prompt = f"""
You returned an incomplete/truncated JSON object. Continue from where it cut off and return ONLY one complete valid JSON object.
Rules:
- Output must be a single JSON object (no markdown, no extra commentary).
- Preserve the same schema and keys as the partial object.
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
    resp = call_openai_with_retry(client, messages, max_retries=2, max_tokens=max_tokens)
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
            if a2 in ICON:
                return a2
            if a2 == "AI+ERP+HUMAN":
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
        st.info("No steps to display.")
        return

    blocks = []
    for i, s in enumerate(steps[:12]):
        sid = (s.get("id") or "").strip()
        label = shorten_label((s.get("label") or "").strip())
        actor = normalize_actor(s.get("actor") or "HUMAN")
        intent = (s.get("intent") or "").strip()
        icon = ICON.get(actor, "👤")

        ai_step = ("AI" in actor)
        human_upshift = (intent in ("Decision", "Relationship"))

        step_classes = ["step"]
        if highlight_ai and ai_step:
            step_classes.append("ai-highlight")
        if highlight_ai and human_upshift:
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
        if i != min(len(steps), 12) - 1:
            blocks.append('<div class="arrow-down">↓</div>')

    st.markdown(f'<div class="flow-vertical">{"".join(blocks)}</div>', unsafe_allow_html=True)


# -------------------------
# Generate
# -------------------------
if generate:
    steps = clean_lines(current_workflow_text)
    if len(steps) < 4:
        st.warning("Please enter at least 4 workflow steps (one per line).")
        st.stop()

    if "OPENAI_API_KEY" not in st.secrets or not str(st.secrets["OPENAI_API_KEY"]).strip():
        st.error("Missing OPENAI_API_KEY in Streamlit Secrets.")
        st.stop()

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    tool_lib_json = json.dumps(TOOL_LIBRARY, ensure_ascii=False, indent=2)

    # Build prompt WITHOUT .format (prevents KeyError issues)
    prompt = f"""
You are an evidence-minded operating model + process analyst.

Return ONLY one valid JSON object (no markdown, no extra text).

Goal:
Transform the user's CURRENT workflow into an optimized workflow for {YEAR},
showing (a) fewer handoffs, (b) more touchless processing for clean cases,
(c) clear controls, and (d) humans moved to higher-value work.

Important:
- Use the user's input steps as the baseline.
- You may reorder, merge, rename, or add up to 2 missing control steps.
- Keep step labels short: 1–2 words (max 3).
- Include at least one control checkpoint.

Actors:
- today_steps actor: HUMAN or ERP only
- future_steps actor: HUMAN, ERP, AI, AI+HUMAN, AI+ERP, AI+ERP+HUMAN

Intent (each step): Admin / Control / Decision / Relationship
- Today should skew more Admin.
- Future should increase Decision + Relationship for HUMAN-owned steps.

Mapping requirement:
- Every future step MUST include maps_to: array of TODAY step ids it replaces/absorbs (e.g., ["T2","T3"]).

Tools:
Use ONLY the provided TOOL_LIBRARY. Do NOT invent tools.
Return exactly 4 tool suggestions (to reduce output size and truncation risk).

Terminology:
Provide a glossary of 6 terms used in the workflow lens.

TOOL_LIBRARY (JSON):
{tool_lib_json}

JSON schema (exact keys):
domain (string)
workflow (string)
today_steps (array of 6–12 objects):
  id ("T1".."T12"), label, actor ("HUMAN"|"ERP"), intent
future_steps (array of 6–12 objects):
  id ("F1".."F12"), label, actor, intent, maps_to (array of today ids)
human_shift (array of 3 strings)
deltas (array of 4 strings)
glossary (array of 6 objects: term, definition)
tool_suggestions (array of 4 objects: tool_category, example_tools (1–3 from library), use_in_workflow, fit_notes)
notes (array of 3 strings)

Context:
Domain: {domain}
Workflow template name: {workflow}
Workflow goal: {workflow_goal}
Industry: {industry}
Today automation maturity: {maturity}
Constraints: {", ".join(constraints) if constraints else "None"}
User notes: {(extra_notes.strip() if extra_notes else "None")}

User CURRENT workflow steps (one per line):
{chr(10).join(steps)}

Year: {YEAR}
""".strip()

    messages = [
        {"role": "system", "content": "Return ONLY one valid JSON object. No markdown. No extra keys."},
        {"role": "user", "content": prompt}
    ]

    with st.spinner("Generating optimized workflow…"):
        try:
            resp = call_openai_with_retry(client, messages, max_retries=3, max_tokens=2200)
        except RateLimitError:
            st.error("Rate limit/quota hit. Try again (or check billing/usage).")
            st.stop()
        except Exception as e:
            st.error(f"Unexpected error calling OpenAI: {e}")
            st.stop()

    raw = (resp.choices[0].message.content or "").strip()

    # 1) Parse normal
    try:
        data = parse_json_safely(raw)
    except Exception:
        # 2) Attempt repair (handles truncation)
        with st.spinner("Repairing incomplete output…"):
            try:
                repaired = try_repair_json(client, raw, max_tokens=1800)
                data = parse_json_safely(repaired)
                raw = repaired
            except Exception:
                st.error("Model returned incomplete/non-JSON output even after repair. Raw response below:")
                st.code(raw)
                st.stop()

    today_steps = data.get("today_steps") or []
    future_steps = data.get("future_steps") or []
    deltas = data.get("deltas") or []
    human_shift = data.get("human_shift") or []
    glossary = data.get("glossary") or []
    tool_suggestions = data.get("tool_suggestions") or []
    notes = data.get("notes") or []

    # Defensive sanity
    if not isinstance(today_steps, list) or len(today_steps) < 4:
        st.error("Today workflow incomplete. Try again.")
        st.code(raw)
        st.stop()

    if not isinstance(future_steps, list) or len(future_steps) < 4:
        st.error(f"{YEAR} workflow incomplete. Try again.")
        st.code(raw)
        st.stop()

    today_by_id = {s.get("id"): s for s in today_steps if s.get("id")}

    st.subheader("Workflow lens (custom)")

    st.markdown(f"""
    <div class="card">
      <div class="badge-purple">What changes (in plain terms)</div>
      <ul>{''.join([f"<li>{d}</li>" for d in deltas[:4]])}</ul>
      <div style="margin-top:10px;">
        <strong>Human shift:</strong>
        <ul>{''.join([f"<li>{h}</li>" for h in human_shift[:3]])}</ul>
      </div>
    </div>
    """, unsafe_allow_html=True)

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

    st.markdown("### Today → 2026 step mapping (indicative)")
    for f in future_steps[:12]:
        fid = f.get("id", "")
        flabel = shorten_label(f.get("label", ""))
        factor = normalize_actor(f.get("actor", "HUMAN"))
        fmapped = f.get("maps_to") or []

        left_lines = []
        for tid in fmapped:
            t = today_by_id.get(tid)
            if t:
                left_lines.append(f"<div class='kv'><span class='idpill'>{tid}</span> {shorten_label(t.get('label',''))}</div>")
            else:
                left_lines.append(f"<div class='kv'><span class='idpill'>{tid}</span> (step)</div>")

        if not left_lines:
            left_lines = ["<div class='kv'><em>No mapping provided</em></div>"]

        st.markdown(f"""
        <div class="mapping-row">
          <div class="mapping-left">
            <div class="mapping-title">Today steps absorbed</div>
            {''.join(left_lines)}
          </div>
          <div class="mapping-right">
            <div class="mapping-title">{fid} → {flabel}</div>
            <div class="small-muted"><strong>2026 owner:</strong> {ICON.get(factor,'👤')} {factor}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    if isinstance(glossary, list) and len(glossary) > 0:
        st.markdown("### Glossary (plain English)")
        for g in glossary[:6]:
            term = (g.get("term") or "").strip()
            definition = (g.get("definition") or "").strip()
            if term and definition:
                st.markdown(f"""
                <div class="card">
                  <div class="badge-blue">{term}</div>
                  <div>{definition}</div>
                </div>
                """, unsafe_allow_html=True)

    if isinstance(tool_suggestions, list) and len(tool_suggestions) > 0:
        st.markdown("### AI / automation enablers (realistic)")
        st.caption("Examples are common enterprise tools. This is tool-agnostic and indicative.")

        for t in tool_suggestions[:4]:
            cat = (t.get("tool_category") or "").strip()
            ex = t.get("example_tools") or []
            use = (t.get("use_in_workflow") or "").strip()
            fit = (t.get("fit_notes") or "").strip()

            ex_str = ", ".join([e for e in ex if isinstance(e, str)]) if isinstance(ex, list) else ""

            st.markdown(f"""
            <div class="card">
              <div class="badge-blue">{cat}</div>
              <div><strong>Examples:</strong> {ex_str}</div>
              <div><strong>Use in workflow:</strong> {use}</div>
              <div class="small-muted"><strong>Fit notes:</strong> {fit}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
      <div class="badge-black">Controls, constraints & legend</div>
      <ul>{''.join([f"<li>{n}</li>" for n in notes[:3]])}</ul>
      <div class="small-muted">
        <strong>Legend:</strong>
        👤 HUMAN • 🧾 ERP • 🤖 AI • 🤖👤 AI+HUMAN • 🤖🧾 AI+ERP • 🤖🧾👤 AI+ERP+HUMAN<br/>
        <strong>Intent tags:</strong> Admin / Control / Decision / Relationship
      </div>
    </div>
    """, unsafe_allow_html=True)
