run:
	cd web && docker-compose up

test:
	cd web && docker-compose run web pytest

query:
	curl localhost:8000/letters_in_image/ -X post -F image=@web/letters_in_image/test/test-european.jpg

