import numpy as np
from matplotlib import pyplot as plt
import calkulate as calk

# Import D81 simulated titration with and without phosphate
(massAcid0, pH0, tempK0, massSample0, concAcid0, pSal0, alk0, concTotals0,
    eqConstants0) = calk.io.Dickson1981(withPhosphate=False)
(massAcid1, pH1, tempK1, massSample1, concAcid1, pSal1, alk1, concTotals1,
    eqConstants1) = calk.io.Dickson1981(withPhosphate=True)

# Simulate it again with Calkulate and round to the same precision as D81
pHSim0 = calk.simulate.pH(massAcid0, massSample0, concAcid0, alk0, concTotals0,
    eqConstants0)
pHSim1 = calk.simulate.pH(massAcid1, massSample1, concAcid1, alk1, concTotals1,
    eqConstants1, co2Loss=10)
pHSim0r = np.round(pHSim0, decimals=6)
pHSim1r = np.round(pHSim1, decimals=6)

# Convert simulation as if potentiometric
hSim1 = 10.0**-pHSim1r
emf0 = 660
emf = calk.solve.h2emf(hSim1, emf0, tempK1)

# Save simulation as a .dat file
volAcid = massAcid1/calk.density.acid(tempK1)*1e3
datFile = 'datfiles/Dickson1981sim.dat'
calk.io.writeDat(datFile, volAcid, emf, tempK1,
    line0='Dickson1981 re-simulation',
    line1='(with phosphate)')

# Solve the simulation
volSample = massSample1/calk.density.sw(tempK1[0], pSal1)*1e3
totalCarbonate = concTotals1['C']
totalPhosphate = concTotals1['P']
totalSilicate = concTotals1['Si']
alkSolved, emf0Solved = calk.vindta.alk(datFile, volSample, concAcid1, pSal1,
    totalCarbonate, totalPhosphate, totalSilicate)['x']
alkSolvedDir, emf0SolvedDir = calk.solve.complete(massAcid1, emf, tempK1,
    massSample1, concAcid1, concTotals1, eqConstants1)['x']

#(massAcid, emf, massSample, f1Guess, LGuess, alkGuess, emf0Guess,
#        granEmf0, alk_emf0, alkSim, alk0Sim, RMS, Npts, rgb) = calk.plot.prep(
#    datFile, volSample, pSal1, totalCarbonate, totalPhosphate, totalSilicate,
#    concAcid1)

mu = calk.solve.mu(massAcid1, massSample1)
alkSimDir = calk.simulate.alk(hSim1, mu, concTotals1, eqConstants1)[0]

fig, ax = plt.subplots()
ax.scatter(massAcid1, alkSimDir + alk1*(1 - mu) +
    massAcid1*concAcid1/(massAcid1 + massSample1))
ax.scatter(massAcid1, (alkSimDir +
    massAcid1*concAcid1/(massAcid1 + massSample1))/mu)
# Plot the titration
calk.plot.everything(datFile, volSample, pSal1, totalCarbonate, totalPhosphate,
   totalSilicate, concAcid1, concTotals=concTotals1,
   eqConstants=eqConstants1)
