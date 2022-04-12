from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTreeView, QAbstractItemView


class ViewTab(QWidget):
    def __init__(self, controller, titles: list, table: str):
        super(ViewTab, self).__init__()

        self.controller = controller
        self.model = self.controller.model

        self.mainLayout = QVBoxLayout()
        self.table = QTreeView()
        self.titles = titles
        self.table_type = table
        self.tableModel = QStandardItemModel(0, len(self.titles))

    def set_titles(self, titles: list):
        self.titles = titles

    def set_table(self, table: str):
        self.table_type = table

    def main(self):
        for i in range(len(self.titles)):
            self.tableModel.setHeaderData(i, Qt.Horizontal, self.titles[i])

        self.table.setModel(self.tableModel)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.selectionModel().selectionChanged.connect(
            partial(self.controller.selected, self.table, self.table_type))

        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.table)
