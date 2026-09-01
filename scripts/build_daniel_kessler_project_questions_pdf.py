from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
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
OUTPUT = ROOT / "output" / "pdf" / "daniel_kessler_project_questions_brief_20260831.pdf"

NAVY = colors.HexColor("#17324D")
BLUE = colors.HexColor("#2D6A8A")
TEAL = colors.HexColor("#247A78")
GOLD = colors.HexColor("#C18B2F")
RED = colors.HexColor("#A64B4B")
INK = colors.HexColor("#24313A")
MUTED = colors.HexColor("#56646F")
LINE = colors.HexColor("#CBD6DE")
PALE_BLUE = colors.HexColor("#EEF5F9")
PALE_TEAL = colors.HexColor("#EDF7F5")
PALE_GOLD = colors.HexColor("#FBF5E8")
PALE_RED = colors.HexColor("#FAEEEE")
PALE_GRAY = colors.HexColor("#F5F7F8")


def register_fonts():
    candidates = [
        ("/System/Library/Fonts/Supplemental/Arial.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    ]
    for regular, bold in candidates:
        if Path(regular).exists() and Path(bold).exists():
            pdfmetrics.registerFont(TTFont("BriefSans", regular))
            pdfmetrics.registerFont(TTFont("BriefSans-Bold", bold))
            return "BriefSans", "BriefSans-Bold"
    return "Helvetica", "Helvetica-Bold"


FONT, FONT_BOLD = register_fonts()


def make_styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "title", parent=base["Title"], fontName=FONT_BOLD, fontSize=22,
            leading=26, textColor=NAVY, alignment=TA_LEFT, spaceAfter=5,
        ),
        "subtitle": ParagraphStyle(
            "subtitle", parent=base["Normal"], fontName=FONT, fontSize=10.5,
            leading=14, textColor=MUTED, spaceAfter=14,
        ),
        "h1": ParagraphStyle(
            "h1", parent=base["Heading1"], fontName=FONT_BOLD, fontSize=14,
            leading=17, textColor=NAVY, spaceBefore=9, spaceAfter=6,
        ),
        "h2": ParagraphStyle(
            "h2", parent=base["Heading2"], fontName=FONT_BOLD, fontSize=11,
            leading=14, textColor=BLUE, spaceBefore=6, spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "body", parent=base["BodyText"], fontName=FONT, fontSize=9.5,
            leading=13.3, textColor=INK, spaceAfter=6,
        ),
        "small": ParagraphStyle(
            "small", parent=base["BodyText"], fontName=FONT, fontSize=8,
            leading=10.5, textColor=MUTED, spaceAfter=3,
        ),
        "box_title": ParagraphStyle(
            "box_title", parent=base["BodyText"], fontName=FONT_BOLD,
            fontSize=10, leading=12, textColor=NAVY, spaceAfter=3,
        ),
        "box_body": ParagraphStyle(
            "box_body", parent=base["BodyText"], fontName=FONT,
            fontSize=9.2, leading=12.7, textColor=INK,
        ),
        "table_head": ParagraphStyle(
            "table_head", parent=base["BodyText"], fontName=FONT_BOLD,
            fontSize=8.4, leading=10.5, textColor=colors.white,
        ),
        "table": ParagraphStyle(
            "table", parent=base["BodyText"], fontName=FONT,
            fontSize=8.3, leading=10.8, textColor=INK,
        ),
        "script": ParagraphStyle(
            "script", parent=base["BodyText"], fontName=FONT,
            fontSize=9.1, leading=13, textColor=INK, leftIndent=6, rightIndent=6,
        ),
        "footer": ParagraphStyle(
            "footer", parent=base["BodyText"], fontName=FONT,
            fontSize=7.2, leading=8, textColor=MUTED, alignment=TA_CENTER,
        ),
    }


def p(text, style, styles):
    return Paragraph(text, styles[style])


def box(title, body, styles, fill=PALE_BLUE, edge=BLUE):
    content = [p(title, "box_title", styles), p(body, "box_body", styles)]
    tbl = Table([[content]], colWidths=[6.45 * inch])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), fill),
        ("BOX", (0, 0), (-1, -1), 0.8, edge),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return tbl


def bullets(items, styles, style="body"):
    return [p(f"&bull; {item}", style, styles) for item in items]


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(doc.leftMargin, 0.48 * inch, letter[0] - doc.rightMargin, 0.48 * inch)
    canvas.setFont(FONT, 7.2)
    canvas.setFillColor(MUTED)
    canvas.drawString(doc.leftMargin, 0.29 * inch, "Discussion brief for Professor Daniel Kessler")
    canvas.drawRightString(letter[0] - doc.rightMargin, 0.29 * inch, f"Page {doc.page}")
    canvas.restoreState()


def build_pdf():
    styles = make_styles()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(
        str(OUTPUT), pagesize=letter,
        leftMargin=0.72 * inch, rightMargin=0.72 * inch,
        topMargin=0.67 * inch, bottomMargin=0.62 * inch,
        title="Robust-Reference Profile Inference: Questions for Daniel Kessler",
        author="Jialiang Yao",
        subject="Project overview and focused consultation questions",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
    doc.addPageTemplates([PageTemplate(id="main", frames=frame, onPage=header_footer)])
    story = []

    story.append(p("Robust-Reference Profile Inference", "title", styles))
    story.append(p("Big picture, the meaning of T_X and T_Y, and focused questions for Professor Daniel Kessler", "subtitle", styles))
    story.append(box(
        "The project in one sentence",
        "For paired observations, we ask whether the <b>same units stand out in two variables</b>, and then study whether inference for that profile similarity can be trusted when the reference locations used to define \"standing out\" are themselves learned from the same data.",
        styles, PALE_GOLD, GOLD,
    ))

    story.append(p("1. The scientific question", "h1", styles))
    story.append(p(
        "Suppose unit i has paired measurements (X<sub>i</sub>, Y<sub>i</sub>). Ordinary Pearson correlation asks whether high X tends to accompany high Y. Our target is different: <b>if unit i is unusually far from a typical X value, is the same unit also unusually far from a typical Y value?</b> Direction may differ; a unit can be high in X and low in Y but still stand out strongly in both.",
        "body", styles,
    ))

    story.append(p("2. What T_X and T_Y mean", "h1", styles))
    story.append(box(
        "Plain-language definition",
        "T<sub>X</sub> is the population's robust reference location for X, and T<sub>Y</sub> is the corresponding robust reference location for Y. Each is a statistical version of the variable's stable \"typical level.\" They are fitted separately because X and Y may have different units, centers, scales, skewness, and contamination. They are not required to be observed data points, and they are not thresholds that classify observations as outliers.",
        styles, PALE_TEAL, TEAL,
    ))
    story.append(p(
        "In the current implementation, each reference is a median/MAD-scaled Huber location. The median provides an initial center, the MAD provides a robust scale, and the Huber equation balances signed residuals while capping how strongly a very distant observation can pull the fitted location.",
        "body", styles,
    ))
    story.append(p(
        "The population quantities are written T<sub>X</sub> and T<sub>Y</sub>. Their sample estimates are written T-hat<sub>X</sub> and T-hat<sub>Y</sub>. This distinction is central: the paper's difficult inference problem comes from replacing stable population references by data-dependent fitted references.",
        "body", styles,
    ))

    definitions = Table([
        [p("Object", "table_head", styles), p("Meaning", "table_head", styles), p("Role", "table_head", styles)],
        [p("T<sub>X</sub>", "table", styles), p("Robust population reference for the marginal distribution of X", "table", styles), p("Defines how far an X observation stands from its typical level", "table", styles)],
        [p("T<sub>Y</sub>", "table", styles), p("Robust population reference for the marginal distribution of Y", "table", styles), p("Defines how far a Y observation stands from its typical level", "table", styles)],
        [p("T-hat<sub>X</sub>, T-hat<sub>Y</sub>", "table", styles), p("References estimated from the observed sample", "table", styles), p("Introduce shared, data-adaptive uncertainty into all fitted profile scores", "table", styles)],
        [p("|X - T<sub>X</sub>|, |Y - T<sub>Y</sub>|", "table", styles), p("Population distance or salience profiles", "table", styles), p("Discard direction and retain magnitude of departure", "table", styles)],
    ], colWidths=[1.18 * inch, 2.63 * inch, 2.65 * inch], repeatRows=1)
    definitions.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE_GRAY]),
        ("GRID", (0, 0), (-1, -1), 0.45, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(definitions)
    story.append(Spacer(1, 7))
    story.append(box(
        "Primary estimand",
        "<b>rho<sub>P</sub> = Corr(|X - T<sub>X</sub>|, |Y - T<sub>Y</sub>|).</b> A positive value means that the same units tend to be far from both references. A zero value means zero linear covariance between the two magnitude profiles; it does not imply that X and Y are independent.",
        styles,
    ))
    story.append(PageBreak())

    story.append(p("What Has Been Established, and What Remains Open", "title", styles))
    story.append(p("The paper is now about inferential reliability, not simply another new coefficient", "subtitle", styles))

    story.append(p("3. Relation to the original c-delta project", "h1", styles))
    story.append(box(
        "Original versus current target",
        "Original c-delta summarizes each unit by its root-mean-square distance from all other observations. In one-dimensional L2 form, that score collapses to a nonlinear function of distance from the sample mean plus a common variance floor. The current paper instead uses distance from a fitted robust marginal reference and focuses on inference for a specific paired magnitude-profile correlation, not a general distribution or dependence measure.",
        styles,
    ))

    story.append(p("4. Three current claims", "h1", styles))
    claims = [
        ("Regular pointwise validity", "Under a fixed regular IID law, a complete influence-function expansion accounts for the paired observations and the estimated median, MAD, and Huber references. Plug-in Wald inference is asymptotically valid."),
        ("Constructive finite-sample failure", "When the reference equation is nearly flat or has competing modes, small sample fluctuations can cause nonlocal reference switching. Because one fitted reference changes many profile distances at once, severe false correlation can result."),
        ("First-order conditioning", "I<sub>n</sub> = sqrt(n) sigma<sub>min</sub>(J) compares reference-identification strength with sampling noise and orders much of the simulated transition. It is explanatory, not yet a universal warning rule."),
    ]
    claim_table = Table(
        [[p(title, "box_title", styles), p(body, "table", styles)] for title, body in claims],
        colWidths=[1.75 * inch, 4.71 * inch],
    )
    claim_table.setStyle(TableStyle([
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [PALE_BLUE, PALE_RED, PALE_BLUE]),
        ("GRID", (0, 0), (-1, -1), 0.55, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(claim_table)

    story.append(p("5. Mechanism evidence", "h1", styles))
    evidence = Table([
        [p("Intervention", "table_head", styles), p("Observed result", "table_head", styles), p("Interpretation", "table_head", styles)],
        [p("Refit versus fixed population references", "table", styles), p("In a severe two-mode design, rejection was 0.777 versus 0.054 at n=80, and 0.541 versus 0.050 at n=640.", "table", styles), p("The distortion is created by fitted-reference movement, not by the intended fixed-reference target.", "table", styles)],
        [p("IID signs versus exact sign balance", "table", styles), p("Rejection fell from 0.766 to 0.058 at n=80 and from 0.535 to 0.060 at n=640.", "table", styles), p("Random imbalance selects a mode and couples the two fitted references.", "table", styles)],
        [p("Bridge families indexed by I<sub>n</sub>", "table", styles), p("Rejection declined from roughly 0.50-0.57 near I<sub>n</sub>=0.22 to roughly 0.03-0.05 near I<sub>n</sub>=1.74.", "table", styles), p("First-order conditioning organizes the transition, but matched-I family differences remain.", "table", styles)],
    ], colWidths=[1.68 * inch, 2.5 * inch, 2.28 * inch], repeatRows=1)
    evidence.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE_GRAY]),
        ("GRID", (0, 0), (-1, -1), 0.45, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(evidence)
    story.append(Spacer(1, 7))
    story.append(box(
        "Important limitation",
        "The Huber rule makes the <i>reference fitting</i> resistant to individual extreme residuals, but the final radii are uncapped. The full profile correlation is therefore not a globally bounded-influence robust correlation. The method also does not replace classical two-sample or general dependence tests.",
        styles, PALE_GOLD, GOLD,
    ))
    story.append(PageBreak())

    story.append(p("Focused Questions for Professor Kessler", "title", styles))
    story.append(p("The aim is one conceptual judgment and one useful direction, not a review of the full proof", "subtitle", styles))
    story.append(p(
        "Professor Kessler's work on selective inference and data-adaptive network analysis concerns inference after the data help determine the object being analyzed. Our problem is not automatically standard selective inference, but it has a related two-stage structure: the sample determines a reference or mode, and that fitted choice changes all downstream profile scores.",
        "body", styles,
    ))

    story.append(p("The main question", "h1", styles))
    story.append(box(
        "Question 1 - classification of the failure mechanism",
        "Is it technically useful to interpret nonlocal robust-reference switching as an implicit data-adaptive selection step that contaminates downstream profile inference, or would that analogy be misleading because the population reference functional itself becomes weakly identified or nonregular?",
        styles, PALE_GOLD, GOLD,
    ))

    story.append(p("High-priority follow-ups", "h1", styles))
    story.extend(bullets([
        "If the selection analogy is useful, what should the selection event be: the chosen root, the chosen mode, or a region of the reference parameter space?",
        "Would conditioning on a selected root answer a scientifically coherent question, or would it silently change the estimand from a marginal population reference to a sample-selected reference?",
        "Could sample splitting or data fission separate reference fitting from profile inference in a principled way? What validity would it recover, and what target or efficiency would it sacrifice?",
        "Should reference-selection frequency or bootstrap root instability accompany I_n as a diagnostic, even if neither is advertised as a correction?",
    ], styles, style="small"))

    story.append(p("What I would like help with", "h1", styles))
    help_table = Table([
        [p("Decision", "table_head", styles), p("Requested guidance", "table_head", styles)],
        [p("Correct conceptual category", "table", styles), p("Selective inference, nonregular M-estimation, generated-score inference, or a careful combination of these.", "table", styles)],
        [p("One feasible methodological extension", "table", styles), p("Sample splitting/fission, root-stability analysis, or a local-to-degeneracy result - whichever is most defensible and valuable.", "table", styles)],
        [p("Application and literature", "table", styles), p("How to define independent sampling units in a network application, avoid double-dipping, and identify one or two key references on learned structure.", "table", styles)],
    ], colWidths=[1.9 * inch, 4.56 * inch], repeatRows=1)
    help_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE_GRAY]),
        ("GRID", (0, 0), (-1, -1), 0.45, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(help_table)
    story.append(Spacer(1, 7))
    story.append(box(
        "Do not spend the meeting on",
        "The full influence-function algebra, every simulation family, or defending rho_P as a universal dependence measure. The useful outcome is one classification, warning, reference, or development path.",
        styles, PALE_RED, RED,
    ))
    story.append(PageBreak())

    story.append(p("Short-Conversation Plan", "title", styles))
    story.append(p("Lead with the target, show one mechanism, then ask one question", "subtitle", styles))

    story.append(p("If there are only 2-3 minutes", "h1", styles))
    story.append(box(
        "30-second project introduction",
        "I am working with Professor Hoorn on inference for a paired profile-correlation target. For each margin, T_X or T_Y is a robust typical location. We measure how far each unit is from its marginal reference and study rho_P, the correlation of those two distance profiles. Under regular identification, full influence-function inference works pointwise. The problem is that in nearly multimodal settings the fitted reference can switch nonlocally, changing many radii at once and creating severe false rejection.",
        styles,
    ))
    story.append(Spacer(1, 6))
    story.append(box(
        "Ask only this",
        "Would you view that reference switch as a form of implicit data selection requiring selective-inference ideas, or primarily as nonregular estimation of the reference functional? I am trying to decide which framing leads to a defensible next theoretical step.",
        styles, PALE_GOLD, GOLD,
    ))

    story.append(p("If there are 5-10 minutes", "h1", styles))
    short_plan = Table([
        [p("Time", "table_head", styles), p("What to discuss", "table_head", styles)],
        [p("0:00-1:00", "table", styles), p("State the paired salience question and explain T_X, T_Y, and rho_P without derivations.", "table", styles)],
        [p("1:00-2:30", "table", styles), p("Show only the refit-versus-fixed and exact-balance results to establish the reference-switching mechanism.", "table", styles)],
        [p("2:30-5:00", "table", styles), p("Ask the main classification question and whether conditioning, splitting, or fission is conceptually coherent.", "table", styles)],
        [p("5:00-8:00", "table", styles), p("If useful, discuss whether a generic generated-profile theorem or a network application would strengthen the paper.", "table", styles)],
        [p("Final minute", "table", styles), p("Ask for one key reference or permission to send a one-page figure and question after the meeting.", "table", styles)],
    ], colWidths=[1.15 * inch, 5.31 * inch], repeatRows=1)
    short_plan.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE_GRAY]),
        ("GRID", (0, 0), (-1, -1), 0.45, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(short_plan)

    story.append(PageBreak())
    story.append(p("Advance Email Memo", "title", styles))
    story.append(p("A concise note that can be sent before requesting a short conversation", "subtitle", styles))
    email = (
        "<b>Subject: Brief question on data-adaptive reference fitting and downstream inference</b><br/><br/>"
        "Dear Professor Kessler,<br/><br/>"
        "I am developing a methodological paper with Professor Hoorn on inference for paired robust-reference profiles. For each variable, we fit a robust marginal reference, form the distances |X_i - T-hat_X| and |Y_i - T-hat_Y|, and estimate the correlation between the two distance profiles. The scientific target is whether the same observational units stand out in both variables, rather than general dependence or equality of distributions.<br/><br/>"
        "Under regular identification, we have a complete influence-function expansion and pointwise Wald result. In a near-degenerate family, however, small sample fluctuations can move the fitted references between competing regions. This nonlocal switch changes many fitted distances simultaneously and can create severe false rejection. Fixed-reference and exact-balance interventions largely remove the distortion in the studied construction.<br/><br/>"
        "I would be very grateful for your view on one focused question: is this usefully interpreted as an implicit data-adaptive selection problem, or would that analogy be misleading because the reference functional itself becomes weakly identified? I am also interested in whether sample splitting/data fission or a stability diagnostic could add principled value. I can explain the target and mechanism in two minutes and do not expect a review of the full manuscript.<br/><br/>"
        "Best regards,<br/>Jialiang Yao"
    )
    email_box = Table([[p(email, "script", styles)]], colWidths=[6.45 * inch])
    email_box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALE_GRAY),
        ("BOX", (0, 0), (-1, -1), 0.65, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(email_box)
    story.append(Spacer(1, 7))
    story.append(p(
        "Context for tailoring: Daniel Kessler's listed interests include selective inference and statistical analysis of networks; a recent line of work studies inference after community detection on a single observed network. Sources: dankessler.me; Panigrahi, MacDonald, and Kessler, JMLR 24 (2023). Prepared August 31, 2026.",
        "small", styles,
    ))

    doc.build(story)
    print(OUTPUT)


if __name__ == "__main__":
    build_pdf()
