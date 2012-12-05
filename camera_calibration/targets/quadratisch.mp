def tand(expr x)= sind(x)/cosd(x) enddef;
def halfsquareprojected(expr d, alpha) =
  (0,d*tand(alpha))--(d*tand(alpha)/(1+tand(alpha))*(-sqrt(2),1))--(d*tand(alpha)/(1+tand(alpha))*(-sqrt(2),-1))--(0,-d*tand(alpha))
enddef;
    
distance := 50cm;
paperwidth := 210mm;
paperheight := 297mm;

beginfig(1)
path p[];
path frame;
for alpha= 1 upto 9:
  p0:=halfsquareprojected(distance,alpha*4);
  p1:=halfsquareprojected(distance,alpha*4+2);
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

