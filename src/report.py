# Functions to generates reports
from fpdf import FPDF

def generate_report(tipo_var):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, 'Data|Analysis|Pipeline Poetry')
    if tipo_var[0]=="year":
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 40, 'Report for the year ' + str(tipo_var[1]))
        
        pdf.image('output/f_year.png', x = 10, y = 40, w = 150, h = 0, type = 'png')

    if tipo_var[0]=="word":
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 40, 'Report for the word ' + tipo_var[1])
        
        pdf.image('output/f_uw.png', x = 10, y = 40, w = 150, h = 0, type = 'png')

    if tipo_var[0]=="general":
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 40, 'Report General' )
        
        pdf.image('output/f_complex.png', x = 10, y = 40, w =150, h = 0, type = 'png')

    pdf.cell(40, 10, '')
    
    pdf.output('output/report_'+tipo_var[0]+'.pdf', 'F')
   
    return True

def generate_mail_report(mail):
    
    return True
