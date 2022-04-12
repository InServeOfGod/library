from PyQt5.QtWidgets import QMessageBox, QTabWidget, QTreeView, QInputDialog

from model.model import Model
from views.AddBookDialog import AddBookDialog
from views.AddReaderDialog import AddReaderDialog
from views.MainWindow import MainWindow
from views.Menus import Menus
from views.Toolbar import Toolbar
from views.ViewTab import ViewTab


class MainController:
    def __init__(self):
        # model
        self.model = Model()

        # views
        self.mainWindow = MainWindow(self)
        self.menus = Menus(self)
        self.toolBar = Toolbar(self)

        books_tab_titles = ["ID", "İSİM", "STOK", "SAYFA SAYISI", "YAZAR", "DOLAP NO", "DİL", "TÜR", "YAYINEVİ",
                            "DURUM", "YAYIN TARİHİ"]

        readers_tab_titles = ["ID", "İSİM", "SOYİSİM", "EMAİL", "ADRES", "TELEFON NUMARASI"]

        self.booksTab = ViewTab(self, books_tab_titles, self.model.TABLE_BOOKS)
        self.readersTab = ViewTab(self, readers_tab_titles, self.model.TABLE_READERS)

        self.addBookDialog = AddBookDialog(self)
        self.addReaderDialog = AddReaderDialog(self)

    # starters
    def main(self):
        self.mainWindow.main()
        self.menus.main()
        self.toolBar.main()

        self.booksTab.main()
        self.readersTab.main()

    def tabs(self):
        tab = QTabWidget()
        tab.addTab(self.booksTab, self.model.BOOKS)
        tab.addTab(self.readersTab, self.model.READERS)
        self.mainWindow.setCentralWidget(tab)

    # table loaders

    def remove_data(self):
        self.booksTab.tableModel.setRowCount(0)
        self.readersTab.tableModel.setRowCount(0)

    def append_data(self, which: str, data: tuple):
        table_model = None

        if which == self.model.TABLE_BOOKS:
            table_model = self.booksTab.tableModel

        elif which == self.model.TABLE_READERS:
            table_model = self.readersTab.tableModel

        table_model.insertRow(0)

        for i in range(len(data)):
            table_model.setData(table_model.index(0, i), data[i])

    def reload_tables(self):
        cursor = self.model.conn.cursor()
        cursor.execute(self.model.select_books_sql)
        books_data = cursor.fetchall()

        # refresh cursor for each fetching
        cursor = self.model.conn.cursor()
        cursor.execute(self.model.select_readers_sql)
        readers_data = cursor.fetchall()

        self.remove_data()

        # load data into tables
        for books_datum in books_data:
            self.append_data(self.model.TABLE_BOOKS, books_datum)

        for readers_datum in readers_data:
            self.append_data(self.model.TABLE_READERS, readers_datum)

    # sql listeners

    def insert_book(self):
        row_id = self.model.selected_id
        dialog = self.addBookDialog
        contents = [ui.text() for ui in dialog.uis]
        name, surname, phone, mother_name, father_name, job, workplace, loc = contents
        details = dialog.text_details.toPlainText()
        married = dialog.check_married.isChecked()

        if row_id is None:
            sql = "INSERT INTO people(id, name, surname, phone, mother_name, father_name, job, workplace_name, " \
                  "person_loc, married, details) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

        else:
            sql = "UPDATE people " \
                  "SET id = ?, name = ?, surname = ?, phone = ?, mother_name = ?, father_name = ?, job = ?, " \
                  "workplace_name = ?, person_loc = ?, married = ?, details = ? " \
                  f"WHERE id = {row_id}"

        row = (row_id, name, surname, phone, mother_name, father_name, job, workplace, loc, married, details)
        cursor = self.model.conn.cursor()

        cursor.execute(sql, row)
        self.model.conn.commit()
        self.addBookDialog.close()
        self.reload_tables()

    # table listeners
    def selected(self, table: QTreeView, which: str):
        table_model = table.model()
        indexes = table.selectedIndexes()

        if indexes:
            self.model.selected_row = indexes[0].row()
            self.model.selected_table = which
            self.model.selected_id = table_model.data(table_model.index(self.model.selected_row, 0))

            self.menus.enable()
            self.toolBar.enable()

    # listeners
    def action_manage_add(self) -> None:
        selected, _ = QInputDialog.getItem(self.mainWindow, self.model.title, "Seç : ",
                                           [self.model.BOOKS, self.model.READERS], 0, False)

        if _:
            self.model.deselect()
            self.menus.disable()
            self.toolBar.disable()

            if selected == self.model.BOOKS:
                self.addBookDialog.refactor()
                self.addBookDialog.show()

            elif selected == self.model.READERS:
                self.addReaderDialog.refactor()
                self.addReaderDialog.show()

    def action_manage_del(self) -> None:
        if self.model.is_selected():
            confirm = QMessageBox.question(self.mainWindow, self.mainWindow.windowTitle(),
                                           f"Bu satırı silmek istediğinize emin misiniz?\n"
                                           f"id={self.model.selected_id}, table={self.model.selected_table}")

            if confirm == QMessageBox.Yes:
                sql = f"DELETE FROM {self.model.selected_table} WHERE id={self.model.selected_id}"
                cursor = self.model.conn.cursor()

                try:
                    cursor.execute(sql)
                    self.model.conn.commit()
                except Exception as exc:
                    QMessageBox.critical(self.mainWindow, self.mainWindow.windowTitle(), "Veri silinemedi!\n"
                                                                                         f"Hata : {str(exc)}")

                else:
                    self.model.deselect()
                    self.menus.disable()
                    self.toolBar.disable()
                    self.reload_tables()
                    QMessageBox.information(self.mainWindow, self.mainWindow.windowTitle(), "Veri silindi")

    def action_manage_edit(self) -> None:
        if self.model.is_selected():
            dialog = data = None
            cursor = self.model.conn.cursor()

            if self.model.selected_table == self.model.TABLE_BOOKS:
                sql = "SELECT name, surname, phone, mother_name, father_name, job, workplace_name, person_loc, " \
                      f"details FROM people WHERE id={self.model.selected_id}"
                cursor.execute(sql)
                data = cursor.fetchone()
                dialog = self.addBookDialog

            elif self.model.selected_table == self.model.TABLE_READERS:
                sql = "SELECT domain, public_url, dns, organization, details FROM website " \
                      f"WHERE id={self.model.selected_id}"
                cursor.execute(sql)
                data = cursor.fetchone()
                dialog = self.addReaderDialog

            for i in range(len(dialog.uis)):
                dialog.uis[i].setText(data[i])

            dialog.btn_submit.setText("Düzenle")
            dialog.show()

    def action_manage_show_det(self) -> None:
        if self.model.is_selected():
            sql = f"SELECT details FROM {self.model.selected_table} WHERE id = {self.model.selected_id}"
            cursor = self.model.conn.cursor()
            cursor.execute(sql)

            # 0 is the first argument of data we are interested of
            data = cursor.fetchone()[0]
            QMessageBox.information(self.mainWindow, self.mainWindow.windowTitle(), f"Detaylar : '{data}'")

    def action_manage_exit(self) -> bool:
        ask = QMessageBox.question(self.mainWindow, self.model.title, "Uygulamadan çıkmak istediğinize emin misiniz?",
                                   QMessageBox.Yes | QMessageBox.No)
        return True if ask == QMessageBox.Yes else False

    def action_view_full(self) -> None:
        if self.mainWindow.isFullScreen():
            self.mainWindow.showNormal()

        else:
            self.mainWindow.showFullScreen()

    def action_view_menu(self) -> None:
        menubar = self.mainWindow.menuBar()
        menubar.setVisible(False if menubar.isVisible() else True)

    def action_view_toolbar(self) -> None:
        toolbar = self.toolBar.toolbar
        toolbar.setVisible(False if toolbar.isVisible() else True)

    def action_view_dark(self) -> None:
        if self.model.config.get('dark'):
            self.model.update("dark", False)

        else:
            self.model.update("dark", True)

        stylesheets = self.model.read_stylesheets()

        if stylesheets is not None:
            # todo : append stylesheets in order to make program dark or light
            pass

    def action_help_help(self) -> None:
        QMessageBox.information(self.mainWindow, self.model.title,
                                "Program hakkında yardım için\ninserveofgod@gmail.com adresine mail gönderebilirsiniz",
                                QMessageBox.Ok)

    def action_help_about(self) -> None:
        QMessageBox.information(self.mainWindow, self.model.title,
                                "Bu program Python programalama dili ile PyQt5\n"
                                "kütüphanesi kullanılarak yapılmıştır.",
                                QMessageBox.Ok)

