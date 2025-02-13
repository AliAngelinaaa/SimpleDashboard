# SimpleDashboard

A Python-based dashboard application that analyzes spreadsheet data and generates trend visualizations.

## Features

- Import data from Excel/CSV spreadsheets
- Generate interactive trend charts and graphs
- Customizable date range analysis
- Multiple visualization options (line charts, bar graphs, pie charts)
- Export visualizations as PNG/PDF

## Prerequisites

- Python 3.8+
- Required Python packages:
  - pandas
  - plotly
  - dash
  - openpyxl

## Installation

1. Clone the repository: 
```bash
git clone https://github.com/yourusername/SimpleDashboard.git
cd SimpleDashboard
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the dashboard:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:8050`

3. Use the interface to:
   - Upload your data files
   - Select visualization types
   - Adjust date ranges
   - Export results

## Configuration

The dashboard can be configured by modifying `config.yaml`:
- Port number
- Default chart settings
- Data source paths
- Theme preferences

## Project Structure

```
SimpleDashboard/
├── app.py              # Main application file
├── config.yaml         # Configuration settings
├── requirements.txt    # Package dependencies
├── assets/            # Static files (CSS, images)
└── modules/           # Python modules
    ├── data_loader.py
    ├── visualizer.py
    └── utils.py
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
