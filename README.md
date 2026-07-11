# ORCSolver: An Efficient Solver for Adaptive GUI Layout with OR-Constraints

## publications

### ORCSolver: An Efficient Solver for Adaptive GUI Layout with OR-Constraints

[Yue Jiang](https://yuejiang-nj.github.io/) ·
[Wolfgang Stuerzlinger](https://www.sfu.ca/siat/people/research-faculty/wolfgang-stuerzlinger.html) ·
[Matthias Zwicker](https://www.cs.umd.edu/~zwicker/) ·
[Christof Lutteroth](https://people.bath.ac.uk/cl2073/)

ACM CHI Conference on Human Factors in Computing Systems, 2020

[Paper](https://yuejiang-nj.github.io/Publications/2020CHI_ORCSolver/paper.pdf) ·
[Video](https://www.youtube.com/watch?v=5SAZ8iDKFhc) ·
[BibTeX](citations/orcsolver.bib)

### ORC Layout: Adaptive GUI Layout with OR-Constraints

[Yue Jiang](https://yuejiang-nj.github.io/) ·
[Ruofei Du](https://ruofeidu.com/) ·
[Christof Lutteroth](https://people.bath.ac.uk/cl2073/) ·
[Wolfgang Stuerzlinger](https://www.sfu.ca/siat/people/research-faculty/wolfgang-stuerzlinger.html)

ACM CHI Conference on Human Factors in Computing Systems, 2019

[Paper](https://yuejiang-nj.github.io/Publications/2019CHI_ORCLayout/paper.pdf) ·
[Video](https://www.youtube.com/watch?v=eiEmLTfPDZQ) ·
[BibTeX](citations/orc-layout.bib)

## Related Publication

### ReverseORC: Reverse Engineering of Resizable User Interface Layouts with OR-Constraints

[Yue Jiang](https://yuejiang-nj.github.io/) ·
[Wolfgang Stuerzlinger](https://www.sfu.ca/siat/people/research-faculty/wolfgang-stuerzlinger.html) ·
[Christof Lutteroth](https://people.bath.ac.uk/cl2073/)

ACM CHI Conference on Human Factors in Computing Systems, 2021

[Paper](https://yuejiang-nj.github.io/Publications/2021CHI_ReverseORC/paper.pdf) ·
[Video](https://www.youtube.com/watch?v=uBVRtUvLFSk) ·
[BibTeX](citations/reverseorc.bib)
[Code](https://github.com/YueJiang-nj/ReverseORC-CHI2021)


## Prerequisite installation

> **To get started:** 
> 
>     git clone https://github.com/YueJiang-nj/ORCSolver-CHI2020.git
>

    1. Python3 
    2. Tkinter (GUI package)
    3. CVXPY (a Python-embedded language for convex optimization problems)
    4. Microsoft Z3 Solver [Optional] (only needed for running Z3 version)

## Layout

The project has the following file layout:

    README.md
    API_ORCSolver.pdf
    Code/
      ORCSolver (Ours)/
      PureBranch&Bound/
      PureZ3/
      QPforFlows/
      images/

The **API_ORCSolver.pdf** includes the API of ORCSolver which can be used to specify layouts. Our API allows us to plug in different solvers for different ORC patterns (including **ORCSolver(Ours)**, **QP for Flows**, and **Pure Branch & Bound**). 

The **Code** folder contains all the source code for all the four methods as mentioned in the paper (**ORCSolver(Ours)**, **Pure Z3**, **QP for Flows**, **Pure Branch & Bound**). We also provide sample code for some layout patterns and the code generating examples in our teaser and video. 
