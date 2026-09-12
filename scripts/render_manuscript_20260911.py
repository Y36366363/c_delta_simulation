"""Render the integrated Markdown manuscript plus actual S1--S3 into one PDF.

Pandoc/pdflatex intermediates are written only to a temporary directory.
The scientific sources and the original Downloads PDF are never modified.
"""
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
INPUTS = ["manuscript_integrated_20260911.md", "supplement_S1_20260911.md",
          "supplement_S2_20260911.md", "supplement_S3_20260911.md",
          "manuscript_references_20260911.md"]
OUT = ROOT / "output/pdf/rho_p_integrated_20260911.pdf"


def main():
    for executable in ("pandoc", "pdflatex"):
        if shutil.which(executable) is None:
            raise RuntimeError(f"Missing rendering dependency: {executable}")
    header = r"""
\usepackage{url}
\def\UrlBreaks{\do\/\do\_\do\-\do\.}
\usepackage{etoolbox}
\setlength{\emergencystretch}{3em}
\setlength{\tabcolsep}{3pt}
\AtBeginEnvironment{longtable}{\small}
\hypersetup{colorlinks=true,linkcolor=blue,urlcolor=blue}
"""
    content=[]
    for name in INPUTS:
        text=(ROOT/"docs"/name).read_text()
        if name.startswith("supplement_"):
            key=name.split("_")[1].lower()
            text=text.replace("\n",f" {{#{key}}}\n",1)
        for key in ("S1","S2","S3"):
            text=text.replace(f"(supplement_{key}_20260911.md)",f"(#{key.lower()})")
        text=text.replace(r"\[", "$$").replace(r"\]", "$$")
        text=text.replace(r"\(", "$").replace(r"\)", "$")
        # Code paths can wrap at underscores and slashes in the PDF.
        text=re.sub(r"`([^`\n]+)`",lambda m:
                    r"\path{"+m.group(1)+"}" if " " not in m.group(1) else m.group(0),text)
        text=text.replace("../figures/",str(ROOT/"figures")+"/")
        # Keep each table's prose caption and rows together when they fit a page.
        def reserve_table(match):
            caption, block = match.groups()
            return (r"\TableBoxStart"+"\n\n"
                    +caption+block+"\n\n"+r"\TableBoxEnd"+"\n")
        text=re.sub(r"(\*\*Table [\s\S]*?)(<!-- table:[a-z_]+ -->[\s\S]*?<!-- /table:[a-z_]+ -->)",reserve_table,text)
        text=re.sub(r"!\[([^\]]+)\]\(([^)]+)\)",
                    lambda m:f"![]({m.group(2)})\n\n**{m.group(1)}**",text)
        text=text.replace("–","--").replace("—","---")
        content.append(text)
    OUT.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="rho_p_typeset_") as tmp:
        tmp=Path(tmp)
        (tmp/"header.tex").write_text(header)
        # The short supplement directory at the end of the main manuscript
        # shares its page with S1; subsequent supplements start new pages.
        combined=content[0]+"\n\n\\bigskip\n\n"+content[1]
        (tmp/"paper.md").write_text("\n\n\\clearpage\n\n".join([combined]+content[2:]))
        subprocess.run(["pandoc",str(tmp/"paper.md"),"--from=markdown+tex_math_single_backslash-implicit_figures",
                        "--standalone","--include-in-header",str(tmp/"header.tex"),
                        "-V","geometry:margin=0.9in","-V","fontsize:11pt",
                        "-V","papersize:letter","-t","latex",
                        "-o",str(tmp/"paper.tex")],check=True,cwd=tmp)
        # Captioned tables fit on one page. Use natural-height boxes rather
        # than estimating their space; leave the source ledger multipage.
        latex=(tmp/"paper.tex").read_text()
        latex=latex.replace(r"\TableBoxStart",r"\par\noindent\begin{minipage}{\linewidth}")
        latex=latex.replace(r"\TableBoxEnd",r"\end{minipage}\par\medskip")
        def boxed_table(match):
            block=match.group(0)
            block=block.replace(r"\begin{longtable}[]",r"\begin{center}\small\begin{tabular}")
            block=block.replace(r"\endhead","")
            return block.replace(r"\end{longtable}",r"\end{tabular}\end{center}")
        latex=re.sub(r"\\begin\{minipage\}[\s\S]*?\\end\{minipage\}",boxed_table,latex)
        (tmp/"paper.tex").write_text(latex)
        for _ in range(2):
            result=subprocess.run(["pdflatex","-interaction=nonstopmode","-halt-on-error","paper.tex"],
                                  cwd=tmp,capture_output=True,text=True)
            if result.returncode:
                shutil.copy(tmp/"paper.tex",Path(tempfile.gettempdir())/"rho_p_render_failure.tex")
                raise RuntimeError(result.stdout[-3500:])
        log=(tmp/"paper.log").read_text(errors="replace")
        warnings=[line for line in log.splitlines() if "Overfull" in line]
        print("Overfull boxes:",len(warnings))
        if warnings:
            print("\n".join(warnings))
        shutil.copy(tmp/"paper.pdf",OUT)
    print(OUT)


if __name__=="__main__":
    main()
