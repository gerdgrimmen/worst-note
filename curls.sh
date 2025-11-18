# example curl commands for testing
# get curls
curl "http://127.0.0.1:5000/tags"
curl "http://127.0.0.1:5000/notes"

#get image curls
curl "http://127.0.0.1:5000/images" # not working might just get the available IDs out in a list
curl "http://127.0.0.1:5000/images/0" -o downloaded_file.png

# post curls
curl "http://127.0.0.1:5000/tags" -H "Content-Type: application/json" -d '{"text": "tag 01"}'
curl "http://127.0.0.1:5000/notes" -H "Content-Type: application/json" -d '{"text": "note 01"}'

# put curls
curl "http://127.0.0.1:5000/images" -T test_image.png -H "Content-Type: image/png"

# delete curls
curl -X DELETE "http://127.0.0.1:5000/notes" -H "Content-Type: application/json" -d '{"id": "0"}'
