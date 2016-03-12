DOC_DIR=doc
SSL_DIR=ssl
SSL_KEYFILE=key.pem
SSL_CRTFILE=crt.pem

#.PHONY: gen-doc gen-ssl ping clean

$(SSL_DIR):
	mkdir -p $(SSL_DIR)

$(DOC_DIR):
	mkdir -p $(DOC_DIR)

gen-doc: $(DOC_DIR)
	apidoc -i handlers -o doc

gen-ssl: $(SSL_DIR)
	openssl req -nodes -x509 -newkey rsa:2048 -keyout $(SSL_DIR)/$(SSL_KEYFILE) \
		-out $(SSL_DIR)/$(SSL_CRTFILE) -days 30

ping:
	curl -i -Ss --cacert ssl/crt.pem https://localhost:8888
	@echo

run-server:
	./server.py --debug --ssl

run-doc:
	python -m SimpleHTTPServer 8000

test-list-student-all:
	curl -i -Ss -X GET --cacert ssl/crt.pem https://localhost:8888/info
	@echo

test-list-image-info:
	curl -i -Ss -X GET --cacert ssl/crt.pem https://localhost:8888/image/info \
		-d '{"id":"001"}'
	@echo

test-list-image:
	curl -i -Ss -X GET --cacert ssl/crt.pem https://localhost:8888/image \
		-d '{"id":"001"}'
	@echo

clean:
	find . -name "*.pyc" -type f -delete
	find . -name "*.swp" -type f -delete
	find . -name "*.swo" -type f -delete
	rm -rf doc ssl
