run:
	python app.py

setup: requirements.txt
	pip install -r requirements.txt

clean:
	rm -rf __pycache__

compress:
	zip -r artifact/shipfer-bot-app.zip *.py requirements.txt