from PyQt5.QtWidgets import QFormLayout, QLineEdit, QDialog, QPushButton, QTextEdit, QSpinBox,QComboBox, QCalendarWidget


class AddBookDialog(QDialog):
    def __init__(self, controller):
        super(AddBookDialog, self).__init__()

        self.controller = controller
        self.model = self.controller.model

        self.formLayout = QFormLayout()

        self.edit_name = QLineEdit()
        self.edit_stock = QSpinBox()
        self.edit_page = QSpinBox()
        self.combo_author = QComboBox()
        self.combo_case = QComboBox()
        self.combo_lang = QComboBox()
        self.combo_genre = QComboBox()
        self.combo_publish_house = QComboBox()
        self.date_publish = QCalendarWidget()
        self.text_details = QTextEdit()
        self.btn_submit = QPushButton("Ekle")

        self.combos = [self.combo_author, self.combo_case, self.combo_lang, self.combo_genre, self.combo_publish_house]

        self.author_names = []
        self.author_ids = []

        self.case_numbers = []
        self.case_ids = []

        self.lang_names = []
        self.lang_ids = []

        self.genre_names = []
        self.genre_ids = []

        self.house_names = []
        self.house_ids = []

        self.uis = [self.edit_name]

        self._ui()

    def refactor(self):
        for ui in self.uis:
            ui.setText("")

        # we do not want to include text_details variable, so we make it separated
        self.text_details.setText("")

    def checkboxes(self):
        author_sql = "SELECT id, name FROM authors;"
        case_sql = "SELECT id, case_number FROM book_cases;"
        lang_sql = "SELECT id, language FROM languages;"
        genre_sql = "SELECT id, genre FROM book_genres;"
        house_sql = "SELECT id, publish_house FROM publish_houses;"
        cursor = self.model.conn.cursor()

        cursor.execute(author_sql)
        author_data = cursor.fetchall()

        cursor.execute(case_sql)
        case_data = cursor.fetchall()

        cursor.execute(lang_sql)
        lang_data = cursor.fetchall()

        cursor.execute(genre_sql)
        genre_data = cursor.fetchall()

        cursor.execute(house_sql)
        house_data = cursor.fetchall()

        self.author_ids.clear()
        self.author_names.clear()

        self.case_ids.clear()
        self.case_numbers.clear()

        self.lang_ids.clear()
        self.lang_names.clear()

        self.genre_ids.clear()
        self.genre_names.clear()

        self.house_ids.clear()
        self.house_names.clear()

        for _, datum in author_data:
            self.author_ids.append(_)
            self.author_names.append(datum)

        for _, datum in case_data:
            self.case_ids.append(_)
            self.case_numbers.append(datum)

        for _, datum in lang_data:
            self.lang_ids.append(_)
            self.lang_names.append(datum)

        for _, datum in genre_data:
            self.genre_ids.append(_)
            self.genre_names.append(datum)

        for _, datum in house_data:
            self.house_ids.append(_)
            self.house_names.append(datum)

        for combo in self.combos:
            combo.clear()

        for author_name in self.author_names:
            self.combo_author.addItem(author_name)

        for case_number in self.case_numbers:
            self.combo_case.addItem(str(case_number))

        for lang_name in self.lang_names:
            self.combo_lang.addItem(lang_name)

        for genre_name in self.genre_names:
            self.combo_genre.addItem(genre_name)

        for house_name in self.house_names:
            self.combo_publish_house.addItem(house_name)

    def _ui(self):
        self.setWindowTitle(self.model.title)
        self.setWindowIcon(self.model.icon)
        self.setLayout(self.formLayout)

        self.btn_submit.setText("Ekle")
        self.btn_submit.clicked.connect(self.controller.insert_book)

        self.edit_stock.setMinimum(0)
        self.edit_page.setMinimum(1)
        self.edit_stock.setMaximum(1000000)
        self.edit_page.setMaximum(10000)
        self.text_details.setPlaceholderText("Buraya yazın...")

        self.formLayout.addRow("Ad : ", self.edit_name)
        self.formLayout.addRow("Stok : ", self.edit_stock)
        self.formLayout.addRow("Sayfa Sayısı : ", self.edit_page)
        self.formLayout.addRow("Yazar : ", self.combo_author)
        self.formLayout.addRow("Dolap No : ", self.combo_case)
        self.formLayout.addRow("Dil : ", self.combo_lang)
        self.formLayout.addRow("Tür ", self.combo_genre)
        self.formLayout.addRow("Yayınevi : ", self.combo_publish_house)
        self.formLayout.addRow("Yayın Tarihi : ", self.date_publish)
        self.formLayout.addRow("Detaylar : ", self.text_details)
        self.formLayout.addWidget(self.btn_submit)
