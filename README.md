# Xiaoverse Monorepo

This repository is a collection of small experiments and examples written in Go and Python.  Most tasks are run via the `./m` wrapper which delegates to Bazel.

Below is a short summary of the major directories.

## [go_tutorial](./go_tutorial)
Example Go programs following the official Go tutorial.  Contains packages such as `greetings` and small command line utilities (e.g. API server using Gin).

## [helloworld](./helloworld)
Minimal "hello world" programs in Go and Python.

## [ho](./ho)
Experiments with other frameworks.

## [leetcode](./leetcode)
Solutions to various LeetCode problems implemented in Go and Python.  Each problem is kept in its own subdirectory and often includes tests.

## [llm_from_scratch](./llm_from_scratch)
Notebooks and helper files for following along with the "LLM from scratch" series.  Subdirectories `c2` through `c5` contain the chapters and related notebooks.

## [recommender](./recommender)
Notebook experimenting with graph neural networks for a recommender system (`gnn/gnn.ipynb`).

## [sysdesign](./sysdesign)
System design experiments.  Currently contains a small FastAPI application that streams video files with HTTP range requests.


