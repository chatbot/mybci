test:
	#rm -f a.out
	#gcc -I/usr/local/cuda/include/ -L/usr/local/cuda/lib/ 2source2socket.c -lcufftemu -lcutil
	#
	#
	gcc -I/usr/local/cuda/include/ -Wall -fPIC -c myfft.c 
	gcc -shared -L/usr/local/cuda/lib/ -Wl,-soname,libmyfft.so -lcufftemu -lcutil myfft.o -o libmyfft.so
	
	gcc fftest.c -L. -lmyfft -o fftest
	ln -s `pwd`/libmyfft.so ../../pyeeg/libmyfft.so
