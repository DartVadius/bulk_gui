#!/usr/bin/python3 -u

from PyQt5.QtWidgets import QLabel, QMainWindow, QFormLayout, QAction, QFileDialog, QToolButton, QStyle, QComboBox
from PyQt5.QtGui import QIcon


class ParserForm(QMainWindow):
    file_name = None
    client_name = None

    def __init__(self, config):
        QMainWindow.__init__(self)
        self.form_layout = QFormLayout()
        self.file_label = QLabel()
        self.config = config

        openFile = QAction(self.style().standardIcon(getattr(QStyle, 'SP_DirOpenIcon')), 'Select file', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.show_dialog)

        message_file_select = QLabel('Select file:')

        button = QToolButton()
        button.setDefaultAction(openFile)
        button.setFixedSize(80, 30)

        self.clients = QComboBox()
        self.clients.addItems([None, 'silverstreet', 'mmds', 'nrs', 'idm', 'fortyTwo', 'itd'])
        self.clients.currentIndexChanged.connect(self.selectionchange)

        self.form_layout.addRow(message_file_select, button)
        self.form_layout.addRow(QLabel('Selected file:'), self.file_label)
        self.form_layout.addRow(QLabel('Select client:'), self.clients)

    def selectionchange(self):
        self.client_name = self.clients.currentText()

    def get_layout(self):
        return self.form_layout

    def show_dialog(self):
        file_name = QFileDialog.getOpenFileName(self, 'Select file', self.config['parser_path'])[0]
        file_name = file_name.split('/')
        self.file_name = file_name[-1]
        self.file_label.setText(self.file_name)

    def get_file_name(self):
        return self.file_name

    def get_client_name(self):
        return self.client_name
