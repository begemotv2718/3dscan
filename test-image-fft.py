#!/usr/bin/env python
import sys
import numpy, scipy
import matplotlib.pyplot as lab
from scipy.fftpack import fft, fftfreq, ifft

"""In this file we experiment with different FFT based image gradients to find out the line along which laser light crosses the object"""


def otsu(hist):
"""find binarization threshold from image histogram"""
  def safediv(x,y):
    if y == 0:
      return 0
    else:
      return float(x)/float(y)
  totalleft = reduce(lambda x,y: x+[x[-1]+y], hist, [0,])
  total = totalleft[-1]
  totalright = map (lambda x: total -x ,totalleft)

  weighted = [ i*hist[i] for i in range(len(hist))]
  sumweightedleft = reduce(lambda x,y: x+[x[-1]+y], weighted, [0,])
  sumweighted = sumweightedleft[-1]
  sumweightedright = map(lambda x: sumweighted -x, sumweightedleft)

  Wb = map(lambda x: float(x)/float(total), totalleft)
  Wf = map(lambda x: float(x)/float(total), totalright)
  Mb = [ safediv(sumweightedleft[i],totalleft[i]) for i in range(len(totalleft))]
  Mf = [ safediv(sumweightedright[i],totalright[i]) for i in range(len(totalright))]
  sigma2 = [ Wb[i]*Wf[i]*(Mb[i]-Mf[i])**2 for i in range(len(Wb))]
  return sigma2.index(max(sigma2))

class Gradientor:
  """FFT based gradient. We have a class here to calculate the filter matrix only once"""
  def __init__(self):
    self.n=None
    self.grad_multiplyer=None
  def mkgrad(self,data):
    """Calculate gradient by convolution with appropriate gaussian filter"""
    n1=data.shape[0]
    if(not self.n or n1 != self.n):
      self.n= n1
      self.grad_multiplyer= fftfreq(n1)*numpy.exp(-4*fftfreq(n1)**2)
    data_f = fft(data)
    grad_f = data_f*self.grad_multiplyer
    return numpy.absolute(ifft(grad))
  def maxesgrad(self,data):
    """Return two peaks of the gradient (corresponding to the top and bottom edges of the line)"""
    res1=numpy.argsort(mkgrad(data))
    res1=res1[::-1]
    #filter out adjacent values
    i=0
    while(abs(res1[i]-res1[0])<4):
      assert(i<10)
      i+=1
    return numpy.sort([res1[0],res1[i]])


    

def mkgrad(data):
  """This does not take advantage  of precomputed filter"""
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

#Read image
imname = sys.argv[1]
imbasename,extension = imname.rsplit(".",1)
image = scipy.misc.imread(imname)/255.0
r,g,b=image[:,:,0],image[:,:,1],image[:,:,2]


#Plot the gradient
goldenratio = 1.618
lab.figure(0,figsize=(3.0*goldenratio,3.0))
line = r[:,r.shape[1]/5] #select some vertical line in the image
xdata=numpy.arange(0,line.shape[0])
lab.plot(xdata,line)
lab.plot(xdata, 20*mkgrad(line))
lab.xlabel("Pixel number")
lab.ylabel("Intensity")
lab.title("Plot")
lab.savefig(imbasename+"-fftplt.png")
print maxesgrad(line)

from time import time

#Calculate gradient without filter caching
start1=time()
maxes=numpy.asarray([maxesgrad(r[:,i]) for i in xrange(r.shape[1])])
end1=time()
start2=time()
maxes2 = numpy.apply_along_axis(maxesgrad,0,r)
end2=time()
print maxes.shape
print start1,end1,end1-start1
print start2,end2,end2-start2
print maxes2.shape

#Calculate gradient with filter caching
start1=time()
grd=Gradientor()
maxes=numpy.asarray([grd.maxesgrad(r[:,i]) for i in xrange(r.shape[1])])
end1=time()
start2=time()
print maxes.shape
print start1,end1,end1-start1

lab.figure(1,figsize=(5.0*goldenratio,5.0))
lab.plot(numpy.arange(0,maxes.shape[0]),maxes)
#lab.bar(numpy.arange(0,maxes.shape[0]),800*(1-mask))
lab.ylabel("Position of maximum")
lab.savefig(imbasename+"-fftplt2.png")


lab.figure(2,figsize=(5.0*goldenratio,5.0))
lab.plot(numpy.arange(0,maxes.shape[0]),maxes[:,1]-maxes[:,0])
lab.savefig(imbasename+"-fftplt3.png")

mask1=(maxes[:,1]-maxes[:,0])<r.shape[0]*0.02
m1 = maxes[mask1,:]
x=numpy.arange(0,maxes.shape[0])[mask1]
print m1.shape
print x.shape
lab.figure(3,figsize=(5.0*goldenratio,5.0))
lab.plot(x,m1)
lab.savefig(imbasename+"-fftplt4.png")
print float(numpy.sum(numpy.where(mask1,1,0)))/float(r.shape[1])
print r.shape[1]
