start:
	bison -d py_oop.y
	flex py_oop.l
	gcc -o py_oop lex.yy.c py_oop.tab.c -lfl
	cat test.py
	./py_oop < test.py
