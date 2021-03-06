# ORCSolver: An Efficient Solver for Adaptive GUI Layout with OR-Constraints

Conditionally accepted by **the ACM Conference on Human Factors in Computing Systems (CHI), 2020.**

Authors: **Yue Jiang, Wolfgang Stuerzlinger, Matthias Zwicker, Christof Lutteroth**

**Paper:** http://www.cs.umd.edu/~yuejiang/papers/ORCSolver.pdf

**Video:** https://www.youtube.com/watch?v=0S77vVG8btE&feature=youtu.be

**Related Paper: ORC Layout: Adaptive GUI Layout with OR-Constraints**

**Paper:** http://www.cs.umd.edu/~yuejiang/CHI2019/paper.pdf

**Video:** https://www.youtube.com/watch?v=eiEmLTfPDZQ&feature=youtu.be

> **To get started:** 
> 
>     git clone https://github.com/YueJiang-nj/ORCSolver-CHI2020.git
>

## Prerequisite installation

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
