make:
	python -OO -m py_compile user.py
	chmod +x user.py
	ln -f user.py user
	
	python -OO -m py_compile cs.py
	chmod +x cs.py
	ln -f cs.py cs
	
	python -OO -m py_compile ws.py
	chmod +x ws.py
	ln -f ws.py ws

clean:
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	rm user
	rm cs
	rm ws


