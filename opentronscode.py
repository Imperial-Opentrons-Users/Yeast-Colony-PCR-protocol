#Prior to the experiment, each colony should be 
#manually resuspended in 50 uL H20 by a user; do it in a 96-well plate
  
#this is the PCR lyticase lysis buffer part  

from opentrons import simulate
metadata = {'apiLevel': '2.0'}
protocol = simulate.get_protocol_api('2.0')

#Labware required for the lysis buffer 
plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 1)
tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul', 2)

#pipettes required for the lysis buffer reaction
p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tiprack_1])
protocol.max_speeds['Z'] = 10

#commands for position on 96-well plate
p300.transfer(50, plate['A1'], plate['C1'])
p300.transfer(5, plate['B1'], plate['C1'])

p300.transfer(55, plate['C1'], plate['D1'], touch_tip=True, blow_out=True, new_tip='always') 
p300.pick_up_tip()

#mix the yeast colonies with the lyticase to break up cell wall(repetitions, volume, location, rate)
p300.mix(5, 55, plate['D1'], 0.5)
p300.return_tip()

#thermocycler part/or use temperature module
#first incubation time(37˙C for 30 minutes)
#second incubation time(95˙C for 10 minutes)
protocol.delay(minutes=40)   

#Aspirating 
p300.transfer(5, plate['D1'], plate['A2'])

#pause for 5 minutes to prepare for PCR/thermocycler reaction
protocol.delay(minutes=5)           

for line in protocol.commands(): 
    print(line)


# Two master mixes are to pre-prepared by the user beforehand and then added by the opentrons robot during the pcr procedure

# The 1st mastermix contains the primers, DMSO, and H2O, and is added at a volume of 13.4 uL in each well, hence the variable 'mastermix1_volume" is set at 13.4

# The 2nd mastermix contains the buffer, dNTPs, and Phusion Polymerase, and is added at a volume of 4.6 uL in each well, hence the variable 'mastermix2_volume" is set at 4.6

x = 96 # number of samples, max 96

# Determine values for the parameters used by the opentron for the PCR procedure:
def get_values(*names):
    import json
    _all_values = json.loads("""{"number_of_samples":x,"mastermix1_volume":13.4,"mastermix2_volume":4.6,"master_mix_csv":"Reagent,Well,Volume\\nBuffer,A2,3\\nMgCl,A3,40\\ndNTPs,A2,90\\nWater,A3,248\\nprimer 1,A4,25\\nprimer 2,A5,25\\n","tuberack_type":"opentrons_24_aluminumblock_nest_1.5ml_screwcap","single_channel_type":"p1000_single_gen2","single_channel_mount":"right","pipette_2_type":"p1000_single_gen2","pipette_2_mount":"left" "well_vol":50,"lid_temp":110,"init_temp":4,"init_temp1":98,"init_time1":30,"init_time":300, "d_temp":98,"d_time":10,"a_temp":60,"a_time":20,"e_temp":72,"e_time":60,"no_cycles":8,"d_temp1":98,"d_time1":10,"a_temp1":52.4,"a_time1":20,"e_temp1":72,"e_time1":90,"no_cycles1":25,"fe_temp":72,"fe_time":600,"final_temp":4, "well_vol":50}​​​​""")
    return [_all_values[n] for n in names]


import math

# metadata
metadata = {
    'protocolName': 'Complete PCR Workflow with Thermocycler',
    'author': 'Nick <protocols@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.0'
}

# returning all the values for the parameters into the opentrons protocol run function 

def run(ctx):

    [number_of_samples, mastermix1_volume, mastermix2_volume,
     master_mix_csv, tuberack_type, single_channel_type, single_channel_mount,
     pipette_2_type, pipette_2_mount, lid_temp, init_temp, init_time, d_temp,
     d_time, a_temp, a_time, e_temp, e_time, no_cycles, fe_temp, fe_time,
     final_temp, init_temp1, init_time1, d_temp1, d_time1, a_temp1, a_time1, e_temp1, no_cycles1, well_vol] = get_values( # noqa: F821
        'number_of_samples', 'mastermix1_volume', 'mastermix2_volume',
        'master_mix_csv', 'tuberack_type', 'single_channel_type',
        'single_channel_mount', 'pipette_2_type', 'pipette_2_mount',
        'lid_temp', 'init_temp', 'init_time', 'd_temp', 'd_time', 'a_temp',
        'a_time', 'e_temp', 'e_time', 'no_cycles', 'fe_temp', 'fe_time',
        'final_temp', 'init_temp1', 'init_time1','d_temp1','d_time1','a_temp1',
        'a_time1','e_temp1','no_cycles1', 'well_vol')

 # loading settings for opentrons 96 tiprack labware                                                                                                    #
    range1 = single_channel_type.split('_')[0][1:]
    tipracks1 = [
        ctx.load_labware('opentrons_96_tiprack_' + range1 + 'ul', slot)
        for slot in ['2', '3']
    ]
    p1 = ctx.load_instrument(
        single_channel_type, single_channel_mount, tip_racks=tipracks1)

# loading settings for 96 well plate 100uL labware 
    using_multi = True if pipette_2_type.split('_')[1] == 'multi' else False
    if using_multi:
        mm_plate = ctx.load_labware(
            'nest_96_wellplate_100ul_pcr_full_skirt', '4',
            'plate for mastermix distribution')
        
    # defining pipette settings and mounting required for protocol
    if pipette_2_type and pipette_2_mount:
        range2 = pipette_2_type.split('_')[0][1:]
    
    # establishing compatible tiprack settings for opentrons 96 tiprack
        tipracks2 = [
            ctx.load_labware('opentrons_96_tiprack_' + range2 + 'ul', slot)
            for slot in ['6', '9']
        ]
        p2 = ctx.load_instrument(
            pipette_2_type, pipette_2_mount, tip_racks=tipracks2)

    # setting up thermocycler and 96-wellplate
    tc = ctx.load_module('thermocycler')
    tc_plate = tc.load_labware(
        'nest_96_wellplate_100ul_pcr_full_skirt', 'thermocycler plate')
    
    # If the  lid closed, open the lid and set the lid temperature
    if tc.lid_position != 'open':
        tc.open_lid()
    tc.set_lid_temperature(lid_temp)
    
    # loading the thermocycler manual

    tc_mod = protocol.load_module('thermocycler')

    # setting to 4 degress for the begginging for adding things. To replicate on ice for the PCR enzymes. 
    tc_mod.set_block_temperature(init_temp, hold_time_seconds=init_time,
                                 block_max_volume=well_vol)
    
    # Load tuberack and tempdeck settings for mastermix reagent transfer
    if 'cooled' in tuberack_type:
        tempdeck = ctx.load_module('tempdeck', '1')
        tuberack = tempdeck.load_labware(
            tuberack_type, 'rack for mastermix reagents'
        )
    else:
        tuberack = ctx.load_labware(
            tuberack_type, '1', 'rack for mastermix reagents')
    mm_tube = tuberack.wells()[0]
    num_cols = math.ceil(number_of_samples/8)

# Setting up pipette parameters for tiprack association
    pip_counts = {p1: 0, p2: 0}
    p1_max = len(tipracks1)*96
    p2_max = len(tipracks2)*12 if using_multi else len(tipracks2)*96
    pip_maxs = {p1: p1_max, p2: p2_max}

# Incorporating behaviour to replace tipracks appropriately and setup pipette counting

    def pick_up(pip):
        if pip_counts[pip] == pip_maxs[pip]:
            ctx.pause('Replace empty tipracks before resuming.')
            pip.reset_tipracks()
            pip_counts[pip] = 0
        pip.pick_up_tip()
        pip_counts[pip] += 1

    # determine which pipette has the smaller volume range
    if using_multi:
        pip_s, pip_l = p1, p1
    else:
        if int(range1) <= int(range2):
            pip_s, pip_l = p1, p2
        else:
            pip_s, pip_l = p2, p1

 # User places mastermix1 in A1 of the trough

    # """ DISITRUBTE MASTERMIX1 """
    
    # if the lid is closed, open the lid
    if tc.lid_position != 'open':
        tc.open_lid()
        
    # establish well destinations
    if using_multi:
        mm_source = mm_plate.rows()[0][0]
        mm_dests = tc_plate.rows()[0][:num_cols]
        vol_per_well = mastermix1_volume*num_cols*1.05
        pick_up(p1)
        
        # repeatedly pipette up and down in each well
        for well in mm_plate.columns()[0]:
            p1.transfer(vol_per_well, mm_tube, well, new_tip='never')
            p1.blow_out(well.top(-2))
        p1.drop_tip()
        pip_mm = p2

    else:
        mm_source = mm_tube
        mm_dests = tc_plate.wells()[:number_of_samples]
        pip_mm = pip_s if mastermix1_volume <= pip_s.max_volume else pip_l

    for d in mm_dests:
        pick_up(pip_mm)
        pip_mm.transfer(mastermix1_volume, mm_source, d, new_tip='never')
        pip_mm.drop_tip()
        
 
 # Once mastermix1 has been distributed, user places mastermix2 in A1 of the trough

    # """ DISITRUBTE MASTERMIX2 """
    
      # establish well destinations
    if using_multi:
        mm_source = mm_plate.rows()[0][0]
        mm_dests = tc_plate.rows()[0][:num_cols]
        vol_per_well = mastermix1_volume*num_cols*1.05
        pick_up(p1)
        
         # repeatedly pipette up and down in each well
        for well in mm_plate.columns()[0]:
            p1.transfer(vol_per_well, mm_tube, well, new_tip='never')
            p1.blow_out(well.top(-2))
        p1.drop_tip()
        pip_mm = p2

    else:
        mm_source = mm_tube
        mm_dests = tc_plate.wells()[:number_of_samples]
        pip_mm = pip_s if mastermix2_volume <= pip_s.max_volume else pip_l

    for d in mm_dests:
        pick_up(pip_mm)
        pip_mm.transfer(mastermix2_volume, mm_source, d, new_tip='never')
        pip_mm.drop_tip()
        


    # loading the thermocycler manual

    tc_mod = protocol.load_module('thermocycler')
    
    # Close the lid of the PCR modudule
    if tc_mod.lid_position != 'closed':
        tc_mod.close_lid()

    # lid temperature is set above 100C to prevent any evaporation. 
    tc_mod.set_lid_temperature(lid_temp)

    # set to 98 degrees for 30 seconds, before the start in line with the protocol. 
    tc_mod.set_block_temperature(init_temp1, hold_time_seconds=init_time1,
                                 block_max_volume=well_vol)
    
    # Run first cycle total 720 seconds. Repeat 8 times 
    profile = [
        {'temperature': d_temp, 'hold_time_seconds': d_time},# denaturing 98C 10 seconds
        {'temperature': a_temp, 'hold_time_seconds': a_temp},# annealing 60C 20 seconds
        {'temperature': e_temp, 'hold_time_seconds': e_time} # extension 72C 60 seconds
    ]

    tc_mod.execute_profile(steps=profile, repetitions=no_cycles,
                           block_max_volume=well_vol) # run the cycle 8 times
    # Run second cycle total 3000 seconds. Repeat 25 times. 
    profile = [
        {'temperature': d_temp1, 'hold_time_seconds': d_time1},# denaturing 98C for 10 seconds 
        {'temperature': a_temp1, 'hold_time_seconds': a_temp1},# annealing 52.4C for 20 seconds
        {'temperature': e_temp1, 'hold_time_seconds': e_time1}# extension 1:30 seconds 
    ]
    
    tc_mod.execute_profile(steps=profile, repetitions=no_cycles,
                           block_max_volume=well_vol) #run second cycle 25 times 
    
    
    # at 72 degrees for ten mins 

    tc_mod.set_block_temperature(fe_temp, hold_time_seconds=fe_time,
                                 block_max_volume=well_vol)

    # holding at 4 degrees and opening lid (protocol said 10 but 4 degrees much better)
    tc_mod.deactivate_lid() 
    tc_mod.set_block_temperature(final_temp)
    if tc.lid_position != 'open':
        tc.open_lid()
 
