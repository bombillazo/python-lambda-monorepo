SHELL = /bin/bash

compress:	
	cd services/${LAMBDA}; \
	zip main.zip *.py */ -x "test/*" -r 

upload: 
	make install LAMBDA=$$LAMBDA
	make compress LAMBDA=$$LAMBDA
	cd services/${LAMBDA}; \
	aws lambda update-function-code --function-name ${LAMBDA} --region us-east-1 --zip-file fileb://main.zip

install:
	FILE=services/${LAMBDA}/requirements.txt; \
	if [[ -f "$$FILE" ]]; then \
		pip install -r $$FILE --target services/${LAMBDA}/packages/ --find-links ./packages --upgrade; \
	fi

add-all-dinos:
	for FILE in test_requests/*.json ; do \
		sam local invoke createdinosaur -e $$FILE --profile bombillazo; \
	done