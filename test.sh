curl "http://127.0.0.1:5000/notes"
curl "http://127.0.0.1:5000/notes" -H "Content-Type: application/json" -d '{"text": "note 01"}'
curl "http://127.0.0.1:5000/note/0"
curl -X DELETE "http://127.0.0.1:5000/notes" -H "Content-Type: application/json" -d '{"id": "0"}'
curl "http://127.0.0.1:5000/notes"
