# Graph ML File Converter

A cross-platform desktop application for converting between different graph machine learning file formats.

## Features

- Convert between various graph ML file formats (GraphML, GML, JSON)
- Generate Python or Java code output
- Offline operation
- Cross-platform support (Windows, macOS, Linux)
- Modern PyQt6-based user interface

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/graph-ml-converter.git
cd graph-ml-converter
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python src/main.py
```

## Supported Formats

### Input Formats
- GraphML (.graphml)
- GML (.gml)
- JSON (.json)

### Output Formats
- Python code with NetworkX
- Java code with JGraphT

## Development

### Project Structure
```
graph-ml-converter/
├── src/
│   ├── core/         # Core conversion logic
│   ├── ui/           # User interface components
│   └── utils/        # Utility functions
├── tests/            # Test files
├── data/             # Sample data files
├── requirements.txt  # Project dependencies
└── README.md         # This file
```

### Running Tests
```bash
pytest tests/
```

### Code Style
The project uses Black for code formatting and Pylint for code analysis:
```bash
black src/
pylint src/
```

## License

MIT License 