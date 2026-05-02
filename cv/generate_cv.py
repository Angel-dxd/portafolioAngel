"""
CV Generator — Angel Xavier Pons Márquez
10/10 version: Inter font, skill pills, clean two-column layout, no overlaps
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate,
                                 Paragraph, Spacer, FrameBreak, Image,
                                 HRFlowable, Flowable)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage

# ── Paths ──────────────────────────────────────────────────────────────────
OUTPUT = "/Users/angelxavier/portafolioAngel/cv/cv.pdf"
PHOTO  = "/Users/angelxavier/portafolioAngel/img/foto.png"
FONT_VAR = "/tmp/inter_fonts/InterVariable.ttf"

# ── Register fonts ─────────────────────────────────────────────────────────
pdfmetrics.registerFont(TTFont("Inter",       FONT_VAR))
pdfmetrics.registerFont(TTFont("Inter-Bold",  FONT_VAR))  # variable font handles weight
# Use reportlab built-in bold as fallback
pdfmetrics.registerFontFamily("Inter", normal="Inter", bold="Inter-Bold",
                               italic="Inter", boldItalic="Inter-Bold")

# ── Colors ─────────────────────────────────────────────────────────────────
NAVY    = HexColor("#0d1f35")
SIDEBAR = HexColor("#091729")
ACCENT  = HexColor("#3b82f6")
ACCENT2 = HexColor("#1d4ed8")
LIGHT   = HexColor("#e2e8f0")
MUTED   = HexColor("#94a3b8")
WHITE   = HexColor("#ffffff")
PILL_BG = HexColor("#1e3a5f")
SEP     = HexColor("#1e3555")

# ── Page layout ────────────────────────────────────────────────────────────
W, H     = A4
SB_W     = 68 * mm     # sidebar width
MAIN_W   = W - SB_W    # main width
PAD_OUT  = 9 * mm
PAD_IN   = 7 * mm

# ── Style factory ──────────────────────────────────────────────────────────
def S(name, size=9, color=WHITE, bold=False, align=TA_LEFT, leading=None,
      space_before=0, space_after=0):
    fn = "Inter-Bold" if bold else "Inter"
    return ParagraphStyle(name, fontName=fn, fontSize=size, textColor=color,
                          leading=leading or size * 1.45,
                          alignment=align,
                          spaceBefore=space_before, spaceAfter=space_after)

# ── Shared styles ──────────────────────────────────────────────────────────
sNAME    = S("name",    24, WHITE,  bold=True,  leading=28)
sTITLE   = S("title",   11, ACCENT, bold=False, leading=16)
sSEC     = S("sec",      7, ACCENT, bold=True,  leading=10)
sBODY    = S("body",     8.5, LIGHT,  leading=13)
sMUTED   = S("muted",    8, MUTED,  leading=12)
sJOB     = S("job",      9, WHITE,  bold=True,  leading=13)
sDATE    = S("date",     7.5, ACCENT, leading=11)
sBULLET  = S("bullet",   8.5, LIGHT,  leading=13)
sPROJ    = S("proj",     9, ACCENT, bold=True,  leading=13)
sSTACK   = S("stack",    7.5, MUTED,  leading=11)
sCONT    = S("cont",     7.5, LIGHT,  leading=11)

# ── Pill Flowable (skill tags) ──────────────────────────────────────────────
class Pill(Flowable):
    """Single rounded pill badge."""
    PAD_X, PAD_Y, R = 5, 3, 3
    FONT_SIZE = 7

    def __init__(self, text, bg=PILL_BG, fg=LIGHT):
        self.text = text
        self.bg   = bg
        self.fg   = fg
        from reportlab.pdfbase.pdfmetrics import stringWidth
        self._tw  = stringWidth(text, "Inter", self.FONT_SIZE)
        self.width  = self._tw + self.PAD_X * 2
        self.height = self.FONT_SIZE + self.PAD_Y * 2

    def draw(self):
        c = self.canv
        c.setFillColor(self.bg)
        c.roundRect(0, 0, self.width, self.height, self.R, fill=1, stroke=0)
        c.setFillColor(self.fg)
        c.setFont("Inter", self.FONT_SIZE)
        c.drawString(self.PAD_X, self.PAD_Y + 0.5, self.text)


class PillRow(Flowable):
    """Row of pill badges that wraps within container_width."""
    GAP_X, GAP_Y = 4, 4

    def __init__(self, tags, container_width, bg=PILL_BG, fg=LIGHT):
        self.pills  = [Pill(t, bg, fg) for t in tags]
        self.cw     = container_width
        self._rows  = self._layout()
        total_h     = sum(p.height for p in self.pills[:1]) * len(self._rows)
        total_h    += self.GAP_Y * (len(self._rows) - 1)
        self.width  = container_width
        self.height = total_h + 1

    def _layout(self):
        rows, row, x = [], [], 0
        for p in self.pills:
            if x + p.width > self.cw and row:
                rows.append(row); row = []; x = 0
            row.append((x, p)); x += p.width + self.GAP_X
        if row: rows.append(row)
        return rows

    def draw(self):
        c    = self.canv
        ph   = self.pills[0].height if self.pills else 10
        y    = self.height - ph
        for row in self._rows:
            for (x, pill) in row:
                c.saveState()
                c.translate(x, y)
                pill.canv = c
                pill.draw()
                c.restoreState()
            y -= ph + self.GAP_Y


# ── Section heading ─────────────────────────────────────────────────────────
def sec(title):
    return [
        Spacer(1, 5 * mm),
        Paragraph(title.upper(), sSEC),
        HRFlowable(width="100%", thickness=0.4, color=SEP, spaceAfter=3),
    ]


def bul(text, s=sBULLET):
    return Paragraph(f"\u2022\u2002{text}", s)


# ── Document with colored background ───────────────────────────────────────
class CVDoc(BaseDocTemplate):
    def __init__(self, filename):
        super().__init__(filename, pagesize=A4,
                         leftMargin=0, rightMargin=0,
                         topMargin=0, bottomMargin=0)
        sb = Frame(0, 0, SB_W, H,
                   leftPadding=PAD_OUT, rightPadding=PAD_IN,
                   topPadding=PAD_OUT, bottomPadding=PAD_OUT, id="sb")
        mn = Frame(SB_W, 0, MAIN_W, H,
                   leftPadding=PAD_IN, rightPadding=PAD_OUT,
                   topPadding=PAD_OUT, bottomPadding=PAD_OUT, id="mn")
        self.addPageTemplates([
            PageTemplate(id="cv", frames=[sb, mn], onPage=self._bg)
        ])

    def _bg(self, canvas, doc):
        canvas.saveState()
        canvas.setFillColor(SIDEBAR)
        canvas.rect(0, 0, SB_W, H, fill=1, stroke=0)
        canvas.setFillColor(NAVY)
        canvas.rect(SB_W, 0, MAIN_W, H, fill=1, stroke=0)
        # subtle vertical separator line
        canvas.setStrokeColor(SEP)
        canvas.setLineWidth(0.5)
        canvas.line(SB_W, PAD_OUT, SB_W, H - PAD_OUT)
        canvas.restoreState()


# ── Build story ─────────────────────────────────────────────────────────────
story = []
sb_w  = SB_W - PAD_OUT - PAD_IN   # usable sidebar width

# ╔══ SIDEBAR ═══════════════════════════════════════════════════════════════╗

# Photo
if os.path.exists(PHOTO):
    img = PILImage.open(PHOTO).convert("RGB")
    iw, ih = img.size
    side   = min(iw, ih)
    left   = (iw - side) // 2
    top    = int(ih * 0.02)
    cropped = img.crop((left, top, left + side, top + side))
    tmp     = "/tmp/_cv_photo.jpg"
    cropped.save(tmp, quality=92)
    photo_size = sb_w * 0.72
    story.append(Spacer(1, 2 * mm))
    story.append(Image(tmp, width=photo_size, height=photo_size, hAlign="CENTER"))
    story.append(Spacer(1, 5 * mm))

# Name
story.append(Paragraph("Angel Xavier", sNAME))
story.append(Paragraph("Pons Márquez",  sNAME))
story.append(Spacer(1, 1.5 * mm))
story.append(Paragraph("Desarrollador Fullstack", sTITLE))

# ── Contact ────────────────────────────────────────────────────────────────
story += sec("Contacto")
contacts = [
    ("✉", "angelxavierponsmarquez2018\n@gmail.com"),
    ("in", "linkedin/angel-xavier-\npons-marquez"),
    ("⌥", "github.com/Angel-dxd"),
    ("✆", "+34 640 105 492"),
    ("◎", "Valencia, España"),
]
for icon, text in contacts:
    story.append(Paragraph(
        f'<font color="#3b82f6"><b>{icon}</b></font>  '
        + text.replace('\n', '<br/>&nbsp;&nbsp;&nbsp;&nbsp;'),
        sCONT))
    story.append(Spacer(1, 2 * mm))

# ── Skills (pills) ─────────────────────────────────────────────────────────
story += sec("Competencias")

skill_groups = [
    ("Frontend",  ["HTML","CSS","JS","TypeScript","Tailwind","Bootstrap"]),
    ("Backend",   ["Node.js","PHP","Nginx"]),
    ("DevOps",    ["Docker","Kubernetes","Helm","GitLab CI"]),
    ("Databases", ["MySQL","MongoDB","PostgreSQL"]),
    ("SO",        ["Debian","Ubuntu","Linux"]),
    ("Tools",     ["Git","GitHub","VSCode","Figma"]),
]

for cat, tags in skill_groups:
    story.append(Paragraph(f'<font color="#64748b">{cat}</font>', S("cat", 7, MUTED)))
    story.append(Spacer(1, 1 * mm))
    story.append(PillRow(tags, sb_w))
    story.append(Spacer(1, 2.5 * mm))

# ── Languages ──────────────────────────────────────────────────────────────
story += sec("Idiomas")
for lang, level, pct in [("Español","Nativo",100),("Francés","C1",85),("Inglés","B2",65)]:
    story.append(Paragraph(
        f'<b><font color="#ffffff">{lang}</font></b>'
        f'<font color="#64748b">  {level}</font>', sBODY))
    story.append(Spacer(1, 1 * mm))

# ── Extra ──────────────────────────────────────────────────────────────────
story += sec("Otros")
story.append(bul("Incorporación inmediata", sCONT))
story.append(Spacer(1, 1 * mm))
story.append(bul("Carnet de conducir · Vehículo propio", sCONT))

# ╔══ FRAME BREAK → MAIN ════════════════════════════════════════════════════╗
story.append(FrameBreak())

main_w = MAIN_W - PAD_IN - PAD_OUT  # usable main width

# ── Sobre mí ───────────────────────────────────────────────────────────────
story += sec("Sobre mí")
story.append(Paragraph(
    "Desarrollador fullstack recién graduado en DAM, especializado en "
    "<b>backend</b>. Experiencia real en producción con Node.js, TypeScript, "
    "Docker y Kubernetes. Formación en Contabilidad y Finanzas que me permite "
    "construir software con visión de negocio. "
    '<font color="#3b82f6"><b>Disponible de inmediato.</b></font>',
    sBODY))

# ── Experiencia ────────────────────────────────────────────────────────────
story += sec("Experiencia")

jobs = [
    dict(
        role="Desarrollador Fullstack",
        company="Onna Digital",
        badge="Prácticas",
        date="Nov 2025 – Mar 2026",
        bullets=[
            "Desarrollé <b>Contract Manager</b>: app web de gestión de contratos "
            "con doble rol Admin/Cliente integrada con Dolibarr ERP vía API REST",
            "Gestioné pods, Helm charts y clústeres <b>Kubernetes</b> con FreeLens",
            "Implementé autenticación con <b>BCrypt</b> y control de roles",
        ],
        stack=["TypeScript","Tailwind","Docker","Kubernetes","GitLab"],
    ),
    dict(
        role="Desarrollador Web",
        company="La Fábrica de los Hobbies",
        badge="Prácticas",
        date="Feb – May 2025",
        bullets=[
            "Desarrollé sistema de gestión de inventario con panel administrativo",
            "Diseñé interfaces en <b>Figma</b> e implementé con PHP y JavaScript",
        ],
        stack=["PHP","JavaScript","XAMPP","Figma"],
    ),
    dict(
        role="Asesor Financiero",
        company="Asesores & Abogados",
        badge=None,
        date="2022 – 2023",
        bullets=[
            "Gestión de nóminas, seguros sociales y beneficios laborales para cartera de clientes",
        ],
        stack=[],
    ),
]

for job in jobs:
    badge = f'  <font color="#3b82f6">[{job["badge"]}]</font>' if job["badge"] else ""
    story.append(Paragraph(
        f'<b>{job["role"]}</b>'
        f'<font color="#64748b">  ·  {job["company"]}</font>{badge}',
        sJOB))
    story.append(Paragraph(job["date"], sDATE))
    story.append(Spacer(1, 1 * mm))
    for b in job["bullets"]:
        story.append(bul(b))
    if job["stack"]:
        story.append(Spacer(1, 1.5 * mm))
        story.append(PillRow(job["stack"], main_w, PILL_BG, MUTED))
    story.append(Spacer(1, 4 * mm))

# ── Proyectos ──────────────────────────────────────────────────────────────
story += sec("Proyectos")

projects = [
    dict(
        name="Boutique Market ERP",
        link="github.com/Angel-dxd/boutique-market",
        desc="Sistema <b>multitenant</b> de gestión de inventarios y servicios para múltiples "
             "clientes comerciales con aislamiento total de datos por cliente.",
        stack=["Node.js","JavaScript","MySQL","BCrypt","Tailwind"],
    ),
    dict(
        name="Contract Manager",
        link="Onna Digital · privado",
        desc="Aplicación web de gestión de contratos y recursos cloud con <b>doble rol</b> "
             "(Admin/Cliente), integrada con Dolibarr como ERP central.",
        stack=["TypeScript","Docker","Kubernetes","Helm","GitLab CI"],
    ),
]

for p in projects:
    story.append(Paragraph(
        f'<b><font color="#3b82f6">{p["name"]}</font></b>'
        f'<font color="#475569">  —  {p["link"]}</font>', sPROJ))
    story.append(Paragraph(p["desc"], sBODY))
    story.append(Spacer(1, 1.5 * mm))
    story.append(PillRow(p["stack"], main_w, PILL_BG, MUTED))
    story.append(Spacer(1, 3.5 * mm))

# ── Educación ──────────────────────────────────────────────────────────────
story += sec("Educación")

edu = [
    ("2024 – 2026",
     "Grado Superior DAM",
     "Desarrollo de Aplicaciones Multiplataforma · CEAC Valencia"),
    ("2022 – 2024",
     "Grado Superior Contabilidad y Finanzas",
     "Universitat Oberta de Catalunya"),
]
for date, title, sub in edu:
    story.append(Paragraph(
        f'<font color="#3b82f6"><b>{date}</b></font>'
        f'  <b><font color="#ffffff">{title}</font></b>', sJOB))
    story.append(Paragraph(sub, sMUTED))
    story.append(Spacer(1, 3 * mm))

# ── Build ──────────────────────────────────────────────────────────────────
doc = CVDoc(OUTPUT)
doc.build(story)
print(f"✓ CV generated → {OUTPUT}")
