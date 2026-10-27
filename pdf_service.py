import io
from typing import Dict, Any
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable

class PDFService:
    """Generates formatted PDF documents for quizzes and comprehensive study kits."""

    @staticmethod
    def generate_pdf(data: Dict[str, Any], scope: str = "full") -> io.BytesIO:
        """Builds a styled PDF in memory and returns a readable byte stream."""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=45,
            leftMargin=45,
            topMargin=45,
            bottomMargin=45
        )

        styles = getSampleStyleSheet()
        
        primary_color = colors.HexColor("#6d28d9")
        dark_neutral = colors.HexColor("#1e1b4b")
        text_color = colors.HexColor("#2e2a47")
        light_accent = colors.HexColor("#ede9fe")

        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Heading1"],
            fontSize=18,
            leading=22,
            textColor=primary_color,
            spaceAfter=4
        )
        subtitle_style = ParagraphStyle(
            "DocSubtitle",
            parent=styles["Normal"],
            fontSize=9.5,
            textColor=colors.HexColor("#6b7280"),
            spaceAfter=12
        )
        section_style = ParagraphStyle(
            "SectionHeader",
            parent=styles["Heading2"],
            fontSize=12,
            leading=16,
            textColor=dark_neutral,
            spaceBefore=14,
            spaceAfter=6,
            keepWithNext=True
        )
        sub_heading_style = ParagraphStyle(
            "SubHeader",
            parent=styles["Heading3"],
            fontSize=10.5,
            leading=14,
            textColor=primary_color,
            spaceBefore=8,
            spaceAfter=4,
            keepWithNext=True
        )
        body_style = ParagraphStyle(
            "Body",
            parent=styles["Normal"],
            fontSize=9,
            leading=13.5,
            textColor=text_color,
            spaceAfter=6
        )
        bullet_style = ParagraphStyle(
            "Bullet",
            parent=body_style,
            leftIndent=14,
            firstLineIndent=-10,
            spaceAfter=3
        )
        q_title_style = ParagraphStyle(
            "QuestionTitle",
            parent=body_style,
            fontSize=9.5,
            leading=13,
            textColor=dark_neutral,
            fontName="Helvetica-Bold",
            spaceBefore=8,
            spaceAfter=4,
            keepWithNext=True
        )
        option_style = ParagraphStyle(
            "OptionText",
            parent=body_style,
            leftIndent=15,
            fontSize=8.5,
            leading=12,
            spaceAfter=2
        )
        ans_style = ParagraphStyle(
            "AnswerBox",
            parent=body_style,
            fontSize=8.5,
            leading=12,
            textColor=colors.HexColor("#4c1d95"),
            spaceBefore=3,
            spaceAfter=8
        )

        story = []
        doc_heading = data.get("title", "Study Material")
        story.append(Paragraph(doc_heading, title_style))
        story.append(Paragraph(f"Export: {scope.upper()} | Comprehensive Study Dossier", subtitle_style))
        story.append(HRFlowable(width="100%", thickness=1, color=light_accent, spaceAfter=10))

        if scope == "full":
            story.append(Paragraph("EXECUTIVE OVERVIEW", section_style))
            story.append(Paragraph(data.get("overview", ""), body_style))
            story.append(Spacer(1, 6))

            story.append(Paragraph("DEEP-DIVE MODULES", section_style))
            for sec in data.get("sections", []):
                story.append(Paragraph(sec.get("heading", ""), sub_heading_style))
                story.append(Paragraph(sec.get("content", ""), body_style))
                for pt in sec.get("bullet_points", []):
                    story.append(Paragraph(f"&bull;&nbsp;&nbsp;{pt}", bullet_style))
                story.append(Spacer(1, 4))

            if data.get("glossary"):
                story.append(Paragraph("TERMINOLOGY & GLOSSARY", section_style))
                for item in data.get("glossary", []):
                    story.append(Paragraph(f"<b>{item.get('term')}</b>: {item.get('definition')}", body_style))
                story.append(Spacer(1, 6))

            if data.get("high_yield_takeaways"):
                story.append(Paragraph("HIGH-YIELD TAKEAWAYS", section_style))
                for pt in data.get("high_yield_takeaways", []):
                    story.append(Paragraph(f"&bull;&nbsp;&nbsp;{pt}", bullet_style))
                story.append(Spacer(1, 8))

        story.append(Paragraph("ASSESSMENT & QUIZ", section_style))
        quiz_items = data.get("quiz", [])
        for idx, item in enumerate(quiz_items, start=1):
            story.append(Paragraph(f"Q{idx}. {item['question']}", q_title_style))
            for opt in item.get("options", []):
                story.append(Paragraph(f"[  ] {opt}", option_style))
            story.append(Paragraph(
                f"<b>Answer:</b> {item['correct_answer']}<br/><b>Explanation:</b> {item['explanation']}",
                ans_style
            ))
            story.append(Spacer(1, 4))

        doc.build(story)
        buffer.seek(0)
        return buffer