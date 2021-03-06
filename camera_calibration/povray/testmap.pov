global_settings {
  ambient_light <0.01,0.01,0.01>
}

#include "colors.inc"





#declare clock2 = 2*clock-1.0; //running from -1 to 1

#if(scene=1)
  #declare clock_camera = clock2;
  #declare clock_scan = 0.0;
#else
  #declare clock_camera = 0.0;
  #declare clock_scan = clock2;
#end

#declare clock_ypoint = 0.0;
#declare clock_xpoint = 0.0;
#declare clock_xcamera = 0.0;
#declare clock_ycamera = 0.0;
#declare clock_zcamera = 0.0;


#if(shift=0)
  #declare clock_zcamera=clock_camera;
#end
#if(shift=1)
  #declare clock_ypoint = clock_camera;
#end
#if(shift=2)
  #declare clock_xpoint = clock_camera;
#end
#if(shift=3)
  #declare clock_xcamera = clock_camera;
#end
#if(shift=4)
  #declare clock_ycamera = clock_camera;
#end
#if(shift=5)
  #declare clock_xcamera = clock_camera;
  #declare clock_xpoint = clock_camera;
#end
#if(shift=6)
  #declare clock_ycamera = clock_camera;
  #declare clock_ypoint = clock_camera;
#end

camera {
  perspective
  up y
  right -(16/9)*x
  location <clock_xcamera,clock_ycamera,(254.0/210.0)*(1+0.2*clock_zcamera)>
  look_at <clock_xpoint,clock_ypoint,0>
  angle 92
}

#if(scene = 1)
light_source {
  <0,0,1000>,rgb <1,1,1>
}
#end

#declare testplane = plane {
  z,0
//box { <0,0,0> <1,1,0.001>
  pigment { 
    image_map {
      //gif "testpage.gif" 
      //png "circles2.png"
      png "quadratisch2.png"
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

laser_pointer(<0,20,200>,<0,0.7*clock_scan,0>)

object { 
  testplane
  rotate -45*y
}

object {
  testplane
  rotate -45*y
  scale <-1,1,1>
}

#if(scene=2)
#include "bottle.inc"
object {
  bottle
  scale 0.5
  translate <0,-0.25,0.8>
  pigment {color 0.7*White}
}
#end
