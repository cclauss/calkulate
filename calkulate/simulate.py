# Calkulate: seawater total alkalinity from titration data
# Copyright (C) 2019  Matthew Paul Humphreys  (GNU GPLv3)

from scipy.optimize import least_squares as olsq
from numpy import full_like, inf, nan

def AT(H, mu, XT, KC1, KC2, KB, Kw, KHSO4, KHF, KP1, KP2, KP3, KSi):
    """Simulate total alkalinity from known pH and total concentrations."""
    CO2aq = mu * XT['C'] / (1 + KC1/H + KC1*KC2/H**2)
    bicarb = KC1 * CO2aq / H
    carb = KC2 * bicarb / H
    B4 = mu * XT['B']*KB / (H + KB)
    OH = Kw / H
    HSO4 = mu * XT['S']*H / (KHSO4 + H)
    HF = mu * XT['F']*H / (KHF + H)
    P0 = mu * XT['P'] / (1 + KP1/H + KP1*KP2/H**2 + KP1*KP2*KP3/H**3)
    P2 = mu * XT['P'] / (H**2/(KP1*KP2) + H/KP2 + 1 + KP3/H)
    P3 = mu * XT['P'] / (H**3/(KP1*KP2*KP3) + H**2/(KP2*KP3) + H/KP3 + 1)
    SiOOH3 = mu * XT['Si']*KSi / (H + KSi)
    AT = bicarb + 2*carb + B4 + OH - H - HSO4 - HF - P0 + P2 + 2*P3 + SiOOH3
    return AT, [bicarb, 2*carb, B4, OH, -H, -HSO4, -HF, -P0, P2, 2*P3, SiOOH3]

def H(Macid, Msamp, Cacid, AT, XT, KX):
    """Simulate pH from known total alkalinity and total concentrations."""
    H = full_like(Macid, nan)
    mu = Msamp / (Msamp + Macid)
    for i, Macid_i in enumerate(Macid):
        H[i] = olsq(lambda H: \
            AT(H, mu[i], XT, *KX)[0] - mu[i]*AT + \
                Macid_i*Cacid/(Macid_i + Msamp),
            1e-8, method='trf', bounds=(1e-15, inf))['x']
    return H