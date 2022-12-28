from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.platypus.flowables import Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfdoc
from reportlab.pdfbase.pdfmetrics import registerFont, registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_RIGHT
import yaml
# Import our font
registerFont(TTFont('Inconsolata', 'fonts/Inconsolata-Regular.ttf'))
registerFont(TTFont('InconsolataBold', 'fonts/Inconsolata-Bold.ttf'))
registerFontFamily('Inconsolata', normal='Inconsolata', bold='InconsolataBold')

# Set the page height and width
HEIGHT = 11 * inch
WIDTH = 8.5 * inch

# Set our styles
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Content',
                          fontFamily='Inconsolata',
                          fontSize=8,
                          spaceAfter=.1*inch))
                            


def generate_print_pdf(data, contact):
    pdfname = 'resume.pdf'
    doc = SimpleDocTemplate(
        pdfname,
        pagesize=letter,
        bottomMargin=.5 * inch,
        topMargin=.7 * inch,
        rightMargin=.4 * inch,
        leftMargin=.4 * inch)  # set the doc template
    style = styles["Normal"]  # set the style to normal
    story = []  # create a blank story to tell
    contentTable = Table(
        data,
        colWidths=[
            0.8 * inch,
            6.9 * inch])
    tblStyle = TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONT', (0, 0), (-1, -1), 'Inconsolata'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT')])
    contentTable.setStyle(tblStyle)
    story.append(contentTable)
    doc.build(
        story,
        onFirstPage=myPageWrapper(
            contact)
        )
    return pdfname


"""
    Draw the framework for the first page,
    pass in contact info as a dictionary
"""
def myPageWrapper(contact):
    # template for static, non-flowables, on the first page
    # draws all of the contact information at the top of the page
    def myPage(canvas, doc):
        canvas.saveState()  # save the current state
        canvas.setFont('InconsolataBold', 16)  # set the font for the name
        canvas.drawString(
            3.5 * inch,
            HEIGHT - (.4 * inch),
            contact['name'])  # draw the name on top left page 1
        canvas.setFont('Inconsolata', 8)  # sets the font for contact
        canvas.drawRightString(
            WIDTH - (.4 * inch),
            HEIGHT - (.4 * inch),
            contact['website'])  
        canvas.line(.4 * inch, HEIGHT - (.47 * inch), 
            WIDTH - (.4 * inch), HEIGHT - (.47 * inch))
        canvas.drawString(
            .4 * inch,
            HEIGHT - (.6 * inch),
            contact['phone'])
        canvas.drawCentredString(
			0.75 * inch,
			HEIGHT - (.4 * inch),
			contact['address'])
        canvas.drawRightString(
			WIDTH - (.4 * inch),
			HEIGHT - (.6 * inch),
			contact['email'])
        
        # Job Vert Line
        # func_that_draws_line_on_each_company_entry()
        canvas.line(
            WIDTH - (7.35 * inch),
            HEIGHT - (.85 * inch),
            WIDTH - (7.35 * inch),
            HEIGHT - (3.5 * inch)        
            )
        # restore the state to what it was when saved
        canvas.restoreState()
    return myPage



if __name__ == "__main__":
    with open("work_experience.yml", "r") as f: 

        contact = {
            'name': 'Dan DeAngelis',
            'website': 'https://github.com/dd921',
            'email': 'daniel.deangelis98@gmail.com',
            'address': 'Richmond, VA',
            'phone': '617-458-0102'}
        data = {
            
            'education': '<br/>'.join(['<b>Virginia Tech</b>',
                        '<b>B.S.</b>  Industrial & Systems Engineering, Cum Laude <br/>'
                        '<b>Graduated:</b> May 2021']),
            'skills':   '<br/>'.join(['<b>Languages</b>  Python, SQL, Git, Spark',
                        '<b>Services:</b> Snowflake, Databricks, AWS (EC2, S3), Github, Jenkins, Tableau',
                        '<b>Certifications:</b> AWS Solutions Architect Associate']),
            'experience': ['<br/>'.join(value for key, value in yaml.safe_load(f).items())],
                        #[''.join(['<b>Capital One</b> - Richmond, VA<br/>',
                        # '<alignment=TA_RIGHT><b>Senior Data Analyst: </b> Aug 2022 - Present</alignment><br/>',
                        # 'Stuff ',]),
                        # ''.join(['<b>Data Analyst</b> Aug 2021 - Jul 2022<br/>',
                        # 'Developed Stuff ',]),
                        # ''.join(['<b>Data Analyst Intern </b> Jun 2020 - Aug 2020<br/>',
                        # 'Developed Stuff ',])],
            'projects': [
                        ''.join(['<b>Resume Generator</b> - http://github.com/LINK_HERE<br/>',
                        'Created a resume generator with configuration files to input experience, education, skills, and projects.',
                        '<br/>This resume is a product of that project.',]),
                        ''.join(['<b>PROJECT TBD</b> - http://github.com/LINK_HERE<br/>',
                        'Description Here',]),
                        ] 
        }
    tblData = [
        ['EXPERIENCE', [Paragraph(x, styles['Content']) for x in data['experience']]],
        ['EDUCATION', Paragraph(data['education'], styles['Content'])],
        ['SKILLS', Paragraph(data['skills'], styles['Content'])],
        ['PROJECTS', [Paragraph(x, styles['Content']) for x in data['projects']]]
        ]
    
    generate_print_pdf(tblData, contact)
   