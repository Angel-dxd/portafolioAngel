"""
CV Generator — Angel Xavier Pons Márquez
Bilingual: generates cv_es.pdf and cv_en.pdf
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate,
                                 Paragraph, Spacer, FrameBreak, Image,
                                 HRFlowable, Flowable)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage

# ── Paths ──────────────────────────────────────────────────────────────────
OUT_ES   = "/Users/angelxavier/portafolioAngel/cv/cv_es.pdf"
OUT_EN   = "/Users/angelxavier/portafolioAngel/cv/cv_en.pdf"
PHOTO    = "/Users/angelxavier/portafolioAngel/img/foto_clean.png"
# Using standard ReportLab Helvetica font

# ── Colors ─────────────────────────────────────────────────────────────────
NAVY    = HexColor("#0d1f35")
SIDEBAR = HexColor("#091729")
ACCENT  = HexColor("#3b82f6")
LIGHT   = HexColor("#e2e8f0")
MUTED   = HexColor("#94a3b8")
DARK    = HexColor("#475569")
WHITE   = HexColor("#ffffff")
PILL_BG = HexColor("#1e3a5f")
SEP     = HexColor("#1e3555")

# ── Layout ─────────────────────────────────────────────────────────────────
W, H    = A4
SB_W    = 68 * mm
MAIN_W  = W - SB_W
PAD_OUT = 9 * mm
PAD_IN  = 7 * mm

# ── Style helper ───────────────────────────────────────────────────────────
def S(name, size=9, color=WHITE, bold=False, align=TA_LEFT, leading=None):
    return ParagraphStyle(name, fontName="Helvetica-Bold" if bold else "Helvetica",
                          fontSize=size, textColor=color,
                          leading=leading or size * 1.45,
                          alignment=align, spaceBefore=0, spaceAfter=0)

sNAME  = S("name",  24, WHITE,  bold=True,  leading=28)
sTITLE = S("title", 11, ACCENT, leading=16)
sSEC   = S("sec",    7, ACCENT, bold=True,  leading=10)
sBODY  = S("body",  8.5, LIGHT, leading=13)
sMUTED = S("muted",  8, MUTED,  leading=12)
sJOB   = S("job",    9, WHITE,  bold=True,  leading=13)
sDATE  = S("date",  7.5, ACCENT, leading=11)
sBUL   = S("bul",   8.5, LIGHT,  leading=13)
sPROJ  = S("proj",   9, ACCENT, bold=True,  leading=13)
sCONT  = S("cont",  7.5, LIGHT,  leading=11)

# ── Pill Flowable ──────────────────────────────────────────────────────────
class Pill(Flowable):
    PX, PY, R, FS = 5, 3, 3, 7
    def __init__(self, text, bg=PILL_BG, fg=LIGHT):
        from reportlab.pdfbase.pdfmetrics import stringWidth
        self.text = text; self.bg = bg; self.fg = fg
        self.width  = stringWidth(text, "Helvetica", self.FS) + self.PX * 2
        self.height = self.FS + self.PY * 2
    def draw(self):
        c = self.canv
        c.setFillColor(self.bg)
        c.roundRect(0, 0, self.width, self.height, self.R, fill=1, stroke=0)
        c.setFillColor(self.fg)
        c.setFont("Helvetica", self.FS)
        c.drawString(self.PX, self.PY + 0.5, self.text)

class PillRow(Flowable):
    GX, GY = 4, 4
    def __init__(self, tags, cw, bg=PILL_BG, fg=LIGHT):
        self.pills = [Pill(t, bg, fg) for t in tags]
        self.cw    = cw
        self._rows = self._layout()
        ph = self.pills[0].height if self.pills else 10
        self.width  = cw
        self.height = ph * len(self._rows) + self.GY * (len(self._rows) - 1) + 1
    def _layout(self):
        rows, row, x = [], [], 0
        for p in self.pills:
            if x + p.width > self.cw and row:
                rows.append(row); row = []; x = 0
            row.append((x, p)); x += p.width + self.GX
        if row: rows.append(row)
        return rows
    def draw(self):
        ph = self.pills[0].height if self.pills else 10
        y  = self.height - ph
        for row in self._rows:
            for (x, pill) in row:
                self.canv.saveState()
                self.canv.translate(x, y)
                pill.canv = self.canv; pill.draw()
                self.canv.restoreState()
            y -= ph + self.GY

# ── Section heading ────────────────────────────────────────────────────────
def sec(title):
    return [Spacer(1, 3.5*mm),
            Paragraph(title.upper(), sSEC),
            HRFlowable(width="100%", thickness=0.4, color=SEP, spaceAfter=3)]

def bul(text):
    return Paragraph(f"\u2022\u2002{text}", sBUL)

# ── Background painter ─────────────────────────────────────────────────────
class CVDoc(BaseDocTemplate):
    def __init__(self, filename):
        super().__init__(filename, pagesize=A4,
                         leftMargin=0, rightMargin=0, topMargin=0, bottomMargin=0)
        sb = Frame(0, 0, SB_W, H, leftPadding=PAD_OUT, rightPadding=PAD_IN,
                   topPadding=PAD_OUT, bottomPadding=PAD_OUT, id="sb")
        mn = Frame(SB_W, 0, MAIN_W, H, leftPadding=PAD_IN, rightPadding=PAD_OUT,
                   topPadding=PAD_OUT, bottomPadding=PAD_OUT, id="mn")
        self.addPageTemplates([PageTemplate(id="cv", frames=[sb, mn], onPage=self._bg)])

    def _bg(self, canvas, doc):
        canvas.saveState()
        canvas.setFillColor(SIDEBAR)
        canvas.rect(0, 0, SB_W, H, fill=1, stroke=0)
        canvas.setFillColor(NAVY)
        canvas.rect(SB_W, 0, MAIN_W, H, fill=1, stroke=0)
        canvas.setStrokeColor(SEP)
        canvas.setLineWidth(0.5)
        canvas.line(SB_W, PAD_OUT, SB_W, H - PAD_OUT)
        canvas.restoreState()

# ── Content (bilingual) ────────────────────────────────────────────────────
CONTENT = {
    "es": dict(
        title      = "Desarrollador Fullstack",
        sec_contact= "Contacto",
        sec_skills = "Competencias",
        sec_langs  = "Idiomas",
        sec_other  = "Otros",
        sec_about  = "Sobre mí",
        sec_exp    = "Experiencia",
        sec_proj   = "Proyectos",
        sec_edu    = "Educación",
        about      = ("Desarrollador fullstack recién graduado en DAM, especializado en "
                      "<b>backend</b>. Experiencia real en producción con Node.js, TypeScript, "
                      "Docker y Kubernetes. Formación en Contabilidad y Finanzas que me permite "
                      "construir software con visión de negocio. "
                      '<font color="#3b82f6"><b>Disponible de inmediato.</b></font>'),
        available  = "Disponible de inmediato",
        license    = "Carnet de conducir · Vehículo propio",
        internship = "Prácticas",
        jobs = [
            dict(
                role    = "Desarrollador Fullstack",
                company = "Onna Digital",
                badge   = "Prácticas",
                date    = "Nov 2025 – Mar 2026",
                bullets = [
                    "Desarrollé <b>Contract Manager</b>: app web de gestión de contratos "
                    "con doble rol Admin/Cliente integrada con Dolibarr ERP vía API REST",
                    "Gestioné pods, Helm charts y clústeres <b>Kubernetes</b> mediante FreeLens",
                    "Implementé autenticación con BCrypt y control de acceso por roles",
                ],
                stack = ["TypeScript","Tailwind","Docker","Kubernetes","Helm",
                         "GitLab CI","Dolibarr","FreeLens"],
            ),
            dict(
                role    = "Desarrollador Web",
                company = "La Fábrica de los Hobbies",
                badge   = "Prácticas",
                date    = "Feb – May 2025",
                bullets = [
                    "Desarrollé sistema de gestión de inventario con panel administrativo",
                    "Diseñé interfaces en <b>Figma</b> e implementé con PHP y JavaScript",
                ],
                stack = ["PHP","JavaScript","XAMPP","Figma"],
            ),
            dict(
                role    = "Asesor Financiero",
                company = "Asesores & Abogados",
                badge   = None,
                date    = "2022 – 2023",
                bullets = [
                    "Gestión de nóminas, seguros sociales y beneficios laborales",
                ],
                stack = [],
            ),
        ],
        projects = [
            dict(
                name  = "Boutique Market ERP",
                link  = "github.com/Angel-dxd/boutique-market",
                desc  = ("Sistema <b>multitenant</b> de gestión de inventarios y servicios "
                         "para múltiples clientes con aislamiento total de datos por cliente."),
                stack = ["Node.js","JavaScript","MySQL","BCrypt","Tailwind"],
            ),
            dict(
                name  = "Contract Manager",
                link  = "Onna Digital · privado",
                desc  = ("App web de gestión de contratos y recursos cloud con <b>doble rol</b> "
                         "(Admin/Cliente), integrada con Dolibarr como ERP central."),
                stack = ["TypeScript","Docker","Kubernetes","Helm","GitLab CI"],
            ),
        ],
        edu = [
            ("2024 – 2026", "Grado Superior DAM",
             "Desarrollo de Aplicaciones Multiplataforma · CEAC Valencia"),
            ("2022 – 2024", "Grado Superior Contabilidad y Finanzas",
             "Universitat Oberta de Catalunya"),
        ],
        langs = [("Español","Nativo"),("Francés","C1"),("Inglés","B2")],
    ),

    "en": dict(
        title      = "Fullstack Developer",
        sec_contact= "Contact",
        sec_skills = "Skills",
        sec_langs  = "Languages",
        sec_other  = "Other",
        sec_about  = "About me",
        sec_exp    = "Experience",
        sec_proj   = "Projects",
        sec_edu    = "Education",
        about      = ("Fullstack developer freshly graduated in Multiplatform Application "
                      "Development, specializing in <b>backend</b>. Real production experience "
                      "with Node.js, TypeScript, Docker and Kubernetes. Background in Accounting "
                      "&amp; Finance gives me a business perspective applied directly to software. "
                      '<font color="#3b82f6"><b>Available immediately.</b></font>'),
        available  = "Available immediately",
        license    = "Driver's license · Own vehicle",
        internship = "Internship",
        jobs = [
            dict(
                role    = "Fullstack Developer",
                company = "Onna Digital",
                badge   = "Internship",
                date    = "Nov 2025 – Mar 2026",
                bullets = [
                    "Built <b>Contract Manager</b>: web app for contract management with "
                    "dual Admin/Client role system integrated with Dolibarr ERP via REST API",
                    "Managed pods, Helm charts and <b>Kubernetes</b> clusters via FreeLens",
                    "Implemented BCrypt authentication and role-based access control",
                ],
                stack = ["TypeScript","Tailwind","Docker","Kubernetes","Helm",
                         "GitLab CI","Dolibarr","FreeLens"],
            ),
            dict(
                role    = "Web Developer",
                company = "La Fábrica de los Hobbies",
                badge   = "Internship",
                date    = "Feb – May 2025",
                bullets = [
                    "Built inventory management system with admin panel from scratch",
                    "Designed interfaces in <b>Figma</b> and implemented with PHP and JavaScript",
                ],
                stack = ["PHP","JavaScript","XAMPP","Figma"],
            ),
            dict(
                role    = "Financial Advisor",
                company = "Asesores & Abogados",
                badge   = None,
                date    = "2022 – 2023",
                bullets = [
                    "Payroll management, social security and employee benefits for client portfolio",
                ],
                stack = [],
            ),
        ],
        projects = [
            dict(
                name  = "Boutique Market ERP",
                link  = "github.com/Angel-dxd/boutique-market",
                desc  = ("A <b>multitenant</b> inventory and services management system "
                         "for multiple commercial clients with full per-client data isolation."),
                stack = ["Node.js","JavaScript","MySQL","BCrypt","Tailwind"],
            ),
            dict(
                name  = "Contract Manager",
                link  = "Onna Digital · private",
                desc  = ("Web app for contract and cloud resource management with <b>dual role</b> "
                         "(Admin/Client), integrated with Dolibarr as the central ERP."),
                stack = ["TypeScript","Docker","Kubernetes","Helm","GitLab CI"],
            ),
        ],
        edu = [
            ("2024 – 2026", "Higher Degree — DAM",
             "Multiplatform Application Development · CEAC Valencia"),
            ("2022 – 2024", "Higher Degree — Accounting & Finance",
             "Universitat Oberta de Catalunya"),
        ],
        langs = [("Spanish","Native"),("French","C1"),("English","B2")],
    ),
}

SKILL_GROUPS = {
    "es": [
        ("Frontend",  ["HTML","CSS","JS","TypeScript","Tailwind","Bootstrap"]),
        ("Backend",   ["Node.js","PHP","Nginx"]),
        ("DevOps",    ["Docker","Kubernetes","Helm","GitLab CI"]),
        ("Databases", ["MySQL","MongoDB","PostgreSQL"]),
        ("SO",        ["Debian","Ubuntu","Linux"]),
        ("Tools",     ["Git","GitHub","VSCode","Figma","FreeLens"]),
    ],
    "en": [
        ("Frontend",  ["HTML","CSS","JS","TypeScript","Tailwind","Bootstrap"]),
        ("Backend",   ["Node.js","PHP","Nginx"]),
        ("DevOps",    ["Docker","Kubernetes","Helm","GitLab CI"]),
        ("Databases", ["MySQL","MongoDB","PostgreSQL"]),
        ("OS",        ["Debian","Ubuntu","Linux"]),
        ("Tools",     ["Git","GitHub","VSCode","Figma","FreeLens"]),
    ],
}

# ── Generate function ──────────────────────────────────────────────────────
def build(lang, output):
    c   = CONTENT[lang]
    sg  = SKILL_GROUPS[lang]
    story = []
    sb_w   = SB_W - PAD_OUT - PAD_IN
    main_w = MAIN_W - PAD_IN - PAD_OUT

    # ── SIDEBAR ────────────────────────────────────────────────────────────
    if os.path.exists(PHOTO):
        img = PILImage.open(PHOTO).convert("RGB")
        iw, ih = img.size
        side   = min(iw, ih)
        left   = (iw - side) // 2
        cropped = img.crop((left, 0, left + side, side))
        tmp = f"/tmp/_cv_photo_{lang}.jpg"
        cropped.save(tmp, quality=92)
        ps = sb_w * 0.66
        story.append(Spacer(1, 1*mm))
        story.append(Image(tmp, width=ps, height=ps, hAlign="CENTER"))
        story.append(Spacer(1, 3*mm))

    story.append(Paragraph("Angel Xavier", sNAME))
    story.append(Paragraph("Pons Márquez",  sNAME))
    story.append(Spacer(1, 1.5*mm))
    story.append(Paragraph(c["title"], sTITLE))

    story += sec(c["sec_contact"])
    for icon, text in [
        ("✉", "angelxavierponsmarquez2018\n@gmail.com"),
        ("in","linkedin/angel-xavier-\npons-marquez"),
        ("⌥","github.com/Angel-dxd"),
        ("✆","+34 640 105 492"),
        ("◎","Valencia, España"),
    ]:
        story.append(Paragraph(
            f'<font color="#3b82f6"><b>{icon}</b></font>  '
            + text.replace('\n','<br/>&nbsp;&nbsp;&nbsp;&nbsp;'), sCONT))
        story.append(Spacer(1, 1.5*mm))

    story += sec(c["sec_skills"])
    for cat, tags in sg:
        story.append(Paragraph(f'<font color="#64748b">{cat}</font>',
                                S("cat", 7, MUTED)))
        story.append(Spacer(1, 1*mm))
        story.append(PillRow(tags, sb_w))
        story.append(Spacer(1, 2*mm))

    story += sec(c["sec_langs"])
    for lang_name, level in c["langs"]:
        story.append(Paragraph(
            f'<b><font color="#ffffff">{lang_name}</font></b>'
            f'<font color="#64748b">  {level}</font>', sBODY))
        story.append(Spacer(1, 1*mm))

    story += sec(c["sec_other"])
    story.append(bul(c["available"]))
    story.append(Spacer(1, 1*mm))
    story.append(bul(c["license"]))

    # ── MAIN ──────────────────────────────────────────────────────────────
    story.append(FrameBreak())

    story += sec(c["sec_about"])
    story.append(Paragraph(c["about"], sBODY))

    story += sec(c["sec_exp"])
    for job in c["jobs"]:
        badge = (f'  <font color="#3b82f6">[{job["badge"]}]</font>'
                 if job["badge"] else "")
        story.append(Paragraph(
            f'<b>{job["role"]}</b>'
            f'<font color="#64748b">  ·  {job["company"]}</font>{badge}', sJOB))
        story.append(Paragraph(job["date"], sDATE))
        story.append(Spacer(1, 1*mm))
        for b in job["bullets"]:
            story.append(bul(b))
        if job["stack"]:
            story.append(Spacer(1, 1.5*mm))
            story.append(PillRow(job["stack"], main_w, PILL_BG, MUTED))
        story.append(Spacer(1, 4*mm))

    story += sec(c["sec_proj"])
    for p in c["projects"]:
        story.append(Paragraph(
            f'<b><font color="#3b82f6">{p["name"]}</font></b>'
            f'<font color="#475569">  —  {p["link"]}</font>', sPROJ))
        story.append(Paragraph(p["desc"], sBODY))
        story.append(Spacer(1, 1.5*mm))
        story.append(PillRow(p["stack"], main_w, PILL_BG, MUTED))
        story.append(Spacer(1, 3.5*mm))

    story += sec(c["sec_edu"])
    for date, title, sub in c["edu"]:
        story.append(Paragraph(
            f'<font color="#3b82f6"><b>{date}</b></font>'
            f'  <b><font color="#ffffff">{title}</font></b>', sJOB))
        story.append(Paragraph(sub, sMUTED))
        story.append(Spacer(1, 3*mm))

    doc = CVDoc(output)
    doc.build(story)
    print(f"✓ {lang.upper()} → {output}")

# ── Run ────────────────────────────────────────────────────────────────────
build("es", OUT_ES)
build("en", OUT_EN)

# Keep cv.pdf pointing to Spanish version (default)
import shutil
shutil.copy(OUT_ES, "/Users/angelxavier/portafolioAngel/cv/cv.pdf")
print("✓ cv.pdf → ES (default)")
