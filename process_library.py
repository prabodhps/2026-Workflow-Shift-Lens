# =========================
# Process Library (Workflow Lens)
# =========================

DOMAINS = {
    "Purchasing / Procurement": {
        "Source-to-Settle (S2S)": {
            "focus_areas": [
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
            "goal": "Reduce cycle time and exceptions; move humans to negotiation, risk decisions, and supplier relationships."
        },
        "Procure-to-Pay (P2P)": {
            "focus_areas": [
                "Requisition",
                "Approvals",
                "PO creation",
                "Receiving",
                "Invoice capture",
                "Matching",
                "Exceptions",
                "Payment"
            ],
            "goal": "Touchless processing for clean cases; humans handle exceptions, approvals, and supplier escalation."
        },
        "Contract Lifecycle Management (CLM)": {
            "focus_areas": [
                "Intake",
                "Drafting",
                "Redlining",
                "Risk review",
                "Approvals",
                "Signature",
                "Obligations",
                "Renewals"
            ],
            "goal": "Faster contracting with better risk controls; humans focus on judgement, negotiation, and high-risk clauses."
        }
    },

    "Sales": {
        "Lead-to-Cash (L2C) – B2B": {
            "focus_areas": [
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
            "goal": "Reduce manual handoffs; humans focus on discovery, relationship building, and deal strategy."
        },
        "Lead-to-Cash (L2C) – B2C": {
            "focus_areas": [
                "Demand capture",
                "Nurture",
                "Conversion",
                "Checkout",
                "Fulfilment",
                "Support",
                "Returns",
                "Refunds"
            ],
            "goal": "Improve conversion and service; humans handle complex cases and customer trust moments."
        },
        "Quote-to-Cash (Q2C)": {
            "focus_areas": [
                "Configure",
                "Quote",
                "Discount approvals",
                "Contract",
                "Order mgmt",
                "Billing",
                "Revenue recognition",
                "Renewals"
            ],
            "goal": "Accelerate quoting; keep control points for discounting and revenue policy."
        }
    },

    "Human Resources": {
        "Hire-to-Retire (H2R)": {
            "focus_areas": [
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
            "goal": "Reduce admin load; humans focus on coaching, judgement, and employee experience."
        },
        "Recruit-to-Onboard (R2O)": {
            "focus_areas": [
                "Role definition",
                "Sourcing",
                "Screening",
                "Interviewing",
                "Offer approvals",
                "Checks",
                "Onboarding"
            ],
            "goal": "Faster time-to-hire; humans focus on interviews, decision quality, and candidate experience."
        },
        "HR Case Mgmt (Ticket-to-Resolve)": {
            "focus_areas": [
                "Intake",
                "Triage",
                "Policy guidance",
                "Approvals",
                "Resolution",
                "Knowledge update"
            ],
            "goal": "Deflect repetitive queries; humans handle exceptions, empathy moments, and policy judgement."
        }
    },

    "Finance": {
        "Record-to-Report (R2R)": {
            "focus_areas": [
                "Transaction capture",
                "Journals",
                "Reconciliations",
                "Close",
                "Consolidation",
                "Reporting"
            ],
            "goal": "Faster close with fewer manual reconciliations; humans focus on variance explanation and decisions."
        },
        "Invoice-to-Cash (I2C)": {
            "focus_areas": [
                "Billing",
                "Invoice delivery",
                "Cash application",
                "Dunning",
                "Disputes",
                "Collections"
            ],
            "goal": "Automate reminders and matching; humans focus on dispute resolution and customer negotiation."
        },
        "Expense Management": {
            "focus_areas": [
                "Submission",
                "Policy checks",
                "Approvals",
                "Audit",
                "Reimbursement",
                "Reporting"
            ],
            "goal": "Auto-check policies; humans focus on audits, exceptions, and fraud decisions."
        }
    },

    "IT / Operations": {
        "Incident-to-Resolution (ITSM)": {
            "focus_areas": [
                "Intake",
                "Classification",
                "Routing",
                "Diagnosis",
                "Resolution",
                "Confirmation",
                "Post-review"
            ],
            "goal": "Auto-triage and knowledge resolution; humans handle major incidents and change control."
        },
        "Change-to-Deploy": {
            "focus_areas": [
                "Request",
                "Risk assessment",
                "Approvals",
                "Deploy",
                "Validate",
                "Monitor"
            ],
            "goal": "Reduce lead time; keep strong risk controls and human approvals for high-impact changes."
        }
    }
}
