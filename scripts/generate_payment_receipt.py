"""Generate the SmartVantage AI (FZE) UAE Payment Receipt PDF.

Run: python3 scripts/generate_payment_receipt.py
Output: receipts/payment_receipt_template.pdf
"""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

OUTPUT = Path(__file__).resolve().parent.parent / "receipts" / "payment_receipt_template.pdf"

NEON = colors.HexColor("#00D4FF")
NAVY = colors.HexColor("#0d1020")
DIM = colors.HexColor("#4a5568")
LIGHT_BG = colors.HexColor("#f4fbff")
BORDER = colors.HexColor("#cfe8f5")


def build_styles() -> dict:
    base = getSampleStyleSheet()["Normal"]
    return {
        "company": ParagraphStyle(
            "company", parent=base, fontName="Helvetica-Bold",
            fontSize=16, textColor=NAVY, leading=20, spaceAfter=2,
        ),
        "companyMeta": ParagraphStyle(
            "companyMeta", parent=base, fontName="Helvetica",
            fontSize=9, textColor=DIM, leading=12,
        ),
        "title": ParagraphStyle(
            "title", parent=base, fontName="Helvetica-Bold",
            fontSize=22, textColor=NEON, leading=26, alignment=TA_CENTER,
            spaceBefore=6, spaceAfter=10,
        ),
        "sectionHeader": ParagraphStyle(
            "sectionHeader", parent=base, fontName="Helvetica-Bold",
            fontSize=11, textColor=NAVY, leading=14, spaceBefore=8, spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "body", parent=base, fontName="Helvetica",
            fontSize=9.5, textColor=NAVY, leading=13,
        ),
        "bodySmall": ParagraphStyle(
            "bodySmall", parent=base, fontName="Helvetica",
            fontSize=8.5, textColor=DIM, leading=11,
        ),
        "status": ParagraphStyle(
            "status", parent=base, fontName="Helvetica-Bold",
            fontSize=12, textColor=colors.HexColor("#0a8f3b"), alignment=TA_CENTER,
            leading=16,
        ),
        "footerCenter": ParagraphStyle(
            "footerCenter", parent=base, fontName="Helvetica-Oblique",
            fontSize=8.5, textColor=DIM, alignment=TA_CENTER, leading=11,
        ),
        "warnTitle": ParagraphStyle(
            "warnTitle", parent=base, fontName="Helvetica-Bold",
            fontSize=11, textColor=colors.HexColor("#b45309"), leading=14,
            spaceAfter=4,
        ),
        "rightAmount": ParagraphStyle(
            "rightAmount", parent=base, fontName="Helvetica",
            fontSize=9.5, textColor=NAVY, leading=13, alignment=TA_RIGHT,
        ),
    }


def header_block(styles: dict) -> Table:
    left = [
        Paragraph("SmartVantage AI (FZE)", styles["company"]),
        Paragraph(
            "SRTIP Address: Block B -B48-098<br/>"
            "Sharjah, United Arab Emirates<br/>"
            "License No.: 9605<br/>"
            "TRN: [Insert your TRN once registered]<br/>"
            "Email: [Insert email] &nbsp;|&nbsp; Tel: [Insert phone]",
            styles["companyMeta"],
        ),
    ]
    right = [Paragraph("PAYMENT RECEIPT", styles["title"])]
    tbl = Table([[left, right]], colWidths=[95 * mm, 75 * mm])
    tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return tbl


def info_table(rows: list[tuple[str, str]], styles: dict) -> Table:
    data = [[Paragraph(f"<b>{label}</b>", styles["body"]), Paragraph(value, styles["body"])]
            for label, value in rows]
    tbl = Table(data, colWidths=[55 * mm, 115 * mm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), LIGHT_BG),
        ("BOX", (0, 0), (-1, -1), 0.4, BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return tbl


def items_table(styles: dict) -> Table:
    header = ["Item Description", "Qty", "Unit Price (AED)", "Total (AED)"]
    rows = [
        ["AI Training Video – Essential Pack (1 Video)", "1", "500.00", "500.00"],
        ["AI Training Video – Professional Pack (3 Videos)", "1", "1,200.00", "1,200.00"],
        ["Event Management Consultancy – 1 Hour Session", "1", "750.00", "750.00"],
    ]
    total_row = ["Total Paid (Including VAT)", "", "", "2,450.00"]

    data = [header] + rows + [total_row]
    tbl = Table(data, colWidths=[90 * mm, 15 * mm, 32 * mm, 33 * mm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9.5),
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ("ALIGN", (0, 0), (0, -1), "LEFT"),
        ("FONTNAME", (0, 1), (-1, -2), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 9.5),
        ("TEXTCOLOR", (0, 1), (-1, -2), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.white, LIGHT_BG]),
        ("BACKGROUND", (0, -1), (-1, -1), NEON),
        ("TEXTCOLOR", (0, -1), (-1, -1), NAVY),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, -1), (-1, -1), 10),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return tbl


def status_box(styles: dict) -> Table:
    data = [[
        Paragraph("Payment Status: <b>&#10004; PAID IN FULL</b>", styles["status"]),
        Paragraph("<b>Date Paid:</b> [DD/MM/YYYY]", styles["body"]),
    ]]
    tbl = Table(data, colWidths=[105 * mm, 65 * mm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#e6f7ec")),
        ("BACKGROUND", (1, 0), (1, 0), LIGHT_BG),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (1, 0), (1, 0), "LEFT"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return tbl


def signature_block(styles: dict) -> Table:
    lines = [
        Paragraph("<b>SmartVantage AI (FZE)</b>", styles["body"]),
        Spacer(1, 14),
        Paragraph("Authorized Signature: ______________________________", styles["body"]),
        Spacer(1, 4),
        Paragraph("<b>Name:</b> Maria Sonia Baranda Ruba", styles["body"]),
        Paragraph("<b>Title:</b> Manager", styles["body"]),
    ]
    tbl = Table([[lines]], colWidths=[170 * mm])
    tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return tbl


def checklist_table(styles: dict) -> Table:
    items = [
        ("Title \"Payment Receipt\" clearly displayed", "\u2713"),
        ("Business name and legal entity details", "\u2713"),
        ("TRN of the supplier (SmartVantage AI (FZE))", "\u2713"),
        ("Unique sequential receipt number", "\u2713"),
        ("Date and time of payment (UAE local time)", "\u2713"),
        ("Payment method used", "\u2713"),
        ("Customer name", "\u2713"),
        ("Description of goods/services purchased", "\u2713"),
        ("Total amount paid (including VAT)", "\u2713"),
        ("Statement that the amount includes VAT OR VAT breakdown", "\u2713"),
        ("Reference to related Tax Invoice", "\u2713"),
    ]
    data = [["Requirement", "Included"]] + [[r, m] for r, m in items]
    tbl = Table(data, colWidths=[140 * mm, 30 * mm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9.5),
        ("ALIGN", (1, 0), (1, -1), "CENTER"),
        ("TEXTCOLOR", (1, 1), (1, -1), colors.HexColor("#0a8f3b")),
        ("FONTNAME", (1, 1), (1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return tbl


def vat_callout(styles: dict) -> Table:
    body = Paragraph(
        "<b>VAT Treatment:</b> The total amount shown above includes VAT at the "
        "standard rate of 5% as per UAE Federal Decree-Law No. 8 of 2017. "
        "The VAT amount included in this payment is <b>AED 116.67</b> "
        "(calculated as Total &divide; 21).<br/><br/>"
        "<b>Amount in Words:</b> Two Thousand Four Hundred Fifty United Arab "
        "Emirates Dirhams Only.",
        styles["body"],
    )
    tbl = Table([[body]], colWidths=[170 * mm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return tbl


def warning_block(styles: dict) -> Table:
    content = [
        Paragraph("&#9888; Critical VAT Compliance Update (Effective July 2026)",
                  styles["warnTitle"]),
        Paragraph(
            "The UAE Ministry of Finance has published Cabinet Decision No. 100 "
            "of 2025, which amends the VAT Executive Regulations and introduces "
            "major changes ahead of the July 2026 e-invoicing rollout.",
            styles["body"],
        ),
        Spacer(1, 6),
        Paragraph("<b>Key changes affecting your business:</b>", styles["body"]),
        Paragraph(
            "&bull; Simplified tax invoices will no longer be allowed for "
            "businesses covered under the UAE e-invoicing scope.<br/>"
            "&bull; All invoices must be issued as full tax invoices, even for "
            "small-value supplies under AED 10,000 or sales to non-VAT "
            "registered customers.<br/>"
            "&bull; These changes are effective from 29 September 2025 for "
            "businesses within the e-invoicing scope.",
            styles["body"],
        ),
        Spacer(1, 6),
        Paragraph("<b>What this means for SmartVantage AI (FZE):</b>",
                  styles["body"]),
        Paragraph(
            "Your business is expected to fall within Phase 2 (SME) of the "
            "e-invoicing rollout, with a mandatory go-live date of 1 July 2027. "
            "However, the above amendments mean that once you adopt e-invoicing "
            "(whether voluntarily earlier or at the mandatory date), you will "
            "need to issue Full Tax Invoices for all transactions \u2014 "
            "including B2C sales under AED 10,000. Simplified invoices will no "
            "longer be a compliant option.",
            styles["body"],
        ),
        Spacer(1, 6),
        Paragraph("<b>Receipt vs. Tax Invoice Clarification:</b>", styles["body"]),
        Paragraph(
            "This Payment Receipt template remains valid and useful for "
            "confirming payment has been received, but it does not replace the "
            "requirement to issue a Full Tax Invoice for VAT compliance. For "
            "B2C transactions, you will now need to collect and maintain "
            "customer data (name and address) sufficient to issue a Full Tax "
            "Invoice.",
            styles["body"],
        ),
    ]
    tbl = Table([[content]], colWidths=[170 * mm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fff7ed")),
        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#f59e0b")),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    return tbl


def build_story(styles: dict) -> list:
    story: list = []

    story.append(header_block(styles))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1.2, color=NEON))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Receipt Details", styles["sectionHeader"]))
    story.append(info_table([
        ("Receipt No.", "[e.g., RCPT-2025-001]"),
        ("Receipt Date", "[DD/MM/YYYY]"),
        ("Time of Payment", "[HH:MM] (UAE Local Time)"),
        ("Payment Method", "[Card / Bank Transfer / Cash / Digital Wallet]"),
        ("Reference Invoice No.",
         "[e.g., INV-2025-XXX] (Optional \u2014 link to original invoice)"),
    ], styles))

    story.append(Paragraph("Received From", styles["sectionHeader"]))
    story.append(info_table([
        ("Customer Name", "[Customer Full Name]"),
        ("Contact", "[Email or Phone]"),
    ], styles))

    story.append(Paragraph("Items &amp; Services", styles["sectionHeader"]))
    story.append(items_table(styles))
    story.append(Spacer(1, 8))
    story.append(vat_callout(styles))

    story.append(Spacer(1, 10))
    story.append(status_box(styles))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "Thank you for your payment. This receipt confirms that payment has "
        "been received for the above items/services.",
        styles["body"],
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "<i>Note: This is a computer-generated payment receipt. For official "
        "tax documentation, please refer to the corresponding Tax Invoice "
        "issued for this transaction.</i>",
        styles["bodySmall"],
    ))

    story.append(Spacer(1, 14))
    story.append(signature_block(styles))

    story.append(Spacer(1, 16))
    story.append(HRFlowable(width="100%", thickness=0.6, color=BORDER))
    story.append(Spacer(1, 10))

    story.append(Paragraph("&#10004; Receipt Compliance Checklist",
                           styles["sectionHeader"]))
    story.append(checklist_table(styles))

    story.append(Spacer(1, 12))
    story.append(Paragraph("&#128204; Important Usage Notes",
                           styles["sectionHeader"]))
    notes = [
        "<b>Receipt vs. Tax Invoice Distinction:</b> This receipt confirms "
        "payment has been made, whereas a Tax Invoice is the legal document "
        "required for VAT purposes and must be issued at the time of supply. "
        "Always issue both documents when required.",
        "<b>VAT Compliance:</b> The receipt clearly states that the total "
        "includes 5% VAT and provides the VAT amount calculation, satisfying "
        "FTA transparency requirements.",
        "<b>Record Keeping:</b> Retain a copy of each receipt for seven (7) "
        "years as part of your financial records, along with the corresponding "
        "Tax Invoice.",
        "<b>Bank Transfer Payments:</b> If payment is made via bank transfer, "
        "consider attaching a screenshot of the bank confirmation or including "
        "the transaction reference number in the \"Payment Method\" field.",
        "<b>Link to Invoice:</b> Where possible, always include the \"Reference "
        "Invoice No.\" field to maintain a clear audit trail between the "
        "original invoice and the payment confirmation.",
    ]
    for i, note in enumerate(notes, start=1):
        story.append(Paragraph(f"{i}. {note}", styles["body"]))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 10))
    story.append(warning_block(styles))

    story.append(Spacer(1, 14))
    story.append(HRFlowable(width="100%", thickness=0.6, color=BORDER))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "SmartVantage AI (FZE) &nbsp;\u2022&nbsp; SRTIP, Sharjah, UAE "
        "&nbsp;\u2022&nbsp; License No. 9605",
        styles["footerCenter"],
    ))

    return story


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    styles = build_styles()
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title="SmartVantage AI (FZE) - Payment Receipt",
        author="SmartVantage AI (FZE)",
        subject="UAE Payment Receipt Template",
    )
    doc.build(build_story(styles))
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
