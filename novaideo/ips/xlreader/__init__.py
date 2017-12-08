# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi
import xlrd


SEPARATOR = ','

TRUE_VALUE = 'true'

def toInteger(value):
    return int(str(value).strip())


def toBoolean(value):
    return str(value).strip() == TRUE_VALUE


def toString(value):
    return str(value).strip()


def toStrings(value):
    return [a.strip() for a in str(value).split(SEPARATOR) if a.strip()]


transformation_rols = {("String", False): toString,
                       ("String", True): toStrings,
                       ("Integer", False): toInteger,
                       ("Boolean", False): toBoolean}


# properties = {'at1':('Type', Multiplicity),...}
def get_data_from_xl(file, properties):
    book = xlrd.open_workbook(file_contents=file.fp.read())
    sheet = book.sheet_by_index(0)# or: sheet_by_name("Ma feuille") 
    header = []
    for col_index in range(sheet.ncols):
        value = sheet.cell(rowx=0, colx=col_index).value
        header.append(value)

    data = []
    properties_keys = dict([(k.lower(), k) for k in properties.keys()])
    for row_index in range(sheet.nrows)[1:]:
        appstruct = {}
        for col_index in range(sheet.ncols):
            value = sheet.cell(rowx=row_index, colx=col_index).value
            key = header[col_index].lower()
            if key in properties_keys:
                metadata = properties[key]
                property_type = metadata[0]
                multiplicity = metadata[1]
                value = transformation_rols[(property_type, multiplicity)](value)
                appstruct[properties_keys[key]] = value

        data.append(appstruct)

    return data
