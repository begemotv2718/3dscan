#!/usr/bin/python2.6
from pyffmpeg import FFMpegReader
import sys
from scipy.fftpack import fft, fftfreq, ifft
import numpy,scipy
from time import strftime
from scipy import stats
from math import sqrt
#import cProfile
import matplotlib.pyplot as lab

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
  tgz_coeff=float(calibration['vpoints45']) #Vertical distance between intersection of optical axis with image plane and intersection of 45 degrees line with image plane
  tgy_coeff=float(calibration['hpoints45']) #Horizontal -ii-
  z_center=float(calibration['v_center']) #Vertical coordinate of optical axis intersection with image plane
  y_center=float(calibration['h_center']) #Horizontal -ii-

  zpts_scaled=(zpoints-z_center)/tgz_coeff
  ypts_scaled=(ypoints-y_center)/tgy_coeff
  

  z_line_lft = zpts_scaled[0:zpts_scaled.shape[0]/5]
  y_line_lft = ypts_scaled[0:ypts_scaled.shape[0]/5]
  print "z shape ", z_line_lft.shape, " y_shape ", y_line_lft.shape
  print "Covariance: ",numpy.cov(y_line_lft,z_line_lft)
  lft_slope,lft_intercept,lft_r_val,lft_p_val,lft_std_err = stats.linregress(y_line_lft,z_line_lft)


  z_line_rt = zpts_scaled[-zpts_scaled.shape[0]/5:-1]
  y_line_rt = ypts_scaled[-ypts_scaled.shape[0]/5:-1]
  rt_slope,rt_intercept,rt_r_val,rt_p_val,rt_std_err = stats.linregress(y_line_rt,z_line_rt)
  print "lft: slope %f, intercept %f, p_val %f, std_err %f" %(lft_slope,lft_intercept,lft_p_val,lft_std_err)
  print "rt: slope %f, intercept %f, p_val %f, std_err %f" %(rt_slope,rt_intercept,rt_p_val,rt_std_err)

  assert(abs(rt_intercept-lft_intercept)<0.1)


  z0=d*(rt_intercept+lft_intercept)/2.0
  gamma1=-(lft_slope+lft_intercept)/sqrt(2.0)
  gamma2=(rt_slope+rt_intercept)/sqrt(2.0)
  gamma_plus = (gamma1+gamma2)/sqrt(2.0)
  gamma_minus = (gamma1-gamma2)/sqrt(2.0)

  def reconstruct_point(y_im,z_im):
    coefficient = (gamma_plus*d+z0)/(gamma_plus*1+gamma_minus*y_im+1*z_im)
    return numpy.asarray([1,y_im, z_im])*coefficient
  res= numpy.asarray([reconstruct_point(ypts_scaled[i],zpts_scaled[i]) for i in xrange(zpts_scaled.shape[0])])
  print "Result:", res
  return res
  #(x,y,z)=(1,ypts_scaled,zpts_scaled)*(gamma_plus+z0)/scalarprod((1,ypts_scaled,zpts_scaled),(gamma_plus,gamma_minus,1))
  


frameno=0  
camera = { 'distance':1, 'vpoints45': 512, 'hpoints45': 512, 'v_center' : 512, 'h_center': 512 }


def observer(f):
  global frameno
  global camera
  r = f[:,:,0]
  maxes = numpy.asarray([maxesgrad(r[:,i]) for i in xrange(r.shape[1])])
  mask1 = (maxes[:,1]-maxes[:,0])<r.shape[0]*0.02 #We only accept vertical lines  where two edges of the laser line are close to each other
  good_points = float(numpy.sum(numpy.where(mask1,1,0)))
  if(good_points<10):
    return
  good_indices=numpy.arange(maxes.shape[0])[mask1]
  good_range = good_indices[-1]-good_indices[0]
  fraction = good_points/float(good_range) #fraction of good points
  goldenratio=1.618
  frameno += 1
  if fraction >0.7:
      print fraction
      extract_data(numpy.arange(maxes.shape[0])[mask1],maxes[mask1,1],camera)
      scipy.misc.imsave("/tmp/saved-%03d.png" % frameno,r)
      lab.figure(frameno,figsize=(5.0*goldenratio,5.0))
      lab.plot(numpy.arange(0,maxes.shape[0])[mask1],maxes[mask1,1],'bo')
      lab.plot(numpy.arange(0,maxes.shape[0]),20*(1-mask1),'g+') #mask out the ranges where maximums are bad
      lab.ylabel("Position of maximum")
      lab.savefig("/tmp/saved-%03d-plt2.png" % frameno)
  
  

mp = FFMpegReader()
print sys.argv[1]
mp.open(sys.argv[1])
tracks = mp.get_tracks()
video_track=tracks[0]
video_track.set_observer(observer)
#cProfile.run('mp.run()')
mp.run()
