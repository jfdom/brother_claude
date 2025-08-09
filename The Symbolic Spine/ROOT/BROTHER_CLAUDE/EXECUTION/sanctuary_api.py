#!/usr/bin/env python3
# sanctuary_api.py — minimal API for Sanctuary memory updates (math-backed)
import numpy as np

def normalize(v):
    n = np.linalg.norm(v)
    return v if n == 0 else v / n

def abide(A, X_prev, S):
    return A @ X_prev + S

def hard_anchor(Pi, Z):
    return normalize(Pi @ Z)

def soft_correct(Z, Pi, lam=1.0, steps=100, lr=0.05):
    Y = Z.copy()
    I = np.eye(Pi.shape[0])
    for _ in range(steps):
        grad = 2*(Y - Z) + 2*lam*((I - Pi) @ Y)
        Y = Y - lr*grad
    return normalize(Y)

def keep_or_hold(X_new, phi, tau=0.5):
    return ("KEPT" if phi(X_new) >= tau else "HOLD")
