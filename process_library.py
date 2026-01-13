# process_library.py
# =========================
# 2026 Workflow Shift Lens — Process Library (Domain → Sub-domain → Sub-process)
# =========================

# DOMAINS structure:
# DOMAINS[domain][sub_domain] = {
#   "goal": "...",
#   "sub_processes": {
#       "Sub-process name": {
#           "goal": "...(optional override)...",
#           "default_steps": [ ... one step per line ... ]
#       },
#       ...
#   }
# }

DOMAINS = {
    "HR / People": {
        "Hire-to-Retire (H2R)": {
            "goal": "Deliver a seamless employee lifecycle with compliance, speed, and strong experience.",
            "sub_processes": {
                "Hiring (End-to-end)": {
                    "default_steps": [
                        "Workforce need identified",
                        "Job approval & requisition",
                        "Job posting / sourcing",
                        "Screening & shortlist",
                        "Interviews",
                        "Offer & negotiation",
                        "Background checks",
                        "Onboarding setup",
                        "Day-1 onboarding",
                        "Probation check-in",
                    ]
                },
                "Recruiting — Sourcing & Screening": {
                    "default_steps": [
                        "Role intake & success profile",
                        "Sourcing strategy",
                        "Candidate search / outreach",
                        "Inbound application triage",
                        "Resume screening",
                        "Initial phone screen",
                        "Shortlist & hiring manager review",
                    ]
                },
                "Recruiting — Interview to Offer": {
                    "default_steps": [
                        "Interview plan & panel setup",
                        "Candidate scheduling",
                        "Interviews & feedback capture",
                        "Decision meeting",
                        "Offer drafting",
                        "Offer approval",
                        "Offer negotiation",
                        "Offer acceptance",
                    ]
                },
                "Promotion": {
                    "default_steps": [
                        "Eligibility review",
                        "Performance & potential evidence",
                        "Manager justification",
                        "Calibration / talent review",
                        "Budget check",
                        "Approval workflow",
                        "Employee communication",
                        "HRIS update",
                    ]
                },
                "Employee Transfer": {
                    "default_steps": [
                        "Transfer request raised",
                        "Role / position validation",
                        "Comp & grade check",
                        "Approvals",
                        "Effective date confirmation",
                        "HRIS update",
                        "Stakeholder communication",
                        "Handover plan",
                    ]
                },
                "Performance cycle": {
                    "default_steps": [
                        "Goal setting",
                        "Mid-year check-in",
                        "Feedback collection",
                        "Year-end review drafting",
                        "Calibration",
                        "Final ratings & outcomes",
                        "Employee conversations",
                        "HRIS close-out",
                    ]
                },
            },
        },
    },

    "Purchasing / Procurement": {
        "Source-to-Settle (S2S)": {
            "goal": "Enable compliant buying, reduce cycle time, and increase touchless processing.",
            "sub_processes": {
                "Sourcing & RFx": {
                    "default_steps": [
                        "Requisition intake",
                        "Requirements clarification",
                        "Supplier shortlist",
                        "RFx / quotes issued",
                        "Proposal evaluation",
                        "Supplier selection",
                        "Award recommendation",
                        "Approval & sign-off",
                    ]
                },
                "Contracting": {
                    "default_steps": [
                        "Contract request intake",
                        "Template selection",
                        "Clause drafting / redlines",
                        "Legal review",
                        "Risk & compliance checks",
                        "Approvals",
                        "Signature & execution",
                        "Repository upload",
                    ]
                },
                "PO to Goods Receipt": {
                    "default_steps": [
                        "Requisition approval",
                        "PO creation",
                        "PO dispatch to supplier",
                        "Order confirmation",
                        "Delivery scheduling",
                        "Goods receipt",
                        "Discrepancy handling",
                        "Close PO",
                    ]
                },
                "Invoice to Pay": {
                    "default_steps": [
                        "Invoice receipt",
                        "Invoice data capture",
                        "3-way match",
                        "Exception resolution",
                        "Approval for payment",
                        "Payment execution",
                        "Remittance notice",
                        "Supplier query handling",
                    ]
                },
                "Supplier Performance": {
                    "default_steps": [
                        "Define supplier KPIs",
                        "Collect performance data",
                        "Scorecard generation",
                        "Issue identification",
                        "Corrective action plans",
                        "Business reviews",
                        "Renewal / exit decision",
                    ]
                },
            },
        },
    },

    "Finance": {
        "Record-to-Report (R2R)": {
            "goal": "Produce timely, accurate financial reporting with strong controls and auditability.",
            "sub_processes": {
                "Month-end close": {
                    "default_steps": [
                        "Close calendar kickoff",
                        "Accruals & journals",
                        "Intercompany reconciliation",
                        "Account reconciliations",
                        "Variance analysis",
                        "Management review",
                        "Close sign-off",
                        "Financial statements publish",
                    ]
                },
                "Financial Planning & Analysis (FP&A)": {
                    "default_steps": [
                        "Collect actuals",
                        "Driver identification",
                        "Forecast update",
                        "Scenario modeling",
                        "Business partner reviews",
                        "Leadership readout",
                        "Action tracking",
                    ]
                },
                "Accounts Payable (AP)": {
                    "default_steps": [
                        "Invoice receipt",
                        "Invoice coding",
                        "Approval workflow",
                        "Payment run",
                        "Vendor reconciliation",
                        "AP reporting",
                    ]
                },
                "Accounts Receivable (AR)": {
                    "default_steps": [
                        "Invoice issuance",
                        "Collections follow-up",
                        "Dispute management",
                        "Cash application",
                        "Bad debt review",
                        "AR reporting",
                    ]
                },
            },
        },
    },

    "Sales": {
        "Lead-to-Cash (L2C)": {
            "goal": "Convert demand into revenue with disciplined pipeline, pricing, and collections.",
            "sub_processes": {
                "B2B Sales Cycle": {
                    "default_steps": [
                        "Lead qualification",
                        "Discovery meeting",
                        "Solution mapping",
                        "Proposal / quote",
                        "Negotiation",
                        "Contract signing",
                        "Handover to delivery",
                        "Invoice & collections",
                    ]
                },
                "B2C Sales Cycle": {
                    "default_steps": [
                        "Lead / inquiry capture",
                        "Product recommendation",
                        "Offer / promotion",
                        "Checkout / payment",
                        "Fulfillment",
                        "Customer support",
                        "Upsell / retention",
                    ]
                },
                "Collections": {
                    "default_steps": [
                        "Invoice aging review",
                        "Collections outreach",
                        "Dispute resolution",
                        "Promise-to-pay tracking",
                        "Escalation",
                        "Cash receipt",
                        "Account update",
                    ]
                },
            },
        },
    },

    "Marketing": {
        "Plan-to-Perform (Campaign Ops)": {
            "goal": "Run efficient campaigns with measurable impact and fast learning loops.",
            "sub_processes": {
                "Campaign planning": {
                    "default_steps": [
                        "Objective & audience definition",
                        "Channel mix planning",
                        "Content plan",
                        "Creative production",
                        "Launch readiness",
                        "Launch execution",
                        "Performance monitoring",
                        "Optimization & learnings",
                    ]
                },
                "Content production": {
                    "default_steps": [
                        "Brief creation",
                        "Draft content",
                        "Design / creative",
                        "Compliance review",
                        "Publishing",
                        "Distribution",
                        "Performance review",
                    ]
                },
            },
        },
    },

    "IT / Technology": {
        "Build-to-Run (Delivery & Ops)": {
            "goal": "Deliver changes reliably while improving speed, quality, and operational resilience.",
            "sub_processes": {
                "IT Project Delivery": {
                    "default_steps": [
                        "Requirements intake",
                        "Scope & plan",
                        "Resource allocation",
                        "Build / configure",
                        "Testing",
                        "Release approval",
                        "Deployment",
                        "Post-release monitoring",
                    ]
                },
                "Incident management": {
                    "default_steps": [
                        "Incident detection",
                        "Triage & severity",
                        "Assignment",
                        "Diagnosis",
                        "Fix / workaround",
                        "Customer updates",
                        "Post-incident review",
                    ]
                },
                "Change management (ITIL)": {
                    "default_steps": [
                        "Change request",
                        "Impact assessment",
                        "CAB review",
                        "Approval",
                        "Implementation",
                        "Validation",
                        "Close-out",
                    ]
                },
            },
        },
    },
}

# Tool library: keep it stable; model must not invent tools
TOOL_LIBRARY = {
    "IDP / OCR (Document processing)": ["ABBYY", "Google Document AI", "Amazon Textract"],
    "RPA": ["UiPath", "Automation Anywhere", "Blue Prism"],
    "Workflow / BPM": ["ServiceNow", "Appian", "Camunda"],
    "ERP / Finance": ["SAP", "Oracle", "Microsoft Dynamics 365"],
    "CRM / Sales": ["Salesforce", "HubSpot", "Microsoft Dynamics 365 CRM"],
    "HRIS / Talent": ["Workday", "SAP SuccessFactors", "Oracle HCM"],
    "Analytics / BI": ["Power BI", "Tableau", "Looker"],
    "Knowledge / Search": ["Elastic", "OpenSearch", "Microsoft Search"],
    "Integration / iPaaS": ["MuleSoft", "Boomi", "Workato"],
    "Contact Center / CX": ["Genesys", "Zendesk", "Twilio"],
}

def get_default_steps(domain: str, sub_domain: str, sub_process: str | None = None) -> list[str]:
    """Return default steps for selected domain/sub_domain/sub_process if available."""
    d = DOMAINS.get(domain, {})
    sd = d.get(sub_domain, {})
    sp = (sd.get("sub_processes") or {})
    if sub_process and sub_process in sp:
        return sp[sub_process].get("default_steps", []) or []
    # fallback: first sub-process steps if exists
    if isinstance(sp, dict) and len(sp) > 0:
        first_key = list(sp.keys())[0]
        return sp[first_key].get("default_steps", []) or []
    return []
