from pypdf import PdfReader

SAMPLE_RAW_TEXT = """NON-DISCLOSURE & EMPLOYMENT AGREEMENT
1. Non-Compete: The Employee agrees that upon termination, they shall not work in any capacity for any entity in the entire technology sector worldwide for a period of 5 years.
2. IP Assignment: Any concept, code, invention, or idea conceived by the Employee, whether during work hours or off-duty, belongs entirely to the Company in perpetuity.
3. Termination: The Company reserves the right to terminate employment immediately without notice or severance pay.
4. Jurisdiction: Any disputes will be resolved exclusively via binding arbitration in Delaware at the Employee's expense.
"""

def extract_pdf_text(uploaded_file) -> str:
    try:
        reader = PdfReader(uploaded_file)
        extracted = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted.append(text)
        return "\n".join(extracted).strip()
    except Exception:
        return ""

def dynamic_local_audit(contract_text: str) -> dict:
    text_lower = contract_text.lower()
    clauses = []
    score = 18

    if any(k in text_lower for k in ["non-compete", "non compete", "not work", "competitor", "restrictive covenant", "compete"]):
        is_extreme = any(k in text_lower for k in ["worldwide", "global", "5 year", "5-year", "48 month", "48-month", "3 year", "perpetuity", "entire"])
        score += 28 if is_extreme else 16
        clauses.append({
            "title": "Restrictive Non-Compete Covenant",
            "risk_level": "High" if is_extreme else "Medium",
            "issue": "Restricts future career mobility and ability to work in your industry after leaving the organization.",
            "recommendation": "Narrow the restriction to a maximum of 6 months and strictly define direct market competitors."
        })

    if any(k in text_lower for k in ["intellectual property", "ip assignment", "invention", "off-duty", "perpetuity", "conceived", "prior inventions", "work made for hire"]):
        is_off_duty = any(k in text_lower for k in ["off-duty", "personal time", "perpetuity", "whether during work hours", "any concept", "all inventions"])
        score += 26 if is_off_duty else 14
        clauses.append({
            "title": "Broad Intellectual Property Assignment",
            "risk_level": "High" if is_off_duty else "Medium",
            "issue": "Claims ownership over personal projects, code, or ideas developed outside working hours without company equipment.",
            "recommendation": "Add an explicit carve-out excluding inventions developed on personal time using personal resources."
        })

    if any(k in text_lower for k in ["without notice", "without severance", "immediately", "at-will", "unilateral", "terminate employment", "sole discretion"]):
        no_notice = any(k in text_lower for k in ["without notice", "without severance", "immediately", "forfeit"])
        score += 20 if no_notice else 12
        clauses.append({
            "title": "Unilateral Termination & Notice Waiver",
            "risk_level": "High" if no_notice else "Medium",
            "issue": "Allows immediate termination without standard notice periods, cure windows, or severance protection.",
            "recommendation": "Request a mutual 30-day written notice period or equivalent severance pay upon termination without cause."
        })

    if any(k in text_lower for k in ["arbitration", "delaware", "wilmington", "attorney fees", "employee's expense", "bear all legal", "jurisdiction", "indemnif"]):
        fee_shift = any(k in text_lower for k in ["employee's expense", "bear all legal", "employee shall bear", "indemnify"])
        score += 18 if fee_shift else 10
        clauses.append({
            "title": "Dispute Venue & Legal Cost Shifting",
            "risk_level": "High" if fee_shift else "Medium",
            "issue": "Mandates out-of-state binding arbitration or shifts company legal and transcription expenses onto the individual.",
            "recommendation": "Require arbitration expenses to be borne by the employer and set venue to your local jurisdiction."
        })

    if any(k in text_lower for k in ["liquidated damages", "penalty", "injunctive relief", "indefinite", "fine"]):
        score += 15
        clauses.append({
            "title": "Disproportionate Penalty & Remedies Clause",
            "risk_level": "Medium",
            "issue": "Exposes the signatory to severe financial penalties or immediate injunctive action without standard proof of damages.",
            "recommendation": "Cap liability to actual proven direct damages and remove automatic liquidated penalty figures."
        })

    if not clauses:
        score = 22
        clauses.append({
            "title": "Standard Commercial Obligations",
            "risk_level": "Low",
            "issue": "The uploaded text contains standard legal terms without overt predatory traps detected.",
            "recommendation": "Ensure all payment timelines, deliverables, and termination notice periods are mutually balanced."
        })

    score = min(max(score, 12), 98)
    if score >= 75:
        verdict = "Critical Risk - Do Not Sign Unmodified"
    elif score >= 45:
        verdict = "Moderate Risk - Negotiation Advised"
    else:
        verdict = "Low Risk - Standard Terms"

    high_count = sum(1 for c in clauses if c["risk_level"] == "High")
    summary = f"Audit completed across {len(contract_text.split())} words. Detected {len(clauses)} key risk vector(s) ({high_count} High Risk) yielding a {score}% overall risk rating."

    return {
        "risk_score": score,
        "verdict": verdict,
        "summary": summary,
        "clauses": clauses[:4]
    }
