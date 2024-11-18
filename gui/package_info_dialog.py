from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QWidget, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QDesktopServices
from PyQt6.QtCore import QUrl

class PackageInfoDialog(QDialog):
    def __init__(self, package_info):
        super().__init__()
        self.package_info = package_info
        self.init_ui()

    def init_ui(self):
        # Set up the dialog window
        self.setWindowTitle("Package Info")
        self.setMinimumSize(600, 400)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        # Container for scrollable content
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(15)

        # Extract package info
        name = self.package_info['name'].split('\n')[0]
        version = self.package_info['name'].split('\n')[1] if len(self.package_info['name'].split('\n')) > 1 else "Version not available"
        
        # Package name section
        name_label = QLabel(name)
        name_label.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        container_layout.addWidget(name_label)

        # Version section
        version_label = QLabel(f"Version {version}")
        version_label.setFont(QFont('Arial', 14))
        version_label.setStyleSheet("color: #8a8a8a;")
        container_layout.addWidget(version_label)

        # Description section
        if self.package_info['description']:
            desc_container = self.create_section("Description")
            desc_label = QLabel(self.package_info['description'])
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet("color: #c4c4c4;")
            desc_container.layout().addWidget(desc_label)
            container_layout.addWidget(desc_container)

        # Installation section
        install_container = self.create_section("Installation")
        install_command = QLabel(f"pip install {name}")
        install_command.setStyleSheet("""
            background-color: #2a2a2a;
            padding: 10px;
            border-radius: 4px;
            color: #c4c4c4;
        """)
        copy_button = QPushButton("Copy")
        copy_button.setFixedWidth(80)
        copy_button.clicked.connect(lambda: self.copy_to_clipboard(f"pip install {name}"))
        
        command_layout = QHBoxLayout()
        command_layout.addWidget(install_command)
        command_layout.addWidget(copy_button)
        install_container.layout().addLayout(command_layout)
        container_layout.addWidget(install_container)

        # Links section
        links_container = self.create_section("Links")
        pypi_link = self.create_link("View on PyPI", self.package_info['url'])
        links_container.layout().addWidget(pypi_link)
        container_layout.addWidget(links_container)

        # Add scroll area to main layout
        scroll.setWidget(container)
        layout.addWidget(scroll)

        # Close button at bottom
        close_button = QPushButton("Close")
        close_button.setFixedWidth(100)
        close_button.clicked.connect(self.close)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)

        # Apply dark theme styling
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a1a;
                color: #E0E0E0;
            }
            QLabel {
                color: #E0E0E0;
            }
            QPushButton {
                background-color: #0078d7;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1982d7;
            }
            QScrollArea {
                background-color: #1a1a1a;
            }
            .section {
                background-color: #2a2a2a;
                border-radius: 4px;
            }
            QLabel[link="true"] {
                color: #0078d7;
            }
            QLabel[link="true"]:hover {
                color: #1982d7;
                text-decoration: underline;
            }
        """)

    def create_section(self, title):
        section = QWidget()
        section.setProperty("class", "section")
        layout = QVBoxLayout(section)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        title_label = QLabel(title)
        title_label.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        layout.addWidget(title_label)
        
        return section

    def create_link(self, text, url):
        link = QLabel(f'<a href="{url}" style="color: #0078d7; text-decoration: none;">{text}</a>')
        link.setTextFormat(Qt.TextFormat.RichText)
        link.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        link.setOpenExternalLinks(True)
        return link

    def copy_to_clipboard(self, text):
        QApplication.clipboard().setText(text)