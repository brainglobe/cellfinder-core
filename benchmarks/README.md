# Benchmarking with asv
[Install asv](https://asv.readthedocs.io/en/stable/installing.html) by running:
```
pip install asv
```

`asv` works roughly as follows:
1. It creates a virtual environment (as defined in the config)
2. It installs the software package version of a specific commit (or of a local commit)
3. It times the benchmarking tests and saves the results to json files
4. The json files are 'published' into an html dir
5. The html dir can be visualised in a static website

## Running benchmarks
To run benchmarks on a specific commit:
```
$ asv run 88fbbc33^!
```

To run them up to a specific commit:
```
$ asv run 88fbbc33
```

To run them on a range of commits:
```
$ asv run 827f322b..729abcf3
```

To collate the benchmarks' results into a viewable website:
```
$ asv publish
```
This will create a tree of files in the `html` directory, but this cannot be viewed directly from the local filesystem, so we need to put them in a static site. `asv publish` also detects satistically significant decreases of performance, the results can be inspected in the 'Regression' tab of the static site (more on that on the next section).

To visualise the results in a static site:
```
$ asv preview
```
To share the website on the internet, put the files in the `html` directory on any webserver that can serve static content (e.g. GitHub pages).

To put the results in the `gh-pages` branch and push them to GitHub:
```
$asv gh-pages
```

## Managing the results

To remove benchmarks from the database, for example, for a specific commit:

```
$ asv rm commit_hash=a802047be
```
See more options in the [documentation](https://asv.readthedocs.io/en/stable/using.html#managing-the-results-database).

This will remove the selected results from the files in the `results` directory. To update the results in the static site, remember to run `publish` again!


To compare the results of running the benchmarks on two commits:
```
$ asv compare 88fbbc33 827f322b
```

## Automatically detecting performance regressions



## Other handy commands
To update the machine information
```
$ asv machine
```

To display results from previous runs on the command line
```
$ asv show
```

To use binary search to find a commit within the benchmarked range that produced a large regression
```
$ asv find
```

To check the validity of written benchmarks
```
$ asv check
```


## Development notes:
In development, the following flags to `asv run` are often useful:
- `--bench`: to specify a subset of benchmarks (e.g., `tools.prep.PrepTF`). Regexp can be used.
- `--dry-run`: will not write results to disk
- `--quick`: will only run one repetition, and no results to disk
- `--show-stderr`: will print out stderr
- `--verbose`: provides further info on intermediate steps
- `--python=same`: runs the benchmarks in the same environment that `asv` was launched from

E.g.:
```
asv run --bench bench tools.prep.PrepTF --dry-run --show-stderr --quick
```

### Running benchmarks against a local commit
To run the benchmarks against a local commit (for example, if you are trying to improve the performance of the code), you need to edit the `repo` field in the asv config file `asv.conf.json`.

To use the upstream repository, use:
```
"repo": "https://github.com/brainglobe/cellfinder-core.git",
```

To use the local repository, use:
```
"repo": "..",
```

### setup and setup_cache

- `setup` includes initialisation bits that should not be included
in the timing of the benchmark. It can be added as:
    - a method of a class, or
    - an attribute of a free function, or
    - a module-level setup function (run for every benchmark in the
    module, prior to any function-specific setup)

    If `setup` raises `NotImplementedError`, the benchmark is skipped

- `setup_cache` only performs the setup calculation once
(for each benchmark and each repeat) and caches the
result to disk. This may be useful if the setup is computationally
expensive.

    A separate cache is used for each environment and each commit. The cache is thrown out between benchmark runs.

    There are two options to persist the data for the benchmarks:
    - `setup_cache` returns a data structure, which asv pickles to disk,
        and then loads and passes as the first argument to each benchmark (not
        automagically though), or
    - `setup_cache` saves files to the cwd (which is a temp dir managed by
        asv), which are then explicitly loaded in each benchmark. The recommended practice is to actually read the data in a `setup` function, so that loading time is not part of the benchmark timing.



----
## References
- [astropy-benchmarks repository](https://github.com/astropy/astropy-benchmarks/tree/main)
- [numpy benchmarks](https://github.com/numpy/numpy/tree/main/benchmarks/benchmarks)
- [asv documentation](https://asv.readthedocs.io/en/stable/index.html)
