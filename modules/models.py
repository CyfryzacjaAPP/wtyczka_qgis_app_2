# -*- coding: utf-8 -*-
class FormElement:
    """ reprezentuje element definicji formularza zdefiniowany w XSD"""

    def __init__(self, name, form, type='', minOccurs=1, documentation='', value=[], attributes={}):
        self.setName(name)
        self.setType(type)
        self.setMinOccurs(minOccurs)
        self.setDocumentation(documentation)
        self.__isComplex = False
        self.innerFormElements = []
        self.isNillable = False
        self.setValue(value)  # obiekt ET.Element w XML
        self.attributes = {}  # atrybuty przyjmowane przez element
        self.refObject = None  # referencja na obiekt
        self.refNilObject = None  # referencja na obiekt
        self.maxOccurs = None
        self.form = form    # wskazanie formularza do ktorego obiekt nalezy

    def setName(self, name):
        self.name = name

    def setType(self, type):
        self.type = type

    def setNillable(self):
        self.isNillable = False
        self.minOccurs = 0

    def setMinOccurs(self, minOccurs):
        self.minOccurs = int(minOccurs)

    def setMaxOccurs(self, maxOccurs):
        self.maxOccurs = maxOccurs

    def setDocumentation(self, documentation):
        self.documentation = documentation

    def markAsComplex(self):
        self.__isComplex = True

    def isComplex(self):
        return self.__isComplex

    def setInnerFormElement(self, form):
        if self.isComplex():
            self.innerFormElements.append(form)
        else:
            raise NotImplementedError

    def setValue(self, value):
        self.value = value

    def setAttribute(self, attributes):
        # Lista (slownik) atrybutów elementu
        for key in attributes.keys():
            self.attributes[key] = attributes[key]


class AppTableModel:
    """Wiersz tabeli przygotowanai zbioru APP"""

    def __init__(self, rowId, path, date):
        self.rowId = rowId
        self.path = path
        self.date = date

    def __str__(self):
        return "%s, %s, %s" % (self.rowId, self.path, self.date)
