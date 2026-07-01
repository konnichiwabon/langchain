import os
import html
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas

# Define the custom NumberedCanvas for professional page footer/header
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(HexColor("#4A5568"))
        
        # Draw running footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(self._pagesize[0] - 54, 36, page_text)
        self.drawString(54, 36, "LangChain Project Documentation — July 1, 2026")
        
        # Footer line
        self.setStrokeColor(HexColor("#CBD5E0"))
        self.setLineWidth(0.5)
        self.line(54, 48, self._pagesize[0] - 54, 48)
        
        # Draw running header on page 2 and later
        if self._pageNumber > 1:
            self.drawString(54, self._pagesize[1] - 36, "LangChain Agent Development & Execution Report")
            self.line(54, self._pagesize[1] - 42, self._pagesize[0] - 54, self._pagesize[1] - 42)
            
        self.restoreState()

def create_code_block(code_text, styles):
    escaped = html.escape(code_text)
    lines = []
    for line in escaped.splitlines():
        # Preserve leading spaces using &nbsp;
        num_spaces = len(line) - len(line.lstrip(' '))
        line_content = '&nbsp;' * num_spaces + line.lstrip(' ')
        lines.append(line_content)
    formatted = "<br/>".join(lines)
    
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=HexColor('#1A202C')
    )
    
    p = Paragraph(formatted, code_style)
    
    t = Table([[p]], colWidths=[504])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor('#F7FAFC')),
        ('BOX', (0,0), (-1,-1), 0.5, HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    return t

def create_callout_box(text, styles, border_color='#0D9488', bg_color='#F0FDF4'):
    p = Paragraph(text, styles['Normal'])
    t = Table([[p]], colWidths=[504])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor(bg_color)),
        ('LINELEFT', (0,0), (0,0), 3.0, HexColor(border_color)),
        ('BOX', (0,0), (-1,-1), 0.5, HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    return t

def main():
    # Make sure output directory exists
    os.makedirs("july", exist_ok=True)
    
    # Date formatting for file name and document
    current_date = "2026-07-01"
    pdf_path = os.path.join("july", f"langchain_{current_date}.pdf")
    
    # Setup document
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Define custom paragraph styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=HexColor('#1A365D'),
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=HexColor('#0D9488'),
        spaceAfter=20
    )
    
    h1_style = ParagraphStyle(
        'Heading1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=HexColor('#1A365D'),
        spaceBefore=18,
        spaceAfter=8,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=HexColor('#0D9488'),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14.5,
        textColor=HexColor('#2D3748'),
        spaceAfter=10
    )
    
    body_bold_style = ParagraphStyle(
        'BodyTextBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    
    bullet_style = ParagraphStyle(
        'BulletText',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )
    
    story = []
    
    # --- HEADER / TITLE BAND ---
    # Decorative line at top
    t_top = Table([[""]], colWidths=[504], rowHeights=[4])
    t_top.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor('#1A365D')),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_top)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("LANGCHAIN AI AGENT DEVELOPMENT REPORT", title_style))
    story.append(Paragraph("Document Q&amp;A Integration with Deep Agents &amp; Gemini 2.5 Flash", subtitle_style))
    
    # Metadata Table
    meta_data = [
        [Paragraph("<b>Date:</b> July 1, 2026", body_style), Paragraph("<b>Framework:</b> LangChain / DeepAgents", body_style)],
        [Paragraph("<b>Author:</b> Developer (AI Assistant)", body_style), Paragraph("<b>Target Model:</b> google_genai:gemini-2.5-flash", body_style)],
        [Paragraph("<b>Workspace:</b> /Desktop/langchain", body_style), Paragraph("<b>Status:</b> Executed Successfully", body_style)]
    ]
    t_meta = Table(meta_data, colWidths=[252, 252])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.5, HexColor('#E2E8F0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, HexColor('#F1F5F9')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 20))
    
    # --- SECTION 1: OVERVIEW ---
    story.append(Paragraph("1. Project Overview &amp; Objective", h1_style))
    story.append(Paragraph(
        "This project implements a local <b>Document Question Answering (Q&amp;A) system</b> using the <code>deepagents</code> wrapper around LangChain components. "
        "The agent is configured to ingest a demographic profile document, extract its content, and answer specific analytical queries. "
        "The objective is to perform <i>single-shot context injection</i> where the model responds strictly based on the extracted document content rather than pre-trained general knowledge.",
        body_style
    ))
    
    # --- SECTION 2: SYSTEM ARCHITECTURE &amp; LAYOUT ---
    story.append(Paragraph("2. System Architecture &amp; File Structure", h1_style))
    story.append(Paragraph(
        "The workspace consists of a simple yet robust directory structure containing environment configurations, source document, and the main invocation script:",
        body_style
    ))
    
    story.append(Paragraph("&bull; <b>app.py:</b> The main entry point script containing logic for PDF text extraction and deep agent execution.", bullet_style))
    story.append(Paragraph("&bull; <b>.env:</b> Configuration file holding the Google API Key (<code>GOOGLE_API_KEY</code>) required for GenAI authentication.", bullet_style))
    story.append(Paragraph("&bull; <b>FF2023-28-Phil-Demographic-Profile.pdf:</b> The target source document containing demographic statistics of the Philippines.", bullet_style))
    story.append(Paragraph("&bull; <b>.venv/:</b> The python virtual environment containing dependencies: <code>google-genai</code>, <code>langchain</code>, <code>pypdf</code>, and <code>deepagents</code>.", bullet_style))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("Workflow Pipeline:", h2_style))
    story.append(Paragraph(
        "1. <b>Text Extraction:</b> <code>app.py</code> uses <code>pypdf.PdfReader</code> to parse the local demographic document page-by-page and concatenate the raw text.<br/>"
        "2. <b>Agent Initialization:</b> A deep agent is instantiated with a system prompt setting its role as a precise data analyst.<br/>"
        "3. <b>Context Injection &amp; Query:</b> The extracted text (6,259 characters) is dynamically wrapped inside a prompt template along with the user question.<br/>"
        "4. <b>Inference:</b> The prompt is sent to Gemini, and the structured response is output to the console.",
        body_style
    ))
    
    # --- SECTION 3: CODE IMPLEMENTATION ---
    story.append(PageBreak()) # Let's put Code on Page 2 for clean formatting
    story.append(Paragraph("3. Source Code Implementation (app.py)", h1_style))
    story.append(Paragraph(
        "Below is the complete implementation of the LangChain agent script. It reads the local file, loads the agent, and executes the question-answering workflow:",
        body_style
    ))
    
    # Read the code from app.py
    try:
        with open("app.py", "r") as f:
            app_code = f.read()
    except Exception as e:
        app_code = "# Error loading app.py content: " + str(e)
        
    story.append(create_code_block(app_code, styles))
    story.append(Spacer(1, 10))
    
    # --- SECTION 4: TROUBLESHOOTING &amp; ITERATION ---
    story.append(Paragraph("4. Debugging &amp; Model Selection", h1_style))
    story.append(Paragraph(
        "During initial development and execution, the system encountered API communication errors. Below is a summary of the diagnostic history and resolution:",
        body_style
    ))
    
    trouble_text = (
        "<b>Model Error (404 Not Found):</b><br/>"
        "The agent was initially set to use the <code>gemini-1.5-flash</code> model. However, invocation returned a client error: "
        "<i>'models/gemini-1.5-flash is not found for API version v1beta, or is not supported for generateContent.'</i><br/><br/>"
        "<b>Resolution:</b><br/>"
        "The model parameter in <code>create_deep_agent</code> was updated to <b><code>google_genai:gemini-2.5-flash</code></b>. "
        "This matched the supported Google GenAI API endpoint, enabling successful authentication and inference."
    )
    story.append(create_callout_box(trouble_text, styles, border_color='#C53030', bg_color='#FFF5F5'))
    
    # --- SECTION 5: EXECUTION RESULTS ---
    story.append(Spacer(1, 10))
    story.append(Paragraph("5. Execution Results &amp; Agent Output", h1_style))
    story.append(Paragraph(
        "When successfully executed, the terminal logs the reading status, character length, and the final response from the Gemini model:",
        body_style
    ))
    
    terminal_output = (
        "[Reading] Reading the PDF file locally...<br/>"
        "[Success] Successfully read 6259 characters from the document.<br/>"
        "[Sending] Sending the text context and your question to Gemini in a single hop...<br/><br/>"
        "<b>[Agent Response] Final Agent Response:</b><br/>"
        "The Philippine total population reached 109,035,343 as of 01 May 2020."
    )
    story.append(create_callout_box(terminal_output, styles, border_color='#2F855A', bg_color='#F0FDF4'))
    
    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"🎉 Report generated successfully at {pdf_path}")

if __name__ == "__main__":
    main()
