%.png: %.pov
	povray -H576 -W1024 $<

%.dvi: %.tex
	latex $<
	latex $<

%.ps: %.dvi
	dvips -o $@ $<

%.gif: %.ps
	convert -density 300x300 -alpha off $< $@


all: testmap.png

