# jupyterlab

## install

- remove all notebook, jupyter on your computer first
- then, pip install jupyter-lab

## start

- jupyter-lab
- fix error if seen after getting started `jupyter-lab`

## install jupyter-lsp

- can be install in jupyter-lab
- pip install python-language-server[all]
- jupyter serverextension enable --user --py jupyter_lsp

## .lsp_symlink problem fix

- refer 6:
  https://github.com/jupyter-lsp/jupyterlab-lsp/blob/master/README.md

## code folding

go to code console settings

# magic commands

- ref: https://ipython.readthedocs.io/en/stable/interactive/magics.html

## change the current wording directory

- %cd

## Load code into the current frontend

- %load

## Run a statement through the python code profiler

- %prun

## 自动重新加载更改的模块

%load_ext autoreload
%autoreload 2

## 以 latex 渲染当前 cell

%%latex

%run
%run [options] file [args]，相当于在 terminal 中执行 python [options] file [args]
%system
执行 shell 命令，并且捕获输出
%time
%time 统计单行 python 语句的执行时间，%%time，统计当前 cell 的执行时间
%%bash

在子进程中用 bash 执行当前 cell
%%html
以 HTML 渲染当前 cell
%%js
以 javascript 渲染当前 cell
%%latex
以 latex 渲染当前 cell
%%markdown
以 markdown 渲染当前 cell
%%writefile
将当前 cell 的内容保存到文件

# jupyter notebook

## display

* 