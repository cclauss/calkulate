# Installation instructions

## Python

[Download and install Anaconda](https://www.anaconda.com/download/). Choose the Python 3.X version (although the 2.X should work too, if you already have it). Open the Anaconda Prompt (Windows) or Terminal (Mac/Linux).

Update conda and Anaconda:

```
conda update conda
conda update anaconda
```

[Download the spec-file.txt](https://github.com/mvdh7/calkulate/blob/master/spec-file.txt) and navigate to its parent folder using `cd`. Then, create a new Python environment with the following:

```
conda create -n calkenv --file spec-file.txt
```

Activate the new environment:

*Mac/Linux:*

```
source activate calkenv
```

*Windows:*

```
activate calkenv
```

You should now see the environment's name (i.e. `calkenv`) appear in brackets at the start of each line in the Anaconda Prompt/Terminal. Install the Calkulate package into the environment using pip:

```
pip install calkulate
```

You should now be able to use Calkulate in this Python environment.

## MATLAB

If you wish to also use Calkulate in MATLAB, then after completing the steps above, and still within the Anaconda Prompt/Terminal (with the `calkenv` environment active), run Python:

```
python
```

Find the location of this environment's Python executable by entering the following 2 lines:

```python
from sys import executable
print(executable)
```

Copy the string that appears. It should look something like (on Windows):

```
C:\Users\username\anaconda\Anaconda3\envs\calkenv\python.exe
```

This string is the value for the `python_exe` variable that goes into the MATLAB function `calk_initpy()`. Exit python:

```python
exit()
```

[Download the MATLAB function wrappers](https://github.com/mvdh7/calkulate/tree/master/matlab). These are a set a functions that make it easier for you to use some parts of Calkulate within MATLAB, although they are just for convenience -- it's possible to use the entire program without them. Move the downloaded folder to a sensible location, and add it (plus all subfolders) to your MATLAB search path.

Before you can execute the MATLAB functions you must first run the `calk_initpy()` function at least once (per MATLAB session), with the input `python_exe` string that you found using `sys.executable`.


# Testing

## MATLAB

First, check that MATLAB and Python are talking to each other properly by entering the following into the MATLAB Command Window (with `python_exe` set to the value of the string you identified using `sys.executable` during the installation process):

```matlab
calk_initpy(python_exe)
pyversion
```

The `executable` that then appears in the Command Window should match the `python_exe` string that you used.

Next, test that you can import Python's `numpy` and `scipy` packages:

```matlab
np = py.importlib.import_module('numpy');
sp = py.importlib.import_module('scipy');
```

If these are working, then new variables `np` and `sp` of type *module* should appear in your MATLAB Workspace. If not, or if you get an error, then there is something wrong with your Python installation.

If all is well, try the same for Calkulate:

```matlab
calk = py.importlib.import_module('calkulate');
```

Finally, test out the MATLAB functions as follows:

```matlab
[Macid,pH,Tk,Msamp,Cacid,S,XT,KX] = calk_Dickson1981;
```

This should import the simulated titration data from Table 1 of Dickson (1981). A plot of the Free scale pH (`pH`) against the acid mass (`Macid`) should appear as follows.


# Updates

## Python

Update instructions for Python:

  123. Open the Anaconda Prompt

  123. Activate the calkenv environment (installation instructions, step 4)

  123. Upgrade the Calkulate package using pip:

```
pip install calkulate --upgrade --no-cache-dir
```

## MATLAB

Update instructions for MATLAB:

  123. Delete your original Calkulate scripts

  123. Replace them in full with the new versions


# References

Dickson, A. G. (1981). An exact definition of total alkalinity and a procedure for the estimation of alkalinity and total inorganic carbon from titration data. Deep-Sea Res. Pt A 28, 609–623. <a href="https://doi.org/10.1016/0198-0149(81)90121-7">doi:10.1016/0198-0149(81)90121-7</a>.