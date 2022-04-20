from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QDialog, QPushButton, QTextEdit, QComboBox, QCalendarWidget


class AddLoansDialog(QDialog):
    def __init__(self, controller):
        super(AddLoansDialog, self).__init__()

        self.controller = controller
        self.model = self.controller.model

        self.mainLayout = QVBoxLayout()
        self.formLayout = QFormLayout()

        self.combo_book = QComboBox()
        self.combo_reader = QComboBox()
        self.date_loaned = QCalendarWidget()
        self.text_details = QTextEdit()
        self.btn_submit = QPushButton("Ekle")

        self.book_names = []
        self.book_ids = []

        self.reader_names = []
        self.reader_ids = []

        self.uis = []

        self._checkboxes()
        self._ui()

    def refactor(self):
        # we do not want to include text_details variable, so we make it separated
        self.text_details.setText("")

    def _checkboxes(self):
        book_sql = "SELECT id, name FROM book;"
        reader_sql = "SELECT id, name FROM reader;"

        cursor = self.model.conn.cursor()

        cursor.execute(book_sql)
        book_data = cursor.fetchall()

        cursor.execute(reader_sql)
        reader_data = cursor.fetchall()

        for _, datum in book_data:
            self.book_ids.append(_)
            self.book_names.append(datum)

        for _, datum in reader_data:
            self.reader_ids.append(_)
            self.reader_names.append(datum)

    def _ui(self):
        self.setWindowTitle(self.model.title)
        self.setWindowIcon(self.model.icon)
        self.setLayout(self.formLayout)

        self.btn_submit.setText("Ekle")
        self.btn_submit.clicked.connect(self.controller.insert_loan)

        self.text_details.setPlaceholderText("Buraya yazın...")

        for book_name in self.book_names:
            self.combo_book.addItem(book_name)

        for reader_name in self.reader_names:
            self.combo_reader.addItem(reader_name)

        self.formLayout.addRow("Kitap Adı : ", self.combo_book)
        self.formLayout.addRow("Okuyucu Adı : ", self.combo_reader)
        self.formLayout.addRow("Ödünç Alma Tarihi : ", self.date_loaned)
        self.formLayout.addRow("Detaylar : ", self.text_details)
        self.formLayout.addWidget(self.btn_submit)
