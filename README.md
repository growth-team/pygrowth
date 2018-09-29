PYGROWTH: python library for GROWTH 
===
This python package provides analyses softwares for  the GROWTH (Gamma-Ray Observation of Winter THundercloud) project. 
Authors: [GitHub GROWTH-Team](https://github.com/growth-team/)

### Environmental Preparation 
- The "pipenv" is recommended. 


## Class structure instance

- pygrowth
  - `__init__.py` (plot default values will be read.)
  - `eventfile.py`
    - EventFile
    - EventFileFITS
    - EventFileROOT
    - EventFileTAC(tentative)
    - ...
  - `counthistory.py`
    - CountHistoryExtractor (1-dimensional, 2-dimensional)
    - CountHistory
    - CountHistoryFileWriter... (FITS LC, ROOT Histogram, CSV, ...)
    - CountHistoryPlotter...
    - ...
  - `spectrum.py` (`energyspectrum.py`)
    - SpectrumExtractor
    - Spectrum
    - SpectrumFileWriter... (FITS PHA, ROOT Histogram, CSV, ...)
    - SpectrumFilePlotter...
    - ...
  - `gti.py` (to be discussed whether necessary)
    - GTI
    - ...
  - `calibrator.py`
    - EnergyCalibrator
    - TimingCalibrator
  
### Example of `CountrateHistory` class:

CountrateHistory
  - Member variables
    - Time-bin-edge list 
    - Count bin list
    - Good-time-interval list

CountrateHistoryFileWriter
  - Member methods
    - write(countrate_history_obj, buffer)
  - Derived classes (example)
    - CountrateHistoryFileWriterFITS
    - CountrateHistoryFileWriterCSV
    - CountrateHistoryFileWriterROOT

## GROWTH Gamma-ray Event List

The GROWTH Gamma-ray Event List contains follwoing columns.

- Event name ("TRByymmdd")
- Fiscal year (FY20XX)
- Burst type (long,short,long/short)
- Maximum time (UT)
- Maximum time (JST)
- Start time (UT)
- Start time (JST)
- Stop time (UT)
- Stop time (JST)
- Detected location
- Detectors (name list)
- Scintillators 
- Duration (sec)
- Number of Events (counts)
- Significance


## Pipeline before the PYGROWTH 
Wada will add pipeline process for GROWTH-Shimajuji board version.


## Tips for PYGROWTH developpers 
### Git Workflow

- New functionalities should be developed under a new branch. Following command lines show the default workflow.
  ```
  # Checkout the latest master
  git checkout master
  git fetch origin
  git merge origin/master
  git log -1
  
  # Create a new branch
  git checkout -b <dev_branch_name>
  
  # Show the present branch
  git branch
  
  # Add/modify code
  ...
  
  # Add the file(s) to the repo, and commit
  git add <new_file>
  git commit <new_file> -m "new_file - implemented *** function"
  
  # Repeat until the new feature is implemented, and tested.
  # For example, running python unit tests, use `tox` in the top dir.
  tox
  
  # Push the dev branch to github
  git push origin <dev_branch_name>
  
  # The pushed branch will be visible in the branches page.
  open https://github.com/growth-team/pygrowth/branches
  
  # Create pull request by clicking
  
  ```

- Retrieve the latest master (updated by someone's PR)

  ```
  git fetch origin
  git checkout master
  git pull
  
  # If new commits have been merged to master, you should see
  # them in the commit history.
  git log
  ```

- Following commands show how to change the branch name. 
    ```
    git checkout master
    git branch -m enoto/plot_lightcurve
    git push origin enoto/plot_lightcurve
    ```

- Retrieve remote branch:
    ```
    # Fetch remote repository
    git fetch origin

    # Show remote branches
    git branch -r

    # Checkout the remote branch
    git checkout <some_remote_branch>
    e.g. git checkout yuasa/tox

    # Check the commit history
    git log
    ```

- The following command line shows the diffference / history of a file.
    ```
    git log -p <filename>
    ```

- Rename/move files

  ```
  git mv <old_path> <new_path>
  git commit -a -m "moved <old_path> to <new_path>"
  ```

### Unit Test 
1. Prerequisites
    1. Make sure `git-lfs` is installed.
       ```
       # On macOS
       brew install git-lfs
       ```
    3. Make sure `tox` and `pipenv` are installed, or run `pip install tox pipenv`.
2. Clone the pygrowth repository
    ```
    git lfs clone git@github.com:growth-team/pygrowth.git
    ```
3. Install in a virtual environment.
    ```
    cd pygrowth
    pipenv install .
    pipenv shell
    pip install .
    # To exit from the pipenv shell, type exit.
    ```
3. Run test.
    ```
    cd pygrowth
    pipenv shell
    tox
    ```

### Large/binary files in LFS

Use [Git Large File System](https://git-lfs.github.com) when committing large files and/or binary files used,
for example, for unit tests.

```shell
# Track a file using the Git LFS (add as LFS-stored file)
git lfs track <path_to_file>

# Commit (Please do not forget to commit .gitattribute file as well)
git add .gitattribute <path_to_file>
git commit .gitattribute <path_to_file> -m "commit message"
```

### references for PyPI
https://docs.python.jp/3/distutils/
https://qiita.com/airtoxin/items/2eafb930fa9b54ee7149
https://qiita.com/kinpira/items/0a4e7c78fc5dd28bd695
https://qiita.com/NaotakaSaito/items/329e2a94bcc45d308a3a
https://packaging.python.org/tutorials/packaging-projects/#create-an-account