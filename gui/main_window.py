from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLineEdit, 
    QListWidget, QListWidgetItem, QMenu, QApplication,
    QLabel, QHBoxLayout, QPushButton
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QFont
from store.store import Store
from gui.package_info_dialog import PackageInfoDialog

class PackageListItem(QWidget):
    def __init__(self, package_info, parent=None):
        super().__init__(parent)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(layout)
        
        # Updated emoji map with more relevant icons
        emoji_map = {
            'a': '📊', 'b': '📦', 'c': '⚙️', 'd': '📱', 'e': '🔧',
            'f': '📁', 'g': '🎮', 'h': '🔨', 'i': '💻', 'j': '🎯',
            'k': '🔑', 'l': '📚', 'm': '🛠️', 'n': '📈', 'o': '💾',
            'p': '🐍', 'q': '⚡', 'r': '🚀', 's': '⭐', 't': '🔄',
            'u': '📥', 'v': '👁️', 'w': '🌐', 'x': '✨', 'y': '🔗',
            'z': '⚡'
        }
        
        # Get package name and version
        name_parts = package_info['name'].split('\n')
        package_name = name_parts[0]
        version = name_parts[1] if len(name_parts) > 1 else ""
        first_letter = package_name[0].lower()
        emoji = emoji_map.get(first_letter, '📦')
        
        # Create labels with better styling
        emoji_label = QLabel(emoji)
        emoji_label.setFont(QFont('Segoe UI Emoji', 16))
        emoji_label.setStyleSheet('color: #E0E0E0;')
        
        # Package info container
        info_container = QWidget()
        info_layout = QVBoxLayout(info_container)
        info_layout.setSpacing(2)
        info_layout.setContentsMargins(0, 0, 0, 0)
        
        # Name and version layout
        name_layout = QHBoxLayout()
        name_layout.setSpacing(10)
        
        name_label = QLabel(package_name)
        name_label.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        name_label.setStyleSheet('color: #E0E0E0;')
        
        version_label = QLabel(version)
        version_label.setFont(QFont('Arial', 10))
        version_label.setStyleSheet('color: #808080;')
        
        name_layout.addWidget(name_label)
        name_layout.addWidget(version_label)
        name_layout.addStretch()
        
        desc_label = QLabel(package_info['description'])
        desc_label.setFont(QFont('Arial', 10))
        desc_label.setStyleSheet('color: #B0B0B0;')
        desc_label.setWordWrap(True)
        
        info_layout.addLayout(name_layout)
        info_layout.addWidget(desc_label)
        
        # Add widgets to main layout
        layout.addWidget(emoji_label)
        layout.addWidget(info_container, stretch=1)
        
        # Store the package info
        self.package_info = package_info

class PyPIBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.store = Store()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('PyPIBrowser 📦')
        self.setGeometry(100, 100, 800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Search layout
        search_container = QWidget()
        search_container.setObjectName("searchContainer")
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(10, 10, 10, 10)
        
        search_icon = QLabel('🔍')
        search_icon.setFont(QFont('Segoe UI Emoji', 14))
        search_icon.setStyleSheet('color: #B0B0B0;')
        
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText('Search PyPI packages...')
        self.search_bar.setFont(QFont('Arial', 12))
        self.search_bar.returnPressed.connect(self.perform_search)
        
        self.search_button = QPushButton('Search')
        self.search_button.setFont(QFont('Arial', 11))
        self.search_button.clicked.connect(self.perform_search)
        self.search_button.setCursor(Qt.CursorShape.PointingHandCursor)
        
        search_layout.addWidget(search_icon)
        search_layout.addWidget(self.search_bar)
        search_layout.addWidget(self.search_button)
        
        # Results list
        self.results_list = QListWidget()
        self.results_list.setFont(QFont('Arial', 11))
        self.results_list.setSpacing(2)
        self.results_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.results_list.customContextMenuRequested.connect(self.show_context_menu)
        
        layout.addWidget(search_container)
        layout.addWidget(self.results_list)
        
        # Context menu actions
        self.info_action = QAction('📄 View Package Info', self)
        self.info_action.triggered.connect(self.show_package_info)
        self.install_action = QAction('⬇️ Copy Install Command', self)
        self.install_action.triggered.connect(self.copy_install_command)
        
        # Dark theme styling
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #1a1a1a;
                color: #E0E0E0;
            }
            #searchContainer {
                background-color: #1a1a1a;
                border-radius: 4px;
            }
            QLineEdit {
                padding: 8px;
                background-color: #2a2a2a;
                border: none;
                border-radius: 4px;
                color: #E0E0E0;
            }
            QPushButton {
                padding: 8px 20px;
                background-color: #0078d7;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }
            QListWidget {
                background-color: #1a1a1a;
                border: none;
                border-radius: 4px;
                padding: 5px;
            }
            QListWidget::item {
                background-color: #2a2a2a;
                border-radius: 4px;
                margin: 2px 5px;
            }
            QListWidget::item:selected {
                background-color: #333333;
            }
        """)

    def perform_search(self):
        query = self.search_bar.text().strip()
        if query:
            self.results_list.clear()
            results = self.store.search_package_store(query)
            
            for result in results:
                item = QListWidgetItem(self.results_list)
                item_widget = PackageListItem(result)
                item.setSizeHint(item_widget.sizeHint())
                self.results_list.setItemWidget(item, item_widget)

    def show_context_menu(self, position):
        current_item = self.results_list.currentItem()
        if current_item:
            context_menu = QMenu(self)
            context_menu.addAction(self.info_action)
            context_menu.addAction(self.install_action)
            context_menu.exec(self.results_list.mapToGlobal(position))
    
    def show_package_info(self):
        current_item = self.results_list.currentItem()
        if current_item:
            item_widget = self.results_list.itemWidget(current_item)
            dialog = PackageInfoDialog(item_widget.package_info)
            dialog.exec()
    
    def copy_install_command(self):
        current_item = self.results_list.currentItem()
        if current_item:
            item_widget = self.results_list.itemWidget(current_item)
            package_name = item_widget.package_info['name'].split('\n')[0]
            command = f"pip install {package_name}"
            QApplication.clipboard().setText(command)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    browser = PyPIBrowser()
    browser.show()
    sys.exit(app.exec())