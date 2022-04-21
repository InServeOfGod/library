from functools import partial

from PyQt5.QtWidgets import QFormLayout, QListWidget, QPushButton, QLineEdit, QGridLayout, QDialog


class ViewList(QDialog):
    def __init__(self, controller, table: str, title: str):
        super(ViewList, self).__init__()

        self.controller = controller
        self.model = self.controller.model

        self.table = table
        self.title = title

        self.formLayout = QFormLayout()
        self.childLayout = QGridLayout()
        self.itemList = QListWidget()
        self.entry = QLineEdit()
        self.btn = QPushButton("Ekle")

        self._ui()

    def refactor(self):
        self.entry.setText("")

    def refresh(self, data: list):
        self.itemList.clear()

        for datum in data:
            self.itemList.addItem(str(datum[0]))

    def _ui(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(self.model.icon)
        self.setLayout(self.formLayout)

        self.btn.clicked.connect(partial(self.controller.add_field, self.table))
        self.childLayout.addWidget(self.entry, 0, 0)
        self.childLayout.addWidget(self.btn, 0, 1, 0, 1)

        self.formLayout.addWidget(self.itemList)
        self.formLayout.addRow(self.childLayout)

