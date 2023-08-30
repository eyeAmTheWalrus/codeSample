#!/bin/bash
mydir=$(basename "$PWD")

#sets delimiter as '-' for splitting directory name
IFS='-'   
read -a strarr <<< "$mydir"
as=${strarr[0]}
bs=${strarr[1]}

#strip 'a' and 'b' from '0.94a' , '1.03b'
a=${as::-1} 
b=${bs::-1}

#lattice vector norms in absence of strain
x=4.20654853871661 
y=3.62810917188305
ax=$(expr $a*$x | bc) 
bx=$(expr $b*$x | bc)
ay=$(expr $a*$y | bc)
by=$(expr $b*$y | bc)

#POSCAR is a plain-text input file for VASP software, containing lattice vectors + atom positions
#we overwrite it with our newly computed values
cp ../POSCAR.original .   
sed "3s/.*/    $ax     -$ay   0.000000000000000/" POSCAR.original > POSCAR.a 
sed "4s/.*/    $bx     $by   0.000000000000000/" POSCAR.a > POSCAR.b
sed '5s/.*/    0.0000000000000000     0.0000000000000000   5.6206616627868291/' POSCAR.b > POSCAR
rm POSCAR.a POSCAR.b
cp POSCAR POSCAR.original

#phonopy package enforces group symmetries on atom positions + lattice vectors to arbitrary tolerance
~/anaconda3/bin/phonopy --tolerance 0.000001 --symmetry -c POSCAR > outpos0.000001
pos2aBR #writes to canonical form, will alter POSCAR iff strain profile asymmetric about y=x
cp POSCAR_std POSCAR

#starts self-consistent field calculations within density functional theory, within VASP package
sbatch reg.sh & 
wait
cd nonscf
cp ../POSCAR .
cp ../CHGCAR .
sbatch reg.sh & # non self consistent field DFT
wait
mkdir irvsp
cp OUTCAR WAVECAR irvsp
cd irvsp

#determines Z4 invariant from wavefunctions computed in nonscf
irvsp -sg 11 -nb 1 36 > out.ir & 
echo ALLDONE
