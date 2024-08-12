# SmartCart

Welcome to SmartCart! This application provides statistics and analytics for your shopping cart. It helps you track your purchases, manage your budget, and make smarter shopping decisions.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Make targets](#make-targets)
- [License](#license)

## Features
- Scan receipts to upload your purchases.
- View statistics and analytics for your shopping cart by items and categories.
- Set a budget and track your spending.
- Get recommendations for similar products.
- Generate shopping lists based on your preferences.

## Installation

### Prerequisites
- Python 3.8 or later
- pip (Python package installer)
- Docker (optional)
- make (optional)

### Clone the Repository
```bash
git clone https://github.com/Guy-Ronen/smartcart.git
cd src
```

### Install Dependencies
You can install the required packages using pip, I would recommend using a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Run the Application
I recommend using the `make` command to run the application:

```bash
make run
```

### Using the Application
- upload a receipt
- view statistics
- set a budget
- get recommendations
- generate a shopping list

## Make Targets (for development)
```bash
make help          # Display available make targets.
make build         # Builds the smart_cart image.
make run           # Runs the smart_cart and dependency containers.
make debug         # Runs the smart_cart and dependency containers with a configuration that allows pdb breakpoints.
make shell         # Runs the smart_cart and database, and enters a bash prompt in the src directory.
make test          # Runs all tests.
make format        # Formats the codebase using black and isort.
make lint          # Runs static checks.
make lint-fix      # Fixes linting errors.
make generate-jwt  # Outputs the generated JWT for local API authentication
```


## Contributing
Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a Pull Request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---