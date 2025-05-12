"""
Main window implementation for the Graph ML File Converter.
"""

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QComboBox,
    QLabel,
    QFileDialog,
    QMessageBox,
)
from PyQt6.QtCore import Qt
from core.converter import GraphConverter

class MainWindow(QMainWindow):
    """Main window of the application."""

    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        self.converter = GraphConverter()
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Graph ML File Converter")
        self.setMinimumSize(600, 400)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Input file selection
        input_layout = QHBoxLayout()
        self.input_file_label = QLabel("Input File:")
        self.input_file_path = QLabel("No file selected")
        self.input_file_button = QPushButton("Browse...")
        self.input_file_button.clicked.connect(self.select_input_file)
        input_layout.addWidget(self.input_file_label)
        input_layout.addWidget(self.input_file_path)
        input_layout.addWidget(self.input_file_button)
        layout.addLayout(input_layout)

        # Input format selection
        input_format_layout = QHBoxLayout()
        self.input_format_label = QLabel("Input Format:")
        self.input_format_combo = QComboBox()
        self.input_format_combo.addItems(["GraphML", "GML", "JSON"])
        input_format_layout.addWidget(self.input_format_label)
        input_format_layout.addWidget(self.input_format_combo)
        layout.addLayout(input_format_layout)

        # Output format selection
        output_format_layout = QHBoxLayout()
        self.output_format_label = QLabel("Output Format:")
        self.output_format_combo = QComboBox()
        self.output_format_combo.addItems(["Python", "Java"])
        output_format_layout.addWidget(self.output_format_label)
        output_format_layout.addWidget(self.output_format_combo)
        layout.addLayout(output_format_layout)

        # Output file selection
        output_layout = QHBoxLayout()
        self.output_file_label = QLabel("Output File:")
        self.output_file_path = QLabel("No file selected")
        self.output_file_button = QPushButton("Browse...")
        self.output_file_button.clicked.connect(self.select_output_file)
        output_layout.addWidget(self.output_file_label)
        output_layout.addWidget(self.output_file_path)
        output_layout.addWidget(self.output_file_button)
        layout.addLayout(output_layout)

        # Convert button
        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.convert_file)
        layout.addWidget(self.convert_button)

        # Add stretch to push everything to the top
        layout.addStretch()

    def select_input_file(self):
        """Handle input file selection."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Input File",
            "",
            "Graph Files (*.graphml *.gml *.json);;All Files (*.*)"
        )
        if file_path:
            self.input_file_path.setText(file_path)

    def select_output_file(self):
        """Handle output file selection."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Select Output File",
            "",
            "All Files (*.*)"
        )
        if file_path:
            self.output_file_path.setText(file_path)

    def convert_file(self):
        """Handle file conversion."""
        input_file = self.input_file_path.text()
        output_file = self.output_file_path.text()
        input_format = self.input_format_combo.currentText().lower()
        output_format = self.output_format_combo.currentText().lower()

        if input_file == "No file selected" or output_file == "No file selected":
            QMessageBox.warning(
                self,
                "Error",
                "Please select both input and output files."
            )
            return

        try:
            self.converter.convert(
                input_file,
                output_file,
                input_format,
                output_format
            )
            QMessageBox.information(
                self,
                "Success",
                "File conversion completed successfully!"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Conversion failed: {str(e)}"
            ) 