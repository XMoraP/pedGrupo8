login = $@
signup = $@

cli:
	@cd app/
	@python3 cli7.py $(login) $(signup)

serv: 
	@cd app/
	@python3 serv7.py 

test:
	@cd test/ && python3 -m unittest discover -v

%:
	@echo "La regla '$@' no está definida en el Makefile."
	@false

clean:
	@echo "Limpiando..."
	rm -r cliserv2.py.swp
	rm -r k*
