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

5. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
API documentation will be available at `http://localhost:8000/docs`

## API Endpoints

- `/news`: News management endpoints
  - GET: Retrieve news articles
  - POST: Add new articles
  - PUT: Update existing articles

## Requirements

- Python 3.7+
- MongoDB
- FastAPI
- Other dependencies listed in `requirements.txt`

## Contributing

Feel free to submit issues and enhancement requests.

## License

This project is licensed under the terms of the MIT license.
