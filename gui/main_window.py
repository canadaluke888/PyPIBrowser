from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLineEdit, 
    QListWidget, QListWidgetItem, QMenu, QApplication,
    QLabel, QHBoxLayout, QPushButton
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QFont
from store.store import Store
from gui.package_info_dialog import PackageInfoDialog  # Import the dialog we created earlier

class PackageListItem(QWidget):
    def __init__(self, package_info, parent=None):
        super().__init__(parent)
        
        layout = QHBoxLayout()
        self.setLayout(layout)
        
        # Emoji based on package name first letter
        emoji_map = {
            'a': '📱', 'b': '🔋', 'c': '⚡', 'd': '🔮', 'e': '🎮',
            'f': '🔥', 'g': '🎨', 'h': '🏠', 'i': '💡', 'j': '🎯',
            'k': '🔑', 'l': '📚', 'm': '🎵', 'n': '📊', 'o': '🌊',
            'p': '🐍', 'q': '❓', 'r': '🚀', 's': '⭐', 't': '🎯',
            'u': '🔄', 'v': '👁️', 'w': '🌊', 'x': '❌', 'y': '💫',
            'z': '⚡'
        }
        
        # Get package name and split off version info
        package_name = package_info['name']
        first_letter = package_name[0].lower()
        emoji = emoji_map.get(first_letter, '📦')
        
        # Create labels
        emoji_label = QLabel(emoji)
        emoji_label.setFont(QFont('Segoe UI Emoji', 14))
        
        name_label = QLabel(package_name)
        name_label.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        
        desc_label = QLabel(package_info['description'])
        desc_label.setFont(QFont('Arial', 10))
        desc_label.setStyleSheet('color: #666;')
        desc_label.setWordWrap(True)
        
        # Create a vertical layout for name and description
        text_layout = QVBoxLayout()
        text_layout.addWidget(name_label)
        text_layout.addWidget(desc_label)
        
        # Add widgets to main layout
        layout.addWidget(emoji_label)
        layout.addSpacing(10)
        layout.addLayout(text_layout)
        layout.addStretch()
        
        # Store the package info for later use
        self.package_info = package_info

class PyPIBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.store = Store()  # Create an instance of Store
        self.init_ui()
    
    def init_ui(self):
        # Set up the main window
        self.setWindowTitle('PyPIBrowser 📦')
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create search layout with search bar and button
        search_layout = QHBoxLayout()
        
        # Search icon
        search_icon = QLabel('🔍')
        search_icon.setFont(QFont('Segoe UI Emoji', 14))
        
        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText('Search PyPI packages...')
        self.search_bar.setFont(QFont('Arial', 12))
        self.search_bar.returnPressed.connect(self.perform_search)  # Allow Enter key to trigger search
        
        # Search button
        self.search_button = QPushButton('Search')
        self.search_button.setFont(QFont('Arial', 11))
        self.search_button.clicked.connect(self.perform_search)
        
        # Add widgets to search layout
        search_layout.addWidget(search_icon)
        search_layout.addWidget(self.search_bar)
        search_layout.addWidget(self.search_button)
        
        # Create results list
        self.results_list = QListWidget()
        self.results_list.setFont(QFont('Arial', 11))
        self.results_list.setSpacing(4)
        self.results_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.results_list.customContextMenuRequested.connect(self.show_context_menu)
        
        # Add widgets to main layout
        layout.addLayout(search_layout)
        layout.addWidget(self.results_list)
        
        # Set up context menu actions
        self.info_action = QAction('📄 View Package Info', self)
        self.info_action.triggered.connect(self.show_package_info)
        self.install_action = QAction('⬇️ Copy Install Command', self)
        self.install_action.triggered.connect(self.copy_install_command)
        
        # Apply styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 4px;
                margin: 8px 0;
            }
            QPushButton {
                padding: 8px 15px;
                border: none;
                border-radius: 4px;
                background-color: #2B5B84;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1e3d5c;
            }
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
                color: black;
            }
        """)

    def perform_search(self):
        query = self.search_bar.text().strip()
        if query:
            # Clear previous results
            self.results_list.clear()
            
            # Get search results using Store class
            results = self.store.search_package_store(query)
            
            # Add results to list
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
            package_name = item_widget.package_info['name'].strip().split('\n')[0]
            command = f"pip install {package_name}"
            QApplication.clipboard().setText(command)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    browser = PyPIBrowser()
    browser.show()
    sys.exit(app.exec())