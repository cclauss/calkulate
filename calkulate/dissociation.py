# Calkulate: seawater total alkalinity from titration data
# Copyright (C) 2019-2020  Matthew Paul Humphreys  (GNU GPLv3)
"""Evaluate stoichiometric equilibrium constants."""
import PyCO2SYS as pyco2

def eqConstants(tempK, pSal, concTotals, WhichKs=10, WhoseKSO4=1, WhoseKF=1):
    """Assemble a dict of dissociation constants on the Free pH scale.
    Use PyCO2SYS functions.
    """
    eqConstants = {} # for Free scale dissociation constants
    inputs = pyco2.engine.condition({
        'TempC': tempK - 273.15,
        'Pdbar': 0,
        'pHScale': 3,
        'WhichKs': WhichKs,
        'WhoseKSO4': WhoseKSO4,
        'WhoseKF': WhoseKF,
        'TP': concTotals['P'],
        'TSi': concTotals['Si'],
        'SAL': pSal,
        'TF': concTotals['F'],
        'TS': concTotals['S'],
        })[0]
    (_, eqConstants['C1'], eqConstants['C2'], eqConstants['w'],
            eqConstants['B'], eqConstants['F'], eqConstants['S'],
            eqConstants['P1'], eqConstants['P2'], eqConstants['P3'],
            eqConstants['Si'], eqConstants['NH3'], eqConstants['H2S'], _) = \
        pyco2.equilibria.assemble(**inputs)
    return eqConstants
