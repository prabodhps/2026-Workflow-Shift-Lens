# =========================
# Process + Tool Library (for Workflow Shift Lens)
# =========================

# Controlled tool library: model must choose ONLY from these examples.
TOOL_LIBRARY = [
    {
        "tool_category": "Process mining",
        "examples": ["Celonis", "SAP Signavio", "Microsoft Process Mining (Power Automate)", "UiPath Process Mining"],
        "best_for": "Finding bottlenecks and variants from event logs."
    },
    {
        "tool_category": "iPaaS / Integration",
        "examples": ["MuleSoft", "Boomi", "Azure Logic Apps", "Workato"],
        "best_for": "Connecting ERP/CRM/HRIS and orchestrating workflows across systems."
    },
    {
        "tool_category": "RPA",
        "examples": ["UiPath", "Automation Anywhere", "Microsoft Power Automate (Desktop)"],
        "best_for": "Automating repetitive UI steps where APIs aren’t available."
    },
    {
        "tool_category": "IDP / OCR (Document processing)",
        "examples": ["ABBYY", "Google Document AI", "Azure AI Document Intelligence", "Amazon Textract"],
        "best_for": "Extracting structured data from invoices/forms/PDFs."
    },
    {
        "tool_category": "AI copilots for office work",
        "examples": ["Microsoft Copilot", "Google Gemini for Workspace"],
        "best_for": "Drafting, summarizing, synthesizing across email/docs."
    },
    {
        "tool_category": "Service desk / ITSM AI",
        "examples": ["ServiceNow (Now Assist)", "Jira Service Management AI", "Zendesk AI"],
        "best_for": "Ticket triage, knowledge suggestions, assisted resolution."
    },
    {
        "tool_category": "CRM / Sales AI",
        "examples": ["Salesforce Einstein", "Microsoft Dynamics 365 Copilot", "HubSpot AI"],
        "best_for": "Lead scoring, next-best action, forecasting assistance."
    },
    {
        "tool_category": "CLM (Contract lifecycle management)",
        "examples": ["Icertis", "DocuSign CLM", "Ironclad"],
        "best_for": "Contract workflows, clause libraries, approvals, obligations."
    },
    {
        "tool_category": "e-Signature",
        "examples": ["DocuSign", "Adobe Acrobat Sign"],
        "best_for": "Faster signature cycles + audit trails."
    },
    {
        "tool_category": "Spend / Procurement suites",
        "examples": ["SAP Ariba", "Coupa", "Jaggaer"],
        "best_for": "Catalog buying, approvals, supplier onboarding, spend visibility."
    },
    {
        "tool_category": "Finance close / controls automation",
        "examples": ["BlackLine", "FloQast"],
        "best_for": "Reconciliations, close checklists, controls evidence."
    },
    {
        "tool_category": "Analytics / BI",
        "examples": ["Power BI", "Tableau", "Looker"],
        "best_for": "Dashboards, operational reporting, KPI monitoring."
    },
    {
        "tool_category": "Knowledge base / enterprise search",
        "examples": ["Confluence", "SharePoint", "Notion"],
        "best_for": "Publishing SOPs/policies/playbooks; searchable knowledge."
    },
]

DOMAINS = {
    "Purchasing / Procurement": {
        "Source-to-Settle (S2S)": {
            "goal": "Reduce cycle time and exceptions; move humans to negotiation, risk decisions, and supplier relationships.",
            "default_steps": [
                "Request intake",
                "Requirements clarify",
                "Supplier shortlist",
                "RFx / quotes",
                "Evaluation",
                "Negotiation",
                "Contract draft",
                "Approvals",
                "PO issue",
                "Goods receipt",
                "Invoice capture",
                "3-way match",
                "Exceptions resolve",
                "Payment",
                "Supplier review"
            ]
        },
        "Procure-to-Pay (P2P)": {
            "goal": "Touchless processing for clean cases; humans handle exceptions, approvals, supplier escalation.",
            "default_steps": [
                "Requisition",
                "Budget check",
                "Approvals",
                "PO creation",
                "Receiving",
                "Invoice capture",
                "Matching",
                "Exception handling",
                "Payment"
            ]
        },
        "Contract Lifecycle (CLM)": {
            "goal": "Faster contracting with better risk controls; humans focus on judgement, negotiation, high-risk clauses.",
            "default_steps": [
                "Request intake",
                "Template select",
                "Draft contract",
                "Redline / review",
                "Risk assessment",
                "Approvals",
                "e-Sign",
                "Obligations track",
                "Renewals"
            ]
        }
    },

    "Sales": {
        "Lead-to-Cash (B2B)": {
            "goal": "Reduce manual handoffs; humans focus on discovery, relationship, deal strategy.",
            "default_steps": [
                "Lead capture",
                "Qualification",
                "Discovery",
                "Solution fit",
                "Proposal",
                "Pricing approvals",
                "Negotiation",
                "Contract",
                "Order",
                "Billing",
                "Collections"
            ]
        },
        "Lead-to-Cash (B2C)": {
            "goal": "Improve conversion + service; humans handle complex cases and trust moments.",
            "default_steps": [
                "Demand capture",
                "Nurture",
                "Conversion",
                "Checkout",
                "Fulfilment",
                "Support",
                "Returns",
                "Refunds"
            ]
        },
        "Quote-to-Cash (Q2C)": {
            "goal": "Accelerate quoting; keep control points for discounting + revenue policy.",
            "default_steps": [
                "Configure",
                "Quote",
                "Discount approval",
                "Contract",
                "Order mgmt",
                "Billing",
                "Revenue recognition",
                "Renewals"
            ]
        }
    },

    "Human Resources": {
        "Hire-to-Retire (H2R)": {
            "goal": "Reduce admin; humans focus on coaching, judgement, employee experience.",
            "default_steps": [
                "Workforce plan",
                "Requisition",
                "Sourcing",
                "Screening",
                "Interviews",
                "Offer approvals",
                "Onboarding",
                "Performance cycle",
                "Learning",
                "Rewards",
                "Employee support",
                "Moves",
                "Offboarding"
            ]
        },
        "Recruit-to-Onboard (R2O)": {
            "goal": "Faster time-to-hire; humans focus on decision quality + candidate experience.",
            "default_steps": [
                "Role definition",
                "Sourcing",
                "Screening",
                "Interview loop",
                "Hiring decision",
                "Offer approvals",
                "Checks",
                "Onboarding"
            ]
        },
        "HR Case Mgmt": {
            "goal": "Deflect repetitive queries; humans handle exceptions, empathy moments, policy judgement.",
            "default_steps": [
                "Case intake",
                "Triage",
                "Policy guidance",
                "Approvals",
                "Resolution",
                "Knowledge update"
            ]
        }
    },

    "Finance": {
        "Record-to-Report (R2R)": {
            "goal": "Faster close with fewer manual reconciliations; humans focus on variance + decisions.",
            "default_steps": [
                "Transaction capture",
                "Journal entries",
                "Reconciliations",
                "Close checklist",
                "Consolidation",
                "Reporting"
            ]
        },
        "Invoice-to-Cash (I2C)": {
            "goal": "Automate reminders + matching; humans focus on disputes + negotiation.",
            "default_steps": [
                "Billing",
                "Invoice delivery",
                "Cash application",
                "Dunning",
                "Disputes",
                "Collections"
            ]
        }
    },

    "IT / Operations": {
        "Incident-to-Resolution (ITSM)": {
            "goal": "Auto-triage + knowledge resolution; humans handle major incidents + change control.",
            "default_steps": [
                "Ticket intake",
                "Categorize",
                "Route",
                "Diagnose",
                "Resolve",
                "Confirm",
                "Post-review"
            ]
        },
        "Change-to-Deploy": {
            "goal": "Reduce lead time; keep strong risk controls and approvals for high-impact changes.",
            "default_steps": [
                "Change request",
                "Risk assess",
                "Approvals",
                "Deploy",
                "Validate",
                "Monitor"
            ]
        }
    }
}


def get_default_steps(domain: str, workflow: str) -> list[str]:
    try:
        return DOMAINS[domain][workflow].get("default_steps", [])
    except Exception:
        return []
