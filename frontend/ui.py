from PyQt5 import QtCore, QtGui, QtWidgets
from backend.db_saver import db_titles_saves, db_load


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(1350, 770)
        self.MainWindow = MainWindow

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(30, 10, 550, 440))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 548, 218))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.scrollArea_2 = QtWidgets.QScrollArea(self.centralwidget)

        self.scrollArea_2.setGeometry(QtCore.QRect(30, 550, 550, 175))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.programm_massege = QtWidgets.QTextEdit(self.scrollAreaWidgetContents_2)
        self.programm_massege.setGeometry(QtCore.QRect(0, 0, 550, 175))
        self.programm_massege.setReadOnly(True)
        self.programm_massege.setObjectName("programm_massege")
        self.programm_massege.setStyleSheet('''QTextEdit {font: 14pt "Consolas";}''')

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 548, 418))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.textEdit = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
        self.textEdit.setGeometry(QtCore.QRect(0, 0, 550, 440))
        self.textEdit.setAutoFormatting(QtWidgets.QTextEdit.AutoAll)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setStyleSheet('''QTextEdit {font: 14pt "Consolas";}''')

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        # Кнопочки
        btn_wight, indent = 115, 30

        self.button_start = QtWidgets.QPushButton(self.centralwidget)
        self.button_start.setGeometry(QtCore.QRect(indent, 465, btn_wight, 70))
        self.button_start.setObjectName("button_start")

        self.button_start_with_reset = QtWidgets.QPushButton(self.centralwidget)
        self.button_start_with_reset.setGeometry(QtCore.QRect(1*btn_wight + 2*indent, 465, btn_wight, 70))
        self.button_start_with_reset.setObjectName("button_start_with_reset")

        self.button_stop = QtWidgets.QPushButton(self.centralwidget)
        self.button_stop.setGeometry(QtCore.QRect(2*btn_wight + 3*indent, 465, btn_wight, 70))
        self.button_stop.setObjectName("button_stop")

        self.button_reformat = QtWidgets.QPushButton(self.centralwidget)
        self.button_reformat.setGeometry(QtCore.QRect(3*btn_wight + 4*indent, 465, btn_wight, 70))
        self.button_reformat.setObjectName("button_reformat")

        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(610, 30, 720, 720))
        self.widget.setObjectName("widget")

        # "Всплывашки"
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1360, 21))
        self.menubar.setObjectName("menubar")

        self.menu_file = QtWidgets.QMenu(self.menubar)
        self.menu_file.setObjectName("menu_file")

        self.menu_export_import = QtWidgets.QMenu(self.menubar)
        self.menu_export_import.setGeometry(QtCore.QRect(302, 133, 135, 94))
        self.menu_export_import.setObjectName("menu_export_import")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionNew_file = QtWidgets.QAction(MainWindow)
        self.actionNew_file.setObjectName("actionNew_file")
        self.menu_file.addAction(self.actionNew_file)

        self.actionOpen_txt = QtWidgets.QAction(MainWindow)
        self.actionOpen_txt.setObjectName("actionOpen_txt")
        self.actionOpen_txt.setShortcut("Ctrl+O")
        self.menu_file.addAction(self.actionOpen_txt)

        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave.setShortcut("Ctrl+S")
        self.menu_file.addAction(self.actionSave)

        self.actionSave_as_txt = QtWidgets.QAction(MainWindow)
        self.actionSave_as_txt.setObjectName("actionSave_as_txt")
        self.actionSave_as_txt.setShortcut("Ctrl+D")
        self.menu_file.addAction(self.actionSave_as_txt)

        self.actionImport_file = QtWidgets.QAction(MainWindow)
        self.actionImport_file.setObjectName("actionImport_file")
        self.menu_export_import.addAction(self.actionImport_file)

        self.actionImport_db = QtWidgets.QAction(MainWindow)
        self.actionImport_db.setObjectName("actionImport_db")
        self.menu_export_import.addAction(self.actionImport_db)

        self.actionExport_as_txt = QtWidgets.QAction(MainWindow)
        self.actionExport_as_txt.setObjectName("actionExport_as_txt")
        self.menu_export_import.addAction(self.actionExport_as_txt)

        self.actionSave_coords = QtWidgets.QAction(MainWindow)
        self.actionSave_coords.setObjectName("actionSave_coords")
        self.menu_file.addAction(self.actionSave_coords)

        self.actionLoad_coords = QtWidgets.QAction(MainWindow)
        self.actionLoad_coords.setObjectName("actionLoad_coords")
        self.menu_file.addAction(self.actionLoad_coords)

        # Всплывашки всплывашки
        self.delete_menu = QtWidgets.QMenu(self.menubar)
        self.delete_menu.setObjectName("delete_menu")

        self.export_menu = QtWidgets.QMenu(self.menubar)
        self.export_menu.setObjectName("export_menu")

        for db_save_name in db_titles_saves():
            self.__dict__["export_for_sub_menu_" + db_save_name] = QtWidgets.QAction(self.MainWindow)
            self.__dict__["export_for_sub_menu_" + db_save_name].setText(db_save_name)
            self.export_menu.addAction(self.__dict__["export_for_sub_menu_" + db_save_name])

            # Делуем глубокую копию кнопок, специально для удаления
            self.__dict__["deleting_for_sub_menu_" + db_save_name] = QtWidgets.QAction(self.MainWindow)
            self.__dict__["deleting_for_sub_menu_" + db_save_name].setText(db_save_name)
            self.delete_menu.addAction(self.__dict__["deleting_for_sub_menu_" + db_save_name])

        self.menu_export_import.addMenu(self.export_menu)
        self.menu_export_import.addMenu(self.delete_menu)

        # Добавляем элементы меню в прогу
        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_export_import.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        """Даём стили и названия"""
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Нейрошарики: GridMaster"))
        MainWindow.setWindowIcon(QtGui.QIcon("./_internal/frontend/Icon.ico"))
        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\n</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">fdfsd</span></p></body></html>"))
        self.programm_massege.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\n</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">Всё работает</span></p></body></html>"))

        self.button_start.setText(_translate("MainWindow", "СТАРТ"))
        self.button_start_with_reset.setText(_translate("MainWindow", "СТАРТ СО\nСБРОСОМ"))
        self.button_stop.setText(_translate("MainWindow", "ПАУЗА"))
        self.button_reformat.setText(_translate("MainWindow", "ФОРМАТИРОВАТЬ\nКОД"))

        self.menu_file.setTitle(_translate("MainWindow", "Файл"))
        self.actionSave_coords.setText(_translate("MainWindow", "Сохранить координаты"))
        self.actionLoad_coords.setText(_translate("MainWindow", "Загрузить координаты"))
        self.actionNew_file.setText(_translate("MainWindow", "Новый файл"))
        self.actionSave.setText(_translate("MainWindow", "Сохранить"))
        self.actionOpen_txt.setText(_translate("MainWindow", "Открыть файл"))
        self.actionSave_as_txt.setText(_translate("MainWindow", "Сохранить как txt"))

        self.menu_export_import.setTitle(_translate("MainWindow", "Экспорт/Импорт"))
        self.actionExport_as_txt.setText(_translate("MainWindow", "Экспортировать как txt"))
        self.actionImport_db.setText(_translate("MainWindow", "Импортировать в бд"))
        self.actionImport_file.setText(_translate("MainWindow", "Импортировать файл"))
        self.export_menu.setTitle("Экспорт:")
        self.delete_menu.setTitle("Удалить:")
