# =========================
# Process Library (Dropdown Taxonomy)
# =========================
# Keep this file SIMPLE:
# - No functions required
# - All data at module level
# - Values are plain strings so Streamlit dropdowns work reliably

DOMAINS = {
    # -------------------------
    # PROCUREMENT / PURCHASING
    # -------------------------
    "Purchasing / Procurement": {
        "Source-to-Settle (S2S)": [
            "Spend analysis & demand aggregation",
            "Supplier discovery & pre-qualification",
            "RFx / tendering",
            "Negotiation & award recommendation",
            "Contracting (CLM)",
            "Catalog / guided buying",
            "Requisition-to-PO",
            "Goods receipt / service confirmation",
            "Invoice capture & 2/3-way matching",
            "Exception handling & approvals",
            "Payment & supplier performance"
        ],
        "Procure-to-Pay (P2P)": [
            "Requisition creation",
            "Approval routing",
            "Purchase order creation",
            "Supplier confirmation / ASN (if relevant)",
            "Goods receipt / service entry",
            "Invoice capture",
            "2/3-way matching",
            "Exception resolution",
            "Payment run",
            "Supplier reconciliation"
        ],
        "Contract Lifecycle Management (CLM)": [
            "Request / intake",
            "Clause selection & drafting",
            "Redlining & negotiation",
            "Risk / legal review",
            "Approvals",
            "Signature & repository",
            "Obligation tracking",
            "Renewals / amendments"
        ]
    },

    # -------------------------
    # SALES
    # -------------------------
    "Sales": {
        "Lead-to-Cash (L2C) – B2B": [
            "Lead capture",
            "Qualification",
            "Discovery",
            "Solutioning / proposal",
            "Pricing & approvals",
            "Negotiation",
            "Contracting",
            "Order booking",
            "Fulfilment / delivery handoff",
            "Billing / invoicing",
            "Collections / dispute handling"
        ],
        "Lead-to-Cash (L2C) – B2C": [
            "Lead / demand capture",
            "Nurture & conversion",
            "Checkout / order placement",
            "Payment authorization",
            "Fulfilment & delivery",
            "Customer support / returns",
            "Refunds / adjustments"
        ],
        "Quote-to-Cash (Q2C)": [
            "Configuration & quoting (CPQ)",
            "Discounting & approvals",
            "Proposal generation",
            "Contracting",
            "Order management",
            "Billing & invoicing",
            "Revenue recognition (if applicable)",
            "Renewals / expansions"
        ],
        "Customer Success – Adopt-to-Renew": [
            "Onboarding",
            "Adoption tracking",
            "Value realization",
            "QBRs / stakeholder management",
            "Risk & churn prevention",
            "Renewal / upsell"
        ]
    },

    # -------------------------
    # HUMAN RESOURCES
    # -------------------------
    "Human Resources": {
        "Hire-to-Retire (H2R)": [
            "Workforce planning",
            "Recruiting",
            "Hiring & offers",
            "Onboarding",
            "Performance & goals",
            "Learning & development",
            "Rewards & benefits",
            "Employee relations / case management",
            "Mobility / internal moves",
            "Offboarding & knowledge transfer"
        ],
        "Recruit-to-Onboard (R2O)": [
            "Role definition / JD",
            "Sourcing",
            "Screening",
            "Interview coordination",
            "Interviewing & evaluation",
            "Offer & approvals",
            "Background checks",
            "Onboarding"
        ],
        "Performance Management (Goals-to-Reviews)": [
            "Goal setting",
            "Check-ins",
            "Feedback / coaching",
            "Calibration",
            "Performance review",
            "Development planning"
        ],
        "HR Case Management (Ticket-to-Resolution)": [
            "Employee query intake",
            "Triage & routing",
            "Policy guidance",
            "Approvals / exceptions",
            "Resolution",
            "Knowledge base update"
        ]
    },

    # -------------------------
    # FINANCE
    # -------------------------
    "Finance": {
        "Record-to-Report (R2R)": [
            "Transaction capture",
            "Journal entries",
            "Reconciliations",
            "Close activities",
            "Consolidation",
            "Management reporting",
            "External reporting"
        ],
        "Invoice-to-Cash (I2C)": [
            "Billing / invoice creation",
            "Invoice delivery",
            "Cash application",
            "Dunning / reminders",
            "Dispute management",
            "Collections",
            "Write-offs (if needed)"
        ],
        "FP&A (Plan-to-Perform)": [
            "Driver-based planning",
            "Budgeting",
            "Forecasting",
            "Variance analysis",
            "Decision support / business partnering"
        ],
        "Expense Management": [
            "Expense submission",
            "Policy checks",
            "Approvals",
            "Audit / compliance",
            "Reimbursement",
            "Reporting"
        ]
    },

    # -------------------------
    # MANUFACTURING / SUPPLY CHAIN
    # -------------------------
    "Manufacturing / Supply Chain": {
        "Plan-to-Produce (Plan-to-Make)": [
            "Demand planning",
            "Supply planning / MRP",
            "Production scheduling",
            "Materials availability",
            "Production execution",
            "Quality checks",
            "Maintenance coordination",
            "Finished goods booking"
        ],
        "Order-to-Deliver (O2D)": [
            "Order capture",
            "Availability & allocation",
            "Warehouse pick/pack",
            "Shipment planning",
            "Delivery",
            "Proof of delivery",
            "Returns / reverse logistics"
        ],
        "Procure-to-Stock (P2S)": [
            "Replenishment triggers",
            "Purchase order creation",
            "Inbound logistics",
            "Receiving & put-away",
            "Inventory optimization",
            "Cycle counts"
        ]
    },

    # -------------------------
    # IT / OPERATIONS
    # -------------------------
    "IT / Operations": {
        "Incident-to-Resolution (ITSM)": [
            "Incident intake",
            "Triage & classification",
            "Routing to resolver group",
            "Diagnosis / knowledge search",
            "Resolution / workaround",
            "User confirmation",
            "Post-incident review"
        ],
        "Change-to-Deploy": [
            "Change request",
            "Impact & risk assessment",
            "Approvals",
            "Implementation / deployment",
            "Validation",
            "Monitoring",
            "Rollback (if needed)"
        ],
        "Request-to-Fulfil (Service Requests)": [
            "Request intake",
            "Approval (if needed)",
            "Fulfilment",
            "Confirmation",
            "Knowledge update"
        ]
    },

    # -------------------------
    # MARKETING
    # -------------------------
    "Marketing": {
        "Campaign-to-Revenue": [
            "Audience / segmentation",
            "Creative & content development",
            "Channel planning",
            "Campaign execution",
            "Optimization",
            "Lead handoff to sales",
            "Attribution & reporting"
        ],
        "Content-to-Conversion": [
            "Topic research",
            "Content creation",
            "Publishing",
            "Distribution",
            "Engagement tracking",
            "Conversion optimization"
        ]
    },

    # -------------------------
    # CUSTOMER SERVICE / CONTACT CENTER
    # -------------------------
    "Customer Service": {
        "Ticket-to-Resolution": [
            "Ticket intake",
            "Classification & prioritization",
            "Knowledge search",
            "Resolution / escalation",
            "Customer update",
            "Closure & QA",
            "Insights & knowledge update"
        ],
        "Complaint-to-Closure": [
            "Complaint intake",
            "Triage & severity assessment",
            "Investigation",
            "Resolution proposal",
            "Approvals (if needed)",
            "Customer communication",
            "Closure & learning"
        ]
    },

    # -------------------------
    # HEALTHCARE (HIGH-LEVEL GENERIC)
    # -------------------------
    "Healthcare (Generic)": {
        "Patient Intake-to-Discharge": [
            "Appointment / registration",
            "Clinical intake & triage",
            "Diagnostics / labs",
            "Care plan & orders",
            "Treatment / procedures",
            "Documentation & coding",
            "Billing & claims",
            "Discharge & follow-up"
        ],
        "Claims Processing (Payer)": [
            "Claim intake",
            "Eligibility & policy checks",
            "Adjudication",
            "Exception handling",
            "Payment",
            "Appeals / rework",
            "Reporting"
        ]
    },

    # -------------------------
    # HOSPITALITY (HIGH-LEVEL GENERIC)
    # -------------------------
    "Hospitality (Generic)": {
        "Booking-to-Checkout": [
            "Reservation",
            "Pre-arrival communication",
            "Check-in",
            "Room/service fulfilment",
            "Issue handling",
            "Billing",
            "Checkout & feedback"
        ],
        "Event-to-Execution": [
            "Inquiry & requirements",
            "Quotation",
            "Planning & coordination",
            "Vendor management",
            "Event execution",
            "Post-event billing & feedback"
        ]
    }
}

# Optional metadata you can use later (not required by the app)
PROCESS_META = {
    "notes": "Curated starter library for workflow shift visualization. Keep items high-level and domain-agnostic."
}
