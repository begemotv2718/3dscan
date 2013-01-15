import numpy as n
import numpy.linalg as l
import cv
import sys
from math import tan,sqrt

def solve_camera(xyz, xy):
  """Given a numpy array of (x,y,z) triples and a numpy array of the corresponding image (x,y) pairs find a 12-element matrix of camera"""
  npoints = min(xyz.shape[0], xy.shape[0])
  print npoints
  syst = n.zeros((3*npoints+1,12+npoints))
  print syst.shape
  print syst
  print xyz[0,:]
  for i in xrange(npoints):
    syst[3*i,0:3]=xyz[i,0:3]
    syst[3*i,3]=1
    syst[3*i,12+i]=-xy[i,0]

    syst[3*i+1,4:7]=xyz[i,0:3]
    syst[3*i+1,7]=1
    syst[3*i+1,12+i]=-xy[i,1]

    syst[3*i+2,8:11]=xyz[i,0:3]
    syst[3*i+2,11]=1
    syst[3*i+2,12+i]=-1
  syst[3*npoints,12+npoints-1]=1
  print syst


xyz = n.array([[1,2,3],[3,4,5],[0,1,2],[4,5,6]])
xy = n.array([[1,2],[1,3],[1,4],[2,7]])

class UnionFind:
    """ From http://code.activestate.com/recipes/215912/"""
    def __init__(self):
        '''\
Create an empty union find data structure.'''
        self.num_weights = {}
        self.parent_pointers = {}
        self.num_to_objects = {}
        self.objects_to_num = {}
        self.__repr__ = self.__str__
    def insert_objects(self, objects):
        '''\
Insert a sequence of objects into the structure.  All must be Python hashable.'''
        for object in objects:
            self.find(object);
    def find(self, object):
        '''\
Find the root of the set that an object is in.
If the object was not known, will make it known, and it becomes its own set.
Object must be Python hashable.'''
        if not object in self.objects_to_num:
            obj_num = len(self.objects_to_num)
            self.num_weights[obj_num] = 1
            self.objects_to_num[object] = obj_num
            self.num_to_objects[obj_num] = object
            self.parent_pointers[obj_num] = obj_num
            return object
        stk = [self.objects_to_num[object]]
        par = self.parent_pointers[stk[-1]]
        while par != stk[-1]:
            stk.append(par)
            par = self.parent_pointers[par]
        for i in stk:
            self.parent_pointers[i] = par
        return self.num_to_objects[par]
    def union(self, object1, object2):
        '''\
Combine the sets that contain the two objects given.
Both objects must be Python hashable.
If either or both objects are unknown, will make them known, and combine them.'''
        o1p = self.find(object1)
        o2p = self.find(object2)
        if o1p != o2p:
            on1 = self.objects_to_num[o1p]
            on2 = self.objects_to_num[o2p]
            w1 = self.num_weights[on1]
            w2 = self.num_weights[on2]
            if w1 < w2:
                o1p, o2p, on1, on2, w1, w2 = o2p, o1p, on2, on1, w2, w1
            self.num_weights[on1] = w1+w2
            del self.num_weights[on2]
            self.parent_pointers[on2] = on1
    def length(self):
        return len(self.num_weights)
    def sets(self):
        sets = {}
        for x in self.objects_to_num.keys():
          if self.find(x) in sets:
            sets[self.find(x)].append(x)
          else:
            sets[self.find(x)]=[x]
        return [sets[x] for x in sets.keys()]
    def __str__(self):
        '''\
Included for testing purposes only.
All information needed from the union find data structure can be attained
using find.'''
        sets = {}
        for i in xrange(len(self.objects_to_num)):
            sets[i] = []
        for i in self.objects_to_num:
            sets[self.objects_to_num[self.find(i)]].append(i)
        out = []
        for i in sets.itervalues():
            if i:
                out.append(repr(i))
        return ', '.join(out)


def cluster_points(values):
  clusters = UnionFind()
  l = range(len(values))
  clusters.insert_objects(l)
  pairs = [ (i,j) for i in range(len(values)) for j in range(i)]
  spairs = sorted(pairs, reverse=True,key=lambda x: abs(values[x[0]]-values[x[1]]))
  while(clusters.length()>2):
    pair = spairs.pop()
    clusters.union(pair[0],pair[1])
  return clusters.sets()



def GetCornerType(x,y,img):
  """Get type of corner point: upper left, bottom left, upper right, bottom right, vertical half, horizontal half, 
  also white on dark background or dark on white background. Greyscale image is presumed"""
  x1=int(x)
  y1=int(y)
  height = 5
  width = 5
  rect1 = cv.Avg(cv.GetSubRect(img,(x1,y1, width, height)))
  rect2 = cv.Avg(cv.GetSubRect(img,(x1-width,y1,width, height)))
  rect3 = cv.Avg(cv.GetSubRect(img,(x1-width,y1-height,width,height)))
  rect4 = cv.Avg(cv.GetSubRect(img,(x1,y1-height,width,height)))
  averages = [rect1[0],rect2[0],rect3[0],rect4[0]]
  clusters=cluster_points(averages)
  if(len(clusters[0]) == 2):
    return("bad","")
  else:
    fg,bg=None,None
    corner=None
    if(len(clusters[0])==1):
      fg = averages[clusters[0][0]]
      bg = averages[clusters[1][0]]
      corner = clusters[0][0]
    else:
      fg = averages[clusters[1][0]]
      bg = averages[clusters[0][0]]
      corner = clusters[1][0]

    if(fg>bg):
      return (corner,"w")
    else:
      return (corner,"b")


  




#solve_camera(xyz,xy)
print sys.argv[1]
capture = cv.CaptureFromFile(sys.argv[1])
cv.GrabFrame(capture)
img=cv.RetrieveFrame(capture)
img2=cv.CloneImage(img)
eig_image = cv.CreateMat(img.height, img.width, cv.CV_32FC1)
temp_image = cv.CreateMat(img.height, img.width, cv.CV_32FC1)
img32f = cv.CreateImage((img.width,img.height),cv.IPL_DEPTH_32F, 3)
cv.Convert(img,img32f)
img_gs=cv.CreateImage((img.width,img.height),cv.IPL_DEPTH_32F,1)
cv.CvtColor(img32f,img_gs,cv.CV_RGB2GRAY)


font = cv.InitFont(cv.CV_FONT_HERSHEY_PLAIN,1.0,1.0)

def tand(alpha):
  return tan(alpha*3.1415926/180)

d=254

goldencorners2d=[]

for alpha in range(1,10):
  alpha1=4*alpha
  alpha2=4*alpha+2
  factor1 = d*tand(alpha1)/(1+tand(alpha1))
  factor2 = d*tand(alpha2)/(1+tand(alpha2))
  goldencorners2d.append( (factor1*sqrt(2),factor1) )
  goldencorners2d.append( (factor2*sqrt(2),factor2) )

goldencorners=[[],[],[],[]]
for (xt,yt) in goldencorners2d:
  x=-xt/sqrt(2)
  y=yt
  z=d-xt/sqrt(2)
  goldencorners[0].append((x,y,z))
  goldencorners[1].append((-x,y,z))
  goldencorners[2].append((-x,-y,z))
  goldencorners[3].append((x,-y,z))


goodcorners=[[],[],[],[]]
for (x,y) in cv.GoodFeaturesToTrack(img_gs, eig_image, temp_image, 50, 0.04, 3.0, blockSize=5):
  ptype = GetCornerType(x,y,img_gs)
  if(ptype[0] in [0,1,2,3]):
    goodcorners[ptype[0]].append((x,y,ptype[1]))

goodcorners[0].sort(key=lambda point: point[0],reverse=True)
goodcorners[1].sort(key=lambda point: point[0])
goodcorners[2].sort(key=lambda point: point[0])
goodcorners[3].sort(key=lambda point: point[0],reverse=True)

for typ in range(4):
  for n in range(len(goodcorners[typ])):
     (x,y,t1)=goodcorners[typ][n]
     print "x=%s y=%s z=%s" % (x,y,t1)
     cv.PutText(img2,"%s%s%s" % (n,t1,typ), (int(x),int(y)),font,cv.RGB(100,100,0))
     cv.Circle(img2,(int(x),int(y)),5,cv.RGB(155,0,2))

cv.SaveImage("test.jpg",img2)

datacorners=zip(goodcorners[0],goldencorners[0])+zip(goodcorners[1],goldencorners[1])+zip(goodcorners[2],goldencorners[2])+zip(goodcorners[3],goldencorners[3])
print datacorners
objectPoints=cv.CreateMat(len(datacorners),3,cv.CV_32FC1)
imPoints=cv.CreateMat(len(datacorners),2,cv.CV_32FC1)
for i in range(len(datacorners)):
  p2d,p3d=datacorners[i]  
  objectPoints[i,0]=p3d[0]
  objectPoints[i,1]=p3d[1]
  objectPoints[i,2]=p3d[2]
  imPoints[i,0]=p2d[0]
  imPoints[i,1]=p2d[1]

pointCounts = cv.CreateMat(1,1,cv.CV_32SC1)
pointCounts[0,0]=len(datacorners)
cameraMatrix=cv.CreateMat(3,3,cv.CV_32FC1)
distCoefs=cv.CreateMat(4,1,cv.CV_32FC1)
rvecs=cv.CreateMat(1,1,cv.CV_32FC3)
tvecs=cv.CreateMat(1,1,cv.CV_32FC3)
cv.CalibrateCamera2(objectPoints, imPoints, pointCounts, (img.width,img.height), cameraMatrix, distCoefs, rvecs, tvecs)

print cameraMatrix
print distCoefs
print rvecs
print tvecs



