# pygrowth
This python package provides analyses tools for public data from the GROWTH (Gamma-Ray Observation of Winter THundercloud) project. 

## Development

1. Prerequisites
    1. Make sure `git-lfs` is installed.
    2. Make sure `tox` and `pipenv` are installed, or run `pip install tox pipenv`.
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

Use Git Large File System when committing large files and/or binary files used,
for example, for unit tests.

```shell
# Track a file using the Git LFS (add as LFS-stored file)
git lfs track <path_to_file>

# Commit (Please do not forget to commit .gitattribute file as well)
git add .gitattribute <path_to_file>
git commit .gitattribute <path_to_file> -m "commit message"
```

<!--
references for PyPI
https://docs.python.jp/3/distutils/
https://qiita.com/airtoxin/items/2eafb930fa9b54ee7149
https://qiita.com/kinpira/items/0a4e7c78fc5dd28bd695
https://qiita.com/NaotakaSaito/items/329e2a94bcc45d308a3a
https://packaging.python.org/tutorials/packaging-projects/#create-an-account
-->
