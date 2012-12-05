#include "colors.inc"
#declare clock2 = 2*clock-1.0; //running from -1 to 1
camera {
  perspective
  up y
  right -(16/9)*x
  location <0,0,(254.0/210.0)*(1+0.2*clock2)>
  look_at <0,0,0>
  angle 92
}

//light_source {
//  <0,0,1000>,rgb <1,1,1>
//}

#declare testplane = plane {
  z,0
//box { <0,0,0> <1,1,0.001>
  pigment { 
    image_map {
      //gif "testpage.gif" 
      png "circles2.png"
      map_type 0
      interpolate 2
      once
    }
    scale sqrt(2)*y
  }
  translate (-1/sqrt(2))*y
  //scale 1.4142*y
}

#declare laser_pointer_obj = light_source {
  <0,0,0>, rgb <1,0,0>
  projected_through {
    cylinder {
      <0,-0.00001,0>,<0,0.00001,0>,1
      open
    }
  }
}

#macro laser_pointer(loc,lookat) 

  #local dir = vnormalize(lookat-loc);
  #local rotvect = vcross(y,dir);
  #local axis = vnormalize(rotvect);
  #local theta = degrees(acos(vlength(rotvect)));
  
  object {
    laser_pointer_obj
    //rotate 30*z
    rotate theta*axis
    translate loc
  }
#end

laser_pointer(<0,5,200>,<0,0.1,0>)

object { 
  testplane
  rotate -45*y
}

object {
  testplane
  rotate -45*y
  scale <-1,1,1>
}

#include "bottle.inc"
object {
  bottle
  scale 0.5
  translate <0,-0.25,0.8>
  pigment {color 0.7*White}
}
