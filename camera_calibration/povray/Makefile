target.png: testmap.pov
	povray -H576 -W1024 -K0.5 Declare=scene=1 +O$@ $<

scan.png: testmap.pov bottle.inc
	povray -H576 -W1024 -K0.5 Declare=scene=2 +O$@ $<

%.dvi: %.tex
	latex $<
	latex $<

%.ps: %.dvi
	dvips -o $@ $<

%.gif: %.ps
	convert -density 300x300 -alpha off $< $@

scan.mp4: testmap.pov
	povray -H576 -W1024 -KFF90 Declare=scene=2 Declare=shift=0 $< 
	ffmpeg -f image2 -r 1 -i testmap%02d.png -vcodec mpeg4 scan.mp4
	rm testmap[0-9][0-9].png

target%.mp4: testmap.pov
	povray -H576 -W1024 -KFF90 Declare=scene=1 Declare=shift=$* $< 
	ffmpeg -f image2 -r 1 -i testmap%02d.png -vcodec mpeg4 target$*.mp4
	rm testmap[0-9][0-9].png

all: testmap.png

