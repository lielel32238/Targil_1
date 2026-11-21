from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QFileDialog,
    QSpinBox,
    QLabel,
    QDialog,
    QHeaderView,
)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices


class AboutWindow(QDialog):
    """חלון אודות מעוצב עם פרטים אישיים וקישור ל-GitHub"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About")
        self.setFixedSize(360, 240)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(25, 25, 25, 25)

        # כותרת ראשית
        title_label = QLabel("Grades Modifier Application")
        title_label.setObjectName("aboutTitle")
        layout.addWidget(title_label)

        # פרטים אישיים (שם ופרטים נוספים)
        self.name_label = QLabel("Name: Liel Eliyahu")
        self.name_label.setObjectName("aboutDetails")
        layout.addWidget(self.name_label)

        self.course_label = QLabel("Course: Mechatronics | Python GUI Project")
        self.course_label.setObjectName("aboutDetails")
        layout.addWidget(self.course_label)

        # קישור לחיץ למאגר GitHub
        self.github_link = QLabel(
            'GitHub: <a href="https://github.com/lielel32238">My GitHub Repository</a>'
        )
        self.github_link.setObjectName("aboutDetails")
        self.github_link.setOpenExternalLinks(True)
        layout.addWidget(self.github_link)

        layout.addStretch()

        # כפתור סגירה
        btn_close = QPushButton("Close")
        btn_close.setObjectName("btnSecondary")
        btn_close.clicked.connect(self.close)
        layout.addWidget(btn_close)


class MainWindow(QMainWindow):
    """החלון הראשי של האפליקציה"""

    def __init__(self):
        super().__init__()

        # כותרת ומימדי החלון
        self.setWindowTitle("Grades Management System")
        self.resize(650, 520)

        # רשימות ומשתנים לשמירת נתוני הקובץ והציונים
        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []
        self.selected_file = ""

        # ווידג'ט מרכזי וסידור אנכי
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(14)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 1. כפתור לבחירת קובץ CSV
        top_layout = QHBoxLayout()
        self.btn_select_file = QPushButton("Select CSV File")
        self.btn_select_file.clicked.connect(self.select_csv_file)
        top_layout.addWidget(self.btn_select_file)

        self.lbl_file_path = QLabel("No file selected")
        top_layout.addWidget(self.lbl_file_path)
        top_layout.addStretch()
        main_layout.addLayout(top_layout)

        # 2. טבלה (QTableWidget) - 50 שורות ו-3 עמודות
        self.table = QTableWidget(50, 3)
        self.table.setHorizontalHeaderLabels(["ID", "Original Grades", "Corrected Grades"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.table)

        # 3. ווידג'ט מספרי להזנת נקודות בונוס (מספר שלם, מגיב ל-ENTER)
        bonus_layout = QHBoxLayout()
        lbl_bonus = QLabel("Bonus Points (Press ENTER):")
        lbl_bonus.setObjectName("sectionTitle")
        bonus_layout.addWidget(lbl_bonus)

        self.spin_bonus = QSpinBox()
        self.spin_bonus.setRange(0, 100)
        self.spin_bonus.lineEdit().returnPressed.connect(self.apply_bonus)
        bonus_layout.addWidget(self.spin_bonus)

        bonus_layout.addStretch()
        main_layout.addLayout(bonus_layout)

        # 4 + 5. כפתור Update File וכפתור About
        bottom_layout = QHBoxLayout()

        self.btn_update = QPushButton("Update File")
        self.btn_update.setObjectName("btnUpdate")
        self.btn_update.clicked.connect(self.update_file)
        bottom_layout.addWidget(self.btn_update)

        bottom_layout.addStretch()

        self.btn_about = QPushButton("About")
        self.btn_about.setObjectName("btnSecondary")
        self.btn_about.clicked.connect(self.show_about)
        bottom_layout.addWidget(self.btn_about)

        main_layout.addLayout(bottom_layout)

    # =========================================================================
    # מתודות האפליקציה
    # =========================================================================

    def select_csv_file(self):
        """פתיחת חלון לבחירת קובץ CSV"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )
        if file_path:
            # TODO: שמור את נתיב הקובץ ב-self.selected_file
            # TODO: קרא את קובץ ה-CSV ומלא את self.student_ids, self.original_grades ו-self.corrected_grades
            # TODO: קרא למתודת self.update_table() כדי לעדכן את הטבלה בתצוגה
            pass

    def update_table(self):
        """
        מעדכנת את תוכן הטבלה מתוך שלוש הרשימות:
        self.student_ids, self.original_grades ו-self.corrected_grades
        """
        num_rows = max(50, len(self.student_ids))
        self.table.setRowCount(num_rows)

        for row in range(len(self.student_ids)):
            # עמודה 0: מזהה תלמיד (ID)
            id_item = QTableWidgetItem(str(self.student_ids[row]))
            id_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, id_item)

            # עמודה 1: ציון מקורי (Original Grades)
            if row < len(self.original_grades):
                orig_item = QTableWidgetItem(str(self.original_grades[row]))
                orig_item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, 1, orig_item)

            # עמודה 2: ציון מתוקן (Corrected Grades)
            if row < len(self.corrected_grades):
                corr_item = QTableWidgetItem(str(self.corrected_grades[row]))
                corr_item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, 2, corr_item)

    def apply_bonus(self):
        """מופעלת בלחיצה על ENTER בווידג'ט נקודות הבונוס"""
        bonus_value = self.spin_bonus.value()
        # TODO: עדכן את רשימת הציונים המתוקנים (self.corrected_grades) לפי ערך הבונוס (bonus_value)
        # TODO: קרא למתודת self.update_table() כדי לרענן את הנתונים בטבלה

    def update_file(self):
        """שמירת הנתונים המעודכנים לקובץ ופתיחתו בתוכנת ברירת המחדל"""
        # TODO: כתוב כאן את דריסת קובץ ה-CSV (בנתיב self.selected_file) עם הנתונים המעודכנים מתוך הרשימות

        # פתיחת הקובץ בתוכנת ברירת המחדל בכל מערכות ההפעלה באמצעות PySide6
        if self.selected_file:
            QDesktopServices.openUrl(QUrl.fromLocalFile(self.selected_file))

    def show_about(self):
        """פתיחת חלון About מעוצב"""
        self.about_window = AboutWindow(self)
        self.about_window.show()


if __name__ == "__main__":
    app = QApplication([])

    # קריאת קובץ העיצוב (QSS) באמצעות פקודת open הרגילה של פייתון
    try:
        with open("style.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        pass

    window = MainWindow()
    window.show()
    app.exec()
