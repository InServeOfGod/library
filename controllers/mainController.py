from PyQt5.QtWidgets import QMessageBox, QTabWidget, QTreeView, QInputDialog

from model.model import Model
from views.AddBookDialog import AddBookDialog
from views.AddLoansDialog import AddLoansDialog
from views.AddReaderDialog import AddReaderDialog
from views.MainWindow import MainWindow
from views.Menus import Menus
from views.Toolbar import Toolbar
from views.ViewTab import ViewTab


# todo : neither let user add empty field nor same field


class MainController:
    def __init__(self):
        # model
        self.model = Model()

        # views
        self.mainWindow = MainWindow(self)
        self.menus = Menus(self)
        self.toolBar = Toolbar(self)

        self.booksTab = ViewTab(self, self.model.books_tab_titles, self.model.TABLE_BOOKS)
        self.readersTab = ViewTab(self, self.model.readers_tab_titles, self.model.TABLE_READERS)
        self.loansTab = ViewTab(self, self.model.loans_tab_titles, self.model.TABLE_LOANS)

        self.addBookDialog = AddBookDialog(self)
        self.addReaderDialog = AddReaderDialog(self)
        self.addLoansDialog = AddLoansDialog(self)

    # starters
    def main(self):
        self.mainWindow.main()
        self.menus.main()
        self.toolBar.main()

        self.booksTab.main()
        self.readersTab.main()
        self.loansTab.main()

    def tabs(self):
        tab = QTabWidget()
        tab.addTab(self.booksTab, self.model.BOOKS)
        tab.addTab(self.readersTab, self.model.READERS)
        tab.addTab(self.loansTab, self.model.LOANS)
        self.mainWindow.setCentralWidget(tab)

    # table loaders

    def remove_data(self):
        self.booksTab.tableModel.setRowCount(0)
        self.readersTab.tableModel.setRowCount(0)
        self.loansTab.tableModel.setRowCount(0)

    def append_data(self, which: str, data: tuple):
        table_model = None

        if which == self.model.TABLE_BOOKS:
            table_model = self.booksTab.tableModel

        elif which == self.model.TABLE_READERS:
            table_model = self.readersTab.tableModel

        elif which == self.model.TABLE_LOANS:
            table_model = self.loansTab.tableModel

        table_model.insertRow(0)

        for i in range(len(data)):
            table_model.setData(table_model.index(0, i), data[i])

    def reload_tables(self):
        cursor = self.model.conn.cursor()
        cursor.execute(self.model.select_books_sql)
        books_data = cursor.fetchall()

        cursor.execute(self.model.select_readers_sql)
        readers_data = cursor.fetchall()

        cursor.execute(self.model.select_loans_sql)
        loans_data = cursor.fetchall()

        self.remove_data()

        # load data into tables
        for books_datum in books_data:
            self.append_data(self.model.TABLE_BOOKS, books_datum)

        for readers_datum in readers_data:
            self.append_data(self.model.TABLE_READERS, readers_datum)

        for loans_datum in loans_data:
            self.append_data(self.model.TABLE_LOANS, loans_datum)

    # sql listeners

    def insert_book(self):
        # todo : do not add status id from here instead add it from 'insert_loan' function()
        row_id = self.model.selected_id
        dialog = self.addBookDialog
        name = dialog.edit_name.text()
        stock = dialog.edit_stock.text()
        page = dialog.edit_page.text()
        selected_author = dialog.combo_author.currentIndex()
        selected_case = dialog.combo_case.currentIndex()
        selected_lang = dialog.combo_lang.currentIndex()
        selected_genre = dialog.combo_genre.currentIndex()
        selected_house = dialog.combo_publish_house.currentIndex()
        selected_status = dialog.combo_status.currentIndex()
        publish_date = dialog.date_publish.selectedDate().toPyDate()
        details = dialog.text_details.toPlainText()

        author_id = dialog.author_ids[selected_author]
        case_id = dialog.case_ids[selected_case]
        lang_id = dialog.lang_ids[selected_lang]
        genre_id = dialog.genre_ids[selected_genre]
        house_id = dialog.house_ids[selected_house]
        status_id = dialog.status_ids[selected_status]

        if row_id is None:
            sql = "INSERT INTO book(id, name, stock, page_count, author_id, case_id, language_id, genre_id, " \
                  "publish_house_id, status_id, publish_year, details) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            self.mainWindow.statusBar().showMessage("Veri eklendi")

        else:
            sql = "UPDATE book " \
                  "SET id = ?, name = ?, stock = ?, page_count = ?, author_id = ?, case_id = ?, language_id = ?, " \
                  "genre_id = ?, publish_house_id = ?, status_id = ?, publish_year = ?, details = ? " \
                  f"WHERE id = {row_id}"
            self.mainWindow.statusBar().showMessage("Veri düzenlendi")

        row = (
            row_id, name, stock, page, author_id, case_id, lang_id, genre_id, house_id, status_id, publish_date, details
        )
        cursor = self.model.conn.cursor()

        cursor.execute(sql, row)
        self.model.conn.commit()
        dialog.close()
        self.reload_tables()

    def insert_reader(self):
        row_id = self.model.selected_id
        dialog = self.addReaderDialog
        contents = [ui.text() for ui in dialog.uis]
        name, surname, email, phone = contents
        address = dialog.text_address.toPlainText()
        details = dialog.text_details.toPlainText()

        if row_id is None:
            sql = "INSERT INTO reader(id, name, surname, email, address, phone, details) VALUES(?, ?, ?, ?, ?, ?, ?)"
            self.mainWindow.statusBar().showMessage("Veri eklendi")

        else:
            sql = "UPDATE reader " \
                  "SET id = ?, name = ?, surname = ?, phone = ?, details = ? " \
                  f"WHERE id = {row_id}"
            self.mainWindow.statusBar().showMessage("Veri düzenlendi")

        row = (row_id, name, surname, email, address, phone, details)
        cursor = self.model.conn.cursor()

        cursor.execute(sql, row)
        self.model.conn.commit()
        dialog.close()
        self.reload_tables()

    def insert_loan(self):
        row_id = self.model.selected_id
        dialog = self.addLoansDialog
        selected_book = dialog.combo_book.currentIndex()
        selected_reader = dialog.combo_reader.currentIndex()
        loan_date = dialog.date_loaned.selectedDate().toPyDate()
        details = dialog.text_details.toPlainText()

        book_id = dialog.book_ids[selected_book]
        reader_id = dialog.reader_ids[selected_reader]

        if row_id is None:
            sql = "INSERT INTO loans(id, book_id, reader_id, loaned_date, details) VALUES(?, ?, ?, ?, ?)"
            self.mainWindow.statusBar().showMessage("Veri eklendi")

        else:
            sql = "UPDATE loans " \
                  "SET id = ?, book_id = ?, reader_id = ?, loaned_date = ?, details = ? " \
                  f"WHERE id = {row_id}"
            self.mainWindow.statusBar().showMessage("Veri düzenlendi")

        row = (row_id, book_id, reader_id, loan_date, details)
        cursor = self.model.conn.cursor()

        cursor.execute(sql, row)
        self.model.conn.commit()
        dialog.close()
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
                                           [self.model.BOOKS, self.model.READERS, self.model.LOANS], 0, False)

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

            elif selected == self.model.LOANS:
                self.addLoansDialog.refactor()
                self.addLoansDialog.show()

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
                    self.mainWindow.statusBar().showMessage("Veri silinemedi")

                else:
                    self.model.deselect()
                    self.menus.disable()
                    self.toolBar.disable()
                    self.reload_tables()
                    self.mainWindow.statusBar().showMessage("Veri silindi")

    def action_manage_edit(self) -> None:
        if self.model.is_selected():
            dialog = data = None
            cursor = self.model.conn.cursor()

            # todo : try to get selected combobox from database
            if self.model.selected_table == self.model.TABLE_BOOKS:
                sql = f"SELECT name FROM book WHERE id={self.model.selected_id}"
                cursor.execute(sql)
                data = cursor.fetchone()
                dialog = self.addBookDialog

            elif self.model.selected_table == self.model.TABLE_READERS:
                sql = f"SELECT name, surname, email, phone FROM reader WHERE id={self.model.selected_id}"
                cursor.execute(sql)
                data = cursor.fetchone()
                dialog = self.addReaderDialog

            elif self.model.selected_table == self.model.TABLE_LOANS:
                dialog = self.addLoansDialog

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
            data = "Detay yok" if data is None else data
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

