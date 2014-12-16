# Copyright (c) 2014 by Ecreall under licence AGPL terms 
# avalaible on http://www.gnu.org/licenses/agpl.html 

# licence: AGPL
# author: Amen Souissi
import xlrd


def toInteger(value):
    return int(value)


def toBoolean(value):
    return bool(value)


def toString(value):
    return value


transformation_rols = {("String", False): toString,
                       ("Integer", False): toInteger,
                       ("Boolean", False): toBoolean}


# properties = {'at1':('Type', Multiplicity),...}
def create_object_from_xl(file, factory, properties):
    book = xlrd.open_workbook(file_contents=file.fp.read())
    sheet = book.sheet_by_index(0)# or: sheet_by_name("Ma feuille") 
    header = []
    for col_index in range(sheet.ncols):
        value = sheet.cell(rowx=0, colx=col_index).value
        header.append(value)

    objects = []
    properties_keys = dict([(k.lower(), k) for k in properties.keys()])
    for row_index in range(sheet.nrows)[1:]:
        obj = factory()
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

        obj.set_data(appstruct)
        objects.append(obj)

    return objects
