from PyQt5.Qt import QSize
from PyQt5.QtWidgets import QToolBar

from views.Actions import Actions


class Toolbar(Actions):
    def __init__(self, controller):
        super(Toolbar, self).__init__(controller)

        self.controller = controller
        self.win = self.controller.mainWindow
        self.toolbar = QToolBar()

        self._actions()

    def _actions(self):
        self.toolbar.addAction(self.manage_add)
        self.toolbar.addAction(self.manage_edit)
        self.toolbar.addAction(self.manage_del)
        self.toolbar.addAction(self.manage_show_det)

    def main(self):
        self.toolbar.setIconSize(QSize(16, 16))
        self.win.addToolBar(self.toolbar)
