#!/usr/bin/env python3
from math import exp, floor, log


def extinction_probability(lam: float) -> float:
    if lam <= 1.0:
        return 1.0
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        residual = mid - exp(-lam * (1.0 - mid))
        if residual > 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def attack_bound(lam: float, s0: float, F: float) -> float:
    return extinction_probability(lam) ** (s0 / F)


def verdict_counts(N: int):
    K = floor(2*N/3) + 1
    W = floor(N/3)
    return K, W, K-W


def required_s0(N: int, nu: float, gamma: float, F: float) -> float:
    eps = nu / (N + nu)
    lam = (1-gamma)*F
    q = extinction_probability(lam)
    return F * log(eps) / log(q)


if __name__ == '__main__':
    N=1023
    K,W,WN = verdict_counts(N)
    print('verdict counts', N, K, W, WN, 'max positives for bad', N-K)

    print('\nF tradeoff')
    for F in [2.0,2.0794,2.08,2.5,2.9]:
        fc13=1-1/((1-1/3)*F)
        fc02=1-1/(0.8*F)
        sf=30/(1-0.3*F)
        p=attack_bound((2/3)*F,30,F)
        print(F, fc13, fc02, sf, p)
    p2=attack_bound((2/3)*2,30,2)
    p208=attack_bound((2/3)*2.0794,30,2.0794)
    print('F=2 / F=2.0794 bound ratio', p2/p208)

    print('\nsampling dilution exact-count baseline')
    N0=1023; A=205; B=164; C=N0-A-B
    for add in [0,100,200,400]:
        N=N0+add
        lam=2*C/N
        fixed30=attack_bound(lam,30,2)
        s0_fixed_cores=10*N/341
        fixedcores=attack_bound(lam,s0_fixed_cores,2)
        print(add,N,A,B+add,C,lam,fixed30,s0_fixed_cores,fixedcores)

    print('\nrequired initial sample')
    for N in [1023,3000,6000]:
        print(N, required_s0(N,.05,1/3,2), 30, 10*N/341)

    print('\ncore opportunity at r=.2')
    r=.2
    prob=3*r*r*(1-r)+r**3
    print(prob,341*prob)
