import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QCalendarWidget, QListWidget, QLineEdit, QComboBox, QColorDialog, QTimeEdit, 
    QInputDialog, QFileDialog, QListWidgetItem, QStyleFactory, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt, QDate, QTime, QTimer
from PyQt6.QtGui import QColor, QFont, QPalette

class Event:
    def __init__(self, date, title, description, category, color=Qt.GlobalColor.green, time=None, recurrence="None"):
        self.date = date
        self.title = title
        self.description = description
        self.category = category
        self.color = color
        self.time = time or QTime.currentTime()
        self.recurrence = recurrence

    def to_dict(self):
        return {
            "date": self.date.toString(Qt.DateFormat.ISODate),
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "color": self.color.name(),
            "time": self.time.toString(Qt.DateFormat.ISODate),
            "recurrence": self.recurrence
        }

    @staticmethod
    def from_dict(data):
        date = QDate.fromString(data["date"], Qt.DateFormat.ISODate)
        color = QColor(data["color"])
        time = QTime.fromString(data.get("time", QTime.currentTime().toString(Qt.DateFormat.ISODate)), Qt.DateFormat.ISODate)
        return Event(date, data["title"], data["description"], data["category"], color, time, data.get("recurrence", "None"))

class CalendarWidget(QCalendarWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.events = {}
        self.setGridVisible(True)
        self.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)

    def paintCell(self, painter, rect, date):
        super().paintCell(painter, rect, date)
        if date in self.events:
            painter.save()
            for i, event in enumerate(self.events[date][:3]):
                painter.setPen(event.color)
                text_rect = rect.adjusted(5, 15 + i * 12, -5, -5)
                painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft, event.title[:10])
            painter.restore()

    def add_event(self, event):
        if event.date not in self.events:
            self.events[event.date] = []
        self.events[event.date].append(event)
        self.updateCell(event.date)

class CalendarReminderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enhanced Calendar and Reminder App")
        self.setGeometry(100, 100, 1200, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Calendar widget setup
        calendar_frame = QFrame()
        calendar_frame.setFrameShape(QFrame.Shape.StyledPanel)
        calendar_layout = QVBoxLayout(calendar_frame)
        self.calendar = CalendarWidget()
        self.calendar.clicked.connect(self.date_clicked)
        calendar_layout.addWidget(self.calendar)
        main_layout.addWidget(calendar_frame, 2)

        # Right panel setup
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        main_layout.addWidget(right_panel, 1)

        # Event input fields
        input_frame = QFrame()
        input_frame.setFrameShape(QFrame.Shape.StyledPanel)
        input_layout = QVBoxLayout(input_frame)

        self.event_title = QLineEdit()
        self.event_title.setPlaceholderText("Event Title")
        input_layout.addWidget(self.event_title)

        self.event_description = QLineEdit()
        self.event_description.setPlaceholderText("Event Description")
        input_layout.addWidget(self.event_description)

        self.event_category = QComboBox()
        self.event_category.addItems(["Work", "Personal", "Holiday"])
        input_layout.addWidget(self.event_category)

        color_button = QPushButton("Choose Color")
        color_button.clicked.connect(self.choose_color)
        input_layout.addWidget(color_button)

        self.event_time = QTimeEdit()
        input_layout.addWidget(self.event_time)

        self.event_recurrence = QComboBox()
        self.event_recurrence.addItems(["None", "Daily", "Weekly", "Monthly"])
        input_layout.addWidget(self.event_recurrence)

        add_button = QPushButton("Add Event")
        add_button.clicked.connect(self.add_event)
        input_layout.addWidget(add_button)

        right_layout.addWidget(input_frame)

        # Event list setup
        list_frame = QFrame()
        list_frame.setFrameShape(QFrame.Shape.StyledPanel)
        list_layout = QVBoxLayout(list_frame)

        self.event_list = QListWidget()
        list_layout.addWidget(self.event_list)

        button_layout = QHBoxLayout()
        edit_button = QPushButton("Edit Selected Event")
        edit_button.clicked.connect(self.edit_selected_event)
        button_layout.addWidget(edit_button)

        delete_button = QPushButton("Delete Selected Event")
        delete_button.clicked.connect(self.delete_selected_event)
        button_layout.addWidget(delete_button)

        list_layout.addLayout(button_layout)
        right_layout.addWidget(list_frame)

        # Toolbar for additional options
        self.create_toolbar()
        self.current_color = Qt.GlobalColor.green
        self.apply_style()

        # Notifications setup
        self.notification_timer = QTimer(self)
        self.notification_timer.timeout.connect(self.check_notifications)
        self.notification_timer.start(60000)  # Check every minute

    def apply_style(self):
        self.setStyle(QStyleFactory.create("Fusion"))
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
        self.setPalette(palette)

        self.setStyleSheet("""
            QMainWindow, QCalendarWidget {
                background-color: #353535;
                color: white;
            }
            QCalendarWidget QAbstractItemView:enabled {
                color: white;
                selection-background-color: #2A82DA;
                selection-color: black;
            }
            QCalendarWidget QWidget {
                alternate-background-color: #525252;
            }
            QLineEdit, QComboBox, QPushButton, QListWidget, QTimeEdit {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #5b5b5b;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #3b3b3b;
            }
            QFrame {
                border: 1px solid #5b5b5b;
                border-radius: 5px;
            }
        """)

    def create_toolbar(self):
        toolbar = self.addToolBar("Options")
        toolbar.setMovable(False)
        toolbar.setFloatable(False)

        save_button = QPushButton("Save Events")
        save_button.clicked.connect(self.save_events_json)
        toolbar.addWidget(save_button)

        load_button = QPushButton("Load Events")
        load_button.clicked.connect(self.load_events)
        toolbar.addWidget(load_button)

        bg_button = QPushButton("Change Background")
        bg_button.clicked.connect(self.change_background)
        toolbar.addWidget(bg_button)

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.current_color = color

    def add_event(self):
        title = self.event_title.text()
        description = self.event_description.text()
        category = self.event_category.currentText()
        date = self.calendar.selectedDate()
        time = self.event_time.time()
        recurrence = self.event_recurrence.currentText()
        if title:
            event = Event(date, title, description, category, self.current_color, time, recurrence)
            self.calendar.add_event(event)
            self.event_title.clear()
            self.event_description.clear()
            self.update_event_list(date)

    def date_clicked(self, date):
        self.update_event_list(date)

    def update_event_list(self, date):
        self.event_list.clear()
        for event in self.calendar.events.get(date, []):
            item = QListWidgetItem(f"{event.category}: {event.title} at {event.time.toString()}")
            item.setData(Qt.ItemDataRole.UserRole, event)
            self.event_list.addItem(item)

    def edit_selected_event(self):
        if self.event_list.currentItem():
            item = self.event_list.currentItem()
            event = item.data(Qt.ItemDataRole.UserRole)
            new_title, ok = QInputDialog.getText(self, "Edit Event", "Enter new title:", text=event.title)
            if ok and new_title:
                event.title = new_title
                item.setText(f"{event.category}: {event.title} at {event.time.toString()}")
                self.calendar.updateCell(event.date)

    def delete_selected_event(self):
        if self.event_list.currentItem():
            item = self.event_list.currentItem()
            event = item.data(Qt.ItemDataRole.UserRole)
            self.calendar.events[event.date].remove(event)
            if not self.calendar.events[event.date]:
                del self.calendar.events[event.date]
            self.update_event_list(event.date)

    def save_events_json(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Events", "", "JSON Files (*.json);;All Files (*)")
        if file_name:
            events_data = []
            for date, events in self.calendar.events.items():
                for event in events:
                    events_data.append(event.to_dict())
            
            with open(file_name, 'w') as file:
                json.dump(events_data, file, indent=4)

    def load_events(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Events", "", "JSON Files (*.json);;All Files (*)")
        if file_name:
            with open(file_name, 'r') as file:
                events_data = json.load(file)
                for data in events_data:
                    event = Event.from_dict(data)
                    self.calendar.add_event(event)
            self.update_event_list(self.calendar.selectedDate())

    def check_notifications(self):
        current_date = QDate.currentDate()
        current_time = QTime.currentTime()
        for event in self.calendar.events.get(current_date, []):
            if event.time == current_time:
                self.statusBar().showMessage(f"Reminder: {event.title}")

    def change_background(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Choose Background Image", "", "Image Files (*.png *.jpg *.bmp)")
        if file_name:
            self.setStyleSheet(f"QMainWindow {{ background-image: url({file_name}); }}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalendarReminderApp()
    window.show()
    sys.exit(app.exec())