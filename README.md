# codeSample
This code, taken from my thesis this past year, produces a phase diagram depicting how within the material we studied, different 
strain profiles can induce transitions between distinct values of the "Z<sub>4</sub>" invariant for topological insulators.

First we obtain a sufficient amount of data points to construct a phase diagram, as seen below. 

![image](https://github.com/iAmTheWalrusOperator/codeSample/assets/123112044/7bafdc0f-fc88-4efc-b884-47df1a310fd3)


We roughly apply a binary search to identify the critical points in the diagram, where our search space is reduced by half because of the material's crystalline mirror symmetry.
The bash script jobScript.sh greatly expedites this search. A copy of it resides in the directory "_template_" as below.

Supposing the next strain profile we'd like to calculate is (a=0.975*a<sub>0</sub> , b=1.04*b<sub>0,</sub>) then we simply copy the template directory:

cp -r template 0.975a-1.04b

<img width="937" alt="image" src="https://github.com/iAmTheWalrusOperator/codeSample/assets/123112044/c670da50-0874-4e1c-a1bc-315f129e3c8e">

When jobScript.sh is executed within this new directory, it reads the strain profile from the working directory's name.
It then prompts a series of jobs (within the VASP and irvsp software packages) which obtain the Z4 invariant for this strain.

We store this data in a csv file, which is read into Python via Pandas.

Then we use NumPy to fit polynomial curves about these critical points.

Lastly using Matplotlib we output a plot of the raw data (depicted above) and fill the area between curves with different colors, as below.
It is also possible to modify the _shade_ variable so that each fill color is translucent, revealing the raw data points underneath. 

![image](https://github.com/iAmTheWalrusOperator/codeSample/assets/123112044/3b8cd713-7817-441f-ba69-7802fc04b3ca)

