# Yeast Colony PCR protocol

# Materials Need:

 - Lyticase (from Sigma)
 - TE 
 - PCR buffers, primers, polymerase, etc.

# Procedure:

The basic idea is breaking the cells with lyticase and heat, then doing PCR.

  1. Dilute stock of lyticase to 50 U/mL in TE.
  2. Aliquot lyticase in 50uL quantities
  3. Pick colonies (I use a pipette tip) and add to lyticase aliquots, pipette up and down or agitate to break up colony
  4. Incubate at 37°C for 30 min
  5. Incubate at 95°C for 10 min
  6. Use as a template for PCR - e.g., 5uL of the cells for a 50uL PCR reaction or 2uL of the cells for a 20uL PCR reaction 


Prior to the experiment, each colony should be manually resuspended in 50 uL H20 by a user; do it in a 96-well plate. Then, the robot would add 5 uL of lyticase (need to calculate the concentration of stock that the user should bring so that the final concentration of lyticase is 2.5U per 55 uL of the cell suspension). Next, the robot can pipette this volume (55 uL) up and down 2-3 times in each well. Steps 4 and 5 involve incubations at different temperatures (see above). Finally, 2 uL / 5 uL (for 20 uL or 50 uL PCR reaction respectively) of the lysate from each well should be transferred into corresponding wells of a new empty 96 well plate for PCR.

For PCR, the user should bring two master mixes: 1 with the primers (can be kept at room t), 2nd with the polymerase in the buffer (must be kept cold). Here we need to think about how to split the components of the reaction better in terms of the temperature that they need to be kept at.

# PCR reaction mixes for Multiplex PCRs: 
 20 uL final volume:
  - template: 2 uL
  - 5x Phusion Buffer: 4 uL
  - dNTPs: 0.4 uL
  - DMSO: 0.6 uL
  - Phusion Polymerase: 0.2 uL
  - FWD Primer (AM233): 0.2 uL stock concentration
  - REV Primers (AM234-AM237): 0.67 uL of 10x dilution each primer (x4)
  - REV Primer (AM238): 1 uL of 10x dilution
  - H2O: 8.92 uL

The above can be then calculated for the number of reactions on the 96-well plate plus always prepare some spare to allow some space for handling errors. The robot would then add the first master mix at a given volume, pipette up and down, then add the second master mix, pipette up and down.The first buffer can contain the primers, DMSO, and H2O (so 13.4 uL to add to each well by a robot). The second master mix to be kept on ice and can contain 5x Phusion Buffer, dNTPs, and Phusion Polymerase (4.6 uL to add to each well by a robot).

Thermocycler protocol:

   98C               ( 98C  ----> 60C   ----> 72C )          ( 98C  ----> 52.4C   ------->       72C      )         (72C   ---->  10C)
   30 sec           10 sec      20 sec       60 sec            10 sec      20 sec            1 min 30 sec            10 min        ∞
   1 cycle                     8 cycles                                  25 cycles                                         1 cycle
