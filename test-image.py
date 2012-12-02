#!/usr/bin/env python
import sys
import numpy, scipy
import matplotlib.pyplot as lab
""" Various tests for the simple image processing (extracting beam intersection line by simple maximum on red part)"""

def otsu(hist):
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

#load image
imname = sys.argv[1]
imbasename,extension = imname.rsplit(".",1)
image = scipy.misc.imread(imname)/255.0

#save components of the image
r,g,b=image[:,:,0],image[:,:,1],image[:,:,2]
scipy.misc.imsave(imbasename+"r"+".png",r)
scipy.misc.imsave(imbasename+"g"+".png",g)
scipy.misc.imsave(imbasename+"b"+".png",b)

#plot intensity along a selected vertical line
goldenratio = 1.618
lab.figure(0,figsize=(3.0*goldenratio,3.0))
line = r[:,r.shape[1]/5]
xdata=numpy.arange(0,line.shape[0])
lab.plot(xdata,line)
lab.xlabel("Pixel number")
lab.ylabel("Intensity")
lab.title("Plot")
lab.savefig(imbasename+"-plt.png")

#select maximums along the vertical axis and find out if the maximum is really good
maxes = numpy.argmax(r,axis=0)
maxvalues = numpy.amax(r,axis=0)
averages = numpy.average(r,axis=0)
mask = maxvalues > 7.0*averages #find lines where maximum is well separated from the average
(hist,bins) = numpy.histogram(255*r.copy().ravel(),bins=256)
otsuthr = otsu(hist)
mask2 = maxvalues > (1.1/255.0)*otsuthr #find lines where maximum is greater than Otsu threshold
print "Otsu threshold: ",otsuthr


#Plot the positions of the maximum masking out bad areas found by maxvalues < 7.0*averages
lab.figure(1,figsize=(5.0*goldenratio,5.0))
lab.plot(numpy.arange(0,maxes.shape[0]),maxes)
lab.bar(numpy.arange(0,maxes.shape[0]),800*(1-mask)) #mask out the ranges where maximums are bad
lab.ylabel("Position of maximum")
lab.savefig(imbasename+"-plt2.png")


#Plot the positions of the maximum masking out bad areas found by Otsu threshold
lab.figure(1,figsize=(5.0*goldenratio,5.0))
lab.plot(numpy.arange(0,maxes.shape[0]),maxes)
lab.bar(numpy.arange(0,maxes.shape[0]),800*(1-mask2))
lab.ylabel("Position of maximum")
lab.savefig(imbasename+"-plt3.png")

