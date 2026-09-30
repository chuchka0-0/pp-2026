CXX      = g++
CXXFLAGS = -I. -O3 -std=c++11 -Wall

mandelbrot: main.cpp mandelbrotSerial.cpp mandelbrotThread.cpp ppm.cpp
	$(CXX) $(CXXFLAGS) -o $@ $^ -lm -lpthread

clean:
	rm -f mandelbrot *.ppm
