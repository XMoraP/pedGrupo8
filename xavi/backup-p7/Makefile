login = $@
signup = $@

cli:
	@python3 cli7.py $(login) $(signup)

serv: 
	@python3 serv7.py 
%:
	@echo "La regla '$@' no está definida en el Makefile."
	@false

clean:
	@echo "Limpiando..."
	rm -r cliserv2.py.swp
	rm -r k*
