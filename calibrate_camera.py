import numpy as n
import numpy.linalg as l

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

solve_camera(xyz,xy)
