%.png: %.pov
	povray -H576 -W1024 -K0.5 $<

%.dvi: %.tex
	latex $<
	latex $<

%.ps: %.dvi
	dvips -o $@ $<

%.gif: %.ps
	convert -density 300x300 -alpha off $< $@

testmap.mp4: testmap.pov
	povray -H576 -W1024 -KFF10 $< 
	ffmpeg -f image2 -r 1/5 -i testmap%02d.png -vcodec mpeg4 testmap.mp4
	rm testmap[0-9][0-9].png

all: testmap.png

