# Calkulate: seawater total alkalinity from titration data
# Copyright (C) 2019  Matthew Paul Humphreys  (GNU GPLv3)

from scipy.optimize import least_squares as olsq
from numpy import full_like, nan

def AT(H, mu, XT, KXF):
    """Simulate total alkalinity from known pH and total concentrations."""
    OH = KXF['w'] / H
    if 'C' in XT.keys():
        CO2aq = mu * XT['C'] / (1 + KXF['C1']/H + KXF['C1']*KXF['C2']/H**2)
        bicarb = KXF['C1'] * CO2aq / H
        carb = KXF['C2'] * bicarb / H
    else:
        CO2aq = bicarb = carb = 0
    if 'B' in XT.keys():
        B4 = mu * XT['B']*KXF['B'] / (H + KXF['B'])
    else:
        B4 = 0
    if 'S' in XT.keys():
        HSO4 = mu * XT['S']*H / (KXF['S'] + H)
    else:
        HSO4 = 0
    if 'F' in XT.keys():
        HF = mu * XT['F']*H / (KXF['F'] + H)
    else:
        HF = 0
    if 'P' in XT.keys():
        P0 = mu * XT['P'] / (1 + KXF['P1']/H + KXF['P1']*KXF['P2']/H**2
            + KXF['P1']*KXF['P2']*KXF['P3']/H**3)
        P2 = mu * XT['P'] / (H**2/(KXF['P1']*KXF['P2']) + H/KXF['P2'] + 1
            + KXF['P3']/H)
        P3 = mu * XT['P'] / (H**3/(KXF['P1']*KXF['P2']*KXF['P3'])
            + H**2/(KXF['P2']*KXF['P3']) + H/KXF['P3'] + 1)
    else:
        P0 = P2 = P3 = 0
    if 'Si' in XT.keys():
        SiOOH3 = mu * XT['Si']*KXF['Si'] / (H + KXF['Si'])
    else:
        SiOOH3 = 0
    AT = bicarb + 2*carb + B4 + OH - H - HSO4 - HF - P0 + P2 + 2*P3 + SiOOH3
    return AT, [bicarb, 2*carb, B4, OH, -H, -HSO4, -HF, -P0, P2, 2*P3, SiOOH3]

def pH(Macid, Msamp, Cacid, AT0, XT, KXF):
    """Simulate pH from known total alkalinity and total concentrations."""
    pH = full_like(Macid, nan)
    mu = Msamp/(Msamp + Macid)
    for i, Macid_i in enumerate(Macid):
        pH[i] = olsq(lambda pH: \
            AT(10.0**-pH, mu[i], XT, KXF)[0] - mu[i]*AT0 + \
                Macid_i*Cacid/(Macid_i + Msamp),
            8.0, method='lm')['x']
    return pH
