run:
	docker-compose up --build

test:
	docker-compose run web pytest

query:
	curl localhost:8000/letters_in_image/ -X POST -F image=@web/letters_in_image/test/test-european.jpg

