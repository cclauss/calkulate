# Calkulate: seawater total alkalinity from titration data.
# Copyright (C) 2019-2020  Matthew Paul Humphreys  (GNU GPLv3)
"""Estimate total concentrations from practical salinity."""
import PyCO2SYS as pyco2


def concTotals(
    pSal,
    totalCarbonate=0,
    totalPhosphate=0,
    totalSilicate=0,
    totalAmmonia=0,
    totalH2Sulfide=0,
    WhichKs=10,
    WhoseTB=2,
):
    """Assemble a dict of sample concentrations in mol/kg-sw using PyCO2SYS."""
    inputs = pyco2.engine.condition(
        {"SAL": pSal, "WhichKs": WhichKs, "WhoseTB": WhoseTB,}
    )[0]
    salts = pyco2.salts.assemble(**inputs)
    return {
        "C": totalCarbonate,
        "B": salts["TB"][0],
        "S": salts["TSO4"][0],
        "F": salts["TF"][0],
        "P": totalPhosphate,
        "Si": totalSilicate,
        "NH3": totalAmmonia,
        "H2S": totalH2Sulfide,
    }
