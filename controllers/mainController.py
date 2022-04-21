import sqlite3

from PyQt5.QtWidgets import QMessageBox, QTabWidget, QTreeView, QInputDialog

from model.model import Model
from views.AddBookDialog import AddBookDialog
from views.AddLoansDialog import AddLoansDialog
from views.AddReaderDialog import AddReaderDialog
from views.MainWindow import MainWindow
from views.Menus import Menus
from views.Toolbar import Toolbar
from views.ViewList import ViewList
from views.ViewTab import ViewTab


# todo : append stylesheets in order to make program dark or light


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

        self.authorList = ViewList(self, self.model.TABLE_AUTHORS, self.model.AUTHORS)
        self.caseList = ViewList(self, self.model.TABLE_CASES, self.model.CASES)
        self.genreList = ViewList(self, self.model.TABLE_GENRES, self.model.GENRES)
        self.houseList = ViewList(self, self.model.TABLE_HOUSES, self.model.HOUSES)

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
        publish_date = dialog.date_publish.selectedDate().toPyDate()
        details = dialog.text_details.toPlainText()

        author_id = dialog.author_ids[selected_author]
        case_id = dialog.case_ids[selected_case]
        lang_id = dialog.lang_ids[selected_lang]
        genre_id = dialog.genre_ids[selected_genre]
        house_id = dialog.house_ids[selected_house]

        if row_id is None:
            sql = "INSERT INTO books(id, name, stock, page_count, author_id, case_id, language_id, genre_id, " \
                  "publish_house_id, publish_year, details) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            self.mainWindow.statusBar().showMessage("Veri eklendi")

        else:
            sql = "UPDATE books " \
                  "SET id = ?, name = ?, stock = ?, page_count = ?, author_id = ?, case_id = ?, language_id = ?, " \
                  "genre_id = ?, publish_house_id = ?, publish_year = ?, details = ? " \
                  f"WHERE id = {row_id}"
            self.mainWindow.statusBar().showMessage("Veri düzenlendi")

        row = (
            row_id, name, stock, page, author_id, case_id, lang_id, genre_id, house_id, publish_date, details
        )
        cursor = self.model.conn.cursor()

        if name != '':
            try:
                cursor.execute(sql, row)

            except sqlite3.IntegrityError:
                QMessageBox.warning(self.mainWindow, self.mainWindow.windowTitle(), "Bu kitap adı zaten kayıtlı")

            else:
                self.model.conn.commit()
                dialog.close()
                self.reload_tables()

        else:
            QMessageBox.warning(self.mainWindow, self.mainWindow.windowTitle(), "Boş kitap adı girmeyin")

    def insert_reader(self):
        row_id = self.model.selected_id
        dialog = self.addReaderDialog
        contents = [ui.text() for ui in dialog.uis]
        name, surname, email, phone = contents
        address = dialog.text_address.toPlainText()
        details = dialog.text_details.toPlainText()

        if row_id is None:
            sql = "INSERT INTO readers(id, name, surname, email, address, phone, details) VALUES(?, ?, ?, ?, ?, ?, ?)"
            self.mainWindow.statusBar().showMessage("Veri eklendi")

        else:
            sql = "UPDATE readers " \
                  "SET id = ?, name = ?, surname = ?, phone = ?, details = ? " \
                  f"WHERE id = {row_id}"
            self.mainWindow.statusBar().showMessage("Veri düzenlendi")

        row = (row_id, name, surname, email, address, phone, details)
        cursor = self.model.conn.cursor()

        if name != '':
            try:
                cursor.execute(sql, row)

            except sqlite3.IntegrityError:
                QMessageBox.warning(self.mainWindow, self.mainWindow.windowTitle(), "Bu okuyucu adı zaten kayıtlı")

            else:
                self.model.conn.commit()
                dialog.close()
                self.reload_tables()

        else:
            QMessageBox.warning(self.mainWindow, self.mainWindow.windowTitle(), "Boş okuyucu adı girmeyin")

    def insert_loan(self):
        row_id = self.model.selected_id
        dialog = self.addLoansDialog
        selected_book = dialog.combo_book.currentIndex()
        selected_reader = dialog.combo_reader.currentIndex()
        loan_date = dialog.date_loaned.selectedDate().toPyDate()
        details = dialog.text_details.toPlainText()

        book_id = dialog.book_ids[selected_book]
        reader_id = dialog.reader_ids[selected_reader]

        stock = self.model.check_stock(book_id)

        if stock > 0:
            if row_id is None:
                sql = "INSERT INTO loans(id, book_id, reader_id, loaned_date, details) VALUES(?, ?, ?, ?, ?)"
                self.mainWindow.statusBar().showMessage("Veri eklendi")
                self.model.minus_stock(book_id, stock)

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

        else:
            QMessageBox.warning(self.mainWindow, self.mainWindow.windowTitle(), "Bu kitap stoklarda yok")

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
    def action_manage_add_author(self) -> None:
        self.authorList.refactor()
        self.authorList.refresh(self.model.authors())
        self.authorList.show()

    def action_manage_add_case(self) -> None:
        self.caseList.refactor()
        self.caseList.refresh(self.model.cases())
        self.caseList.show()

    def action_manage_add_genre(self) -> None:
        self.genreList.refactor()
        self.genreList.refresh(self.model.genres())
        self.genreList.show()

    def action_manage_add_house(self) -> None:
        self.houseList.refactor()
        self.houseList.refresh(self.model.houses())
        self.houseList.show()

    def add_field(self, table: str) -> None:
        conn = self.model.conn
        cursor = conn.cursor()
        dialog = object
        sql = str()

        if table == self.model.TABLE_AUTHORS:
            dialog = self.authorList
            sql = "INSERT INTO authors (name) VALUES ('{}')"

        elif table == self.model.TABLE_CASES:
            dialog = self.caseList
            sql = "INSERT INTO book_cases (case_number) VALUES ('{}')"

        elif table == self.model.TABLE_GENRES:
            dialog = self.genreList
            sql = "INSERT INTO book_genres (genre) VALUES ('{}')"

        elif table == self.model.TABLE_HOUSES:
            dialog = self.houseList
            sql = "INSERT INTO publish_houses (publish_house) VALUES ('{}')"

        buff = dialog.entry.text()

        if buff != '':
            try:
                # format the {} sign
                sql = sql.format(buff)
                cursor.execute(sql)
                conn.commit()

                # add new item
                dialog.itemList.insertItem(dialog.itemList.count(), buff)
                dialog.refactor()
                # QMessageBox.information(self.mainWindow, self.mainWindow.windowTitle(), "Veri eklendi")

            except sqlite3.IntegrityError:
                QMessageBox.warning(self.mainWindow, self.mainWindow.windowTitle(), "Bu veri zaten kayıtlı")

    def action_manage_add(self) -> None:
        selected, _ = QInputDialog.getItem(self.mainWindow, self.model.title, "Seç : ",
                                           [self.model.BOOKS, self.model.READERS, self.model.LOANS], 0, False)

        if _:
            self.model.deselect()
            self.menus.disable()
            self.toolBar.disable()

            dialog = object

            # refresh the checkboxes for each opening

            if selected == self.model.BOOKS:
                dialog = self.addBookDialog
                dialog.checkboxes()

            elif selected == self.model.READERS:
                dialog = self.addReaderDialog

            elif selected == self.model.LOANS:
                dialog = self.addLoansDialog
                dialog.checkboxes()

            dialog.refactor()
            dialog.show()

    def action_manage_del(self) -> None:
        if self.model.is_selected():
            confirm = QMessageBox.question(self.mainWindow, self.mainWindow.windowTitle(),
                                           f"Bu satırı silmek istediğinize emin misiniz?\n"
                                           f"id={self.model.selected_id}, table={self.model.selected_table}")

            if self.model.selected_table == self.model.TABLE_LOANS:
                book_id = self.model.book_id_from_loan(self.model.selected_id)
                self.model.plus_stock(book_id, self.model.check_stock(book_id))

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

            if self.model.selected_table == self.model.TABLE_BOOKS:
                dialog = self.addBookDialog

                sql = f"""SELECT b.name, stock, page_count, a.name, bc.case_number, l.language, bg.genre, 
                ph.publish_house
                FROM books as b
                INNER JOIN authors a on a.id = b.author_id
                INNER JOIN book_cases bc on bc.id = b.case_id
                INNER JOIN languages l on l.id = b.language_id
                INNER JOIN book_genres bg on bg.id = b.genre_id
                INNER JOIN publish_houses ph on ph.id = b.publish_house_id
                WHERE b.id = {self.model.selected_id};"""
                cursor.execute(sql)

                datum = cursor.fetchone()
                data, stock, page, author, case, lang, genre, house = datum

                # getting values from database to edit
                dialog.edit_stock.setValue(stock)
                dialog.edit_page.setValue(page)
                dialog.combo_author.setCurrentText(author)
                dialog.combo_case.setCurrentText(str(case))
                dialog.combo_lang.setCurrentText(lang)
                dialog.combo_genre.setCurrentText(genre)
                dialog.combo_publish_house.setCurrentText(house)

            elif self.model.selected_table == self.model.TABLE_READERS:
                dialog = self.addReaderDialog

                sql = f"SELECT name, surname, email, phone FROM readers WHERE id={self.model.selected_id}"
                cursor.execute(sql)
                data = cursor.fetchone()

            elif self.model.selected_table == self.model.TABLE_LOANS:
                dialog = self.addLoansDialog

                sql = """SELECT b.name, r.name
                FROM loans as l
                INNER JOIN books b on b.id = l.book_id
                INNER JOIN readers r on l.reader_id = r.id
                WHERE l.id = 3;"""

                cursor.execute(sql)
                datum = cursor.fetchone()
                book, reader = datum

                # getting values from database to edit
                dialog.combo_book.setCurrentText(book)
                dialog.combo_reader.setCurrentText(reader)

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
            print(stylesheets)

    def action_help_help(self) -> None:
        QMessageBox.information(self.mainWindow, self.model.title,
                                "Program hakkında yardım için\ninserveofgod@gmail.com adresine mail gönderebilirsiniz",
                                QMessageBox.Ok)

    def action_help_about(self) -> None:
        QMessageBox.information(self.mainWindow, self.model.title,
                                "Bu program Python programalama dili ile PyQt5\n"
                                "kütüphanesi kullanılarak yapılmıştır.",
                                QMessageBox.Ok)

