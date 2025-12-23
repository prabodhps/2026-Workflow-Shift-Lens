# =========================
# Process Library (Diagram-first)
# =========================
# Keep values as plain strings for Streamlit dropdowns.

DOMAINS = {
    "Purchasing / Procurement": {
        "Source-to-Settle (S2S)": [
            "Spend analysis",
            "Supplier discovery",
            "RFx",
            "Negotiation",
            "Contracting",
            "Ordering",
            "Receiving",
            "Invoice matching",
            "Exception handling",
            "Payment"
        ],
        "Procure-to-Pay (P2P)": [
            "Requisition",
            "Approvals",
            "PO creation",
            "Receiving",
            "Invoice capture",
            "Matching",
            "Exceptions",
            "Payment"
        ],
        "Contract Lifecycle Management (CLM)": [
            "Intake",
            "Drafting",
            "Redlining",
            "Risk review",
            "Approvals",
            "Signature",
            "Obligations",
            "Renewals"
        ]
    },

    "Sales": {
        "Lead-to-Cash (L2C) – B2B": [
            "Lead capture",
            "Qualification",
            "Discovery",
            "Proposal",
            "Pricing approvals",
            "Negotiation",
            "Contract",
            "Order",
            "Billing",
            "Collections"
        ],
        "Lead-to-Cash (L2C) – B2C": [
            "Demand capture",
            "Nurture",
            "Conversion",
            "Checkout",
            "Fulfilment",
            "Support",
            "Returns",
            "Refunds"
        ],
        "Quote-to-Cash (Q2C)": [
            "Configure",
            "Quote",
            "Discount approvals",
            "Contract",
            "Order mgmt",
            "Billing",
            "Revenue recognition",
            "Renewals"
        ]
    },

    "Human Resources": {
        "Hire-to-Retire (H2R)": [
            "Workforce plan",
            "Recruit",
            "Hire",
            "Onboard",
            "Performance",
            "Learning",
            "Rewards",
            "Employee support",
            "Move",
            "Offboard"
        ],
        "Recruit-to-Onboard (R2O)": [
            "Role definition",
            "Sourcing",
            "Screening",
            "Interviewing",
            "Offer approvals",
            "Checks",
            "Onboarding"
        ],
        "HR Case Mgmt (Ticket-to-Resolve)": [
            "Intake",
            "Triage",
            "Policy guidance",
            "Approvals",
            "Resolution",
            "Knowledge update"
        ]
    },

    "Finance": {
        "Record-to-Report (R2R)": [
            "Transaction capture",
            "Journals",
            "Reconciliations",
            "Close",
            "Consolidation",
            "Reporting"
        ],
        "Invoice-to-Cash (I2C)": [
            "Billing",
            "Invoice delivery",
            "Cash application",
            "Dunning",
            "Disputes",
            "Collections"
        ],
        "Expense Management": [
            "Submission",
            "Policy checks",
            "Approvals",
            "Audit",
            "Reimbursement",
            "Reporting"
        ]
    },

    "IT / Operations": {
        "Incident-to-Resolution (ITSM)": [
            "Intake",
            "Classification",
            "Routing",
            "Diagnosis",
            "Resolution",
            "Confirmation",
            "Post-review"
        ],
        "Change-to-Deploy": [
            "Request",
            "Risk assessment",
            "Approvals",
            "Deploy",
            "Validate",
            "Monitor"
        ]
    }
}
