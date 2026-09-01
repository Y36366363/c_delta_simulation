from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
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
OUTPUT = ROOT / "output" / "pdf" / "unc_stor_faculty_consultation_guide_20260831.pdf"

NAVY = colors.HexColor("#183153")
BLUE = colors.HexColor("#275D8C")
PALE_BLUE = colors.HexColor("#EAF2F8")
PALE_GOLD = colors.HexColor("#FFF5DA")
PALE_GREEN = colors.HexColor("#EAF5EF")
INK = colors.HexColor("#202A33")
MUTED = colors.HexColor("#607080")
LINE = colors.HexColor("#CCD6DF")
WHITE = colors.white


def register_fonts() -> None:
    pdfmetrics.registerFont(
        TTFont("ArialUnicode", "/System/Library/Fonts/Supplemental/Arial Unicode.ttf")
    )


def styles():
    base = getSampleStyleSheet()
    return {
        "cover_title": ParagraphStyle(
            "cover_title",
            parent=base["Title"],
            fontName="ArialUnicode",
            fontSize=25,
            leading=34,
            textColor=NAVY,
            alignment=TA_CENTER,
            spaceAfter=14,
        ),
        "cover_sub": ParagraphStyle(
            "cover_sub",
            parent=base["Normal"],
            fontName="ArialUnicode",
            fontSize=12.5,
            leading=19,
            textColor=MUTED,
            alignment=TA_CENTER,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontName="ArialUnicode",
            fontSize=16.5,
            leading=21,
            textColor=NAVY,
            spaceBefore=4,
            spaceAfter=6,
            keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontName="ArialUnicode",
            fontSize=11.8,
            leading=15.5,
            textColor=BLUE,
            spaceBefore=7,
            spaceAfter=3,
            keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["BodyText"],
            fontName="ArialUnicode",
            fontSize=9.2,
            leading=13.2,
            textColor=INK,
            spaceAfter=3,
        ),
        "small": ParagraphStyle(
            "small",
            parent=base["BodyText"],
            fontName="ArialUnicode",
            fontSize=8,
            leading=10.5,
            textColor=MUTED,
            spaceAfter=4,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            parent=base["BodyText"],
            fontName="ArialUnicode",
            fontSize=8.5,
            leading=11.8,
            leftIndent=14,
            firstLineIndent=-8,
            bulletIndent=4,
            textColor=INK,
            spaceAfter=2,
        ),
        "callout": ParagraphStyle(
            "callout",
            parent=base["BodyText"],
            fontName="ArialUnicode",
            fontSize=8.8,
            leading=12.4,
            textColor=INK,
            leftIndent=10,
            rightIndent=10,
            spaceBefore=2,
            spaceAfter=2,
        ),
        "email": ParagraphStyle(
            "email",
            parent=base["BodyText"],
            fontName="ArialUnicode",
            fontSize=7.8,
            leading=10.8,
            textColor=INK,
            spaceAfter=3,
        ),
        "table_head": ParagraphStyle(
            "table_head",
            parent=base["BodyText"],
            fontName="ArialUnicode",
            fontSize=9.2,
            leading=13,
            textColor=WHITE,
            alignment=TA_LEFT,
        ),
        "table": ParagraphStyle(
            "table",
            parent=base["BodyText"],
            fontName="ArialUnicode",
            fontSize=8.8,
            leading=13,
            textColor=INK,
        ),
    }


def header_footer(canvas, doc):
    canvas.saveState()
    width, height = letter
    if doc.page > 1:
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.5)
        canvas.line(0.7 * inch, height - 0.54 * inch, width - 0.7 * inch, height - 0.54 * inch)
        canvas.setFont("ArialUnicode", 8.3)
        canvas.setFillColor(MUTED)
        canvas.drawString(0.7 * inch, height - 0.40 * inch, "UNC STOR 教授咨询使用手册")
        canvas.drawRightString(width - 0.7 * inch, 0.42 * inch, f"{doc.page}")
    canvas.restoreState()


def p(text, style, s):
    return Paragraph(text, s[style])


def bullets(items, s):
    return [Paragraph("• " + item, s["bullet"]) for item in items]


def callout(title, text, s, color=PALE_BLUE):
    data = [[p(f"<b>{title}</b>", "callout", s)], [p(text, "callout", s)]]
    table = Table(data, colWidths=[6.55 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), color),
                ("BOX", (0, 0), (-1, -1), 0.7, BLUE),
                ("LINEBELOW", (0, 0), (-1, 0), 0.35, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return table


def professor_page(
    story,
    s,
    rank,
    name,
    role,
    why,
    primary,
    backups,
    avoid,
    subject,
    email_paragraphs,
):
    story.append(p(f"{rank}. {name}", "h1", s))
    story.append(p(role, "small", s))
    story.append(p("为什么找这位老师", "h2", s))
    story.append(p(why, "body", s))
    story.append(callout("如果只有 5–10 分钟，只问这一题", primary, s, PALE_GOLD))
    story.append(p("时间允许时的备用问题", "h2", s))
    story.extend(bullets(backups, s))
    story.append(p("短谈中不要展开", "h2", s))
    story.extend(bullets(avoid, s))
    story.append(p("可提前发送的英文 memo", "h2", s))
    story.append(callout("Subject", subject, s, PALE_GREEN))
    for para in email_paragraphs:
        story.append(p(para, "email", s))
    story.append(PageBreak())


def build_pdf() -> None:
    register_fonts()
    s = styles()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    doc = BaseDocTemplate(
        str(OUTPUT),
        pagesize=letter,
        rightMargin=0.72 * inch,
        leftMargin=0.72 * inch,
        topMargin=0.72 * inch,
        bottomMargin=0.65 * inch,
        title="UNC STOR 教授咨询使用手册",
        author="Jialiang Yao",
        subject="Faculty consultation plan and advance memos",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
    doc.addPageTemplates([PageTemplate(id="main", frames=frame, onPage=header_footer)])

    story = []
    story.append(Spacer(1, 1.05 * inch))
    story.append(p("UNC STOR 教授咨询使用手册", "cover_title", s))
    story.append(p("项目介绍、短谈策略、核心问题与可直接发送的英文 memo", "cover_sub", s))
    story.append(Spacer(1, 0.45 * inch))
    cover_box = Table(
        [
            [p("项目", "table_head", s), p("Trustworthy Inference for Robust-Reference Divergence Profiles", "table", s)],
            [p("建议顺序", "table_head", s), p("Jan Hannig → Kai Zhang → Daniel Kessler → Richard L. Smith", "table", s)],
            [p("使用原则", "table_head", s), p("先用一分钟介绍项目，再集中讨论一个会影响论文决策的问题。", "table", s)],
            [p("准备日期", "table_head", s), p("2026-08-31", "table", s)],
        ],
        colWidths=[1.1 * inch, 5.35 * inch],
    )
    cover_box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), NAVY),
                ("BACKGROUND", (1, 0), (1, -1), colors.HexColor("#F5F8FB")),
                ("GRID", (0, 0), (-1, -1), 0.5, LINE),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(cover_box)
    story.append(Spacer(1, 0.5 * inch))
    story.append(p("说明：本手册不以请求老师审阅整篇论文为目标，而以获得一个明确判断、一条关键文献或一次后续交流机会为目标。", "cover_sub", s))
    story.append(PageBreak())

    story.append(p("快速使用页", "h1", s))
    story.append(p("推荐联系顺序", "h2", s))
    quick_data = [
        [p("老师", "table_head", s), p("最适合解决的决策", "table_head", s), p("短谈目标", "table_head", s)],
        [p("Jan Hannig", "table", s), p("是否需要 local-to-degeneracy 理论；I_n 如何定位", "table", s), p("得到理论范围判断或关键文献", "table", s)],
        [p("Kai Zhang", "table", s), p("estimand 与一般 dependence test 的边界；permutation 的角色", "table", s), p("确定论文定位与展示方式", "table", s)],
        [p("Daniel Kessler", "table", s), p("reference switching 是否可解释为 data-adaptive selection", "table", s), p("判断该类比是否成立", "table", s)],
        [p("Richard L. Smith", "table", s), p("strong-skew 下的非对称慢收敛如何报告", "table", s), p("控制高阶理论扩展的范围", "table", s)],
    ]
    quick = Table(quick_data, colWidths=[1.15 * inch, 3.15 * inch, 2.25 * inch], repeatRows=1)
    quick.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F8FB")]),
                ("GRID", (0, 0), (-1, -1), 0.45, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(quick)
    story.append(p("一分钟英文项目介绍", "h2", s))
    intro = (
        "I am working with Professor Hoorn on a separate methodological paper about inference for paired "
        "robust-reference divergence profiles. For paired IID observations, we fit a median/MAD-scaled Huber "
        "reference in each margin and study <i>rho</i><sub>P</sub> = Corr(|X - T<sub>X</sub>|, |Y - T<sub>Y</sub>|). "
        "Under regular identification, I have derived a complete influence-function expansion and plug-in Wald "
        "inference. The main difficulty is that poorly conditioned reference equations can lead to nonlocal fitted-"
        "reference switching and severe finite-sample distortion. The quantity I<sub>n</sub> = sqrt(n) "
        "sigma<sub>min</sub>(J) orders much of this transition, but higher-order family effects remain. I am now "
        "deciding how formally to develop this boundary and how to present the diagnostic without overstating it."
    )
    story.append(callout("60-second introduction", intro, s))
    story.append(p("只携带三项材料", "h2", s))
    story.extend(
        bullets(
            [
                "rho_P 的定义，以及一句话说明它不同于原始 all-to-all c_d。",
                "regular pointwise theorem，以及它在 sqrt(n) sigma_min(J) = O(1) 时不具有 uniformity 的一句说明。",
                "一张 fitted-reference 与 fixed-reference 对照图；有空间时再标出 I_n。",
            ],
            s,
        )
    )
    story.append(callout("短谈目标", "得到一个判断、一条文献或发送一页 memo 的许可；不要讲完整模拟历史。", s, PALE_GREEN))
    story.append(PageBreak())

    professor_page(
        story,
        s,
        1,
        "Jan Hannig",
        "首选议题：弱/非正则识别、局部渐近与 conditioning index",
        "最重要的价值是判断：当前的 pointwise theorem、constructive failure 与 I_n 诊断是否已经构成完整论文，还是必须加入正式的 local-to-degeneracy / triangular-array 理论。",
        "Is it statistically appropriate to present I<sub>n</sub> = sqrt(n) sigma<sub>min</sub>(J) as an explanatory conditioning diagnostic separating regular pointwise behavior from a nonuniform boundary, or would a convincing paper need an explicit triangular-array or local-to-degeneracy theorem?",
        [
            "“Weakly identified robust reference” 是否合适，还是应称为 nonregular root selection？",
            "最小奇异值是否足够，还是 formal diagnostic 必须显式包含 curvature 与 root separation？",
            "与其校准统一 cutoff，是否更值得给出 nonuniformity 或 impossibility proposition？",
            "哪些 weak-identification 或 nonregular M-estimation 文献最应该作为锚点？",
        ],
        ["完整的 median/MAD influence-function 代数。", "每一种 bridge distribution。", "Permutation inference，除非老师主动提起。"],
        "Brief methodological question on nonregular reference fitting",
        [
            "Dear Professor Hannig,",
            "I am developing a methodological paper with Professor Hoorn on inference for similarity of paired robust-reference profiles. For paired IID data, the primary estimand is rho<sub>P</sub> = Corr(|X - T<sub>X</sub>|, |Y - T<sub>Y</sub>|), where each T is a median/MAD-scaled Huber location functional.",
            "Under fixed regular laws, I have derived a complete influence-function expansion and plug-in studentized Wald result. The main finite-sample issue appears near weak reference identification: shallow or competing roots can cause nonlocal fitted-reference switching and severe distortion. The standardized quantity I<sub>n</sub> = sqrt(n) sigma<sub>min</sub>(J) naturally measures first-order nuisance conditioning and orders much of the simulated transition, although family-specific higher-order effects remain.",
            "I am trying to decide whether the paper should retain I<sub>n</sub> as an explanatory diagnostic alongside a pointwise theorem and constructive failure example, or whether it needs an explicit local-to-degeneracy or triangular-array theory. If you had a few minutes, I would be very grateful for your view on that specific question and on the appropriate terminology or literature for this boundary. I can bring a one-page summary and do not expect a review of the full manuscript.",
            "Best regards,<br/>Jialiang Yao",
        ],
    )

    professor_page(
        story,
        s,
        2,
        "Kai Zhang",
        "第二优先议题：profile correlation 的定位与 permutation 边界",
        "最重要的价值是避免论文被理解为又一个通用 dependence coefficient，并确认 rho_P = 0、independence 与 label exchangeability 的区别以及 Wald/permutation 的正确分工。",
        "Does the paper have a sufficiently distinct statistical target if it is framed as inference for paired robust-reference profile correlation rather than as a general dependence measure, and is it correct to keep permutation analysis secondary to the IID influence-function Wald theory?",
        [
            "是否需要把 rho_P 与广义 independence tests 系统比较，还是这会模糊 estimand-specific 问题？",
            "rho_P = 0、independence 和 label exchangeability 的区别是否需要更强地强调？",
            "C - 1 与 rho_P 的 fixed-margin permutation ordering 等价，应放主文还是补充材料？",
            "只有 group invariance 才保证 exactness 时，studentized permutation 是否还应保留在主模拟中？",
            "什么样的真实数据 illustration 才不是装饰性的？",
        ],
        ["Empirical-process 条件。", "完整 nuisance Jacobian。", "要求老师在很多模拟分布中替你挑选。"],
        "Brief question on positioning a paired profile-correlation estimand",
        [
            "Dear Professor Zhang,",
            "I am developing a separate methodological paper with Professor Hoorn on a paired-data question: whether the same observational units are relatively far from robust references in two margins. The primary estimand is rho<sub>P</sub> = Corr(|X - T<sub>X</sub>|, |Y - T<sub>Y</sub>|), with median/MAD-scaled Huber references. The paper is not intended to introduce a general-purpose dependence coefficient. Its focus is when inference for this particular paired profile similarity is reliable and how unstable reference fitting can create misleading finite-sample results.",
            "The regular theory uses a complete influence-function Wald statistic. We also have fully recomputed studentized-permutation evidence, but exact randomization validity requires group invariance and does not follow merely from the weak null rho<sub>P</sub> = 0.",
            "I would value your opinion on one focused issue: whether this estimand is positioned clearly enough relative to general dependence testing, and whether the Wald/permutation separation is the right presentation. If you had a few minutes, I could show the estimand, one theorem statement, and one simulation figure on a single page.",
            "Best regards,<br/>Jialiang Yao",
        ],
    )

    professor_page(
        story,
        s,
        3,
        "Daniel Kessler",
        "第三优先议题：data-adaptive construction、selection analogy 与应用设计",
        "有用的联系不是把问题直接归入传统 post-selection inference，而是判断同一数据先确定 reference/mode、再构造用于推断的 profile，这一过程能否用隐式 selection 机制解释。",
        "Is it useful and technically defensible to interpret nonlocal robust-reference switching as a data-adaptive selection step that contaminates downstream profile inference, or would that analogy mislead readers because the target functional itself changes nonregularly?",
        [
            "Selection frequency 或 stability diagnostic 能否补充 I_n，而不被误解为修复方法？",
            "Sample splitting 是否仅在概念上有帮助，尽管它会改变 estimator？",
            "如果使用 network application，独立 sampling unit 应如何界定？",
            "Fitted-versus-fixed reference intervention 是否足以被理解为 mechanism experiment？",
        ],
        ["要求核查全部 influence-function 计算。", "把项目直接称为标准 selective inference。", "在 sampling units 未明确前承诺 network data。"],
        "Brief question on data-adaptive reference fitting and downstream inference",
        [
            "Dear Professor Kessler,",
            "I am working with Professor Hoorn on a methodological paper about paired robust-reference profiles. We fit a robust marginal reference in each variable, form the radii |X<sub>i</sub> - T-hat<sub>X</sub>| and |Y<sub>i</sub> - T-hat<sub>Y</sub>|, and estimate their correlation.",
            "Under regular identification, complete influence-function inference is asymptotically valid. In a near-degenerate family, however, small sample fluctuations can select substantially different reference roots. The resulting nonlocal switch changes many fitted radii simultaneously and can create severe false rejection. Fixed-reference and exact-balance counterfactuals largely remove the distortion in the studied construction.",
            "I would appreciate your view on whether this is usefully interpreted as an implicit data-adaptive selection problem, or whether that analogy would be technically misleading because the instability belongs to the target functional itself. A related question is whether a stability diagnostic or a carefully chosen network application would add value. I can summarize the mechanism in one figure if you have a few minutes.",
            "Best regards,<br/>Jialiang Yao",
        ],
    )

    professor_page(
        story,
        s,
        4,
        "Richard L. Smith",
        "专项议题：strong-skew 下的非对称慢收敛",
        "该问题应与 reference switching 分开。Strong-skew stress model 中，即使使用 population reference，studentized tails 仍明显不对称，更像高阶 bias、self-normalization 或 tail approximation 问题。",
        "When a pointwise asymptotic normal result is valid and the reported standard error is already close to the empirical standard deviation, but the studentized statistic retains strongly asymmetric tails, what is the most defensible way to analyze and report the slow convergence without starting an unnecessary full Edgeworth project?",
        [
            "Tail regular variation 或 moment/skewness summaries 是否比继续增加命名分布更有价值？",
            "Sample-size trajectory 加 studentized quantiles 是否足以支持 pointwise-but-slow warning？",
            "Absolute-residual profile 的 self-normalized statistics 应参考哪类高阶展开？",
            "是否应把 strong-skew 现象留作局限，并与 I_n conditioning 故事严格分开？",
        ],
        ["整篇论文结构。", "Permutation analysis。", "寻求统一的 heavy-tail correction。"],
        "Brief question on asymmetric slow convergence under strong skew",
        [
            "Dear Professor Smith,",
            "I am developing a methodological paper with Professor Hoorn on inference for correlation between paired distances from fitted robust references. The estimator has a pointwise IID influence-function central limit theorem under regular conditions.",
            "One stress model exhibits a persistent finite-sample phenomenon that is separate from weak reference identification. At n = 2560, the average estimated standard error is already close to the empirical standard deviation, but the studentized 2.5% and 97.5% quantiles remain substantially asymmetric and the nominal 5% rejection rate remains elevated. Replacing fitted references with population references gives nearly the same result.",
            "I would be grateful for your view on how best to characterize this: as a higher-order skewness/self-normalization problem, a tail-approximation problem, or simply a documented slow-convergence boundary. In particular, I would like to avoid claiming more than the evidence supports or beginning a large expansion that is unnecessary for the paper. I can bring one compact table of standard-error ratios and studentized quantiles.",
            "Best regards,<br/>Jialiang Yao",
        ],
    )

    story.append(p("谈话时间模板", "h1", s))
    timing_data = [
        [p("可用时间", "table_head", s), p("结构", "table_head", s), p("结束时应获得", "table_head", s)],
        [p("3–5 分钟", "table", s), p("一分钟简介 → 一句 tension → 一个主问题", "table", s), p("判断、文献或发送 memo 的许可", "table", s)],
        [p("10–15 分钟", "table", s), p("简介 → 一个 theorem block → 一张 figure → 主问题 + 一个备用问题", "table", s), p("明确一个 manuscript decision", "table", s)],
        [p("20–30 分钟", "table", s), p("2 分钟问题背景；4 分钟 estimand/theorem；5 分钟机制；4 分钟 I_n；余下问答", "table", s), p("范围判断、文献与可能的 follow-up", "table", s)],
    ]
    timing = Table(timing_data, colWidths=[1.05 * inch, 3.75 * inch, 1.75 * inch], repeatRows=1)
    timing.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F8FB")]),
                ("GRID", (0, 0), (-1, -1), 0.45, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    story.append(timing)
    story.append(p("三五分钟时的结束语", "h2", s))
    story.append(callout("Suggested closing", "I do not want to take more of your time. Even a quick judgment on whether this framing is defensible—or one reference I should read—would be very helpful. May I send you the one-page summary?", s, PALE_GOLD))
    story.append(p("谈后立即记录", "h2", s))
    story.extend(
        bullets(
            [
                "老师明确接受或质疑了哪一条 claim。",
                "建议阅读的作者、论文或关键词。",
                "这次意见将改变哪一个 manuscript decision。",
                "是否需要发送 follow-up memo，以及承诺发送什么。",
            ],
            s,
        )
    )
    story.append(p("最终建议", "h2", s))
    story.append(p("先找 Hannig，只讨论是否需要 local-to-degeneracy 理论；Wald/permutation 展示压缩后再找 Kai Zhang；只有在发展 selection 解释或 network application 时找 Kessler；Smith 仅处理 strong-skew 的独立慢收敛现象。获得一个明确的判断，比获得四个笼统反应更有价值。", "body", s))

    doc.build(story)


if __name__ == "__main__":
    build_pdf()
