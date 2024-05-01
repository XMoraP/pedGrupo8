file = $@

cli:
	@python3 cli6.py $(file)

serv: 
	@python3 serv6.py 
%:
	@echo "La regla '$@' no está definida en el Makefile."
	@false

clean:
	@echo "Limpiando..."
	rm -r cliserv2.py.swp
	rm -r k*
