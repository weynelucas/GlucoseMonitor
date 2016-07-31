from reportlab.platypus  import Table, Spacer
from reportlab.lib.units import mm
from .styles             import tableStyles


def add_space(doc_data, width=1, height=25):
    """ Add white space to document
        Args:
            doc_data : Document data to append spacer
            width    : Horizontal space value
            height   : Vertical space value
    """
    doc_data.append(Spacer(width, height))

def add_table(doc_data, table_data, table_style, **kwargs):
    """ Add table to document data
        Args:
            doc_data   : Document data to append table
            table_data : Tuple of tuples with table data
            table_style: Table style object
            **kwargs   : Table settings arguments (hAlign, colWidths)
    """
    table = Table(
        table_data,
        colWidths = kwargs.get('colWidths', [None]*len(table_data[0])),
        hAlign    = kwargs.get('hAlign', 'CENTER')
    )
    table.setStyle(table_style)
    doc_data.append(table)
    add_space(doc_data)

def add_info_table(doc_data, title, labels, values):
    """ Add an info table, a table with two columns, one of labels,
        and other of values

        Args:
            doc_data : Document data to append table
            title    : Title of info table
            labels   : Array with labels (strings)
            values   : Array of values
    """
    titlePair = ((title, ''),)
    labelsValuesPair = tuple(zip(labels, values))

    table_data = titlePair + labelsValuesPair

    add_table(doc_data, table_data, tableStyles['info'])

def add_history_table(doc_data, labels, history_data):
    """ Add an history table, a table to display distribution of
        data

        Args:
            doc_data     : Document data to append table
            labels       : Array with labels (strings)
            history_data : Array of arrays with values (each array is a arrange of object properties - values)
    """

    table_data = [labels] + history_data
    add_table(doc_data, table_data, tableStyles['history'], colWidths=tuple([None]*(len(labels)-1)) + (75*mm,))
