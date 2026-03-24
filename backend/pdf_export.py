import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from schemas import TerrainAnalysis


def generate_pdf(filename: str, analysis: TerrainAnalysis, created_at: datetime) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=20,
        textColor=colors.HexColor("#1a5276"),
        alignment=TA_CENTER,
        spaceAfter=10,
    )
    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontSize=11,
        textColor=colors.HexColor("#555555"),
        alignment=TA_CENTER,
        spaceAfter=20,
    )
    section_style = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontSize=13,
        textColor=colors.HexColor("#1a5276"),
        spaceBefore=15,
        spaceAfter=8,
        borderPad=4,
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontSize=10,
        leading=16,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
    )
    bullet_style = ParagraphStyle(
        "Bullet",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        leftIndent=15,
        spaceAfter=4,
    )

    story = []

    story.append(Paragraph("Relatório de Análise de Terreno", title_style))
    story.append(Paragraph(
        f"Arquivo: {filename} &nbsp;&nbsp;|&nbsp;&nbsp; Data: {created_at.strftime('%d/%m/%Y %H:%M')}",
        subtitle_style
    ))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1a5276")))
    story.append(Spacer(1, 0.4 * cm))

    summary_data = [
        ["Campo", "Valor"],
        ["Tipo de Terreno", analysis.terrain_type],
        ["Score de Fertilidade", f"{analysis.overall_fertility_score:.1f} / 10"],
        ["Componentes Identificados", str(len(analysis.components))],
        ["Áreas Férteis", str(len(analysis.fertile_areas))],
    ]
    summary_table = Table(summary_data, colWidths=[6 * cm, 11 * cm])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a5276")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 11),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 10),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#eaf0fb"), colors.white]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(Paragraph("Resumo", section_style))
    story.append(summary_table)
    story.append(Spacer(1, 0.3 * cm))

    if analysis.components:
        story.append(Paragraph("Composição do Terreno", section_style))
        comp_data = [["Componente", "Percentual", "Cor"]]
        for c in analysis.components:
            comp_data.append([c.name, f"{c.percentage:.1f}%", c.color])
        comp_table = Table(comp_data, colWidths=[8 * cm, 4 * cm, 5 * cm])
        comp_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2e86c1")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 1), (-1, -1), 10),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#d6eaf8"), colors.white]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(comp_table)
        story.append(Spacer(1, 0.3 * cm))

    if analysis.fertile_areas:
        story.append(Paragraph("Áreas Férteis Identificadas", section_style))
        for area in analysis.fertile_areas:
            story.append(Paragraph(f"• {area}", bullet_style))
        story.append(Spacer(1, 0.2 * cm))

    if analysis.technical_report:
        story.append(Paragraph("Relatório Técnico", section_style))
        story.append(Paragraph(analysis.technical_report, body_style))
        story.append(Spacer(1, 0.2 * cm))

    if analysis.recommendations:
        story.append(Paragraph("Recomendações", section_style))
        for i, rec in enumerate(analysis.recommendations, 1):
            story.append(Paragraph(f"{i}. {rec}", bullet_style))

    story.append(Spacer(1, 0.5 * cm))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cccccc")))
    story.append(Paragraph(
        "Relatório gerado automaticamente pelo sistema AnaliseTerrenoIA",
        ParagraphStyle("Footer", parent=styles["Normal"], fontSize=8,
                       textColor=colors.grey, alignment=TA_CENTER, spaceBefore=6)
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
