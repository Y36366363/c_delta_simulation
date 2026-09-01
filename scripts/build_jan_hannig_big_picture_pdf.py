from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "jan_hannig_big_picture_brief_20260831.pdf"

NAVY = colors.HexColor("#17365D")
BLUE = colors.HexColor("#2A6592")
TEAL = colors.HexColor("#2F7D76")
GOLD = colors.HexColor("#C18B2C")
RED = colors.HexColor("#A6473E")
INK = colors.HexColor("#1F2A35")
MUTED = colors.HexColor("#5E6D7B")
LINE = colors.HexColor("#C9D4DE")
PALE_BLUE = colors.HexColor("#EAF2F8")
PALE_TEAL = colors.HexColor("#EAF5F2")
PALE_GOLD = colors.HexColor("#FFF5DB")
PALE_RED = colors.HexColor("#FBEDEB")
PALE_GRAY = colors.HexColor("#F4F6F8")
WHITE = colors.white


def make_styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "title",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=23,
            leading=28,
            textColor=NAVY,
            alignment=TA_CENTER,
            spaceAfter=7,
        ),
        "subtitle": ParagraphStyle(
            "subtitle",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=11.5,
            leading=16,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceAfter=10,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=17,
            leading=21,
            textColor=NAVY,
            spaceBefore=2,
            spaceAfter=7,
            keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12.2,
            leading=15,
            textColor=BLUE,
            spaceBefore=8,
            spaceAfter=4,
            keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.7,
            leading=14.1,
            textColor=INK,
            spaceAfter=5,
        ),
        "body_center": ParagraphStyle(
            "body_center",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.3,
            leading=13.4,
            textColor=INK,
            alignment=TA_CENTER,
        ),
        "small": ParagraphStyle(
            "small",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.2,
            leading=11.7,
            textColor=MUTED,
            spaceAfter=3,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.3,
            leading=13.4,
            leftIndent=13,
            firstLineIndent=-7,
            bulletIndent=4,
            textColor=INK,
            spaceAfter=3,
        ),
        "box_title": ParagraphStyle(
            "box_title",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=10.2,
            leading=13,
            textColor=NAVY,
            spaceAfter=2,
        ),
        "box_body": ParagraphStyle(
            "box_body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.1,
            leading=13.2,
            textColor=INK,
        ),
        "flow_title": ParagraphStyle(
            "flow_title",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=9.1,
            leading=11,
            textColor=NAVY,
            alignment=TA_CENTER,
        ),
        "flow_body": ParagraphStyle(
            "flow_body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.8,
            leading=10.2,
            textColor=INK,
            alignment=TA_CENTER,
        ),
        "quote": ParagraphStyle(
            "quote",
            parent=base["BodyText"],
            fontName="Helvetica-Oblique",
            fontSize=10,
            leading=14.5,
            textColor=INK,
            leftIndent=9,
            rightIndent=9,
        ),
        "table_head": ParagraphStyle(
            "table_head",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=8.8,
            leading=11.5,
            textColor=WHITE,
        ),
        "table": ParagraphStyle(
            "table",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.6,
            leading=12.2,
            textColor=INK,
        ),
    }


def p(text, key, styles):
    return Paragraph(text, styles[key])


def bullets(items, styles):
    return [Paragraph("• " + item, styles["bullet"]) for item in items]


def box(title, body, styles, background=PALE_BLUE, border=BLUE):
    table = Table(
        [[p(title, "box_title", styles)], [p(body, "box_body", styles)]],
        colWidths=[6.55 * inch],
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), background),
                ("BOX", (0, 0), (-1, -1), 0.75, border),
                ("LINEBELOW", (0, 0), (-1, 0), 0.35, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def header_footer(canvas, doc):
    canvas.saveState()
    width, height = letter
    if doc.page > 1:
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.5)
        canvas.line(0.72 * inch, height - 0.52 * inch, width - 0.72 * inch, height - 0.52 * inch)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(MUTED)
        canvas.drawString(0.72 * inch, height - 0.39 * inch, "Robust-reference profile inference: big-picture brief")
        canvas.drawRightString(width - 0.72 * inch, 0.40 * inch, str(doc.page))
    canvas.restoreState()


def flow_diagram(styles):
    cells = [
        ("1. Paired units", "The same people, buildings, models, or objects are measured in X and Y."),
        ("2. Fit references", "Estimate one robust center for X and one for Y."),
        ("3. Build profiles", "For every unit, record its distance from each fitted center."),
        ("4. Compare profiles", "Correlate the two distance lists: do the same units stand out?"),
        ("5. Make inference", "Estimate uncertainty and test whether the profile correlation is zero."),
    ]
    row = []
    widths = []
    for idx, (title, body) in enumerate(cells):
        node = Table(
            [[p(title, "flow_title", styles)], [p(body, "flow_body", styles)]],
            colWidths=[1.08 * inch],
        )
        node.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), PALE_BLUE if idx < 4 else PALE_TEAL),
                    ("BOX", (0, 0), (-1, -1), 0.65, BLUE if idx < 4 else TEAL),
                    ("LEFTPADDING", (0, 0), (-1, -1), 4),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]
            )
        )
        row.append(node)
        widths.append(1.08 * inch)
        if idx < len(cells) - 1:
            row.append(p("→", "body_center", styles))
            widths.append(0.23 * inch)
    outer = Table([row], colWidths=widths)
    outer.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    return outer


def build_pdf():
    styles = make_styles()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(
        str(OUTPUT),
        pagesize=letter,
        leftMargin=0.72 * inch,
        rightMargin=0.72 * inch,
        topMargin=0.70 * inch,
        bottomMargin=0.64 * inch,
        title="Big Picture of the Robust-Reference Profile Inference Project",
        author="Jialiang Yao",
        subject="Brief for discussion with Professor Jan Hannig",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
    doc.addPageTemplates([PageTemplate(id="main", frames=frame, onPage=header_footer)])

    story = []
    story.append(p("Big Picture of the Project", "title", styles))
    story.append(p("Robust-reference profile similarity, when its inference can be trusted, and how it can fail", "subtitle", styles))
    story.append(
        box(
            "The project in one sentence",
            "We ask whether the <b>same paired observational units stand out in two different variables</b>, and then study whether statistical inference for that pattern remains reliable when the reference points used to define \"standing out\" are estimated from the data.",
            styles,
            PALE_GOLD,
            GOLD,
        )
    )
    story.append(p("1. The motivating question", "h1", styles))
    story.append(
        p(
            "Suppose the data consist of paired measurements (X<sub>i</sub>, Y<sub>i</sub>) on the same units. Ordinary correlation asks whether large X values tend to come with large Y values. Our question is different: <b>if unit i is unusual relative to the X group, is that same unit also unusual relative to the Y group?</b>",
            "body",
            styles,
        )
    )
    story.append(
        p(
            "For example, a building might have an unusual energy-use pattern and also an unusual occupancy pattern, even if the raw measurements are on unrelated scales. The scientifically meaningful feature is the label of the building: the same unit stands out in both domains.",
            "body",
            styles,
        )
    )
    story.append(p("2. How the project represents \"standing out\"", "h1", styles))
    story.append(flow_diagram(styles))
    story.append(Spacer(1, 5))
    story.append(
        box(
            "Primary quantity",
            "For population robust references T<sub>X</sub> and T<sub>Y</sub>, the main estimand is<br/><br/><b>rho<sub>P</sub> = Corr(|X - T<sub>X</sub>|, |Y - T<sub>Y</sub>|).</b><br/><br/>A positive value means the same units tend to be far from both references. A value of zero means no linear association between the two distance profiles; it does <b>not</b> imply that X and Y are independent.",
            styles,
            PALE_TEAL,
            TEAL,
        )
    )
    story.append(p("3. How this grew out of the original c-delta project", "h1", styles))
    compare = Table(
        [
            [p("Original c-delta idea", "table_head", styles), p("New robust-reference paper", "table_head", styles)],
            [
                p("Each unit is compared with all other observations in its group. The resulting all-to-all divergence profiles are compared across X and Y.", "table", styles),
                p("Each unit is compared with a fitted robust marginal reference. The resulting radius profiles are compared across X and Y.", "table", styles),
            ],
            [
                p("Main goal: define and motivate a broad divergence-concordance coefficient.", "table", styles),
                p("Main goal: understand the <b>reliability of inference</b> for a specific robust-reference profile correlation.", "table", styles),
            ],
        ],
        colWidths=[3.27 * inch, 3.27 * inch],
    )
    compare.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE_GRAY]),
                ("GRID", (0, 0), (-1, -1), 0.45, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(compare)
    story.append(PageBreak())

    story.append(p("What the Paper Is Actually Studying", "h1", styles))
    story.append(
        box(
            "The central inferential problem",
            "The profile correlation is computed after fitting T<sub>X</sub> and T<sub>Y</sub>. Therefore, uncertainty comes from both the paired observations and the estimated references. A robust fitting rule limits the influence of extreme residuals, but it does <b>not</b> automatically guarantee that its reference is uniquely or strongly identified.",
            styles,
        )
    )
    story.append(p("Question A: When does standard inference work?", "h2", styles))
    story.append(
        p(
            "Under a fixed regular IID distribution - unique median and MAD, a unique Huber root, positive local curvature, adequate moments, and nondegenerate profiles - we derive the full influence function for the estimated profile correlation. This gives a pointwise central limit theorem, a consistent plug-in standard error, and asymptotically valid Wald inference.",
            "body",
            styles,
        )
    )
    story.append(
        box(
            "Current answer",
            "Yes, under regular identification. The theorem is <b>pointwise</b>: it applies to each fixed regular distribution. It does not promise uniform accuracy as the reference-fitting problem approaches degeneracy.",
            styles,
            PALE_TEAL,
            TEAL,
        )
    )
    story.append(p("Question B: How can the inference fail?", "h2", styles))
    story.append(
        p(
            "The most severe mechanism occurs when the population reference equation is nearly flat or has competing modes. Then a small random imbalance in the sample can make the fitted Huber reference jump from one region to another. Because every profile distance is measured from that fitted reference, one jump changes many radii at once. If the X and Y reference choices are coupled, the two fitted profiles can appear highly aligned even when the intended population profile effect is zero.",
            "body",
            styles,
        )
    )
    mechanism = Table(
        [
            [p("Small sampling imbalance", "flow_title", styles), p("→", "body_center", styles), p("Reference selects or moves toward a different mode", "flow_title", styles), p("→", "body_center", styles), p("Many fitted radii change together", "flow_title", styles), p("→", "body_center", styles), p("Misleading profile correlation and rejection", "flow_title", styles)],
        ],
        colWidths=[1.22 * inch, 0.25 * inch, 1.45 * inch, 0.25 * inch, 1.22 * inch, 0.25 * inch, 1.65 * inch],
    )
    mechanism.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), PALE_GOLD),
                ("BACKGROUND", (2, 0), (2, 0), PALE_RED),
                ("BACKGROUND", (4, 0), (4, 0), PALE_RED),
                ("BACKGROUND", (6, 0), (6, 0), PALE_RED),
                ("BOX", (0, 0), (0, 0), 0.6, GOLD),
                ("BOX", (2, 0), (2, 0), 0.6, RED),
                ("BOX", (4, 0), (4, 0), 0.6, RED),
                ("BOX", (6, 0), (6, 0), 0.6, RED),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    story.append(mechanism)
    story.append(Spacer(1, 5))
    story.append(
        box(
            "Why we believe this is the mechanism",
            "In the studied near-degenerate construction, severe rejection largely disappears when we hold the population reference fixed, and it also disappears when we force exact balance in the sample. It returns monotonically as the X and Y mode-selection decisions are made more strongly coupled. These are mechanism interventions, not proposed general corrections.",
            styles,
            PALE_GOLD,
            GOLD,
        )
    )
    story.append(p("Question C: Can proximity to failure be diagnosed?", "h2", styles))
    story.append(
        p(
            "Let J denote a standardized Jacobian for the median, MAD, and Huber reference system. Its smallest singular value measures the weakest local direction of identification. We study",
            "body",
            styles,
        )
    )
    story.append(
        box(
            "Conditioning index",
            "<b>I<sub>n</sub> = sqrt(n) sigma<sub>min</sub>(J).</b><br/><br/>Large I<sub>n</sub>: sampling noise is small relative to local identifying strength. Small or order-one I<sub>n</sub>: nuisance estimation can be strongly amplified. Across our simulation families, this index organizes much of the transition, but it does not fully predict it; root geometry, curvature, skewness, and tails still matter.",
            styles,
            PALE_BLUE,
            BLUE,
        )
    )
    story.append(p("What is already established, and what remains open", "h2", styles))
    status = Table(
        [
            [p("Established", "table_head", styles), p("Not yet established", "table_head", styles)],
            [
                p("Pointwise regular IID influence-function/Wald theory; a constructive switching failure; positive-affine invariance of the standardized index; substantial simulation validation.", "table", styles),
                p("Uniform validity near degeneracy; a universal cutoff for I<sub>n</sub>; a general repair; a formal weak-null permutation theorem; a complete explanation of strong-skew higher-order effects.", "table", styles),
            ],
        ],
        colWidths=[3.27 * inch, 3.27 * inch],
    )
    status.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), TEAL),
                ("BACKGROUND", (1, 0), (1, 0), RED),
                ("BACKGROUND", (0, 1), (0, 1), PALE_TEAL),
                ("BACKGROUND", (1, 1), (1, 1), PALE_RED),
                ("GRID", (0, 0), (-1, -1), 0.45, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(status)

    story.append(p("The Specific Question for Professor Hannig", "h1", styles))
    story.append(
        box(
            "The manuscript decision we need help making",
            "Is the paper complete and correctly framed with (i) a pointwise regular theorem, (ii) a constructive nonregular failure mechanism, and (iii) I<sub>n</sub> as an explanatory conditioning diagnostic? Or should it add an explicit local-to-degeneracy / triangular-array theory before presenting the boundary as a central contribution?",
            styles,
            PALE_GOLD,
            GOLD,
        )
    )
    story.append(p("Plain-language version", "h2", styles))
    story.append(
        p(
            "We understand what happens when the reference is comfortably stable, and we have a concrete example of what can go badly wrong when it is nearly unstable. We also have a numerical index that measures local stability. What we do not yet know is whether the paper should mathematically describe the entire transition between those two regimes, or whether it is more honest and useful to keep the index as a warning diagnostic and state clearly that it is incomplete.",
            "body",
            styles,
        )
    )
    story.append(p("Technical version", "h2", styles))
    story.append(
        box(
            "Primary question",
            "Is it statistically appropriate to present I<sub>n</sub> = sqrt(n) sigma<sub>min</sub>(J) as a first-order organizer of the loss of uniformity, while retaining only a pointwise theorem? Or would the paper need an explicit triangular-array result for sequences satisfying sqrt(n) sigma<sub>min</sub>(J<sub>n</sub>) = O(1)?",
            styles,
            PALE_BLUE,
            BLUE,
        )
    )
    story.append(p("What we specifically hope Professor Hannig can help with", "h2", styles))
    story.extend(
        bullets(
            [
                "<b>Conceptual label:</b> Should the phenomenon be called weak identification, nonregular M-estimation, unstable root selection, or something else?",
                "<b>Theory scope:</b> Is a pointwise theorem plus a constructive failure sufficient, or is a local asymptotic sequence essential for a convincing paper?",
                "<b>Diagnostic scope:</b> Is sigma<sub>min</sub>(J) a defensible first-order summary, or must a serious diagnostic also include global root separation and higher-order curvature?",
                "<b>Research direction:</b> Would a nonuniformity/impossibility result be more valuable than trying to calibrate a universal cutoff for I<sub>n</sub>?",
                "<b>Literature:</b> Which weak-identification, nonregular estimating-equation, or fiducial/likelihood references would best anchor this boundary?",
            ],
            styles,
        )
    )
    story.append(p("What we are not asking him to do", "h2", styles))
    story.extend(
        bullets(
            [
                "Review the entire manuscript or verify every median/MAD/Huber derivative.",
                "Choose among many simulation distributions.",
                "Provide a universal correction for all near-degenerate cases.",
            ],
            styles,
        )
    )
    story.append(p("Suggested 4-minute spoken route", "h2", styles))
    talk = Table(
        [
            [p("Time", "table_head", styles), p("What to say", "table_head", styles)],
            [p("0:00-1:00", "table", styles), p("The same paired units may stand out in two domains. We summarize standing out by distances from fitted robust references and correlate the two profiles.", "table", styles)],
            [p("1:00-2:00", "table", styles), p("Regularly identified references give standard influence-function inference. But near competing roots, a small sample imbalance can move the reference nonlocally and change many distances at once.", "table", styles)],
            [p("2:00-3:00", "table", styles), p("Our interventions isolate that switching mechanism. I<sub>n</sub> = sqrt(n) sigma<sub>min</sub>(J) orders much of the transition, but family effects remain.", "table", styles)],
            [p("3:00-4:00", "table", styles), p("Ask whether this should remain a pointwise theorem plus diagnostic, or whether the paper needs explicit local-to-degeneracy theory; then ask for terminology and one or two key references.", "table", styles)],
        ],
        colWidths=[1.0 * inch, 5.55 * inch],
        repeatRows=1,
    )
    talk.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE_GRAY]),
                ("GRID", (0, 0), (-1, -1), 0.45, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(talk)
    story.append(Spacer(1, 7))
    story.append(
        box(
            "If there is only time for one question",
            "Professor Hannig, does this look like a setting where a pointwise regular theorem plus a constructive nonregular failure is enough, or would you expect an explicit local asymptotic theory before treating sqrt(n) sigma<sub>min</sub>(J) as the organizing boundary?",
            styles,
            PALE_RED,
            RED,
        )
    )
    story.append(Spacer(1, 6))
    story.append(p("Prepared for a focused methodological discussion. This brief does not claim uniform validity, a universal diagnostic cutoff, or an automatic benefit from robust reference fitting.", "small", styles))

    doc.build(story)


if __name__ == "__main__":
    build_pdf()
