# -*- coding: utf-8 -*-
"""
Created on Sat May 20 23:35:23 2017

@author: gmini
"""

import pandas
import numpy as np
import cvxopt
import cvxopt.solvers

etfs = pandas.read_csv("~/Dropbox/etfs_rate_example.csv")

avg_rr = etfs.mean().as_matrix()
N = avg_rr.shape[0]
cov_rr = etfs.cov().as_matrix()

P = np.nan_to_num(cov_rr)
p = - avg_rr
p = p[:, np.newaxis]
G = -np.identity(N)
h = np.zeros([N,1])
A = np.ones([1,N])
b = 1.0;

print P.shape
print p.shape
print G.shape
print h.shape
print A.shape

G = cvxopt.matrix(0.0, (N,N))
G[::N+1] = -1.0
h = cvxopt.matrix(0.0, (N,1))
A = cvxopt.matrix(1.0, (1,N))
b = cvxopt.matrix(1.0)

cvxopt.solvers.options['show_progress'] = False
result = cvxopt.solvers.qp(cvxopt.matrix(P), cvxopt.matrix(p), G, h, A, b)
