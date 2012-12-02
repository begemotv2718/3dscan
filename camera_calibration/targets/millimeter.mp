prologues:=3;
unit=1mm;
paperwidth=210mm;
paperheight=297mm;
beginfig(1)
%draw (0,paperheight/2)--(paperwidth,paperheight/2);
pickup pencircle scaled 0.5mm;
for i=0 upto 21:
  draw (i*10*unit,0)--(i*10*unit,paperheight);
  %label.lrt (decimal(i),(i*10*unit,paperheight/2));
endfor;
pickup pencircle scaled 0.3mm;
for i=0 upto 42:
  draw (i*5*unit,0)--(i*5*unit,paperheight);
endfor;
pickup pencircle scaled 0.1mm;
for i=0 upto 210:
  draw (i*unit,0)--(i*unit,paperheight);
endfor;
%draw (paperwidth/2,0)--(paperwidth/2,paperheight);

pickup pencircle scaled 0.5mm;
for i=0 upto 29:
  draw (0,i*10*unit)--(paperwidth,i*10*unit);
endfor;
pickup pencircle scaled 0.3mm;
for i=0 upto (29*2+1):
  draw (0,i*5*unit)--(paperwidth,i*5*unit);
endfor;

pickup pencircle scaled 0.1mm;
for i=0 upto 297:
  draw (0,i*unit)--(paperwidth,i*unit);
endfor;
endfig;
end
