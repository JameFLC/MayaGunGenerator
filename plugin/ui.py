import random
from chess_ui.api import *
from PySide2.QtGui import *  # A cleanner plus tard
from PySide2.QtCore import *
from PySide2.QtWidgets import *
import maya.OpenMayaUI as omui


from shiboken2 import wrapInstance
from PySide2.QtWidgets import QWidget


import importlib
import procedural_guns.plugin.api as gapi
importlib.reload(gapi)


CHECK_BOXES_OFFSETS = 10
seed: int = random.randrange(0, gapi.MAX_SEED_NUMBER)


def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QWidget)


def generate_random_gun():
    global seed
    seed = random.randrange(0, gapi.MAX_SEED_NUMBER)
    my_ui.seed_line_edit.setText(str(seed))
    generate_new_gun()


def get_new_seed():
    global seed
    seed_text: str = my_ui.seed_line_edit.text()
    print(seed_text)
    if seed_text.isdigit():
        seed = int(seed_text)
    else:
        seed = hash(seed_text) % gapi.MAX_SEED_NUMBER

    my_ui.seed_line_edit.setText(str(seed))


def generate_new_gun():
    get_new_seed()
    gapi.generate_gun(seed)


def on_body_checked():
    gapi.part_options["body"] = my_ui.body_checkbox.isChecked()
    if not my_ui.body_checkbox.isChecked():
        switch_all(False)


def check_body():
    my_ui.body_checkbox.setChecked(True)
    gapi.part_options["body"] = True


def on_barrel_checked():
    checked: bool = my_ui.barrel_checkbox.isChecked()
    gapi.part_options["barrel"] = checked
    if checked:
        check_body()
    else:
        my_ui.accessory_checkbox.setChecked(False)
        gapi.part_options["accessory"] = False


def on_accessory_checked():
    checked: bool = my_ui.accessory_checkbox.isChecked()
    gapi.part_options["accessory"] = checked
    if checked:
        my_ui.barrel_checkbox.setChecked(True)
        on_barrel_checked()


def on_sight_checked():
    checked: bool = my_ui.sight_checkbox.isChecked()
    gapi.part_options["sight"] = my_ui.sight_checkbox.isChecked()
    if checked:
        check_body()


def on_stock_checked():
    checked: bool = my_ui.stock_checkbox.isChecked()
    gapi.part_options["stock"] = my_ui.stock_checkbox.isChecked()
    if checked:
        check_body()


def on_gripp_checked():
    checked: bool = my_ui.gripp_checkbox.isChecked()
    gapi.part_options["gripp"] = my_ui.gripp_checkbox.isChecked()
    if checked:
        check_body()


def on_magazine_checked():
    checked: bool = my_ui.magazine_checkbox.isChecked()
    gapi.part_options["magazine"] = my_ui.magazine_checkbox.isChecked()
    if checked:
        check_body()


def on_reset_clicked():
    switch_all(True)


def switch_all(checked: bool):
    my_ui.body_checkbox.setChecked(checked)
    my_ui.barrel_checkbox.setChecked(checked)
    my_ui.accessory_checkbox.setChecked(checked)
    my_ui.sight_checkbox.setChecked(checked)
    my_ui.stock_checkbox.setChecked(checked)
    my_ui.gripp_checkbox.setChecked(checked)
    my_ui.magazine_checkbox.setChecked(checked)

    gapi.part_options["body"] = my_ui.body_checkbox.isChecked()
    gapi.part_options["barrel"] = my_ui.barrel_checkbox.isChecked()
    gapi.part_options["accessory"] = my_ui.accessory_checkbox.isChecked()
    gapi.part_options["sight"] = my_ui.sight_checkbox.isChecked()
    gapi.part_options["stock"] = my_ui.stock_checkbox.isChecked()
    gapi.part_options["gripp"] = my_ui.gripp_checkbox.isChecked()
    gapi.part_options["magazine"] = my_ui.magazine_checkbox.isChecked()


def on_path_override():
    line_path: str = my_ui.override_path_line_edit.text()
    print(line_path)
    gapi.RELATIVE_PATH = line_path
    pass


class MyUI(QDialog):

    def __init__(self):
        super(MyUI, self).__init__(parent=maya_main_window())

        # Layouts
        self.main_vertical = None
        self.checkbox_horizontal = None
        self.accessory_checkbox_horizontal = None
        self.checkbox_vertical = None

        # Widgets ==============================================================

        self.generate_random_gun_button = None
        self.seed_label = None
        self.seed_line_edit = None
        self.generate_gun_button = None
        self.generation_option_label = None

        # Spacers

        self.checkbox_spacer = None
        # Checkboxes
        self.body_checkbox = None
        self.barrel_checkbox = None
        self.accessory_checkbox = None
        self.sight_checkbox = None
        self.stock_checkbox = None
        self.gripp_checkbox = None
        self.magazine_checkbox = None

        self.reset_generation_button = None
        self.remove_gun_button = None

        self.override_path_label = None
        self.override_path_line_edit = None
        self.override_path_button = None

    def init_ui(self):
        self.init_layouts()
        self.init_widgets()
        self.set_layouts()
        self.set_connections()
        self.set_default()

    def init_layouts(self):
        self.main_vertical = QVBoxLayout(self)
        self.checkbox_horizontal = QHBoxLayout(self)
        self.accessory_checkbox_horizontal = QHBoxLayout(self)
        self.checkbox_vertical = QVBoxLayout(self)
        pass

    def init_widgets(self):
        self.generate_random_gun_button = QPushButton("New Random Gun")
        self.seed_label = QLabel("Gun Seed")
        self.generate_gun_button = QPushButton("New Gun")
        self.seed_line_edit = QLineEdit()
        self.generation_option_label = QLabel("Generation Option")

        self.checkbox_spacer = QSpacerItem(
            CHECK_BOXES_OFFSETS, CHECK_BOXES_OFFSETS)

        # Checkboxes
        self.body_checkbox = QCheckBox("Body")
        self.barrel_checkbox = QCheckBox("Barrel")
        self.accessory_checkbox = QCheckBox("Accessory")
        self.sight_checkbox = QCheckBox("Sight")
        self.stock_checkbox = QCheckBox("Stock")
        self.gripp_checkbox = QCheckBox("Gripp")
        self.magazine_checkbox = QCheckBox("Magazine")

        switch_all(True)

        self.reset_generation_button = QPushButton("Reset Generation")
        self.remove_gun_button = QPushButton("Remove Gun")

        self.override_path_label = QLabel("Models path override")
        self.override_path_line_edit = QLineEdit()
        self.override_path_button = QPushButton("Override Model Path")
        pass

    def set_layouts(self):
        self.main_vertical.addWidget(self.generate_random_gun_button)

        self.main_vertical.addWidget(self.seed_label)
        self.main_vertical.addWidget(self.seed_line_edit)
        self.main_vertical.addWidget(self.generate_gun_button)

        self.main_vertical.addSpacerItem(self.checkbox_spacer)

        self.main_vertical.addWidget(self.generation_option_label)

        # Checkboxes
        self.main_vertical.addWidget(self.body_checkbox)

        self.main_vertical.addLayout(self.checkbox_horizontal)

        # Spacers

        self.checkbox_horizontal.addSpacerItem(self.checkbox_spacer)
        self.checkbox_horizontal.addLayout(self.checkbox_vertical)

        self.checkbox_vertical.addWidget(self.barrel_checkbox)
        self.checkbox_vertical.addLayout(
            self.accessory_checkbox_horizontal)

        self.accessory_checkbox_horizontal.addSpacerItem(self.checkbox_spacer)
        self.accessory_checkbox_horizontal.addWidget(self.accessory_checkbox)

        self.checkbox_vertical.addWidget(self.sight_checkbox)
        self.checkbox_vertical.addWidget(self.stock_checkbox)
        self.checkbox_vertical.addWidget(self.gripp_checkbox)
        self.checkbox_vertical.addWidget(self.magazine_checkbox)

        self.main_vertical.addWidget(self.reset_generation_button)
        self.main_vertical.addWidget(self.remove_gun_button)

        self.main_vertical.addSpacerItem(self.checkbox_spacer)

        self.main_vertical.addWidget(self.override_path_label)
        self.main_vertical.addWidget(self.override_path_line_edit)
        self.main_vertical.addWidget(self.override_path_button)

    def set_connections(self):
        self.generate_random_gun_button.clicked.connect(generate_random_gun)

        self.generate_gun_button.clicked.connect(generate_new_gun)

        self.body_checkbox.clicked.connect(on_body_checked)
        self.barrel_checkbox.clicked.connect(on_barrel_checked)
        self.accessory_checkbox.clicked.connect(on_accessory_checked)
        self.sight_checkbox.clicked.connect(on_sight_checked)
        self.stock_checkbox.clicked.connect(on_stock_checked)
        self.gripp_checkbox.clicked.connect(on_gripp_checked)
        self.magazine_checkbox.clicked.connect(on_magazine_checked)

        self.reset_generation_button.clicked.connect(on_reset_clicked)
        self.remove_gun_button.clicked.connect(gapi.clear_gun)
        self.override_path_button.clicked.connect(on_path_override)
        pass

    def set_default(self):
        self.main_vertical.setAlignment(Qt.AlignTop)
        pass

    def show(self):
        self.init_ui()
        return super(MyUI, self).show()


if __name__ == '__main__':
    if "my_ui" in globals():
        globals()["my_ui"].deleteLater()

    my_ui = MyUI()
    my_ui.show()
