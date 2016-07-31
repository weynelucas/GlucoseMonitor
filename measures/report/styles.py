from reportlab.pdfbase         import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units       import mm
from reportlab.lib             import colors
from reportlab.platypus        import TableStyle
from GlucoseMonitor.settings   import STATIC_ROOT

# Load fonts
pdfmetrics.registerFont(TTFont('Type Writer',             STATIC_ROOT + '/fonts/cmuntt.ttf'))
pdfmetrics.registerFont(TTFont('Type Writer Bold',        STATIC_ROOT + '/fonts/cmuntb.ttf'))
pdfmetrics.registerFont(TTFont('Type Writer Italic',      STATIC_ROOT + '/fonts/cmunit.ttf'))
pdfmetrics.registerFont(TTFont('Type Writer Italic Bold', STATIC_ROOT + '/fonts/cmuntb.ttf'))

# Table styles
tableStyles = {
    'info': TableStyle([
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
    'history': TableStyle([
        ('FONT', (0,0), (-1,0),  'Type Writer Bold'),
        ('FONT', (0,1), (-1,-1), 'Type Writer'),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('VALIGN', (0,0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (-1,0), colors.gray),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
    ]),
}
