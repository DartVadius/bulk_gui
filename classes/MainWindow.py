#!/usr/bin/python3 -u

from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QAction, QSystemTrayIcon, QStyle, QMenu, \
    QMessageBox, QDesktopWidget, QPushButton, QVBoxLayout, QHBoxLayout, \
    QFrame, QGroupBox, QScrollArea, QSizePolicy
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from connector import Connector
from classes.CurlForm import CurlForm
from classes.ConfigForm import ConfigForm
from classes.ParserForm import ParserForm
from classes.HlrForm import HlrForm
import requests
import subprocess


def clear_layout(layout):
    while layout.count() > 0:
        item = layout.takeAt(0)
        if not item:
            continue
        w = item.widget()
        if w:
            w.deleteLater()


def action_decorator(method_to_decorate):
    def action_wrapper(self):
        clear_layout(self.main_field)
        method_to_decorate(self)

    return action_wrapper


# Наследуемся от QMainWindow
class MainWindow(QMainWindow):
    main_window = None
    main_field = None
    main_widget = None
    left_menu = None
    form_layout = None
    connector = None
    hlr_res = None

    # Переопределяем конструктор класса
    def __init__(self):
        # Обязательно нужно вызвать метод супер класса
        QMainWindow.__init__(self)

        self.connector = Connector()

        self.setup_app()
        self.set_main_menu()
        self.set_tray()
        self.statusBar()

        # создаем центральный виджет
        self.central_widget = QWidget(self)  # Создаём центральный виджет
        self.setCentralWidget(self.central_widget)  # Устанавливаем центральный виджет
        self.central_widget.setLayout(self.set_main_window())  # Устанавливаем представление в центральный виджет

    # настраиваем рабочую область приложения
    def set_main_window(self):
        self.main_window = QHBoxLayout()
        self.main_field = QVBoxLayout()
        self.main_widget = QFrame(self)
        self.main_field.addWidget(self.main_widget)
        self.left_menu = self.left_menu()
        self.main_window.addLayout(self.left_menu)
        self.main_window.addLayout(self.main_field)
        self.main_window.setStretchFactor(self.left_menu, 1)
        self.main_window.setStretchFactor(self.main_field, 9)
        return self.main_window

    def left_menu(self):
        left_menu = QVBoxLayout()
        names = [
            'SMPP/HTTP API',
            'HLR',
            'Parser',
            'Config',
        ]
        actions = [
            self.query,
            self.hlr,
            self.parse,
            self.config,
        ]
        for name, action in zip(names, actions):
            button = QPushButton(name)
            button.clicked.connect(action)
            button.setStyleSheet("width: 130px; height: 40px;")
            left_menu.addWidget(button)
        left_menu.addStretch()
        return left_menu

    @action_decorator
    def hlr(self):
        self.main_widget = QGroupBox()
        self.form_layout = HlrForm()
        self.main_widget.setLayout(self.form_layout.get_layout())
        self.main_field.addWidget(self.main_widget)
        button_layout = self.hlr_button_layout()
        group_box = QGroupBox(self)
        group_box.setLayout(button_layout)
        self.main_field.addWidget(group_box)
        self.hlr_res = QLabel()
        self.hlr_res.setWordWrap(True)
        self.main_field.addWidget(self.hlr_res)
        self.main_field.addStretch()

    @action_decorator
    def parse(self):
        config = self.connector.get_config()
        self.main_widget = QGroupBox()
        self.form_layout = ParserForm(config)
        self.main_widget.setLayout(self.form_layout.get_layout())
        self.main_field.addWidget(self.main_widget)
        button_layout = self.parser_button_layout()
        group_box = QGroupBox(self)
        group_box.setLayout(button_layout)
        self.main_field.addWidget(group_box)
        self.main_field.addStretch()

    @action_decorator
    def query(self):
        sms = self.connector.get_last_sms()
        self.main_widget = QGroupBox()

        self.form_layout = CurlForm(sms)

        self.main_widget.setLayout(self.form_layout.get_layout())
        self.main_field.addWidget(self.main_widget)
        button_layout = self.query_button_layout()
        group_box = QGroupBox(self)
        group_box.setLayout(button_layout)
        self.main_field.addWidget(group_box)
        sms_box = self.sms_box()
        self.main_field.addWidget(sms_box)
        self.main_field.addStretch()

    @action_decorator
    def config(self):

        config = self.connector.get_config()

        self.main_widget = QGroupBox()
        self.form_layout = ConfigForm(config)
        self.main_widget.setLayout(self.form_layout.get_layout())
        self.main_field.addWidget(self.main_widget)
        button_layout = self.config_button_layout()
        group_box = QGroupBox(self)
        group_box.setLayout(button_layout)
        self.main_field.addWidget(group_box)
        self.main_field.addStretch()

    def sms_box(self):
        sms = self.connector.get_last_sms(10)
        sms_box = QScrollArea()
        sms_box.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        sms_box.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        sms_box.setWidgetResizable(True)
        widget = QWidget()
        sms_box.setWidget(widget)
        layout = QVBoxLayout(widget)
        for row in sms:
            view = self.sms_view(row)
            view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            layout.addWidget(view)
        layout.addStretch()

        return sms_box

    def sms_view(self, row=None):
        group_box = QGroupBox(self)
        # group_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sms = QGridLayout()
        sms.addWidget(QLabel('From: '), 0, 1)
        sms_from = QLabel(row[1])
        sms_from.setTextInteractionFlags(Qt.TextSelectableByMouse)
        sms.addWidget(sms_from, 0, 2)
        sms.addWidget(QLabel('To: '), 1, 1)
        sms_to = QLabel(row[2])
        sms_to.setTextInteractionFlags(Qt.TextSelectableByMouse)
        sms.addWidget(sms_to, 1, 2)
        sms.addWidget(QLabel('Text: '), 2, 1)
        sms_text = QLabel(row[3])
        sms_text.setTextInteractionFlags(Qt.TextSelectableByMouse)
        sms.addWidget(sms_text, 2, 2)
        sms.addWidget(QLabel('Status: '), 3, 1)
        status = QLabel(row[4])
        status.setTextInteractionFlags(Qt.TextSelectableByMouse)
        status.setWordWrap(True)
        sms.addWidget(status, 3, 2, 1, 10)
        group_box.setLayout(sms)
        return group_box

    def hlr_button_layout(self):
        button_layout = QGridLayout()

        button = QPushButton('HLR check')
        button.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_MediaPlay')))
        button.clicked.connect(self.hlr_check)
        button.setStyleSheet("width: 90px; height: 20px;")
        button_layout.addWidget(button, 1, 1, 1, 1)
        button_layout.addWidget(QLabel(''), 1, 2, 1, 10)
        return button_layout

    def parser_button_layout(self):
        button_layout = QGridLayout()

        button = QPushButton('Parse')
        button.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_MediaPlay')))
        button.clicked.connect(self.parse_file)
        button.setStyleSheet("width: 90px; height: 20px;")
        button_layout.addWidget(button, 1, 1, 1, 1)
        button_layout.addWidget(QLabel(''), 1, 2, 1, 10)
        return button_layout

    def parse_file(self):
        config = self.form_layout.config
        file_name = self.form_layout.get_file_name()
        client_name = self.form_layout.get_client_name()
        bash_command = config['script_command'] + ' ' + file_name + ' ' + client_name
        if file_name is not None and client_name is not None:
            process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            self.form_layout.msg.setText(output.decode("utf-8"))

    def config_button_layout(self):
        button_layout = QGridLayout()
        button = QPushButton('Save')
        button.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_DialogSaveButton')))
        button.clicked.connect(self.save_config)
        button.setStyleSheet("width: 90px; height: 20px;")
        button_layout.addWidget(button, 1, 1, 1, 1)
        button_layout.addWidget(QLabel(''), 1, 2, 1, 10)
        return button_layout

    def query_button_layout(self):
        button_layout = QGridLayout()
        button = QPushButton('Send by SMPP')
        button.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_ArrowUp')))
        button.clicked.connect(self.send_sms)
        button.setStyleSheet("width: 90px; height: 20px;")
        button_layout.addWidget(button, 1, 1, 1, 1)
        button = QPushButton('Send by API')
        button.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_ArrowUp')))
        button.clicked.connect(self.send_sms_api)
        button.setStyleSheet("width: 90px; height: 20px;")
        button_layout.addWidget(button, 1, 2, 1, 1)
        return button_layout

    def save_config(self):
        path = self.form_layout.get_path()
        user = self.form_layout.get_user()
        password = self.form_layout.get_pass()
        api_user = self.form_layout.get_user_api()
        api_pass = self.form_layout.get_pass_api()
        parser_path = self.form_layout.get_parser_path()
        script_command = self.form_layout.get_parser_script_command()
        if path == '' or user == '' or password == '':
            self.config()
        data = [
            ('path', path),
            ('user', user),
            ('pass', password),
            ('username', api_user),
            ('api_key', api_pass),
            ('parser_path', parser_path),
            ('script_command', script_command)
        ]
        self.connector.save_config(data)

    def send_sms(self):
        message_from = self.form_layout.get_from()
        message_to = self.form_layout.get_to()
        message_text = self.form_layout.get_text()
        params = self.connector.get_config()
        data = dict()
        data['path'] = params['path']
        data['user'] = params['user']
        data['pass'] = params['pass']
        data['from'] = message_from
        data['to'] = message_to
        data['text'] = message_text
        if message_from == '' or message_to == '' or message_text == '':
            self.query()
        r = requests.get(params.pop('path'), params=data)
        data = [
            (None, data['from'], data['to'], data['text'], r.text),
        ]
        self.connector.save_sms(data)
        self.query()

    def hlr_check(self):
        phone = self.form_layout.get_phone()
        params = self.connector.get_config()
        data = dict()
        data['username'] = params['username']
        data['api_key'] = params['api_key']
        data['destination'] = phone
        r = requests.get('http://api.bulkness.com/hlr/', params=data)
        self.hlr_res.setText(r.text)
        print(r.text)

    def send_sms_api(self):
        message_from = self.form_layout.get_from()
        message_to = self.form_layout.get_to()
        message_text = self.form_layout.get_text()
        params = self.connector.get_config()
        data = dict()
        data['username'] = params['username']
        data['api_key'] = params['api_key']
        data['from'] = message_from
        data['to'] = message_to
        data['message'] = message_text
        if message_from == '' or message_to == '' or message_text == '':
            self.query()
        r = requests.get('https://api.bulkness.com/message/send/', params=data)
        data = [
            (None, data['from'], data['to'], data['message'], r.text),
        ]
        self.connector.save_sms(data)
        self.query()

    # настраиваем окно приложения
    def setup_app(self):
        self.setMinimumSize(QSize(800, 600))  # Устанавливаем размеры
        self.center()
        self.setWindowTitle("Solar combine")  # Устанавливаем заголовок окна
        self.setWindowIcon(QIcon('icon.png'))

    # настраиваем трей
    def set_tray(self):
        tray_icon = QSystemTrayIcon(self)
        icon = QIcon("icon.png")
        tray_icon.setIcon(icon)
        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        hide_action = QAction("Hide", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(self.close)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        tray_icon.setContextMenu(tray_menu)
        tray_icon.show()
        tray_icon.setToolTip('Solar combine')
        # tray_icon.showMessage('Title', 'Text')

    # настраиваем главное меню и тулбар
    def set_main_menu(self):
        # экшены
        hide_action = QAction(QIcon("icon.png"), "&Hide", self)
        hide_action.triggered.connect(self.hide)
        exit_action = QAction("&Exit", self)  # Создаём Action с помощью которого будем выходить из приложения
        exit_action.setShortcut('Ctrl+Q')  # Задаём для него хоткей
        exit_action.triggered.connect(self.close)  # Подключаем сигнал triggered к слоту quit у qApp.
        # test_action = QAction("&Test", self)
        # test_action.triggered.connect(self.test)

        # панель меню
        main_menu = self.menuBar()
        hide_menu = main_menu.addMenu('Hide')
        file_menu = main_menu.addMenu('Exit')
        # test_menu = main_menu.addMenu('Test')
        hide_menu.addAction(hide_action)
        file_menu.addAction(exit_action)
        # test_menu.addAction(test_action)

        # тулбар
        # toolbar = self.addToolBar('Exit')
        # toolbar.addAction(exit_action)

    # переопределяем событие close
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Сообщение', "Really?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # центрируем окно приложения
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
