import random
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QVBoxLayout, QToolBar, QSpinBox, QSlider, \
    QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPainter, QColor, QPen, QAction
from settings import load_settings, save_settings

size = (800, 600)
class Raindrop:
    def __init__(self, width, height, angle):
        self.width = width
        self.height = height
        self.x = random.randint(-self.width, self.width*2)
        self.y = random.randint(-self.height, 0)
        self.z = random.uniform(0.5, 2)
        self.speed = self.z*5
        self.length = self.z * 10
        self.angle = angle

    def fall(self):
        self.y += self.speed
        self.x += self.speed * (self.angle / 10)

        if self.y > self.height:
            self.y = random.randint(-200, -100)
            self.x = random.randint(-self.width, self.width*2)
class RainWidget(QWidget):
    """Widget settings"""

    def __init__(self, settings, parent = None):
        super().__init__(parent)
        self.raindrops = [Raindrop(*size, settings['angle']) for _ in range(settings['count_of_drops'])]

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(settings['timer_speed'])

    def update_simulation(self):
        for drop in self.raindrops:
            drop.fall()
        self.update()

    def resizeEvent(self, event):
        for drop in self.raindrops:
            drop.width = self.width()
            drop.height = self.height()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(30, 30, 40))

        for drop in self.raindrops:
            pen_color = int(150+105*(drop.z/2))
            pen_width = drop.z

            pen = QPen(QColor(pen_color, pen_color, 220), pen_width)
            painter.setPen(pen)

            end_x = drop.x + drop.length * (drop.angle / 10)
            end_y = drop.y + drop.length
            painter.drawLine(int(drop.x), int(drop.y), int(end_x), int(end_y))

class RainSimulation(QMainWindow):
    """Main class"""
    def __init__(self):
        super().__init__()
        self.settings = load_settings()
        #title and size
        self.setWindowTitle('Rain')
        self.setGeometry(100, 100, *size)
        #Creating widget
        self.canvas = RainWidget(self.settings)
        self.setCentralWidget(self.canvas)
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        button_action = QAction("Settings", self)
        toolbar.addAction(button_action)
        button_action.triggered.connect(self.show_settings_dialog)



    def show_settings_dialog(self):
        settings = SettingsWindow(self.canvas)
        settings.exec()

class SettingsWindow(QDialog):

    def __init__(self, rain_widget):
        super().__init__()
        self.rain_widget = rain_widget
        self.setGeometry(100, 100, 400, 250)
        self.setWindowTitle('Settings')


        main_layout = QVBoxLayout(self)
        count_label = QLabel("Count of drops:")
        self.count_of_drops_changer_box = QSpinBox(self)
        self.count_of_drops_changer_slider = QSlider(Qt.Orientation.Horizontal, self)
        speed_label = QLabel("Speed:")
        self.timer_speed_changer_box = QSpinBox(self)
        self.timer_speed_changer_slider = QSlider(Qt.Orientation.Horizontal, self)
        angle_label = QLabel("Angle:")
        self.angle_changer_box = QSpinBox(self)
        self.angle_changer_slider = QSlider(Qt.Orientation.Horizontal, self)

        count_of_drops_changer_limits = (100, 2000)
        timer_speed_changer_limits = (1, 30)
        angle_changer_limits = (-10, 10)
        self.count_of_drops_changer_box.setMinimum(count_of_drops_changer_limits[0])
        self.count_of_drops_changer_box.setMaximum(count_of_drops_changer_limits[1])
        self.timer_speed_changer_box.setMinimum(timer_speed_changer_limits[0])
        self.timer_speed_changer_box.setMaximum(timer_speed_changer_limits[1])
        self.angle_changer_box.setMinimum(angle_changer_limits[0])
        self.angle_changer_box.setMaximum(angle_changer_limits[1])
        self.count_of_drops_changer_slider.setMinimum(count_of_drops_changer_limits[0])
        self.count_of_drops_changer_slider.setMaximum(count_of_drops_changer_limits[1])
        self.timer_speed_changer_slider.setMinimum(timer_speed_changer_limits[0])
        self.timer_speed_changer_slider.setMaximum(timer_speed_changer_limits[1])
        self.angle_changer_slider.setMinimum(angle_changer_limits[0])
        self.angle_changer_slider.setMaximum(angle_changer_limits[1])

        self.count_of_drops_changer_box.valueChanged.connect(self.count_of_drops_changer_slider.setValue)
        self.timer_speed_changer_box.valueChanged.connect(self.timer_speed_changer_slider.setValue)
        self.angle_changer_box.valueChanged.connect(self.angle_changer_slider.setValue)
        self.count_of_drops_changer_slider.valueChanged.connect(self.count_of_drops_changer_box.setValue)
        self.timer_speed_changer_slider.valueChanged.connect(self.timer_speed_changer_box.setValue)
        self.angle_changer_slider.valueChanged.connect(self.angle_changer_box.setValue)

        main_layout.addWidget(count_label)
        main_layout.addWidget(self.count_of_drops_changer_box)
        main_layout.addWidget(self.count_of_drops_changer_slider)
        main_layout.addWidget(speed_label)
        main_layout.addWidget(self.timer_speed_changer_box)
        main_layout.addWidget(self.timer_speed_changer_slider)
        main_layout.addWidget(angle_label)
        main_layout.addWidget(self.angle_changer_box)
        main_layout.addWidget(self.angle_changer_slider)

        self.count_of_drops_changer_box.setValue(len(self.rain_widget.raindrops))
        self.timer_speed_changer_box.setValue(self.rain_widget.timer.interval())
        if self.rain_widget.raindrops:
            self.angle_changer_box.setValue(self.rain_widget.raindrops[0].angle)

        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.apply_characteristic)

        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.close)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.exit_button)
        h_layout.addWidget(self.apply_button)
        main_layout.addLayout(h_layout)
        self.setLayout(main_layout)

    def apply_characteristic(self):
        new_count_of_drops = self.count_of_drops_changer_box.value()
        new_timer_speed = self.timer_speed_changer_box.value()
        new_angle = self.angle_changer_box.value()
        self.rain_widget.timer.setInterval(new_timer_speed)
        if new_count_of_drops != len(self.rain_widget.raindrops):
            self.rain_widget.raindrops = [Raindrop(self.rain_widget.width(), self.rain_widget.height(), new_angle) for _ in range(new_count_of_drops)]
        else:
            for drop in self.rain_widget.raindrops:
                drop.angle = new_angle
        new_settings = {
            "count_of_drops": new_count_of_drops,
            "timer_speed": new_timer_speed,
            "angle": new_angle
        }
        save_settings(new_settings)
        self.close()


if  __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RainSimulation()
    window.show()
    sys.exit(app.exec())