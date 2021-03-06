import numpy as n
import numpy.linalg as l
import cv
import sys
from math import tan,sqrt,pow

def solve_camera(xyz, xy):
  """Given a numpy array of (x,y,z) triples and a numpy array of the corresponding image (x,y) pairs find a 12-element matrix of camera"""
  npoints = min(xyz.shape[0], xy.shape[0])
  syst = n.zeros((3*npoints+1,12+npoints))
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
  syst2=n.delete(syst,3*npoints,0)
  b=n.zeros(3*npoints+1)
  b[3*npoints]=1
  t=l.lstsq(syst,b)
  rank=t[2]
  if rank<12+npoints:
    raise "Ambigous solution, low matrix rank"
  T=t[0][0:12].reshape((3,4))
  dt=l.det(T[0:3,0:3])
  mod = pow(dt,1/3.0)
  return T/mod



t=n.array([[1.0,0.0,0.0,5.0],
           [0.0,1.0,0.0,2.0],
           [0.0,0.0,1.0,3.0]
           ])


xyz = n.array([[1,2,3,1],[3,4,5,1],[0,1,2,1],[4,5,6,1],[7,8,10,1],[6,5,11,1],[42,-10,50,1]])
xyz_tr= n.dot(t,xyz.T)
print xyz_tr[0:2,0]/xyz_tr[2,0]
print xyz_tr[0:2,1]/xyz_tr[2,1]

xy= xyz_tr[0:2,:]/xyz_tr[2,:]
xyz2 = n.delete(xyz,3,1)

print solve_camera(xyz2,xy.T)
