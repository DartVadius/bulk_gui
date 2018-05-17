#!/usr/bin/python3 -u

from PyQt5.QtWidgets import QLabel, QLineEdit, QFormLayout


class CurlForm:
    id = None

    def __init__(self, sms=None):
        self.form_layout = QFormLayout()
        self.message_from = QLineEdit()
        self.message_to = QLineEdit()
        self.message_text = QLineEdit()
        if sms is not None:
            self.id = sms[0][0]
            self.message_from.setText(sms[0][1])
            self.message_to.setText(sms[0][2])
            self.message_text.setText(sms[0][3])

        message_from_label = QLabel('From:')
        message_to_label = QLabel('To:')
        message_text = QLabel('Text:')

        self.form_layout.addRow(message_from_label, self.message_from)
        self.form_layout.addRow(message_to_label, self.message_to)
        self.form_layout.addRow(message_text, self.message_text)

    def get_layout(self):
        return self.form_layout

    def get_from(self):
        return self.message_from.text()

    def get_to(self):
        return self.message_to.text()

    def get_text(self):
        return self.message_text.text()

    def get_id(self):
        return self.id
