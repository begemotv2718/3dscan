def tand(expr x)= sind(x)/cosd(x) enddef;
def halfcircleprojected( expr d, alpha) =
  begingroup
    save longax, shortax, axshift, mypath;
    path mypath;
    longax = d*tand(2*alpha)/sqrt(2);
    shortax = d*sqrt(tand(alpha)*tand(2*alpha))/sqrt(2);
    axshift = d*tand(alpha)*tand(2*alpha)/sqrt(2);
    mypath = fullcircle xscaled (2*longax) yscaled (2*shortax) shifted (axshift,0);
    subpath (2,6) of mypath
  endgroup
enddef;

distance := 10in;
paperwidth := 210mm;
paperheight := 297mm;

beginfig(1)
path p[];
path frame;
for alpha= 1 upto 9:
  p0:=halfcircleprojected(distance,alpha*4);
  p1:=halfcircleprojected(distance,alpha*4+2);
  p2:=(0,0)--(0,distance);
  p3:=(0,-distance)--(0,0);
  p5:=buildcycle(p2,p0,p3,reverse p1);
  pickup pencircle scaled 0.5;
  fill p5 shifted (paperwidth, paperheight/2) withcolor 0.5*white;
  draw p5 shifted (paperwidth, paperheight/2);
  frame:=(0,0)--(paperwidth,0)--(paperwidth,paperheight)--(0,paperheight)--cycle;
  clip currentpicture to frame;
endfor;
endfig;
end

