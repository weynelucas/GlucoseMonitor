from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from .writer import add_info_table, add_history_table, wrap_word_cell, add_title

class ReportGenerator:
    report_title = 'Relatório'
    info_title  = 'Informações'
    info_labels = ['Usuário', 'Data de emissão do relatório', 'Período de observação', 'Total de registros']
    history_labels = ['Data', 'Hora', 'Condição', 'Nível', 'Notas']

    def __init__(self, **kwargs):
        self.buffer   = kwargs.get('buffer', BytesIO())
        self.pageSize = kwargs.get('pageSize', A4)

        if self.pageSize == 'Letter':
            self.pageSize = letter

        self.width, self.height = self.pageSize
        self.doc    = self.loadDocumentTemplate()

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

    def generatePdfReport(self, objects, period_interval):
        doc_data = []
        add_title(doc_data, self.report_title)

        info_values = [
            objects[0].user.get_full_name(),
            datetime.now().strftime('%d/%m/%Y %H:%M'),
            "%s - %s" % (period_interval[0].strftime('%d/%m/%Y'), period_interval[1].strftime('%d/%m/%Y')),
            objects.count()
        ]
        add_info_table(doc_data, self.info_title, self.info_labels, info_values)


        objects_data = []
        for obj in objects:
            objects_data.append([
                obj.datetime.strftime('%d/%m/%Y'),
                obj.datetime.strftime('%H:%M'),
                obj.get_measure_type_display(),
                "%.2f mg/dL" % (obj.value),
                wrap_word_cell(obj.notes),
            ])

        add_history_table(doc_data, self.history_labels, objects_data)
        self.doc.build(doc_data)
        pdf = self.buffer.getvalue()
        self.buffer.close()

        return pdf
