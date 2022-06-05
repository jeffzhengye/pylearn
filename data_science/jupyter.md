# jupyterlab

## install
* remove all notebook, jupyter on your computer first
* then, pip install jupyter-lab

## start
* jupyter-lab
* fix error if seen after getting started `jupyter-lab`

## install jupyter-lsp
* can be install in jupyter-lab
* pip install python-language-server[all]
* jupyter serverextension enable --user --py jupyter_lsp

## .lsp_symlink problem fix

* refer 6: 
https://github.com/jupyter-lsp/jupyterlab-lsp/blob/master/README.md 

## code folding
 go to code console settings
 
# magic commands
* ref: https://ipython.readthedocs.io/en/stable/interactive/magics.html

## change the current wording directory
* %cd

## Load code into the current frontend.
* %load

## Run a statement through the python code profiler.
* %prun

## 自动重新加载更改的模块
%load_ext autoreload
%autoreload 2

## 以latex渲染当前cell

%%latex

%run
%run [options] file [args]，相当于在terminal中执行python [options] file [args]
%system
执行shell命令，并且捕获输出
%time
%time统计单行python语句的执行时间，%%time，统计当前cell的执行时间
%%bash

在子进程中用bash执行当前cell
%%html
以HTML渲染当前cell
%%js
以javascript渲染当前cell
%%latex
以latex渲染当前cell
%%markdown
以markdown渲染当前cell
%%writefile
将当前cell的内容保存到文件
