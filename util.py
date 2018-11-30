import os, sys
import numpy as np
import pathlib

def env():
    return ('/').join(os.path.abspath(__file__).split('/')[:-1])

def inverse(T):
    R, t = decompose(T)
    invT = np.zeros((4, 4))
    invT[:3, :3] = R.T
    invT[:3, 3] = -R.T.dot(t)
    invT[3, 3] = 1
    return invT

def pack(R, t):
    T = np.zeros((4, 4))
    T[:3, :3] = R
    T[:3, 3] = t
    T[3, 3] = 1.0
    return T

def decompose(T):
    R = T[:3, :3]
    t = T[:3, 3]
    return R, t

"""
    Find a matrix Q \in O(n) such that \|A Q - B\|_F is minimized
    equivalent to maximize trace of (Q^T A^T B)
"""
def project(A, B):
    X = A.T.dot(B)
    U, S, VT = np.linalg.svd(X)
    Q = U.dot(VT)
    return Q

"""
    Find a matrix Q \in SO(n) such that \|Q - X\|_F is minimized
    equivalent to project(I, X)
"""
def project_so(X):
    d = X.shape[0]
    assert X.shape[1] == d
    Q = project(np.eye(d), X)
    Q = Q * np.linalg.det(Q)
    return Q

def make_dirs(path):
    dump_folder = os.path.dirname(path)
    pathlib.Path(dump_folder).mkdir(exist_ok=True, parents=True)

def angular_distance_np(R_hat, R):
    # measure the angular distance between two rotation matrice
    # R1,R2: [n, 3, 3]
    #print('hey')
    n = R.shape[0]
    trace_idx = [0,4,8]
    det = np.linalg.det(R_hat)
    det2 = np.linalg.det(R)
    assert (det > 0).all()
    assert (det2 > 0).all()
    trace = np.matmul(R_hat, R.transpose(0,2,1)).reshape(n,-1)[:,trace_idx].sum(1)
    metric = np.arccos(((trace - 1)/2).clip(-1,1)) / np.pi * 180.0
    return metric

def list_scenes(dataset):
    home = env()
    return os.listdir('%s/processed_dataset/%s/' % (home, dataset))
    

if __name__ == '__main__':
    print('home dir = %s' % env())
    

