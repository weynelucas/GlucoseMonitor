from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from GlucoseMonitor.settings import STATIC_ROOT
from datetime import date, datetime

pdfmetrics.registerFont(TTFont('Type Writer',             STATIC_ROOT + '/fonts/cmuntt.ttf'))
pdfmetrics.registerFont(TTFont('Type Writer Bold',        STATIC_ROOT + '/fonts/cmuntb.ttf'))
pdfmetrics.registerFont(TTFont('Type Writer Italic',      STATIC_ROOT + '/fonts/cmunit.ttf'))
pdfmetrics.registerFont(TTFont('Type Writer Italic Bold', STATIC_ROOT + '/fonts/cmuntb.ttf'))

TABLE_STYLES = {
    'REPORT_INFO_TABLE_STYLE': TableStyle([
        ('FONT', (0,0), (0,-1),  'Type Writer Bold'),
        ('FONT', (1,0), (1,-1),  'Type Writer Bold'),
        ('FONT', (1,1), (-1,-1), 'Type Writer'),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('VALIGN', (0,0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (-1,0), colors.gray),
        ('BACKGROUND', (0,0), (0,-1), colors.gray),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('SPAN', (0,0), (1,0)),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
    ]),
    'HISTORY_TABLE_STYLE': TableStyle([
        ('FONT', (0,0), (-1,0),  'Type Writer Bold'),
        ('FONT', (0,1), (-1,-1), 'Type Writer'),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('VALIGN', (0,0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (-1,0), colors.gray),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
    ]),
}

class PdfPrint:
    def __init__(self, buffer, pageSize):
        self.buffer = buffer
        if pageSize == 'Letter':
            self.pageSize = letter
        else:
            self.pageSize = A4
        self.width, self.height = self.pageSize

    def report(self, history, title):
        doc = SimpleDocTemplate(
            self.buffer,
            rightMargin  = 72,
            leftMargin   = 72,
            bottomMargin = 72,
            topMargin    = 30,
            pagesize     = self.pageSize
        )

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name="ReportTitle",  alignment=TA_CENTER,  fontName="Type Writer Bold", fontSize=25))
        styles.add(ParagraphStyle(name="WrapWord",     alignment=TA_JUSTIFY, fontName="Type Writer", parent=styles['BodyText'] ))

        data = []
        data.append(Paragraph(title, styles['ReportTitle']))
        data.append(Spacer(1, 25))

        report_info_table = Table(
            (('Informações', ''),
            ('Data de emissão', datetime.now().strftime('%d/%m/%Y %H:%M')),
            ('Período de observação', '01/07/2016 - 30/07/2016'),
            ('Total de registros', history.count())),
            (150,150),
            (24,16,16,18),
            hAlign='CENTER'
        )
        report_info_table.setStyle(TABLE_STYLES['REPORT_INFO_TABLE_STYLE'])
        data.append(report_info_table)
        data.append(Spacer(1, 25))

        history_data = []
        history_data.append([
            'Data', 'Hora', 'Condição', 'Nível', 'Notas'
        ])

        for register in history:
            history_data.append([
                register.datetime.strftime('%d/%m/%Y'),
                register.datetime.strftime('%H:%M'),
                register.get_measure_type_display(),
                "%.2f mg/dL" % (register.value),
                Paragraph(register.notes, styles['WrapWord']),
            ])

        history_table = Table(
            history_data,
            colWidths = (None, None, None, None, 75*mm),
            hAlign    = 'CENTER',
        )
        history_table.setStyle(TABLE_STYLES['HISTORY_TABLE_STYLE'])

        data.append(history_table)

        doc.build(data)
        pdf = self.buffer.getvalue()
        self.buffer.close()

        return pdf
