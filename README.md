# Dash Mindmap Maker

## Overview

This project demonstrates a web application built with Dash that converts hierarchical text into a visual mind map using Cytoscape and NetworkX.

## Features

- Converts hierarchical text into a mind map structure.
- Allows users to visualize and interact with the mind map.
- Supports adding new nodes dynamically.
- Responsive layout using Dash components.

## Setup

### Prerequisites

- Python 3.x installed.
- pip package manager.

### Installation

1. Clone the repository:
git clone <repository-url>
cd <repository-directory>

arduino
Copy code

2. Set up a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate # On Windows use venv\Scripts\activate

markdown
Copy code

3. Install dependencies:
pip install -r requirements.txt

shell
Copy code

### Running the Application

Start the Dash server:
python main.py

csharp
Copy code

Open a web browser and navigate to `http://127.0.0.1:8050` to view the application.

## Usage

- Enter hierarchical text into the input area.
- Click "Convert to Mindmap" to generate the mind map.
- Interact with nodes by clicking on them to view details.
- Add new nodes by entering a label and selecting a parent node.

## Technologies Used

- Dash: Python framework for building web applications.
- Cytoscape: JavaScript library for graph visualization.
- NetworkX: Python library for network analysis.
