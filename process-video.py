#!/usr/bin/env python
from pyffmpeg import FFMpegReader
import sys
from scipy.fftpack import fft, fftfreq, ifft
import numpy,scipy
from time import strftime
from scipy import stats
from math import sqrt
import cProfile

def mkgrad(data):
  data_f = fft(data)
  n = data_f.shape[0]
  grad = data_f* fftfreq(n)*numpy.exp(-fftfreq(n)*fftfreq(n)*4)
  return numpy.absolute(ifft(grad))

def maxesgrad(data):
  res1=numpy.argsort(mkgrad(data))
  res1=res1[::-1]
  i=0
  while(abs(res1[i]-res1[0])<4):
    assert(i<10)
    i+=1
  return numpy.sort([res1[0],res1[i]])

def extract_data(ypoints,zpoints,calibration):
  """Function to extract coordinates from the data(not yet tested)"""
  d=calibration['distance']
  tgz_coeff=calibration['vpoints45']
  tgy_coeff=calibration['hpoints45']
  z_center=calibration['v_center'] #Vertical coordinate of optical axis intersection with image plane
  y_center=calibration['h_center'] #Horizontal -ii-
  zpts_scaled=(zpoints-z_center)/tgz_coeff
  ypts_scaled=(ypoints-y_center)/tgy_coeff
  z_line_lft = zpts_scaled[0:zpts_scaled.shape[0]/5]
  y_line_lft = ypts_scaled[0:ypts_scaled.shape[0]/5]
  lft_slope,lft_intercept,lft_r_val,lft_p_val,lft_std_err = stats.linregress(y_line_lft,z_line_lft)
  z_line_rt = zpts_scaled[-zpts_scaled.shape[0]/5:-1]
  y_line_rt = ypts_scaled[-ypts_scaled.shape[0]/5:-1]
  rt_slope,rt_intercept,rt_r_val,rt_p_val,rt_std_err = stats.linregress(y_line_rt,z_line_rt)
  assert(abs(rt_intercept-lft_intercept)<0.1)
  z0=d*(rt_intercept+lft_intercept)/2.0
  gamma1=-(lft_slope+lft_intercept)/sqrt(2.0)
  gamma2=(rt_slope+rt_intercept)/sqrt(2.0)
  (x,y,z)=(1,ypts_scaled,zpts_scaled)*((gamma1+gamma2)/sqrt(2)+z0)/scalarprod((1,ypts_scaled,zpts_scaled),((gamma1+gamma2)/sqrt(2),(gamma1-gamma2)/sqrt(2),1))
  


  

def observer(f):
  r = f[:,:,0]
  maxes = numpy.asarray([maxesgrad(r[:,i]) for i in xrange(r.shape[1])])
  mask1 = (maxes[:,1]-maxes[:,0])<r.shape[0]*0.02 #We only accept vertical lines  where two edges of the laser line are close to each other
  fraction = float(numpy.sum(numpy.where(mask1,1,0)))/float(r.shape[1]) #fraction of good points
  print "current fraction = %f" % fraction
  if fraction >0.8:
      print fraction
      extract_data(numpy.arange(maxes.shape[0])[mask1],maxes[mask1,1])
      scipy.misc.imsave("/tmp/saved-%s.png" % strftime("%d-%m-%y-%H-%M-%S"),r)
  
  

mp = FFMpegReader()
print sys.argv[1]
mp.open(sys.argv[1])
tracks = mp.get_tracks()
video_track=tracks[0]
video_track.set_observer(observer)
#cProfile.run('mp.run()')
mp.run()
