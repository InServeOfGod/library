import json
import os
import sqlite3

from PyQt5.QtGui import QIcon


class Model:
    def __init__(self):
        self.root = os.getcwd()
        self.config = self.read()

        self.encoding = "UTF-8"
        self.title = "Kütüphane Uygulaması"

        self.TABLE_BOOKS = "books"
        self.TABLE_READERS = "readers"

        self.BOOKS = "Kitaplar"
        self.READERS = "Okuyucular"

        self.selected_table = None
        self.selected_row = None
        self.selected_id = None

        # todo : write sql code for selecting all information except details from specific tables
        self.select_books_sql = ""
        self.select_readers_sql = ""

        self.img_assets = os.path.join(self.root, "assets", "img")
        self.css_assets = os.path.join(self.root, "assets", "css")
        self.config_path = os.path.join(self.root, "model", "config.json")

        self.icon = QIcon(os.path.join(self.img_assets, "database.png"))

        self.database = os.path.join(self.root, "model", "datatable.db")
        self.conn = sqlite3.connect(self.database)

        self.add_icon = QIcon(os.path.join(self.img_assets, "database--plus.png"))
        self.del_icon = QIcon(os.path.join(self.img_assets, "database--minus.png"))
        self.edit_icon = QIcon(os.path.join(self.img_assets, "database--pencil.png"))
        self.show_det_icon = QIcon(os.path.join(self.img_assets, "database-property.png"))
        self.show_loc_icon = QIcon(os.path.join(self.img_assets, "geolocation.png"))
        self.exit_icon = QIcon(os.path.join(self.img_assets, "door-open-in.png"))

        self.full_icon = QIcon(os.path.join(self.img_assets, "application-resize-full.png"))
        self.menu_icon = QIcon(os.path.join(self.img_assets, "ui-menu.png"))
        self.toolbar_icon = QIcon(os.path.join(self.img_assets, "ui-toolbar.png"))
        self.dark_icon = QIcon(os.path.join(self.img_assets, "smiley-glass.png"))

        self.help_icon = QIcon(os.path.join(self.img_assets, "question.png"))
        self.about_icon = QIcon(os.path.join(self.img_assets, "information.png"))

    def is_selected(self) -> bool:
        """
        Seçilme ile ilgili verilerin seçili olup olmadığını yansıtır
        :rtype: bool
        """
        if self.selected_id is not None and self.selected_row is not None and self.selected_table is not None:
            return True
        return False

    def deselect(self) -> None:
        """
        Seçili verileri seçilmemiş haline geri döndürür
        :rtype: None
        """
        self.selected_id = self.selected_row = self.selected_table = None

    def _write(self) -> None:
        """
        Sınıf içerisinde dosyaya yazmak için kullanılmalıdır.
        :rtype: None
        """
        dumping = json.dumps(self.config, indent=4, sort_keys=True)

        with open(self.config_path, "w") as f:
            f.write(dumping)

    def update(self, key: str, value: any) -> None:
        """
        Belli bir ayarı değiştirmek ve kaydetmek için kullanılır
        :rtype: None
        """
        self.config = self.read()
        self.config[key] = value
        self._write()

    def read(self) -> dict:
        """
        Ayarları okutur ve geri döndürür
        :rtype: dict
        """
        with open(os.path.join(self.root, "model", "config.json")) as f:
            json_data = f.read()
            dict_data = json.loads(json_data)
            self.config = dict_data
            return dict_data

    def read_stylesheets(self) -> any:
        """
        json dosyasından alınıp css dosyasına yazılan verileri döndürür
        :rtype: any
        """
        self.config = self.read()

        if self.config.get('dark'):
            with open(os.path.join(self.css_assets, "{}.min.css".format('dark'))) as f:
                return f.read()
        return None
