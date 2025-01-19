# NewsManager

A FastAPI-based news management system that aggregates and manages news from multiple sources including CNA and New York Times.

## Features

- Multi-source news aggregation
- RESTful API endpoints for news management
- MongoDB integration for data persistence
- Automated news crawling and updates
- Support for multiple news channels including:
  - CNA (Channel News Asia)
  - New York Times
  - Straits Times
- Category-based news filtering
- Cross-platform support (Windows and Linux)

## Project Structure

```
app/
├── config.py           # Configuration settings
├── crawler/           # News crawling functionality
├── main.py            # FastAPI application entry point
├── models.py          # Data models
├── mongo.py           # MongoDB integration
├── news_channels/     # News source implementations
├── news_control.py    # News management logic
├── routers/          # API route definitions
├── schemas.py         # Pydantic schemas
└── saved_news_items/  # Cached news data
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure MongoDB:
   - Ensure MongoDB is installed and running
   - Update connection settings in `config.py` if needed

## Running the Application

### Development Mode
```bash
uvicorn app.main:app --reload
```

### Production Mode
Use the `pywsgi.py` script which automatically selects the appropriate server:
- Windows: Uses Uvicorn
- Linux: Uses Gunicorn with Uvicorn workers

```bash
python pywsgi.py
```

The API will be available at `http://localhost:8000`
API documentation will be available at `http://localhost:8000/docs`

## API Endpoints

### News Endpoints

- `/news/get_news_simple`: Get news articles with navigation and filtering
  - Query Parameters:
    - `last_retrieved_id` (optional): ID of the last retrieved document
    - `navigation` (optional): Direction of navigation ('next' or 'previous')
    - `category` (optional): Filter news by category
  - Returns:
    - Latest news item if no parameters provided
    - Next/previous items based on navigation direction
    - Category-filtered results when category is specified

## Requirements

- Python 3.7+
- MongoDB
- FastAPI
- Additional dependencies:
  - Uvicorn (Windows/Development)
  - Gunicorn (Linux/Production)
  - Other dependencies listed in `requirements.txt`

## Contributing

Feel free to submit issues and enhancement requests.

## License

This project is licensed under the terms of the MIT license.
