prologues:=3;
unit=1mm;
paperwidth=210mm;
paperheight=297mm;
beginfig(1)
draw (0,paperheight/2)--(paperwidth,paperheight/2);
for i=0 upto 21:
  draw (i*10*unit,paperheight/2-2*unit)--(i*10*unit,paperheight/2+2*unit);
  label.lrt (decimal(i),(i*10*unit,paperheight/2));
endfor;
for i=0 upto 42:
  draw (i*5*unit,paperheight/2-1.41*unit)--(i*5*unit,paperheight/2+1.41*unit);
endfor;
for i=0 upto 210:
  draw (i*unit,paperheight/2-unit)--(i*unit,paperheight/2+unit);
endfor;
draw (paperwidth/2,0)--(paperwidth/2,paperheight);
for i=0 upto 29:
  draw (paperwidth/2-2*unit,i*10*unit)--(paperwidth/2+2*unit,i*10*unit);
endfor;
for i=0 upto (29*2+1):
  draw (paperwidth/2-1.41*unit,i*5*unit)--(paperwidth/2+1.41*unit,i*5*unit);
endfor;
for i=0 upto 297:
  draw (paperwidth/2-unit,i*unit)--(paperwidth/2+unit,i*unit);
endfor;
endfig;
end
