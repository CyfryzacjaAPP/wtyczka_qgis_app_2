# -*- coding: utf-8 -*-
class FormElement:
    """ reprezentuje element definicji formularza zdefiniowany w XSD"""

    def __init__(self, name, form, type='', minOccurs=1, documentation='', value=[], attributes={}):
        """Inicjalizuje obiekt klasy `FormElement` i konfiguruje jego stan początkowy."""
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
        """Ustawia dane lub stan wymagany przez operację `setName`."""
        self.name = name

    def setType(self, type):
        """Ustawia dane lub stan wymagany przez operację `setType`."""
        self.type = type

    def setNillable(self):
        """Ustawia dane lub stan wymagany przez operację `setNillable`."""
        self.isNillable = False
        self.minOccurs = 0

    def setMinOccurs(self, minOccurs):
        """Ustawia dane lub stan wymagany przez operację `setMinOccurs`."""
        self.minOccurs = int(minOccurs)

    def setMaxOccurs(self, maxOccurs):
        """Ustawia dane lub stan wymagany przez operację `setMaxOccurs`."""
        self.maxOccurs = maxOccurs

    def setDocumentation(self, documentation):
        """Ustawia dane lub stan wymagany przez operację `setDocumentation`."""
        self.documentation = documentation

    def markAsComplex(self):
        """Realizuje operację `markAsComplex` w bieżącym module."""
        self.__isComplex = True

    def isComplex(self):
        """Sprawdza warunek określony przez operację `isComplex` i zwraca jego wynik."""
        return self.__isComplex

    def setInnerFormElement(self, form):
        """Ustawia dane lub stan wymagany przez operację `setInnerFormElement`."""
        if self.isComplex():
            self.innerFormElements.append(form)
        else:
            raise NotImplementedError

    def setValue(self, value):
        """Ustawia dane lub stan wymagany przez operację `setValue`."""
        self.value = value

    def setAttribute(self, attributes):
        # Lista (slownik) atrybutów elementu
        """Ustawia dane lub stan wymagany przez operację `setAttribute`."""
        for key in attributes.keys():
            self.attributes[key] = attributes[key]


class AppTableModel:
    """Wiersz tabeli przygotowanai zbioru APP"""

    def __init__(self, rowId, path, date):
        """Inicjalizuje obiekt klasy `AppTableModel` i konfiguruje jego stan początkowy."""
        self.rowId = rowId
        self.path = path
        self.date = date

    def __str__(self):
        """Zwraca wynik operacji `__str__` wykonywanej w bieżącym module."""
        return "%s, %s, %s" % (self.rowId, self.path, self.date)
