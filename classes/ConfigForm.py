#!/usr/bin/python3 -u

from PyQt5.QtWidgets import QLabel, QLineEdit, QFormLayout


class ConfigForm:

    def __init__(self, config=None):
        self.form_layout = QFormLayout()
        self.smpp_path = QLineEdit()
        self.smpp_user = QLineEdit()
        self.smpp_pass = QLineEdit()
        self.api_user = QLineEdit()
        self.api_pass = QLineEdit()
        self.parser_path = QLineEdit()
        self.parser_script_command = QLineEdit()
        if config is not None:
            self.smpp_path.setText(config['path'])
            self.smpp_user.setText(config['user'])
            self.smpp_pass.setText(config['pass'])
            if 'username' in config.keys():
                self.api_user.setText(config['username'])
            if 'api_key' in config.keys():
                self.api_pass.setText(config['api_key'])
            if 'parser_path' in config.keys():
                self.parser_path.setText(config['parser_path'])
            if 'script_command' in config.keys():
                self.parser_script_command.setText(config['script_command'])

        smpp_path_label = QLabel('URL:')
        smpp_user_label = QLabel('Smpp user:')
        smpp_pass_label = QLabel('Smpp pass:')
        api_user_label = QLabel('API user:')
        api_pass_label = QLabel('API key:')
        parser_path_label = QLabel('Path to parser:')
        parser_script_command_label = QLabel('Script command:')

        self.form_layout.addRow(smpp_path_label, self.smpp_path)
        self.form_layout.addRow(smpp_user_label, self.smpp_user)
        self.form_layout.addRow(smpp_pass_label, self.smpp_pass)
        self.form_layout.addRow(api_user_label, self.api_user)
        self.form_layout.addRow(api_pass_label, self.api_pass)
        self.form_layout.addRow(parser_path_label, self.parser_path)
        self.form_layout.addRow(parser_script_command_label, self.parser_script_command)

    def get_layout(self):
        return self.form_layout

    def get_path(self):
        return self.smpp_path.text()

    def get_user(self):
        return self.smpp_user.text()

    def get_pass(self):
        return self.smpp_pass.text()

    def get_user_api(self):
        return self.api_user.text()

    def get_pass_api(self):
        return self.api_pass.text()

    def get_parser_path(self):
        return self.parser_path.text()

    def get_parser_script_command(self):
        return self.parser_script_command.text()
