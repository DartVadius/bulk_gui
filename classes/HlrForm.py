#!/usr/bin/python3 -u

from PyQt5.QtWidgets import QLabel, QLineEdit, QFormLayout


class HlrForm:

    def __init__(self):
        self.form_layout = QFormLayout()
        self.phone = QLineEdit()

        message_phone_label = QLabel('Phone:')

        self.form_layout.addRow(message_phone_label, self.phone)

    def get_layout(self):
        return self.form_layout

    def get_phone(self):
        return self.phone.text()
