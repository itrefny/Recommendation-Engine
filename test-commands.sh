
Linux:
curl -X POST http://localhost:8001/recommend-books -H "Content-Type: application/json" -d '{"favorite-book": "1984"}'

Windows:
curl -X POST http://localhost:8001/recommend-books -H "Content-Type: application/json" -d "{ \"favorite-book\": \"1984\" }"