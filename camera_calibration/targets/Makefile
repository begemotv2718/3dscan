%.ps: %.mp
	mpost $<
	mv $*.1 $*.ps
	sed -e "s/^%%BoundingBox: [0-9][0-9.]* /%%BoundingBox: 0 /" -i $@
	sed -e "s/^%%HiResBoundingBox: [0-9][0-9.]* /%%HiResBoundingBox: 0 /" -i $@

%.png: %.ps
	convert -density 300x300 -alpha off $< $@
