# Amazon.in Clone

A clone of the Amazon India website built with Flask, SQLAlchemy and WTForms.

## Features

- User authentication (register, login, profile management)
- Product browsing by category
- Product search functionality
- Product detail pages with reviews
- Shopping cart
- Checkout process
- Responsive design similar to Amazon India

## Tech Stack

- **Backend**: Flask, SQLAlchemy, WTForms
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Database**: SQLite (can be easily changed to another database)

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd amazon-clone
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python seed_db.py
```

5. Run the application:
```bash
python app.py
```

6. Visit http://localhost:5000 in your browser

## Sample Users

The seed script creates two users:

1. Admin User:
   - Email: admin@example.com
   - Password: admin123

2. Regular User:
   - Email: user@example.com
   - Password: user123

## Project Structure

- `app.py`: Main application file
- `config.py`: Configuration settings
- `extensions.py`: Flask extensions
- `models.py`: Database models
- `forms.py`: Form definitions using WTForms
- `seed_db.py`: Script to populate the database with sample data
- `routes/`: Directory containing route handlers
  - `main.py`: Main routes (homepage, search, etc.)
  - `auth.py`: Authentication routes
  - `product.py`: Product-related routes
  - `cart.py`: Shopping cart routes
- `templates/`: HTML templates
- `static/`: Static files (CSS, JS, images)

## Screenshots

[Screenshots will be added here]

## License

This project is for educational purposes only. Amazon name and logo are trademarks of Amazon.com, Inc.
