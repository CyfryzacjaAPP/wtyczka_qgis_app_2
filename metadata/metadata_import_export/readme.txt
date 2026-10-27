"""

metadataElementDict - słownik zawierający elementID jako klucz np 'e23' i wartość elementu jako:
    - listę - dla elementów wielokrotnych (tam gdzie jest QListWidget) - lista zawiera słowniki "data" przechowywane w QListWidgetItem.
      każdy słownik zawiera jako klucz - nazwę pola, jako wartość -wartość pola np. dla e9: [{'e9_lineEdit': 'Zagospodarowanie przestrzenne'}, {'e9_lineEdit': 'PlannedLandUse'}]
    - słownik - dla pojedynczych - zawierający nazwę pola i wartość np: e13: {'e13_cmbbx': 'utworzenie', 'e13_dateTimeEdit': PyQt5.QtCore.QDateTime(2020, 7, 26, 18, 16, 2, 978)}

"""