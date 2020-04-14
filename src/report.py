# Functions to generates reports
from fpdf import FPDF

def generate_report(tipo_var):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, 'Data|Analysis|Pipeline Poetry')
    if tipo_var[0]=="year":
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(60, 10, 'Report for the year ' + tipo_var[1])
        
        fpdf.image('output/f_year.png', x = 75, y = 10, w = 0, h = 0, type = 'png')

    if tipo_var[0]=="word":
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(60, 10, 'Report for the word ' + tipo_var[1])
        
        fpdf.image('output/f_uw.png', x = 75, y = 10, w = 0, h = 0, type = 'png')
    if tipo_var[0]=="general":


    pdf.cell(40, 10, '')
    
    pdf.output('output/report.pdf', 'F')
   
    return True

def generate_mail_report(mail):

    return True

