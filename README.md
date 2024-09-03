## QUESTION
When you have to design a standard cell libray, you need to choose a number of combinatorial cells.
You can simply ask a friend and start from an existing list or build your own from scratch.
But how? More specifically, how many n-input Boolean functions are there?

This latter question connects to the mathematical concept of group action that is a pivotal part of Algebra.
If you like Rubyk's cube, you should not feel too uncomfortable.

It can be reformulated in this context as follows.
What are the orbits in the action of the symmetric group $S_n$ on the set of n-input Boolean functions $X_n=B^{B^n}$?

## DESCRIPTION
The name of this package is **group_action**.
The version of this package is **0.1.7**.
It contains a library module named **library** and an application named **orbits**.

It computes the orbits in the action of the symmetric group $S_n$ on the set of n-input Boolean functions $X_n=B^{B^n}$.

The result is basically a list of signatures that is presented in 2 formats and 2 levels of details.
Here, a **signature** is a non negative integer representing a Boolean function.

For instance, what 2-input Boolean function does 12 represent?
I use Big Endian format for binary words.
12 = 0101
This gives the following truth table
```
x0 x1 f(x0, x1)
0  0  0
1  0  1
0  1  0
1  1  1
```
and the following expression
f(x0, x1) = x0 & ~x1 | x0 & x1 = x0

Note: x1 does not figure in this expression.

So 12 represents a 1-input Boolean function.
It gives a standard cell called **buffer**.

To move forward, is 12 the only signature representing a buffer cell?
Actually this answer is no!
If you permut x0 and x1, you get the following truth table.
```
x0 x1 f(x0, x1)
0  0  0
1  0  0
0  1  1
1  1  1
```
It corresponds to f(x0, x1) = ~x0 & x1 | x0 & x1 = x1, another instance of the buffer cell.

This is what the group action concept is all about, and behyond :-)

## HOW DOES IT WORK?
Each permutation of $S_n$ is applied to each n-input Boolean function f of $X_n$, computing a new n-input Boolean function g.
These computations are gathered into chunks and run in parallel on a number of cores.

Each pair $\lbrace f, g \rbrace$ forms an edge of a graph that is latter analyzed.
The orbits we are looking for are the connected parts of the obtained graph.

From this analysis, one can get the number of orbits, a list of representatives, and the detailed contents of each orbit.
Boolean functions are represented by their signatures as non negative integers.

The results are printed out to the screen or stored into a json file named **data.json**.
Binary data is considered as Big Endian throughout the code.

## INSTALL
Run ```pip install group_action```.
This application orbits is installed automatically.
You are ready to go :-)

## USAGE
```
orbits [-h] [--n N] [--c C] [--r] [--v] [--j]

Brut force computation of orbits of n-input 1-output Boolean functions under the action of the symmetric group Sn.

options:
  -h, --help  show this help message and exit
  --n N       Number of inputs
  --c C       Number of cores
  --v         Output every element of each orbit
  --j         Output data.json file
```

## EXAMPLE
After installation, run ```orbits --n 3 --c 12``` in order to run on 12 cores and to get the number of orbits and a representative of each orbit as an integer signature for 3-input, 1-output Boolean functions.

## TEST
```
n=0      2 orbits
n=1      4 orbits
n=2     12 orbits
n=3     80 orbits
n=4  3 984 orbits
```
## KNOWN BUGS AND LIMITATIONS
1. The $n=5$ step requires a lot of memory. Let me know if you go through :-)
2. The group action is concrete and set up to $G=S_n$ and $X=B^{B^n}$ in this version.
3. The default number of cores could be set up automatically.
4. The packaging is managed through PyPI, not yet synchronized to GitHub.
5. The documentation for the library has not been generated yet.

## FEEDBACK
Any comment and/or improvement whether on optimization, packaging, documentation, or on any other appropriate topic is welcome :-)

## CONTACT
You can reach me antoine AT sirianni DOT ai.

## DOCUMENTATION
Check OR Conf 2024 paper titled "Open Source Standard Cell Library Design" by Antoine Sirianni once published.

