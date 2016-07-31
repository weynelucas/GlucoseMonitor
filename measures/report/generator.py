from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from .writer import add_info_table, add_history_table

class ReportGenerator:
    info_title  = 'Informações'
    info_labels = ['Data de emissão do relatório', 'Período de observação', 'Total de registros']
    history_labels = ['Data', 'Hora', 'Condição', 'Nível', 'Notas']

    def __init__(self, **kwargs):
        self.buffer   = kwargs.get('buffer', BytesIO())
        self.pageSize = kwargs.get('pageSize', A4)

        if self.pageSize == 'Letter':
            self.pageSize = letter

        self.width, self.height = self.pageSize

        self.styles = self.loadStyles()
        self.doc    = self.loadDocumentTemplate()

    def loadStyles(self):
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name="ReportTitle",  alignment=TA_CENTER,  fontName="Type Writer Bold", fontSize=25))
        styles.add(ParagraphStyle(name="SectionTitle", alignment=TA_JUSTIFY, fontName="Type Writer Bold", fontSize=16))
        styles.add(ParagraphStyle(name="WrapWord",     alignment=TA_JUSTIFY, fontName="Type Writer", parent=styles['BodyText']))

        return styles

    def loadDocumentTemplate(self):
        doc_template =  SimpleDocTemplate(
            self.buffer,
            rightMargin  = 72,
            leftMargin   = 72,
            bottomMargin = 72,
            topMargin    = 30,
            pagesize     = self.pageSize
        )
        return doc_template

    def generatePdfReport(self, objects):
        doc_data = []
        add_info_table(doc_data, self.info_title, self.info_labels, [datetime.now().strftime('%d/%m/%Y %H:%M'), '01/07/2016 - 30/07/2016', objects.count()])


        objects_data = []
        for obj in objects:
            objects_data.append([
                obj.datetime.strftime('%d/%m/%Y'),
                obj.datetime.strftime('%H:%M'),
                obj.get_measure_type_display(),
                "%.2f mg/dL" % (obj.value),
                Paragraph(obj.notes, self.styles['WrapWord']),
            ])

        add_history_table(doc_data, self.history_labels, objects_data)
        self.doc.build(doc_data)
        pdf = self.buffer.getvalue()
        self.buffer.close()

        return pdf
