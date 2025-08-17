from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import re
import os

def booklet_to_pdf(booklet_text, diagram_image_paths, output_pdf_path):
    doc = SimpleDocTemplate(output_pdf_path, pagesize=A4)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=4))

    story = []

    # Split booklet into sections by headings (for better layout)
    sections = re.split(r"\n\s*#+\s*", booklet_text)
    diagram_idx = 0

    for section in sections:
        story.append(Paragraph(section.strip(), styles['Justify']))
        story.append(Spacer(1, 0.1*inch))

        # Insert diagrams after each section if available
        if diagram_idx < len(diagram_image_paths):
            img_path = diagram_image_paths[diagram_idx]
            if os.path.exists(img_path):
                story.append(Image(img_path, width=4*inch, height=3*inch))
                story.append(Spacer(1, 0.2*inch))
            diagram_idx += 1

        story.append(PageBreak())

    doc.build(story)