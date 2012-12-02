#include "colors.inc"
camera {
  perspective
  up y
  right -(16/9)*x
  location <0,0,1>
  look_at <0,0,0>
  angle 92
}

light_source {
  <0,0,1000>,rgb <1,1,1>
}

#declare testplane = plane {
  z,0
//box { <0,0,0> <1,1,0.001>
  pigment { 
    image_map {
      gif "testpage.gif" 
      map_type 0
      interpolate 2
      once
    }
    scale sqrt(2)*y
  }
  translate (-1/sqrt(2))*y
  //scale 1.4142*y
}

object { 
  testplane
  rotate -45*y
}

object {
  testplane
  rotate -45*y
  scale <-1,1,1>
}
