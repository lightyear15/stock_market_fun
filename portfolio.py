# -*- coding: utf-8 -*-
"""
Created on Sat May 20 23:35:23 2017

@author: gmini
"""
from stock import *
import pandas
import numpy as np
import cvxopt
import cvxopt.solvers

N = 10


def print_portfolio_on_time(rr_matrix, weights):

    for el in weights:


stock_name_list = get_stocks_with_biggest_dataset(N)
stocks = get_stock_data (stock_name_list, datetime.datetime(2016,1,1), datetime.datetime(2016,12,23))

rr = get_rr_from_stock_list(stocks)
avg_rr = rr.mean().as_matrix()

cov_rr = rr.cov().as_matrix()
P = cov_rr
p = - avg_rr
p = p[:, np.newaxis]
G = cvxopt.matrix(0.0, (N,N))
G[::N+1] = -1.0
h = cvxopt.matrix(0.0, (N,1))
A = cvxopt.matrix(1.0, (1,N))
b = cvxopt.matrix(1.0)

result = cvxopt.solvers.qp(cvxopt.matrix(P), cvxopt.matrix(p), G, h, A, b)

print type(result["x"])

