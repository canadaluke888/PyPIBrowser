from PyQt6.QtWidgets import QDialog, QTextEdit, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt


class PackageInfoDialog(QDialog):
    def __init__(self, package_info):
        super().__init__()

        self.package_info = package_info
        
        # Setup window
        self.setWindowTitle("Package Info")
        self.setGeometry(200, 200, 600, 400)

        # Create layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create and setup text edit
        self.package_details = QTextEdit()
        self.package_details.setReadOnly(True)
        layout.addWidget(self.package_details)

        # Set the formatted content
        self.set_package_details_box(self.format_details(self.package_info))

    def format_details(self, package_info):
        # Split the name field into name and version
        name_parts = package_info['name'].strip().split('\n')
        package_name = name_parts[0]
        version = name_parts[1] if len(name_parts) > 1 else "Version not available"
        
        html_content = f"""
        <html>
        <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                color: #333;
            }}
            .package-name {{
                font-size: 24px;
                color: #2B5B84;
                margin-bottom: 5px;
            }}
            .version {{
                font-size: 16px;
                color: #666;
                margin-bottom: 15px;
            }}
            .description {{
                font-size: 14px;
                line-height: 1.5;
                margin-bottom: 20px;
            }}
            .url {{
                color: #0366d6;
                text-decoration: none;
                font-size: 14px;
            }}
            .divider {{
                border-bottom: 1px solid #e1e4e8;
                margin: 15px 0;
            }}
        </style>
        </head>
        <body>
            <div class="package-name">{package_name}</div>
            <div class="version">Version: {version}</div>
            <div class="divider"></div>
            <div class="description">{package_info['description']}</div>
            <div class="divider"></div>
            <div class="url">
                <a href="{package_info['url']}">View on PyPI</a>
            </div>
        </body>
        </html>
        """
        return html_content

    def set_package_details_box(self, formatted_details):
        self.package_details.setHtml(formatted_details)