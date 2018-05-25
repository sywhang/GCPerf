#%%
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
#%matplotlib inline
from pylab import rcParams
rcParams['figure.figsize'] = 20, 10

import locale

def print_array (arr):
    num_elements = len(arr)
    index = 0
    while (index < num_elements):
        print("{0}: {1}".format(index, arr[index]))
        index += 1

BGC_MARK_START = 0
BGC_SWEEP_START = 1
BGC_SWEEP_END = 2
BGC_MAX = 3

GC_REASON_TUNING_SOH = 12
GC_REASON_TUNING_LOH = 13
GC_REASON_STEPPING = 14
GC_REASON_PANIC_SOH = 15
GC_REASON_PANIC_LOH = 16
GC_REASON_GROWTH_SOH = 17
GC_REASON_GROWTH_LOH = 18

#b: blue
#g: green
#r: red
#c: cyan
#m: magenta
#y: yellow
#k: black
total_colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'b', 'g', 'r', 'c', 'm', 'y', 'k']
line_styles = ['-', '-.', '--', ':']

# we can get this from BTL: ml: line
g_total_physical_memory = 0

#%%
class bgc_tuning_data():
    # elapsed_since_last_s is the seconds between last bgc end and this bgc start
    # elapsed_ms is the ms between this bgc start and end
    # gen2_actual_gen1_to_trigger is the # of gen1s between this bgc start and last bgc end, same as gen3_actual_gen1_to_trigger
    def __init__(self, gen_index, reason,
                gen2_panic_ca_plugs_size, gen2_panic_ca_plugs_count, gen2_panic_alloc, gen2_panic_fl,
                 elapsed_since_last_s, elapsed_ms, alloc_gen0, alloc_gen3, beg_ml, end_ml, 
                 # end_heap_size is the physical heap size.
                 beg_heap_size, beg_commit_size, beg_ws_size, end_heap_size, end_commit_size, end_ws_size, 
                gen2_last_bgc_size, gen2_current_bgc_start_flr, gen2_current_bgc_sweep_flr, gen2_current_bgc_physical_sweep_flr,
                gen2_current_bgc_end_flr, gen2_gen_increase_flr, gen2_bgc_surv_rate, gen2_actual_gen1_to_trigger, 
                gen2_gen1_since_last, gen2_actual_alloc_to_trigger, gen2_alloc_to_trigger,
                gen3_last_bgc_size, gen3_current_bgc_start_flr, gen3_current_bgc_sweep_flr, gen3_current_bgc_physical_sweep_flr,
                gen3_current_bgc_end_flr, gen3_gen_increase_flr, gen3_bgc_surv_rate, gen3_actual_gen1_to_trigger, 
                gen3_gen1_since_last, gen3_actual_alloc_to_trigger, gen3_alloc_to_trigger,
                in_use_physical_memory):
        self.gen_index = gen_index
        self.reason = reason
        self.gen2_panic_ca_plugs_size = gen2_panic_ca_plugs_size
        self.gen2_panic_ca_plugs_count = gen2_panic_ca_plugs_count
        self.gen2_panic_alloc = gen2_panic_alloc
        self.gen2_panic_fl = gen2_panic_fl
        self.elapsed_since_last_s = elapsed_since_last_s
        self.elapsed_ms = elapsed_ms
        self.alloc_gen0 = alloc_gen0
        self.alloc_gen3 = alloc_gen3
        self.beg_ml = beg_ml
        self.end_ml = end_ml
        self.beg_heap_size = beg_heap_size
        self.beg_commit_size = beg_commit_size
        self.beg_ws_size  = beg_ws_size
        self.end_heap_size = end_heap_size
        self.end_commit_size  = end_commit_size
        self.end_ws_size = end_ws_size        
        self.gen2_last_bgc_size = gen2_last_bgc_size
        self.gen2_current_bgc_start_flr = gen2_current_bgc_start_flr
        self.gen2_current_bgc_sweep_flr = gen2_current_bgc_sweep_flr
        self.gen2_current_bgc_physical_sweep_flr = gen2_current_bgc_physical_sweep_flr
        self.gen2_current_bgc_end_flr = gen2_current_bgc_end_flr
        self.gen2_gen_increase_flr = gen2_gen_increase_flr
        self.gen2_bgc_surv_rate = gen2_bgc_surv_rate
        self.gen2_actual_gen1_to_trigger = gen2_actual_gen1_to_trigger
        self.gen2_gen1_since_last = gen2_gen1_since_last
        self.gen2_actual_alloc_to_trigger = gen2_actual_alloc_to_trigger
        self.gen2_alloc_to_trigger = gen2_alloc_to_trigger
        self.gen3_last_bgc_size = gen3_last_bgc_size
        self.gen3_current_bgc_start_flr = gen3_current_bgc_start_flr
        self.gen3_current_bgc_sweep_flr = gen3_current_bgc_sweep_flr
        self.gen3_current_bgc_physical_sweep_flr = gen3_current_bgc_physical_sweep_flr
        self.gen3_current_bgc_end_flr = gen3_current_bgc_end_flr
        self.gen3_gen_increase_flr = gen3_gen_increase_flr
        self.gen3_bgc_surv_rate = gen3_bgc_surv_rate
        self.gen3_actual_gen1_to_trigger = gen3_actual_gen1_to_trigger
        self.gen3_gen1_since_last = gen3_gen1_since_last
        self.gen3_actual_alloc_to_trigger = gen3_actual_alloc_to_trigger
        self.gen3_alloc_to_trigger = gen3_alloc_to_trigger
        self.in_use_physical_memory = in_use_physical_memory

PATH_ABOVE = 1
PATH_BELOW = 2
PATH_UNCHANGED = 3

class bgc_detailed_tuning_data():
    def __init__(self, ml_kp, ml_ki, pi, gen2_ratio, gen2_alloc_kp, gen2_alloc_ki,  gen3_alloc_kp, gen3_alloc_ki, 
                gen2_end_physical_size, gen2_end_vfl_size, gen3_end_physical_size, gen3_end_vfl_size,
                gen3_end_fl, gen3_fl_goal, gen3_path_taken, gen3_alloc_smoothed, gen3_alloc_ff):
        self.ml_kp = ml_kp
        self.ml_ki = ml_ki
        self.ml_pi = ml_kp + ml_ki
        self.pi = pi
        self.gen2_ratio = gen2_ratio
        self.gen2_alloc_kp = gen2_alloc_kp
        self.gen2_alloc_ki = gen2_alloc_ki
        self.gen3_alloc_kp = gen3_alloc_kp
        self.gen3_alloc_ki = gen3_alloc_ki
        self.gen2_end_physical_size = gen2_end_physical_size
        self.gen2_end_vfl_size = gen2_end_vfl_size
        self.gen3_end_physical_size = gen3_end_physical_size
        self.gen3_end_vfl_size = gen3_end_vfl_size
        self.gen3_end_fl = gen3_end_fl 
        self.gen3_fl_goal = gen3_fl_goal 
        self.gen3_path_taken = gen3_path_taken 
        self.gen3_alloc_smoothed = gen3_alloc_smoothed 
        self.gen3_alloc_ff = gen3_alloc_ff

# num_elements is how many elements you want to get from the src array starting at start_index
# if max_num_elements is > num_elements, the rest will just remain None
def get_fields(src, field_name, start_index, num_elements, max_num_elements):
    field_data = [None]*max_num_elements
    index = 0
    last_element_index = len(src) - 1
    while (index < num_elements):
        if ((start_index + index) > last_element_index):
            break
        field_data[index] = getattr(src[start_index + index], field_name)
        # print("element {0} field {1} value is {2:,}".format(
        #     (start_index + index), field_name, field_data[index]))
        index += 1    
    return field_data

#%%
#
# some general helpers for convenience
# 
def parse_str(str_to_parse, beg_str, end_str): 
    start_index = str_to_parse.find(beg_str) + len(beg_str) 
    end_index = str_to_parse.find(end_str, start_index) 
    str_to_ret = str_to_parse[start_index:end_index]
    # often we want to keep parsing so also return the remaining str
    remaining_str = str_to_parse[end_index:]
    return str_to_ret, remaining_str

def parse_str_no_end(str_to_parse, beg_str): 
    start_index = str_to_parse.find(beg_str) + len(beg_str) 
    str_to_ret = str_to_parse[start_index:] 
    return str_to_ret

# parse BTL2/BTL3 lines
def get_btl_star_info(line, beg_str): 
    last_bgc_size_str, remaining_str = parse_str(line, beg_str, ",") 
    last_bgc_size = int(last_bgc_size_str) 
    start_flr_str, remaining_str = parse_str(remaining_str, " ", ",") 
    current_bgc_start_flr = float(start_flr_str) 
    sweep_flr_str, remaining_str = parse_str(remaining_str, " ", ",") 
    current_bgc_sweep_flr = float(sweep_flr_str) 
    end_flr_str, remaining_str = parse_str(remaining_str, " ", ",") 
    current_bgc_end_flr = float(end_flr_str) 
    gen_increase_flr_str, remaining_str = parse_str(remaining_str, " ", ",") 
    gen_increase_flr = float(gen_increase_flr_str) 
    bgc_surv_rate_str, remaining_str = parse_str(remaining_str, " ", ",") 
    bgc_surv_rate = float(bgc_surv_rate_str) 
    actual_gen1_to_trigger_str, remaining_str = parse_str(remaining_str, " ", ",") 
    actual_gen1_to_trigger = int(actual_gen1_to_trigger_str) 
    gen1_since_last_str, remaining_str = parse_str(remaining_str, " ", ",") 
    gen1_since_last = int(gen1_since_last_str) 
    actual_alloc_to_trigger_str, remaining_str = parse_str(remaining_str, " ", ",") 
    actual_alloc_to_trigger = int(actual_alloc_to_trigger_str) 
    alloc_to_trigger_str = parse_str_no_end(remaining_str, " ") 
    alloc_to_trigger = int(alloc_to_trigger_str) 
    
    return last_bgc_size, current_bgc_start_flr, current_bgc_sweep_flr, current_bgc_end_flr, gen_increase_flr, bgc_surv_rate, actual_gen1_to_trigger, gen1_since_last, actual_alloc_to_trigger, alloc_to_trigger

# this is out of date...
def parse_path_and_fl(line):
    end_fl = 0
    fl_goal = 0
    path_taken = 0
    
    if (line.find("unchanged(") != -1):
        path_taken = PATH_UNCHANGED
        end_fl_str, remaining_str = parse_str(line, "fl ", ",")
        end_fl = int(end_fl_str)
        fl_goal_str = parse_str_no_end(remaining_str, " ")
        fl_goal = int(fl_goal_str)
        
    elif (line.find("path above - fl ") != -1):
        path_taken = PATH_ABOVE
        end_fl_str, remaining_str = parse_str(line, "fl ", " ")
        end_fl = int(end_fl_str)
        fl_goal_str = parse_str_no_end(remaining_str, ">= ")
        fl_goal = int(fl_goal_str)
        
    elif (line.find("path below - fl ") != -1):
        path_taken = PATH_BELOW
        end_fl_str, remaining_str = parse_str(line, "fl ", " ")
        end_fl = int(end_fl_str)
        fl_goal_str = parse_str_no_end(remaining_str, "< ")
        fl_goal = int(fl_goal_str)
        fl_goal = int(float(fl_goal) / 0.9)
    
    return end_fl, fl_goal, path_taken
        
#%%
# general processing for BGC tuning
def process_file_bgc_tuning (file_name): 
    bgc_tuning_per_process = [] 
    bgc_detailed_tuning_per_process = []
    num_gen2s = 0
    goal_ml = 0
    goal_available_memory = 0

    current_gen2_index = 0
    current_gen2_reason = -1

    alloc_gen0_current_gen2 = 0
    alloc_gen3_current_gen2 = 0
    beg_ml = 0
    end_ml = 0
    beg_heap_size = 0
    beg_commit_size = 0
    beg_ws_size = 0
    end_heap_size = 0
    end_commit_size = 0
    end_ws_size = 0
    
    # from the BTL2*/BTL3*
    gen2_last_bgc_size = 0
    gen2_current_bgc_start_flr = 0.0
    gen2_current_bgc_sweep_flr = 0.0
    gen2_current_bgc_physical_sweep_flr = 0.0
    gen2_current_bgc_end_flr = 0.0
    gen2_gen_increase_flr = 0.0
    gen2_bgc_surv_rate = 0.0
    gen2_actual_gen1_to_trigger = 0
    gen2_gen1_since_last = 0
    gen2_actual_alloc_to_trigger = 0
    gen2_alloc_to_trigger = 0
    gen2_end_physical_size = 0
    gen2_end_vfl_size = 0

    gen3_last_bgc_size = 0
    gen3_current_bgc_start_flr = 0.0
    gen3_current_bgc_sweep_flr = 0.0
    gen3_current_bgc_physical_sweep_flr = 0.0
    gen3_current_bgc_end_flr = 0.0
    gen3_gen_increase_flr = 0.0
    gen3_bgc_surv_rate = 0.0
    gen3_actual_gen1_to_trigger = 0
    gen3_gen1_since_last = 0
    gen3_actual_alloc_to_trigger = 0
    gen3_alloc_to_trigger = 0
    gen3_end_physical_size = 0
    gen3_end_vfl_size = 0

    gen2_alloc_kp = 0
    gen2_alloc_ki = 0
    gen3_alloc_kp = 0
    gen3_alloc_ki = 0
    
    gen3_current_end_fl = 0
    gen3_fl_goal = 0
    gen3_path_taken = 0
    gen3_alloc_kp = 0
    gen3_alloc_smoothed = 0
    gen3_alloc_ff = 0

    ml_kp = 0
    ml_kp = 0
    pi = 0
    
    low_memory_induced_p = 0
    recorded_ml = 0

    elapsed_since_last_s = 0
    elapsed_ms = 0
    last_bgc_end = 0.0
    current_bgc_start = 0.0

    gen2_panic_alloc = 0
    gen2_panic_fl = 0
    gen2_panic_ca_plugs_size = 0
    gen2_panic_ca_plugs_count = 0
    
    # We always parse the plugs line but not everyone will lead to a gen2 panic
    # since it may have already paniced. 
    # So set a flag to indicate when we see the "panic trigger" line and clear
    # it when the BGC it triggered ended.
    record_plugs_p = 1
    # stores the info on plugs that were not 100% allocated into fl
    gen2_plugs_size = 0
    gen2_plugs_count = 0

    # based on available physical mem and total mem, calculate this so we know 
    # if the total physical mem consumption is wildly different from our process's ws
    in_use_physical_memory = 0

    total_physical_memory = 0

    with open(file_name, "r") as pause_file:
        lines = pause_file.readlines()
        #for line in pause_file: 
        for i in range(0, len(lines)):
            line = lines[i]

            if (line.find("*GC*") != -1):
                #print(line)

                if (line.find("(2)(NGC)") != -1):
                    if (low_memory_induced_p != 1):
                        print("NGC2 was not low memory triggered, ml is {0}".format(recorded_ml))
                        print(line)
                if (low_memory_induced_p == 1):
                    print("this GC was low mem triggered!")
                    print(line)
                    low_memory_induced_p = 0

                # don't process FGCs for now
                if (line.find("(FGC)") != -1):
                    continue
                #print(lines[i + 1])

                # for calculating alloc, we ignore FGCs and the first eph GC right before we need to do a BGC
                # which is indicated by "before doing a bgc" in the next line after *GC*
                words = line.split(")(")
                #print_array(words)
                #
                # words[1] is generation
                # words[4] is gen0 alloc
                # words[5] beginning is gen3 alloc:
                #
                #0: [ 5524]*GC* 1(gen0:0
                #1: 2
                #2: BGC
                #3: 0
                #4: g0: 688
                #5: g3: 66)fla(2: 0-0, 3: 0)esa3: 69395608
                #
                # skip the eph GC we do at the beginning of a BGC, it displays the same info as the BGC
                # line anyway.
                #[ 8388]*GC* 40012(gen0:40011)(2)(BGC)(0)(g0: 726)(g3: 2234)fla(2: 24004-5427, 3: 1914)esa3: 339211512
                #[ 8396]*GC* 40013(gen0:40011)(0)(NGC)(1)(g0: 726)(g3: 2234)fla(2: 24004-5427, 3: 1914)esa3: 339211512
                #[ 8396]doing gen0 before doing a bgc
                if (lines[i + 1].find("before doing a bgc") != -1):
                    #print("skipping")
                    continue

                alloc_gen0_str = words[4][len("g0: "):]
                #print("gen0 allocated {0}".format(alloc_gen0_str))
                alloc_gen0_current_gen2 += int(alloc_gen0_str)

                if (words[1] == '2'):
                    #print("GEN2!!!")
                    num_gen2s += 1
                    gen_index_str, remaining_str = parse_str(words[0], "*GC* ", "(")
                    current_gen2_index = int(gen_index_str)

                    temp_alloc_gen3_str = words[5][len("g3: "):]
                    alloc_gen3_end = temp_alloc_gen3_str.find(")")
                    alloc_gen3_str = temp_alloc_gen3_str[:alloc_gen3_end]
                    #print("BGC #{0} gen0 alloced {1} so far, gen3 allocated {2}".format(
                            #current_gen2_index, alloc_gen0_current_gen2, alloc_gen3_str))
                    alloc_gen3_current_gen2 = int(alloc_gen3_str)

            elif (line.find("*EGC") != -1):
                #print(line)                    
                if ((line.find("(2)(NGC)") == -1) and (line.find("(BGC)") == -1)):
                    continue

                # it turned out I didn't log beg_ml/end_ml correctly in EGC..
                # what's after -> is just the begin ml
                #[ 3816]*EGC* 21720(gen0:21723)(2)(BGC)(S)(P)(ml: 41->41)
                #[ 8372]*EGC* 23757(gen0:23757)(2)(NGC)(C)(P)(ml: 0->93)
                beg_ml_str, remaining_str = parse_str (line, "->", ")")
                beg_ml = int(beg_ml_str)

                if (line.find("(BGC)") == -1):
                    end_ml = beg_ml

                if (current_gen2_reason == GC_REASON_PANIC_SOH):
                    gen2_panic_ca_plugs_size = gen2_plugs_size
                    gen2_panic_ca_plugs_count = gen2_plugs_count
                    print("bgc {0} reason {1}, gen2 plugs not full alloced in fl {2}->{3}".format(
                        current_gen2_index, current_gen2_reason,
                        gen2_panic_ca_plugs_count, gen2_panic_ca_plugs_size))

                # end of a BGC, add data to our list
                bgc_tuning_per_process.append(bgc_tuning_data(current_gen2_index,
                                                              current_gen2_reason,
                                                              gen2_panic_ca_plugs_size,
                                                              gen2_panic_ca_plugs_count, 
                                                              gen2_panic_alloc,
                                                              gen2_panic_fl,
                                                              elapsed_since_last_s,
                                                              elapsed_ms,
                                                              alloc_gen0_current_gen2,
                                                              alloc_gen3_current_gen2,
                                                              beg_ml,
                                                                end_ml, 
                                                                beg_heap_size, 
                                                                beg_commit_size, 
                                                                beg_ws_size, 
                                                                end_heap_size, 
                                                                end_commit_size, 
                                                                end_ws_size,                                                               
                                                                gen2_last_bgc_size, 
                                                                gen2_current_bgc_start_flr, 
                                                                gen2_current_bgc_sweep_flr, 
                                                                gen2_current_bgc_physical_sweep_flr,
                                                                gen2_current_bgc_end_flr, 
                                                                gen2_gen_increase_flr, 
                                                                gen2_bgc_surv_rate, 
                                                                gen2_actual_gen1_to_trigger, 
                                                                gen2_gen1_since_last, 
                                                                gen2_actual_alloc_to_trigger, 
                                                                gen2_alloc_to_trigger,
                                                                gen3_last_bgc_size, 
                                                                gen3_current_bgc_start_flr, 
                                                                gen3_current_bgc_sweep_flr, 
                                                                gen3_current_bgc_physical_sweep_flr,
                                                                gen3_current_bgc_end_flr, 
                                                                gen3_gen_increase_flr, 
                                                                gen3_bgc_surv_rate, 
                                                                gen3_actual_gen1_to_trigger, 
                                                                gen3_gen1_since_last, 
                                                                gen3_actual_alloc_to_trigger, 
                                                                gen3_alloc_to_trigger,
                                                                in_use_physical_memory))
#                 print("BGC#{0}({1}) reason: {2}, beg heap: {3}, beg commit: {4}, ws: {5}".format(num_gen2s, current_gen2_index,
#                     current_gen2_reason, beg_heap_size, beg_commit_size, beg_ws_size))
                bgc_detailed_tuning_per_process.append(bgc_detailed_tuning_data(
                                    ml_kp,
                                    ml_ki,
                                    pi,
                                    gen2_alloc_kp,
                                    gen2_alloc_ki,
                                    gen3_alloc_kp,
                                    gen3_alloc_ki,
                                    gen2_end_physical_size,
                                    gen2_end_vfl_size,
                                    gen3_end_physical_size,
                                    gen3_end_vfl_size,
                                    gen3_current_end_fl,
                                    gen3_fl_goal,
                                    gen3_path_taken,
                                    gen3_alloc_smoothed,
                                    gen3_alloc_ff))
                # reset stuff
                alloc_gen0_current_gen2 = 0
                alloc_gen3_current_gen2 = 0
                current_gen2_reason = -1
                record_plugs_p = 1
                gen2_panic_ca_plugs_size = 0
                gen2_panic_ca_plugs_count = 0
                gen2_panic_alloc = 0
                gen2_panic_fl = 0

            elif (line.find("BTL tuning parameters: ") != -1):
                ml_goal_str, remaining_str = parse_str(line, "mem goal: ", "(")
                sweep_flr_goal, remaining_str = parse_str(remaining_str, "sweep flr goal: ", ",")
                ml_kp_str, remaining_str = parse_str(remaining_str, "ml: kp ", ",")
                ml_ki_str = parse_str_no_end(remaining_str, ", ki ")
                print("ml goal: {0}, sweep flr goal: {1}, ml kp: {2}, ml ki: {3}".format(ml_goal_str,
                    sweep_flr_goal, ml_kp_str, ml_ki_str))

            elif (line.find(", P: ") != -1):
                if (record_plugs_p == 1):
                    plugs_fa_ratio_str, remaining_str = parse_str(line, ") ", "%")
                    plugs_fa_ratio = int (plugs_fa_ratio_str)
                    if (plugs_fa_ratio != 100) :
                        # print("detected plugs not completely alloced in fl")
                        # print(line)
                        temp_gen2_plugs_count_str, remaining_str = parse_str(line, "P: ", "(")
                        temp_gen2_plugs_count = int(temp_gen2_plugs_count_str)
                        if (temp_gen2_plugs_count > 0):
                            gen2_plugs_count = temp_gen2_plugs_count
                            gen2_plugs_size_str, remaining_str = parse_str(remaining_str, "(", ")")
                            gen2_plugs_size = int(gen2_plugs_size_str)
                            # print("{0} plugs, size {1}".format(gen2_plugs_count, gen2_plugs_size))

            # get alloc kp
            elif (line.find("bytes in alloc, ") != -1):
                if (line.find("BTL2") != -1):
                    gen2_alloc_kp_str, remaining_str = parse_str(line, "= ", " ")
                    gen2_alloc_kp = int(gen2_alloc_kp_str)
                else:
                    gen3_alloc_kp_str, remaining_str = parse_str(line, "= ", " ")
                    gen3_alloc_kp = int(gen3_alloc_kp_str)

            # get alloc ki
            elif (line.find("+accu err ") != -1):
                if (line.find("BTL2:") != -1):
                    gen2_alloc_ki_str, remaining_str = parse_str(line, "accu err ", "=")
                    gen2_alloc_ki = int(gen2_alloc_ki_str)
                else:
                    gen3_alloc_ki_str, remaining_str = parse_str(line, "accu err ", "=")
                    gen3_alloc_ki = int(gen3_alloc_ki_str)

            elif (line.find("panic trigger in free") != -1):
                if (line.find("gen3") != -1):
                    print("currrently we don't let gen3 panic")
                else:
                    # print(line)
                    gen2_panic_size_str, remaining_str = parse_str(line, "->", ",")
                    gen2_panic_size = int(gen2_panic_size_str)
                    gen2_panic_flr_str, remaining_str = parse_str(remaining_str, "flr: ", ",")
                    gen2_panic_flr = float(gen2_panic_flr_str)
                    gen2_panic_fl = int (float(gen2_panic_size) * gen2_panic_flr / 100.0)
                    gen2_current_alloc_str, remaining_str = parse_str(line, "(", " ")
                    gen2_current_alloc = int (gen2_current_alloc_str)
                    gen2_last_alloc_str, remaining_str = parse_str(remaining_str, "- ", ")")
                    gen2_last_alloc = int (gen2_last_alloc_str)
                    gen2_panic_alloc = gen2_current_alloc - gen2_last_alloc
                    # print("{0} - {1} = {2}".format(gen2_current_alloc, gen2_last_alloc, gen2_panic_alloc))
                    record_plugs_p = 0

            elif (line.find("BTL: g2t[st]") != -1):
                # print(line)
                current_bgc_start_str, remaining_str = parse_str (line, "]: ", " ")
                current_bgc_start = float (current_bgc_start_str)
                elapsed_since_last_s = int((current_bgc_start - last_bgc_end) * 60.0)
                # print("GC#{0} start {1:10.3f}, {2}s since last bgc end".format(current_gen2_index,
                #     current_bgc_start, elapsed_since_last_s))
                
                # if (num_gen2s > 10):
                #     break;                

            elif (line.find("BTL: g2t[en]") != -1):
                # print(line)
                current_bgc_end_str, remaining_str = parse_str (line, "]: ", " ")
                current_bgc_end = float (current_bgc_end_str)
                elapsed_ms = int((current_bgc_end - current_bgc_start) * 60.0 * 1000.0)
                # print("GC#{0} start {1:10.3f} end {2:10.3f}, {3}ms since bgc start".format(current_gen2_index,
                #     current_bgc_start, current_bgc_end, elapsed_ms))
                last_bgc_end = current_bgc_end

            elif (line.find("BTL3: path ") != -1):
                gen3_current_end_fl, gen3_fl_goal, gen3_path_taken = parse_path_and_fl(line)
                            
            elif (line.find("smoothed ") != -1):
                if (line.find("BTL3") != -1):
                    gen3_alloc_smoothed_str = parse_str_no_end(line, "->")
                    gen3_alloc_smoothed = int(gen3_alloc_smoothed_str)
                    
            elif (line.find("ff ") != -1):
                if (line.find("BTL3") != -1):
                    gen3_alloc_ff_str = parse_str_no_end(line, "->")
                    gen3_alloc_ff = int(gen3_alloc_ff_str)
            
            # for below goal we don't do kp or ff, use the value we calculated for kp,
            # note that it has a space after ->
            elif (line.find("]: below goal") != -1):
                if (line.find("BTL3") != -1):
                    gen3_alloc_kp_str = parse_str_no_end(line, "-> ")
                    gen3_alloc_kp = int(gen3_alloc_kp_str)
            
            # this is to parse this line during bgc sweep
            # [ 3060]BTL2: sflr: 98.751%->91.115% (49168919753->49168919753, 48554626049->44800081185) (1:0-0/gen1) since start (afl: 40001272097, 52.345)
            # to get the physical sweep flr
            elif (line.find(") since start (afl: ") != -1):
                if (line.find("BTL2:") != -1):
                    gen2_afl_str, remaining_str = parse_str(line, "(afl: ", ",")
                    gen2_physical_sflr_str, remaining_str = parse_str(remaining_str, " ", ")")
                    #print("gen2 afl {0:14}, physical sflr: {1:}".format(gen2_afl_str, gen2_physical_sflr_str))
                    gen2_current_bgc_physical_sweep_flr = float(gen2_physical_sflr_str)
                else:
                    gen3_afl_str, remaining_str = parse_str(line, "(afl: ", ",")
                    gen3_physical_sflr_str, remaining_str = parse_str(remaining_str, " ", ")")
                    #print("gen3 afl {0:14}, physical sflr: {1:}".format(gen3_afl_str, gen3_physical_sflr_str))
                    gen3_current_bgc_physical_sweep_flr = float(gen3_physical_sflr_str)
                    
            elif (line.find("BTL: ml: ") != -1):
                #[ 3816]BTL: ml: 44 (g: 35), a 67038240768 (g: 78168098611)
                #Or this line:
                #[ 4324]BTL: ml: 7 (g: 35), a: 111696109568 (g: 78168098611, elg: 0->272188303, 0->14591389003), +33528010957 = 7054109066 + 26473901890

                # latest version:
                #BTL: ml: 61 (g: 60)(below), a: 6615834624 (g: 6848602112, elg: 5123182664+0=5123182664, 30698544+0=30698544, pi=0), vfl: -5342047895=-232767488+-5109280407

                is_ngc2 = 0
                if (line.find("(NGC2)") != -1):
                    is_ngc2 = 1

                if (goal_ml == 0):
                    goal_ml_str, remaining_str = parse_str(line, "g: ", ")")
                    goal_ml = int(goal_ml_str)
                    goal_available_memory_str, remaining_str = parse_str(remaining_str, "(g: ", ",")
                    goal_available_memory = int(goal_available_memory_str)
                    total_physical_memory = float(goal_available_memory) * 100 / float(100 - goal_ml)
                    print("ml goal is {0}, available mem goal is {1:,}, total phy mem is {2:,}".format(goal_ml, 
                                            goal_available_memory, total_physical_memory))
                    print("after goal : gen2 reason is {0}".format(current_gen2_reason))

                # now get the end ml for the current BGC
                end_ml_str, remaining_str = parse_str(line, "BTL: ml: ", " ")
                end_ml = int(end_ml_str)

                in_use_physical_memory_str, remaining_str = parse_str(line, "a: ", " ")
                in_use_physical_memory = total_physical_memory - int (in_use_physical_memory_str)

                # now get the physical size of gen2/3 and their vfl sizes
                gen2_end_physical_size_str, remaining_str = parse_str(remaining_str, "elg: ", "+")
                gen2_end_physical_size = int(gen2_end_physical_size_str)
                gen2_end_vfl_size_str, remaining_str = parse_str(remaining_str, "+", "=")
                gen2_end_vfl_size = int(gen2_end_vfl_size_str)
                
                gen3_end_physical_size_str, remaining_str = parse_str(remaining_str, ", ", "+")
                gen3_end_physical_size = int(gen3_end_physical_size_str)
                gen3_end_vfl_size_str, remaining_str = parse_str(remaining_str, "+", "=")
                gen3_end_vfl_size = int(gen3_end_vfl_size_str)

                # print("g2 physical size is {0}, vfl is {1}, g3 {2} {3}".format(
                #                                                     gen2_end_physical_size,
                #                                                     gen2_end_vfl_size,
                #                                                     gen3_end_physical_size,
                #                                                     gen3_end_vfl_size))

                # for logs that logged pi (build-0530 and after)
                pi = 0
                if (line.find("pi=") != -1):
                    pi_str, remaining_str = parse_str(line, "pi=", ")")
                    pi = int(pi_str)

                # for logs that recorded the vfl info
                if (line.find("), vfl: ") != -1):
                    vfl_str = parse_str_no_end(line, "), vfl: ")
                    vfl_kp_str, remaining_str = parse_str(vfl_str, "=", "+")
                    ml_kp = int(vfl_kp_str)
                    if (is_ngc2 == 1):
                        vfl_ki_str, remaining_str = parse_str(remaining_str, "+", "(NGC2)")
                    else:
                        vfl_ki_str = parse_str_no_end(remaining_str, "+")
                    ml_ki = int(vfl_ki_str)

            elif (line.find("stepping trigger: yes") != -1):
                current_gen2_reason = GC_REASON_STEPPING
                #print("BGC#{0}({1}), stepping ({2})".format(num_gen2s, current_gen2_index, current_gen2_reason))
            elif (line.find("BTLc: gen2 panic trigger!!!") != -1):
                current_gen2_reason = GC_REASON_PANIC_SOH
                #print("BGC#{0}({1}), gen2 panic ({2})".format(num_gen2s, current_gen2_index, current_gen2_reason))
            elif (line.find("BTLc: gen3 panic trigger!!!") != -1):
                current_gen2_reason = GC_REASON_PANIC_LOH
                #print("BGC#{0}({1}), gen3 panic ({2})".format(num_gen2s, current_gen2_index, current_gen2_reason))
            elif (line.find("BTLc: gen2 below goal growth trigger!!!") != -1):
                current_gen2_reason = GC_REASON_GROWTH_SOH
                #print("BGC#{0}({1}), gen2 growth ({2})".format(num_gen2s, current_gen2_index, current_gen2_reason))
            elif (line.find("BTLc: gen3 below goal growth trigger!!!") != -1):
                current_gen2_reason = GC_REASON_GROWTH_LOH
                #print("BGC#{0}({1}), gen3 growth ({2})".format(num_gen2s, current_gen2_index, current_gen2_reason))
            # otherwise we need to parse the end BGC
            elif (line.find("BTL: reason: ") != -1):
                bgc_reason_str, remaining_str = parse_str(line, "BTL: reason: ", ",")
                bgc_reason = int(bgc_reason_str)
                if (bgc_reason == GC_REASON_PANIC_SOH):
                    gen2_panic_ca_plugs_size = gen2_plugs_size
                    gen2_panic_ca_plugs_count = gen2_plugs_count
                    # print("bgc {0} reason {1}, gen2 plugs not full alloced in fl {2}->{3}".format(
                        # current_gen2_index, bgc_reason,
                        # gen2_panic_ca_plugs_count, gen2_panic_ca_plugs_size))
                if (current_gen2_reason == -1):
                    current_gen2_reason = bgc_reason

            elif (line.find("BTL2* ") != -1):
                #print(line)
                gen2_last_bgc_size, gen2_current_bgc_start_flr, gen2_current_bgc_sweep_flr, gen2_current_bgc_end_flr, gen2_gen_increase_flr, gen2_bgc_surv_rate, gen2_actual_gen1_to_trigger, gen2_gen1_since_last, gen2_actual_alloc_to_trigger, gen2_alloc_to_trigger = get_btl_star_info(line, "BTL2* ")

            elif (line.find("BTL3* ") != -1):
                #print(line)
                gen3_last_bgc_size, gen3_current_bgc_start_flr, gen3_current_bgc_sweep_flr, gen3_current_bgc_end_flr, gen3_gen_increase_flr, gen3_bgc_surv_rate, gen3_actual_gen1_to_trigger, gen3_gen1_since_last, gen3_actual_alloc_to_trigger, gen3_alloc_to_trigger = get_btl_star_info(line, "BTL3* ")

            elif (line.find("init: 0(9)") != -1):
                low_memory_induced_p = 1

            elif (line.find(" ml: ") != -1):
                if ((line.find("interval") == -1) and (line.find("stepping") == -1) and (line.find("elg:") == -1)):
                    ml_index = line.find(" ml: ")
                    ml_str = line[(ml_index + len(" ml: ")):]
                    recorded_ml = int(ml_str)
                    
            elif (line.find("g2 [BEG] ") != -1):
                beg_heap_size_str, remaining_str = parse_str(line, "THS: ", " ")
                beg_heap_size = int(beg_heap_size_str)
                beg_commit_size_str, remaining_str = parse_str(remaining_str, " ", " ")
                beg_commit_size = int(beg_commit_size_str)
                beg_ws_size_str, remaining_str = parse_str(remaining_str, " ", "(")
                beg_ws_size = int(beg_ws_size_str)
#                 print(line)
#                 print("THS beg, heap size {0}, commit {1}, ws {2}".format(beg_heap_size, beg_commit_size, beg_ws_size))
                
            # [ 9080]g(2) #2965 [END] THS: 3358396272 4197388288 4255346688
            # new (and currently not used)
            # [ 6184]g(2) #2 [BEG] #2 THS: 645460720 645697536 662626304(645697536, 662626304)
            elif (line.find("g(2) #") != -1):
                if (line.find("[END]") != -1):
                    end_heap_size_str, remaining_str = parse_str(line, "THS: ", " ")
                    end_heap_size = int(end_heap_size_str)
                    end_commit_size_str, remaining_str = parse_str(remaining_str, " ", " ")
                    end_commit_size = int(end_commit_size_str)
                    end_ws_size_str = parse_str_no_end(remaining_str, " ")
                    # TODO
                    end_ws_size = int(end_ws_size_str)
                    # end_ws_size = 0
    #                 print(line)
    #                 print("THS end, heap size {0}, commit {1}, ws {2}".format(end_heap_size, end_commit_size, end_ws_size))
                
    return num_gen2s, bgc_tuning_per_process, bgc_detailed_tuning_per_process, total_physical_memory

#%%
# for experimenting with the lang
#

def clear_array(arr, num_elems):
    for i in range (0, num_elems):
        arr[i] = 0

gen2_free_spaces_gc = {}

num_elements = 12
gen2_free_buckets = [0 for i in range(num_elements)]
for i in range(0, num_elements):
    gen2_free_buckets[i] = i * 2

gen2_free_spaces_gc[0] = gen2_free_buckets[:]

# for i in range(1):
#     print(gen2_free_spaces_gc[i])

for i in range(0, 12):
    gen2_free_buckets[i] = i * 4

gen2_free_spaces_gc[1] = gen2_free_buckets[:]

for i in range(2):
    print(gen2_free_spaces_gc[i])

clear_array(gen2_free_spaces_gc[0], num_elements)
for i in range(2):
    print(gen2_free_spaces_gc[i])

#%%
import math

class gen2_increase_data():
    def __init__(self,
                    gen_index,
                    gen_num, # 1 or 2
                    bgc_state,
                    gen2_fl_ratio,
                    gen2_fl_size,
                    gen2_size_increase,
                    gen1_plugs_tried_in_gen2,
                    gen2_fl_allocated,
                    gen2_es_allocated,
                    gen2_c_allocated,
                    gen1_plan_ns,
                    soh_allocated_mb_so_far,
                    elapsed_s):
        self.gen_index = gen_index
        self.gen_num = gen_num
        self.bgc_state = bgc_state
        self.gen2_fl_ratio = gen2_fl_ratio
        self.gen2_fl_size = gen2_fl_size
        self.gen2_size_increase = gen2_size_increase
        self.gen1_plugs_tried_in_gen2 = gen1_plugs_tried_in_gen2
        self.gen2_fl_allocated = gen2_fl_allocated
        self.gen2_es_allocated = gen2_es_allocated
        self.gen2_c_allocated = gen2_c_allocated
        self.gen1_plan_ns = gen1_plan_ns
        self.soh_allocated_mb_so_far = soh_allocated_mb_so_far
        self.elapsed_s = elapsed_s

# for every eph GC we fill in this.
# for gen1 GCs, it has 2 gen0 surv lines, we just take the 2nd line
class eph_surv_data():
    def __init__(self,
                gen_index,
                gen_num,
                gen0_alloc,
                gen0_surv,
                # for gen0 GCs these are 0
                gen1_alloc,
                gen1_surv):
        self.gen_index = gen_index
        self.gen_num = gen_num
        self.gen0_alloc = gen0_alloc
        self.gen0_surv = gen0_surv
        self.gen1_alloc = gen1_alloc
        self.gen1_surv = gen1_surv


TYPE_NGC=0
TYPE_FGC=1
TYPE_FGC_BEFORE_BGC=2
TYPE_BGC=3

size_in_pow_2_p = 0

# #
# # this is the power of 2 and they are indexed by the power
# # 
# # we start from 2^8
base_power = 8 # this is only used in convert_bucket_index
total_num_buckets = 12

size_buckets = [0 for i in range(total_num_buckets)]
size_buckets[0] = 256
for temp_b_index in range (1, total_num_buckets - 1):
    size_buckets[temp_b_index] = size_buckets[temp_b_index - 1] * 2
    print("b{0}: size {1}".format(temp_b_index, size_buckets[temp_b_index]))

size_buckets[total_num_buckets - 1] = 1048576

#
# this is the 1st impl of size class - 100 buckets
#
# we just use the size, no power of 2 stuff, so no base_power
# total_num_buckets = 100
# size_buckets = [0 for i in range(total_num_buckets)]

def init_bucket_sizes_0():
    current_bucket_index = 0
    while (current_bucket_index < 8):
        s = (current_bucket_index + 1) * 128
        size_buckets[current_bucket_index] = s
        current_bucket_index = current_bucket_index + 1

    i = 1
    while (current_bucket_index < 23):
        s = (i + 1) * 1024
        size_buckets[current_bucket_index] = s
        current_bucket_index = current_bucket_index + 1
        i = i + 1

    i = 1
    while (current_bucket_index < 83):
        s = (i * 4 + 16) * 1024
        size_buckets[current_bucket_index] = s
        current_bucket_index = current_bucket_index + 1
        i = i + 1

    i = 1
    while (current_bucket_index < 99):
        s = (i * 16 + 256) * 1024
        size_buckets[current_bucket_index] = s
        current_bucket_index = current_bucket_index + 1
        i = i + 1

    size_buckets[current_bucket_index] = 1048576

    # current_bucket_index = 0
    # while (current_bucket_index < total_num_buckets):
    #     print("b{0}: {1}".format(current_bucket_index, size_buckets[current_bucket_index]))
    #     current_bucket_index = current_bucket_index + 1

# this is the 2nd impl of size class - 100 buckets
# total_num_buckets = 42
# size_buckets = [0 for i in range(total_num_buckets)]

def init_size_buckets_1():
    current_bucket_index = 0
    s = 128
    last_bucket_min_size = 559872

    while (s < last_bucket_min_size):
        if (s < 2 * 1024):
            size_buckets[current_bucket_index] = s
            s += 128
        elif (s < 16 * 1024):
            size_buckets[current_bucket_index] = s
            s += 1024
        elif (s < 32 * 1024):
            size_buckets[current_bucket_index] = s
            s += 4 * 1024
        else:
            size_buckets[current_bucket_index] = s
            s += s >> 1

        current_bucket_index = current_bucket_index + 1

    size_buckets[current_bucket_index] = s

    # bucket 41 is the last bucket and it doesn't have a max 
    # size associated with it. but we need it for printing so
    # set it to 1mb
    current_bucket_index = current_bucket_index + 1
    size_buckets[current_bucket_index] = 1048576

    # last_size = 0

    # for i in range (0, total_num_buckets - 1):
    #     current_bucket_size = size_buckets[i]
    #     print("b#{0}: {1}(last + {2})".format(
    #         i, current_bucket_size,
    #         (current_bucket_size - last_size)))
    #     last_size = current_bucket_size
    
    # print("b#{0}: {1}".format((total_num_buckets - 1), size_buckets[(total_num_buckets - 1)]))

def clear_array(arr, num_elems):
    for i in range (0, num_elems):
        arr[i] = 0

def convert_gen_type(type_str):
    gen_type = TYPE_NGC
    if (type_str == "FGC"):
        gen_type = TYPE_FGC
    elif (type_str == "BGC"):
        gen_type = TYPE_BGC
    return gen_type

# buckets start with 2^8
# buckets are either in power form or size
# largest power we get is 2^20 so 20 is passed here
# so if it's >= 128 we know it's a size
def convert_bucket_index(bucket_str):
    bucket_index = int(bucket_str)
    if (bucket_index >= 128):
        for i in range(0, total_num_buckets):
            if (bucket_index == size_buckets[i]):
                return i
    else:
        bucket_index = bucket_index - base_power
        return bucket_index

def convert_index_to_size(bucket_index):
    if (size_in_pow_2_p == 0) :
        return size_buckets[bucket_index]
    else:
        # when it's in 2^n format, b0 starts with 2^8
        return math.pow(2, (bucket_index + 8))

# we return 1 array that encapsulates info from both gen2 and gen1, charting functions can 
# choose to form new arrays if they want to only display gen1 info
def process_file_bgc_tuning_size_increase (file_name): 
    gen2_size_increase_info = []
    eph_surv_info = []

    # the following info is by buckets per GC
    gen2_free_spaces_info = {}
    gen2_free_spaces_consumed_info = {}
    gen1_objs_info = {}
    gen1_plugs_info = {}
    gen1_unfit_plugs_info = {}
    gen0_big_objects_info = {}
    gen2_tb_info = {}

    # pause info - NOTE I am only tracking eph GC pauses
    # each element will be for such a GC
    gen0_pause_ms_info = []
    gen1_pause_ms_info = []
    # the following 2 are duplicated in gen2_increase_data...
    gen1_plan_ns_info = []
    gen1_plugs_tried_in_gen2_info = []

    # when we don't try at allocate in gen2 at all, it means
    # we decided to not promote.
    gen1_plugs_tried_in_gen2_per_gc = 0
    gen1_plan_ns = 0
    gen1_np_plan_ns_info = []
    # currently not used
    gen1_np_size_info = []

    # this is for the whole log
    total_gen0_plugs = [0 for i in range(total_num_buckets)]
    total_gen0_objs = [0 for i in range(total_num_buckets)]
    total_gen0_allocated_big_objs = [0 for i in range(total_num_buckets)]

    # these are temp ones saved in each GC
    gen2_free_spaces_per_gc = [0 for i in range(total_num_buckets)]
    gen2_free_spaces_consumed_per_gc = [0 for i in range(total_num_buckets)]
    gen1_objs_per_gc = [0 for i in range(total_num_buckets)]
    gen1_plugs_per_gc = [0 for i in range(total_num_buckets)]
    gen1_unfit_plugs_per_gc = [0 for i in range(total_num_buckets)]
    # what got threaded back because they were too big for current alloc request
    gen2_threaded_back_per_gc = [0 for i in range(total_num_buckets)]

    # note the first few bucktes in this are always 0 by definition since we only record big ones
    gen0_big_objects_per_gc = [0 for i in range(total_num_buckets)]
    num_gen0_gcs = 0
    num_gen1_gcs = 0
    # the only data I am getting for gen2 is really just the free space info...
    # but it's easier if we maintain this across gen1/2 GCs so they are in order naturally.
    num_gen1_gen2_gcs = 0

    gen2_fl_allocated_per_gc = 0
    gen2_es_allocated_per_gc = 0
    gen2_c_allocated_per_gc = 0

    eph_alloc_per_gc = [0 for i in range(2)]
    eph_surv_per_gc = [0 for i in range(2)]

    gen_num = 0
    gen_type = 0
    bgc_state = 0
    gen2_fl_size = 0
    gen2_fl_ratio = 0
    gen2_size_increase = 0
    fgc_before_bgc = 0
    eph_pause_ms = 0

    found_start_p = 0
    first_gc_index = 0
    last_gc_index = 0

    found_first_elapsed_p = 0
    first_elapsed_min = 0
    last_elapsed_min = 0
    last_elapsed_s = 0
    
    found_first_alloc_soh_p = 0
    first_alloc_soh_mb = 0
    last_alloc_soh_mb = 0

    found_first_alloc_loh_p = 0
    first_alloc_loh_mb = 0
    last_alloc_loh_mb = 0

    with open(file_name, "r") as pause_file:
        lines = pause_file.readlines()
        #for line in pause_file: 
        for i in range(0, len(lines)):
            line = lines[i]

            # the beginng of GC line looks like this:
            # [12148]*GC* 15(gen0:14)(1)(NGC)(0)
            # [12148]*GC* 14(gen0:13)(0)(FGC)(3)
            # [12148]*GC* 13(gen0:12)(2)(BGC)(0)
            # (gen)(type of GC)(bgc state)
            #
            # it's actually not necessary to parse this line...
            if (line.find("*GC*") != -1):
                # some of these are unnecessary to get at GC start...
                fgc_before_bgc = 0
                gen2_size_increase = 0

                gen_index_str, remaining_str = parse_str(line, "* ", "(")
                gen_index = int(gen_index_str)

                if (found_start_p == 0):
                    first_gc_index = gen_index
                    found_start_p = 1

                last_gc_index = gen_index

                gen_num_str, remaining_str = parse_str(remaining_str, ")(", ")")
                gen_num = int(gen_num_str)

                if (gen_num == 0):
                    continue

                gen_type_str, remaining_str = parse_str(remaining_str, ")(", ")")
                #gen_type = convert_gen_type(gen_type_str)
                bgc_state_str, remaining_str = parse_str(remaining_str, ")(", ")")
                bgc_state = int(bgc_state_str)

                # print("GC#{0}: {1}, bgc state {2}".format(gen_index, gen_num, bgc_state))

            elif (line.find("doing gen1 before doing a bgc") != -1):
                fgc_before_bgc = 1

            # only gen1's that increased gen2 size print out this line
            #
            # [31608]g2+ 24->21158960(21158936), esa: 0, ca: 1667104 (diff: 19491832)
            # means 
            # g2+ last_size->current_size(increased), end of seg alloc, condemned alloc (inceased - esc - ca)
            elif (line.find("g2+ ") != -1):
                gen2_size_increase_str, remaining_str = parse_str(line, "(", ")")
                gen2_size_increase = int(gen2_size_increase_str)

            # every gen1 prints out this line
            # [21832]fla: 326136 (1208 fo rej), esa: 0, ca: 1297224, fl: 71967968(40%), fo: 819512, g1 ca: 524648
            elif (line.find("]fla: ") != -1):
                gen2_fl_allocated_str, remaining_str = parse_str(line, "fla: ", " ")
                gen2_fl_allocated_per_gc = int(gen2_fl_allocated_str)

                gen2_es_allocated_str, remaining_str = parse_str(remaining_str, "esa: ", ",")
                gen2_es_allocated_per_gc = int(gen2_es_allocated_str)

                gen2_c_allocated_str, remaining_str = parse_str(remaining_str, "ca: ", ",")
                gen2_c_allocated_per_gc = int(gen2_c_allocated_str)
                
                gen2_fl_size_str, remaining_str = parse_str(remaining_str, "fl: ", "(")
                gen2_fl_size = int(gen2_fl_size_str)
                gen2_fl_ratio_str, remaining_str = parse_str(remaining_str, "(", "%")
                gen2_fl_ratio = int(gen2_fl_ratio_str)

            # use this line to find out the fl ratio of gen2 after a BGC    
            # [102864][END][g2]g2:, s: 10464744, frag: 279360(L: 135208, O: 144152), f: 2% (S)   P
            elif (line.find("][END][g2]g2:") != -1):
                gen2_size_str, remaining_str = parse_str(line, "s: ", ",")
                gen2_size = int(gen2_size_str)
                gen2_fl_size_str, remaining_str = parse_str(line, "L: ", ",")
                gen2_fl_size = int(gen2_fl_size_str)
                gen2_fl_ratio = gen2_fl_size * 100 / gen2_size

            # pass gen0 info
            # [16132][h0][#44642]: 2^10: 0O: 1, 0B: 0, 0P: 6
            # 0O and 0P recorded during plan
            # 0O is recorded during allocation, when we see an alloc larger than alloc quantum
            elif (line.find(", 0B: ") != -1):
                if (line.find("2^") != -1):
                    bucket_str, remaining_str = parse_str(line, "2^", ":")
                else:
                    bucket_str, remaining_str = parse_str(line, "]: ", ":")

                b = convert_bucket_index(bucket_str)

                # print("{0}: b: {1}".format (line, b))

                num_gen0_objs_str, remaining_str = parse_str(remaining_str, "0O: ", ",")
                num_gen0_objs = int(num_gen0_objs_str)
                total_gen0_objs[b] = total_gen0_objs[b] + num_gen0_objs

                num_gen0_allocated_big_objs_str, remaining_str = parse_str(remaining_str, "0B: ", ",")
                num_gen0_allocated_big_objs = int(num_gen0_allocated_big_objs_str)
                total_gen0_allocated_big_objs[b] = total_gen0_allocated_big_objs[b] + num_gen0_allocated_big_objs
                
                num_gen0_plugs_str, remaining_str = parse_str(remaining_str, "0P: ", ",")
                num_gen0_plugs = int(num_gen0_plugs_str)
                total_gen0_plugs[b] = total_gen0_plugs[b] + num_gen0_plugs

            # now parsing the buckets
            # [ 1144][h0][#54778]: 2^11: F: 19782->19762(20), u: 531(553), O: 9, P: 531, g0P: 0
            # now it looks like this:
            # [25160][h0][#7986]: 2^13: F: 1152->1132(20), u: 0(0), O: 11, P: 9, TB: 6
            # or this
            # [24648][h0] 128: F: 29348->29380(-32), u: 0(0), O: 1257, P: 14, TB: 0
            elif (line.find(", u: ") != -1):
                if (line.find("2^") != -1):
                    bucket_str, remaining_str = parse_str(line, "2^", ":")
                else:
                    bucket_str, remaining_str = parse_str(line, "] ", ":")

                b = convert_bucket_index(bucket_str)

                # print("{0}: b: {1}".format(line, b))

                num_gen2_free_spaces_str, remaining_str = parse_str(remaining_str, "->", "(")
                num_gen2_free_spaces = int(num_gen2_free_spaces_str)
                gen2_free_spaces_per_gc[b] = num_gen2_free_spaces

                gen2_free_spaces_consumed_str, remaining_str = parse_str(remaining_str, "(", ")")
                gen2_free_spaces_consumed = int(gen2_free_spaces_consumed_str)
                gen2_free_spaces_consumed_per_gc[b] = gen2_free_spaces_consumed

                num_gen1_unfit_plugs_str, remaining_str = parse_str(remaining_str, "u: ", "(")
                num_gen1_unfit_plugs = int(num_gen1_unfit_plugs_str)
                gen1_unfit_plugs_per_gc[b] = num_gen1_unfit_plugs

                num_gen1_objs_str, remaining_str = parse_str(remaining_str, "O: ", ",")
                num_gen1_objs = int (num_gen1_objs_str)
                gen1_objs_per_gc[b] = num_gen1_objs

                # print("gen1 obj str: {0}, remaining_str: {1}".format(num_gen1_objs_str, remaining_str))
                num_gen1_plugs_str, remaining_str = parse_str(remaining_str, "P: ", ",")
                num_gen1_plugs = int (num_gen1_plugs_str)
                gen1_plugs_per_gc[b] = num_gen1_plugs
                # print("gen1 plug str: {0}, remaining_str: {1}".format(num_gen1_plugs_str, remaining_str))

                bucket_size = int (bucket_str)
                if (bucket_size < 128):
                    bucket_size = convert_index_to_size(bucket_size - 8)

                # if ((gen2_free_spaces_consumed > 0) or (num_gen1_plugs > 0)):
                #     print("free space consumed: {0} x {1} = {2}, plugs: {3} x {1} = {4}".format(
                #         gen2_free_spaces_consumed, 
                #         bucket_size, 
                #         (gen2_free_spaces_consumed * bucket_size),
                #         num_gen1_plugs, 
                #         (num_gen1_plugs * bucket_size)))

                # if (line.find("g0P:") != -1):
                #     num_gen0_big_objects_str = parse_str_no_end(remaining_str, "g0P: ")
                #     num_gen0_big_objects = int (num_gen0_big_objects_str)
                #     gen0_big_objects_per_gc[b] = num_gen0_big_objects

                if (line.find("TB: ") != -1):
                    num_tb_str = parse_str_no_end(remaining_str, "TB: ")
                    num_tb = int (num_tb_str)
                    gen2_threaded_back_per_gc[b] = num_tb
                    
                # print("b{0} size: {1}: F: {2}, consumed F: {3}, P: {4}, TB: {5}".format(
                #         b, bucket_str,
                #         gen2_free_spaces_per_gc[b],
                #         gen2_free_spaces_consumed_per_gc[b],
                #         gen1_plugs_per_gc[b], 
                #         gen2_threaded_back_per_gc[b]))

            # [23400]GC#29051(1196,61)(gen1) took 7ms(elapsed: 435028308, 5196s, 86min) (alloc: 178796mb, 322mb)
            # NOTE this line is before *EGC* so we'll decide then which array to add the pause time to.
            elif (line.find("(elapsed: ") != -1):
                eph_pause_ms_str, remaining_str = parse_str(line, "took ", "ms")
                eph_pause_ms = int (eph_pause_ms_str)

                elapsed_s_str, remaining_str = parse_str(remaining_str, ", ", "s")
                last_elapsed_s = int (elapsed_s_str)

                elapsed_min_str, remaining_str = parse_str(remaining_str, ", ", "min")
                elapsed_min = int (elapsed_min_str)
                if (found_first_elapsed_p == 0):
                    first_elapsed_min = elapsed_min
                    found_first_elapsed_p = 1
                last_elapsed_min = elapsed_min

                alloc_soh_str, remaining_str = parse_str(remaining_str, "alloc: ", "mb")
                alloc_soh_mb = int(alloc_soh_str)
                if (found_first_alloc_soh_p == 0):
                    first_alloc_soh_mb = alloc_soh_mb
                    found_first_alloc_soh_p = 1
                last_alloc_soh_mb = alloc_soh_mb

                alloc_loh_str, remaining_str = parse_str(remaining_str, " ", "mb")
                alloc_loh_mb = int(alloc_loh_str)
                if (found_first_alloc_loh_p == 0):
                    first_alloc_loh_mb = alloc_loh_mb
                    found_first_alloc_loh_p = 1
                last_alloc_loh_mb = alloc_loh_mb

            # [45892]g2 fla effi: 99%, effi: 95% (0,0), 2304ns(802)
            elif (line.find("effi: ") != -1):
                if (line.find("ns(") != -1):
                    gen1_plan_ns_str, remaining_str = parse_str(line, "), ", "ns")
                    gen1_plan_ns = int (gen1_plan_ns_str)
                    gen1_plan_ns_info.append(gen1_plan_ns)

                    gen1_plugs_str, remaining_str = parse_str(remaining_str, "(", ")")
                    gen1_plugs_tried_in_gen2_per_gc = int (gen1_plugs_str)
                    gen1_plugs_tried_in_gen2_info.append(gen1_plugs_tried_in_gen2_per_gc)

                    if (gen1_plugs_tried_in_gen2_per_gc == 0):
                        gen1_np_plan_ns_info.append(gen1_plan_ns)
                    
                    # print("gen1 plan {0}ns".format(gen1_plan_ns))

            # [40496][END][g1]g1:, s: 245568, frag: 0(L: 0, O: 0), f: 0% (C)   NP
            # when we detect that we did not promote, we want to get how much gen1 survived
            elif (line.find("[END][g1]g1:") != -1):
                if (gen1_plugs_tried_in_gen2_per_gc == 0):
                    gen1_size_str, remaining_str = parse_str(line, "s: ", ",")
                    gen1_size_np = int (gen1_size_str)

                    gen1_frag_str, remaining_str = parse_str(remaining_str, "frag: ", "(")
                    gen1_frag_np = int(gen1_frag_str)
                    gen1_surv_size_np = gen1_size_np - gen1_frag_np

                    gen1_np_size_info.append(gen1_surv_size_np)

            # [102864][Bsw][h0][BGC#13]gen2: 2^14: F: 0, P: 54
            elif (line.find("][Bsw][") != -1):
                if (line.find("2^") != -1):
                    bucket_str, remaining_str = parse_str(line, "2^", ":")
                else:
                    bucket_str, remaining_str = parse_str(line, "] ", ":")
                b = convert_bucket_index(bucket_str)

                num_gen2_free_spaces_str, remaining_str = parse_str(remaining_str, "F: ", ",")
                num_gen2_free_spaces = int(num_gen2_free_spaces_str)

                # print("{0}: b {1}".format(line, b))

                gen2_free_spaces_per_gc[b] = num_gen2_free_spaces

                # print("2^{0}: F: {1}".format(
                #         (b + 8),
                #         gen2_free_spaces_per_gc[b]))

            elif (line.find(" surv: ") != -1):
                surv_gen_num = 0
                if (line.find("g1") != -1):
                    surv_gen_num = 1
                
                eph_surv_str, remaining_str = parse_str(line, "surv: ", " ")
                eph_surv_per_gc[surv_gen_num] = int(eph_surv_str)
                
                eph_alloc_str, remaining_str = parse_str(remaining_str, "alloc: ", " ")
                eph_alloc_per_gc[surv_gen_num] = int(eph_alloc_str)

            # 
            # [102864]*EGC* 13(gen0:14)(2)(BGC)
            # [31608]*EGC* 15(gen0:15)(1)(GC)
            elif (line.find("*EGC*") != -1):
                gen_end_index_str, remaining_str = parse_str(line, "*EGC* ", "(")
                gen_end_index = int(gen_end_index_str)
                gen_end_num_str, remaining_str = parse_str(remaining_str, ")(", ")")
                gen_end_num = int(gen_end_num_str)

                if (gen_end_num < 2):                    
                    eph_surv_info.append(eph_surv_data(
                            gen_end_index,
                            gen_end_num,
                            eph_alloc_per_gc[0],
                            eph_surv_per_gc[0],
                            eph_alloc_per_gc[1],
                            eph_surv_per_gc[1]))

                    # intentionally not clearing so we get a smoother line
                    # clear_array(eph_alloc_per_gc, 2)
                    # clear_array(eph_surv_per_gc, 2)

                if (gen_end_num == 0):
                    gen0_pause_ms_info.append(eph_pause_ms)
                    num_gen0_gcs = num_gen0_gcs + 1 
                    continue

                gen_end_type_str, remaining_str = parse_str(remaining_str, ")(", ")")
                gen_end_type = convert_gen_type(gen_end_type_str)
                if (gen_end_num == 1):
                    gen1_pause_ms_info.append(eph_pause_ms)                        
                    num_gen1_gcs = num_gen1_gcs + 1
                    if (fgc_before_bgc):
                        gen_end_type = TYPE_FGC_BEFORE_BGC

                gen2_size_increase_info.append(gen2_increase_data(
                                    gen_end_index,
                                    gen_end_num,
                                    bgc_state,
                                    gen2_fl_ratio,
                                    gen2_fl_size,
                                    gen2_size_increase,
                                    gen1_plugs_tried_in_gen2_per_gc,
                                    gen2_fl_allocated_per_gc,
                                    gen2_es_allocated_per_gc,
                                    gen2_c_allocated_per_gc,
                                    gen1_plan_ns,
                                    last_alloc_soh_mb,
                                    last_elapsed_s))
                
                gen2_free_spaces_info[num_gen1_gen2_gcs] = gen2_free_spaces_per_gc[:]
                gen2_free_spaces_consumed_info[num_gen1_gen2_gcs] = gen2_free_spaces_consumed_per_gc[:]
                gen1_objs_info[num_gen1_gen2_gcs] = gen1_objs_per_gc[:]
                gen1_plugs_info[num_gen1_gen2_gcs] = gen1_plugs_per_gc[:]
                gen2_tb_info[num_gen1_gen2_gcs] = gen2_threaded_back_per_gc[:]
                gen1_unfit_plugs_info[num_gen1_gen2_gcs] = gen1_unfit_plugs_per_gc[:]
                gen0_big_objects_info[num_gen1_gen2_gcs] = gen0_big_objects_per_gc[:]
                
                # print("GC#{0} gen{1}, type {2}, fl size: {3}, fl ratio:{4}, size inc {5}".format(
                #                     gen_end_index,
                #                     gen_end_num,
                #                     gen_end_type,
                #                     gen2_fl_size,
                #                     gen2_fl_ratio,
                #                     gen2_size_increase))

                # re-init
                gen2_size_increase = 0
                gen2_fl_ratio = 0
                gen2_fl_size = 0
                gen1_plugs_tried_in_gen2_per_gc = 0
                gen1_plan_ns = 0
                clear_array(gen2_free_spaces_per_gc, total_num_buckets)
                clear_array(gen2_free_spaces_consumed_per_gc, total_num_buckets)
                clear_array(gen1_objs_per_gc, total_num_buckets)
                clear_array(gen1_plugs_per_gc, total_num_buckets)
                clear_array(gen1_unfit_plugs_per_gc, total_num_buckets)
                clear_array(gen0_big_objects_per_gc, total_num_buckets)
                clear_array(gen2_threaded_back_per_gc, total_num_buckets)

                num_gen1_gen2_gcs = num_gen1_gen2_gcs + 1
                # if (num_gen1_gen2_gcs > 5) :
                #     break
        
    total_gen0_pause_ms = 0
    for gen0_index in range (0, num_gen0_gcs):
        total_gen0_pause_ms = total_gen0_pause_ms + gen0_pause_ms_info[gen0_index]
    
    total_gen1_pause_ms = 0
    total_gen1_plan_ns = 0
    # plugs we tried to allocate in older
    total_gen1_plugs_tried = 0

    print("{0} gen0 pause info recorded, {1} gen1 pause info recorded".format(
        len(gen0_pause_ms_info),
        len(gen1_pause_ms_info)))

    print("{0} gen1 plan recorded".format(len(gen1_plan_ns_info)))

    for gen1_index in range (0, num_gen1_gcs):
        total_gen1_pause_ms = total_gen1_pause_ms + gen1_pause_ms_info[gen1_index]
        total_gen1_plan_ns = total_gen1_plan_ns + gen1_plan_ns_info[gen1_index]
        total_gen1_plugs_tried = total_gen1_plugs_tried + gen1_plugs_tried_in_gen2_info[gen1_index]

    total_eph_pause_ms = total_gen0_pause_ms + total_gen1_pause_ms

    total_gen1_plan_ms = total_gen1_plan_ns / 1000

    # usually we have more than 1ms worth of plan time...this is just for small testing logs
    if (total_gen1_plan_ms == 0):
        total_gen1_plan_ms = 1

    total_elapsed_min = last_elapsed_min - first_elapsed_min
    total_alloc_soh_mb = last_alloc_soh_mb - first_alloc_soh_mb
    total_alloc_loh_mb = last_alloc_loh_mb - first_alloc_loh_mb
    soh_mb_per_min = 0
    loh_mb_per_min = 0

    eph_pause_ratio = 0
    if (total_elapsed_min != 0):
        soh_mb_per_min = total_alloc_soh_mb / total_elapsed_min
        loh_mb_per_min = total_alloc_loh_mb / total_elapsed_min
        eph_pause_ratio = (total_eph_pause_ms / 10.0 / 60.0) / total_elapsed_min

    print("GC#{0} - GC#{1} ({2} GCs total, {3}mins (eph pause: {4}min ({5:.2f}%), soh alloc: {6}mb({7}mb/min), loh alloc: {8}mb({9}mb/min))".format (
        first_gc_index, last_gc_index, (last_gc_index - first_gc_index),
        total_elapsed_min,
        (total_eph_pause_ms / 1000 / 60),
        eph_pause_ratio,
        total_alloc_soh_mb,
        soh_mb_per_min,
        total_alloc_loh_mb,
        loh_mb_per_min))

    print("{0} gen0s {1}ms ({2}ms/gc), {3} gen1s {4}ms ({5}ms/gc) gen1 plan: {6}ms ({7:.2f}%), {8} plugs tried - {9} plugs/ms".format(
        num_gen0_gcs, 
        total_gen0_pause_ms, 
        (total_gen0_pause_ms / num_gen0_gcs),
        num_gen1_gcs,
        total_gen1_pause_ms,
        (total_gen1_pause_ms / num_gen1_gcs),
        total_gen1_plan_ms,
        (0 if (total_gen1_pause_ms == 0) else (total_gen1_plan_ms * 100 / total_gen1_pause_ms)),
        total_gen1_plugs_tried, 
        (0 if (total_gen1_plan_ms == 0) else (total_gen1_plugs_tried / total_gen1_plan_ms))))

    total_gen1_np = len(gen1_np_plan_ns_info)
    total_gen1_np_plan_ns = 0
    for gen1_index in range (0, total_gen1_np):
        total_gen1_np_plan_ns = total_gen1_np_plan_ns + gen1_np_plan_ns_info[gen1_index]
    
    total_gen1_np_plan_ms = total_gen1_np_plan_ns / 1000
    total_gen1_p_plan_ms = total_gen1_plan_ms - total_gen1_np_plan_ms
    print("{0} gen1 didn't promote ({1:.2f}% total gen1s), {2} ms in plan ({3:.2f}% total plan, in promoting gen1 {4} plugs/ms".format(
        total_gen1_np, 
        (total_gen1_np * 100.0 / num_gen1_gcs),
        total_gen1_np_plan_ms, 
        (total_gen1_np_plan_ms * 100.0 / total_gen1_plan_ms),
        (0 if (total_gen1_p_plan_ms == 0) else (total_gen1_plugs_tried / total_gen1_p_plan_ms))))

    return eph_surv_info, total_gen0_plugs, total_gen0_objs, total_gen0_allocated_big_objs, num_gen1_gen2_gcs, gen2_size_increase_info, gen2_free_spaces_info, gen2_free_spaces_consumed_info, gen1_objs_info, gen1_plugs_info, gen1_unfit_plugs_info, gen0_big_objects_info, gen2_tb_info


g_num_gen1_gen2_gcs = 0
g_eph_surv_info = []
g_gen2_size_increase_info = []
g_gen2_free_spaces_info = {}
g_gen2_free_spaces_consumed_info = {}
g_gen1_objs_info = {}
g_gen1_plugs_info = {}
g_gen1_unfit_plugs_info = {}
g_gen0_big_objects_info = {}
g_gen2_tb_info = {}

g_num_gen1_size_increased = 0
g_gen2_size_increased = 0

g_total_gen0_plugs = [0 for i in range(total_num_buckets)]
g_total_gen0_objs = [0 for i in range(total_num_buckets)]
g_total_gen0_allocated_big_objs = [0 for i in range(total_num_buckets)]

# counting all the plugs we observed in gen1
g_plug_buckets = [0 for i in range(total_num_buckets)]
g_obj_buckets = [0 for i in range(total_num_buckets)]
g_tb_buckets = [0 for i in range(total_num_buckets)]

# we only count these for when there are unfit plugs and
# we detect # of obj in a bucket is < # of plugs in that bucket
# which means plugs are made of multiple objs.
g_merged_plug_buckets = [0 for i in range(total_num_buckets)]
g_big_plug_buckets = [0 for i in range(total_num_buckets)]

# inc_file_name = "C:/exchange/3/normalized-new-gclog.57556.log"
# inc_file_name = "C:/exchange/4/new-gclog.62284.log"
# inc_file_name = "C:/exchange/5/new-gclog.65744.log"
# inc_file_name = "C:/exchange/6/new-gclog.31568.log"
inc_file_name = "C:/exchange/8/new-gclog.392.log"
# inc_file_name = "C:/exchange/8/more-logging-1/new-gclog.54216.log"
# inc_file_name = "C:/exchange/8/more-logging-1/test.txt"
# size_in_pow_2_p = 1

# NOTE: need to change the init for these logs!!!!
# inc_file_name = "C:/exchange/9/fix0/test.txt"
# inc_file_name = "C:/exchange/9/fix0/new-gclog.42264-last-58min.log"
# inc_file_name = "C:/exchange/9/fix0/run1/new-gclog.49780.log"
# inc_file_name = "C:/exchange/9/fix0/run2/new-gclog.50988.log"
# inc_file_name = "C:/exchange/9/fix0/simulator/new-gclog.15288.log"

# inc_file_name = "C:/exchange/9/fix0/fix1/test.txt"
# inc_file_name = "C:/exchange/9/fix0/fix1/new-gclog.39684.log"
# inc_file_name = "C:/exchange/9/fix0/fix1/morelogging/new-gclog.61452-last-58min.log"
# inc_file_name = "C:/exchange/9/fix0/fix1/morelogging1/new-gclog.60888.log"
# inc_file_name = "C:/exchange/9/fix0/fix1/morelogging1/run1/new-gclog.9372.log"
# inc_file_name = "C:/exchange/9/fix0/fix1/morelogging1/run1/test.txt"

# inc_file_name = "C:/exchange/9/fix0/fix1/morelogging/fix2/new-gclog.4412.log"

# for 9/fix0 - 100 buckets
# init_bucket_sizes_0()
# for 9/fix0/fix1 - 42 buckets
# init_size_buckets_1()

g_eph_surv_info, g_total_gen0_plugs, g_total_gen0_objs, g_total_gen0_allocated_big_objs, g_num_gen1_gen2_gcs, g_gen2_size_increase_info, g_gen2_free_spaces_info, g_gen2_free_spaces_consumed_info, g_gen1_objs_info, g_gen1_plugs_info, g_gen1_unfit_plugs_info, g_gen0_big_objects_info, g_gen2_tb_info = process_file_bgc_tuning_size_increase(inc_file_name)

g_num_eph_gcs = len(g_eph_surv_info)

print("in {0} total {1} gen1/2 GCs, {2} eph GCs".format(inc_file_name, g_num_gen1_gen2_gcs, g_num_eph_gcs))

# for i in range (0, g_num_eph_gcs):
#     print("GC#{0}, gen{1}, gen0 alloc {2:,}, surv {3:,}, gen1 alloc {4:,}, surv {5:,}".format(
#         g_eph_surv_info[i].gen_index,
#         g_eph_surv_info[i].gen_num,
#         g_eph_surv_info[i].gen0_alloc,
#         g_eph_surv_info[i].gen0_surv,
#         g_eph_surv_info[i].gen1_alloc,
#         g_eph_surv_info[i].gen1_surv))

total_weighted_g1_plugs_in_g2 = 0
total_weighted_g2_fl_consumed = 0

for i in range (0, g_num_gen1_gen2_gcs):
    if (1):
        if (g_gen2_size_increase_info[i].gen2_size_increase > 0):
            g_num_gen1_size_increased = g_num_gen1_size_increased + 1
        g_gen2_size_increased += g_gen2_size_increase_info[i].gen2_size_increase 
        # print("GC#{0} gen{1}, fl size: {2}, fl ratio:{3}, size inc {4}, bgs: {5}".format(
        #                         g_gen2_size_increase_info[i].gen_index,
        #                         g_gen2_size_increase_info[i].gen_num,
        #                         g_gen2_size_increase_info[i].gen2_fl_size,
        #                         g_gen2_size_increase_info[i].gen2_fl_ratio,
        #                         g_gen2_size_increase_info[i].gen2_size_increase,
        #                         g_gen2_size_increase_info[i].bgc_state))
        
        # print("{0:>7}|{1:>7}|{2:>5}|{3:>5}|{4:>5}|{5:>7}|{6:>7}".format(
        #     "size", "F", "O", "P", "UP", "G0", "TB"))
        
        count_weighted_p = 0
        if ((g_gen2_size_increase_info[i].gen2_size_increase == 0) and (g_gen2_size_increase_info[i].gen1_plugs_tried_in_gen2 > 0)):
            count_weighted_p = 1

        for b_index in range (0, total_num_buckets):
            if (count_weighted_p == 1):
                weighted_g2_fl_consumed = g_gen2_free_spaces_consumed_info[i][b_index] * convert_index_to_size(b_index)
                total_weighted_g2_fl_consumed += weighted_g2_fl_consumed

                weighted_g1_plugs_in_g2 = g_gen1_plugs_info[i][b_index] * convert_index_to_size(b_index)
                total_weighted_g1_plugs_in_g2 += weighted_g1_plugs_in_g2

                # if ((weighted_g2_fl_consumed > 0) or (weighted_g1_plugs_in_g2 > 0)):
                #     print("weighted g2 fl: {0}, g1 plugs: {1}, total is {2}, {3}".format(
                #         weighted_g2_fl_consumed, 
                #         weighted_g1_plugs_in_g2, 
                #         total_weighted_g2_fl_consumed,
                #         total_weighted_g1_plugs_in_g2))

            if ((g_gen1_unfit_plugs_info[i][b_index] != 0) or
                (g_gen1_plugs_info[i][b_index] != 0) or 
                (g_gen1_objs_info[i][b_index] != 0)):

                g_plug_buckets[b_index] = g_plug_buckets[b_index] + g_gen1_plugs_info[i][b_index]
                g_obj_buckets[b_index] = g_obj_buckets[b_index] + g_gen1_objs_info[i][b_index]
                g_tb_buckets[b_index] = g_tb_buckets[b_index] + g_gen2_tb_info[i][b_index]

                multiple_objs_in_plug_str = ""

                if (g_gen1_unfit_plugs_info[i][b_index] != 0):
                    if (g_gen1_objs_info[i][b_index] < g_gen1_plugs_info[i][b_index]):
                        multiple_objs_in_plug_str = "Plug with MULTIPLE objs"
                        g_merged_plug_buckets[b_index] = g_merged_plug_buckets[b_index] + g_gen1_plugs_info[i][b_index]
                    else:
                        multiple_objs_in_plug_str = "Plug with BIG objs"
                        g_big_plug_buckets[b_index] = g_big_plug_buckets[b_index] + g_gen1_plugs_info[i][b_index]

                # print("{0:7}|{1:7}|{2:5}|{3:5}|{4:5}|{5:>7}|{6:>7}|{7}".format(
                #     size_buckets[b_index],
                #     g_gen2_free_spaces_info[i][b_index],
                #     g_gen1_objs_info[i][b_index],
                #     g_gen1_plugs_info[i][b_index],
                #     g_gen1_unfit_plugs_info[i][b_index],
                #     g_gen0_big_objects_info[i][b_index],
                #     g_gen2_tb_info[i][b_index],
                #     multiple_objs_in_plug_str))

print("{0} gen1 GCs inc gen2 by {1}".format(
    g_num_gen1_size_increased, g_gen2_size_increased))

print("during gen1s that didn't inc gen2, total weighted g1 plugs: {0:,}, consumed fl space: {1:,}, ratio: {2:.3f}".format(
    total_weighted_g1_plugs_in_g2,
    total_weighted_g2_fl_consumed,
    (float(total_weighted_g1_plugs_in_g2) / float(total_weighted_g2_fl_consumed))))

print("{0:>7}|{1}".format(
    "size", "# unfit merged plugs observed in inc GCs"))
for b_index in range (0, total_num_buckets):
    if (g_merged_plug_buckets[b_index] > 0):
        print("{0:7}|{1:7}".format(
            size_buckets[b_index],
            g_merged_plug_buckets[b_index]))

print("{0:>7}|{1}".format(
    "size", "# unfit big plugs observed in inc GCs"))
for b_index in range (0, total_num_buckets):
    if (g_big_plug_buckets[b_index] > 0):
        print("{0:7}|{1:7}".format(
            size_buckets[b_index],
            g_big_plug_buckets[b_index]))

print("{0:>7}|{1:>7}|{2:>7}|{3:>7}".format(
    "size", "plugs", "objs", "tb"))
for b_index in range (0, total_num_buckets):
    if ((g_plug_buckets[b_index] > 0) or 
        (g_obj_buckets[b_index] > 0) or 
        (g_tb_buckets[b_index] > 0)):
        print("{0:7}|{1:7}|{2:>7}|{3:>7}".format(
            size_buckets[b_index],
            g_plug_buckets[b_index],
            g_obj_buckets[b_index], 
            g_tb_buckets[b_index]))

print("{0:>7}|{1:>10}|{2:>10}|{3:>10}".format(
    "size", "g0 plugs", "g0 objs", "g0allocated large objs"))
for b_index in range (0, total_num_buckets):
    if ((g_total_gen0_plugs[b_index] > 0) or
        (g_total_gen0_objs[b_index] > 0) or
        (g_total_gen0_allocated_big_objs[b_index] > 0)):
        print("{0:7}|{1:10}|{2:>10}|{3:>10}".format(
            size_buckets[b_index],
            g_total_gen0_plugs[b_index],
            g_total_gen0_objs[b_index], 
            g_total_gen0_allocated_big_objs[b_index]))

#%%

total_num_recording_buckets = 105
recording_bucket_sizes = [0 for i in range(total_num_recording_buckets)]

def convert_recording_bucket_index(bucket_str):
    bucket_size = int(bucket_str)
    for i in range(0, total_num_recording_buckets):
        if (bucket_size == recording_bucket_sizes[i]):
            return i
    print("what?! {0} isn't valid".format(bucket_str))

def print_recording_buckets(buckets):
    for i in range(0, total_num_recording_buckets):
        print("b#{0}: {1} - {2}".format(i, recording_bucket_sizes[i], buckets[i]))

def init_recording_buckets():

    current_bucket_index = 0
    s = 128
    last_bucket_min_size = 648 * 1024

    while (s < last_bucket_min_size):
        if (s < 8 * 1024):
            recording_bucket_sizes[current_bucket_index] = s
            s += 128
        elif (s < 16 * 1024):
            recording_bucket_sizes[current_bucket_index] = s
            s += 1024
        elif (s < 128 * 1024):
            recording_bucket_sizes[current_bucket_index] = s
            s += 4 * 1024
        else:
            recording_bucket_sizes[current_bucket_index] = s
            s += s >> 1

        current_bucket_index += 1

    recording_bucket_sizes[current_bucket_index] = s

    # bucket 104 is the last bucket and it doesn't have a max 
    # size associated with it. but we need it for printing so
    # set it to 1mb
    current_bucket_index += 1
    recording_bucket_sizes[current_bucket_index] = 1024 * 1024
    current_bucket_index += 1

    # last_size = 0
    # for i in range (0, current_bucket_index):
    #     current_bucket_size = recording_bucket_sizes[i]
    #     print("b#{0}: {1}(last + {2})".format(i, current_bucket_size,
    #         (current_bucket_size - last_size)))
    #     last_size = current_bucket_size


def process_file_bgc_gc1 (file_name):

    bgc_free_space_bucket_counts = [0 for i in range(total_num_recording_buckets)]
    # this is what we allocated into gen2 from gen1
    gc1_plug_bucket_counts = [0 for i in range(total_num_recording_buckets)]
    # records the very last BGC sweep we see in the file
    last_bgc_sweep_line_num = 0

    bgc_surv = 0
    bgc_total_size = 0
    bgc_fl = 0
    bgc_fo = 0

    gc_timestamp_s = 0
    soh_alloc_mb = 0
    loh_alloc_mb = 0

    with open(file_name, "r") as pause_file:
        lines = pause_file.readlines()
        #for line in pause_file: 
        for i in range(0, len(lines)):
            line = lines[i]

            if (line.find("]end of bgc sweep: ") != -1):
                last_bgc_sweep_line_num = i

            # parse this line
            # [73576]GC#61632(1949,123)(gen0) took 3ms(elapsed: 1574564594, 11374s, 189min) (alloc: 379613mb, 354mb)
            elif(line.find("(elapsed: ") != -1):
                gc_timestamp_s_str, remaining_str = parse_str(line, ", ", "s")                
                gc_timestamp_s = int(gc_timestamp_s_str)

                soh_alloc_mb_str, remaining_str = parse_str(remaining_str, "alloc: ", "mb")
                soh_alloc_mb = int(soh_alloc_mb_str)

                loh_alloc_mb_str, remaining_str = parse_str(remaining_str, " ", "mb")
                loh_alloc_mb = int(loh_alloc_mb_str)

    # print("last bgc sweep observed at line {0}, opening file again".format(last_bgc_sweep_line_num))

    # opening file again
    with open(file_name, "r") as pause_file:
        lines = pause_file.readlines()
        #for line in pause_file: 
        for i in range(last_bgc_sweep_line_num, len(lines)):
            line = lines[i]

            if (line.find("2F: ") != -1):
                bucket_size_str, remaining_str = parse_str(line, " ", ":")
                bucket_size = int(bucket_size_str)

                bucket_index = convert_recording_bucket_index(bucket_size)
                
                bgc_free_space_counts_str, remaining_str = parse_str(remaining_str, "2F: ", ",")
                bgc_free_space_counts =  int(bgc_free_space_counts_str)

                bgc_free_space_bucket_counts[bucket_index] = bgc_free_space_counts

                gc1_plug_counts_str, remaining_str = parse_str(remaining_str, "1P: ", ")")
                gc1_plug_counts = int(gc1_plug_counts_str)

                gc1_plug_bucket_counts[bucket_index] = gc1_plug_counts

            # parse this line to print out some info about gen2
            # [35820]h0 g2 surv: 316220408 current: 316220432 alloc: 8514792 (96%) f: 180% new-size: 564412648 new-alloc: 248192216
            elif (line.find("g2 surv") != -1):
                bgc_surv_str, remaining_str = parse_str(line, "g2 surv: ", " ")
                bgc_surv = int(bgc_surv_str)

            # parse this line
            # [35820][END][g2]g2:, s: 393140432, frag: 76920000(L: 71701840, O: 5218160), f: 19% (S)   P
            elif (line.find("[END][g2]g2") != -1):
                bgc_total_size_str, remaining_str = parse_str(line, "s: ", ",")
                bgc_total_size = int(bgc_total_size_str)

                bgc_fl_str, remaining_str = parse_str(remaining_str, "L: ", ",")
                bgc_fl = int(bgc_fl_str)

                bgc_fo_str, remaining_str = parse_str(remaining_str, "O: ", ")")
                bgc_fo = int(bgc_fo_str)

    print("{0} last bgc".format(file_name))
    print("size: {0:,}, FL: {1:,}, FO: {2:,}, surv: {3:,}, size-fo-fl: {4:,}".format(
        bgc_total_size, bgc_fl, bgc_fo, bgc_surv, (bgc_total_size - bgc_fl - bgc_fo)))

    print("last GC at {0:,}s, soh alloc {1:,}mb, loh alloc {2:,}mb".format(
        gc_timestamp_s, soh_alloc_mb, loh_alloc_mb))

    # print("printing bgc free space counts from {0}".format(file_name))
    # print_recording_buckets(bgc_free_space_bucket_counts)    

    # print("printing g1 surv plug counts from {0}".format(file_name))
    # print_recording_buckets(gc1_plug_bucket_counts) 

    return bgc_free_space_bucket_counts, gc1_plug_bucket_counts, gc_timestamp_s, soh_alloc_mb, loh_alloc_mb

def get_alloc_info_for_gc (file_name, target_gc_timestamp_s):

    saved_gc_timestamp_s = 0
    saved_soh_alloc_mb = 0
    saved_loh_alloc_mb = 0
    
    print("looking for the last GC at {0:,}s in {1}".format(target_gc_timestamp_s, file_name))

    with open(file_name, "r") as pause_file:
        lines = pause_file.readlines()
        #for line in pause_file: 
        for i in range(0, len(lines)):
            line = lines[i]

            # parse this line
            # [73576]GC#61632(1949,123)(gen0) took 3ms(elapsed: 1574564594, 11374s, 189min) (alloc: 379613mb, 354mb)
            if(line.find("(elapsed: ") != -1):
                gc_timestamp_s_str, remaining_str = parse_str(line, ", ", "s")                
                gc_timestamp_s = int(gc_timestamp_s_str)

                # we wanna get the last GC with that timestamp
                if (gc_timestamp_s == (target_gc_timestamp_s + 1)):
                    # print("exiting at this line...found the first GC with {0:,}+1".format(target_gc_timestamp_s))
                    # print(line)
                    break

                soh_alloc_mb_str, remaining_str = parse_str(remaining_str, "alloc: ", "mb")
                soh_alloc_mb = int(soh_alloc_mb_str)

                loh_alloc_mb_str, remaining_str = parse_str(remaining_str, " ", "mb")
                loh_alloc_mb = int(loh_alloc_mb_str)

                saved_gc_timestamp_s = gc_timestamp_s
                saved_soh_alloc_mb = soh_alloc_mb
                saved_loh_alloc_mb = loh_alloc_mb

    print("found GC at {0:,}s, soh alloc {1:,}mb, loh alloc {2:,}mb".format(
        saved_gc_timestamp_s, saved_soh_alloc_mb, saved_loh_alloc_mb))

    return saved_soh_alloc_mb, saved_loh_alloc_mb

def process_file_bgc_gc1_comparison (file_name_0, file_name_1): 
    print("comparing {0} with {1}".format(file_name_0, file_name_1))
    bgc_free_space_bucket_counts_0, gc1_plug_bucket_counts_0, gc_timestamp_s_0, soh_alloc_mb_0, loh_alloc_mb_0 = process_file_bgc_gc1(file_name_0)
    bgc_free_space_bucket_counts_1, gc1_plug_bucket_counts_1, gc_timestamp_s_1, soh_alloc_mb_1, loh_alloc_mb_1 = process_file_bgc_gc1(file_name_1)

    reparse_file_name = file_name_0 if (gc_timestamp_s_0 > gc_timestamp_s_1) else file_name_1
    reparse_gc_timestamp_s = gc_timestamp_s_1 if (gc_timestamp_s_0 > gc_timestamp_s_1) else gc_timestamp_s_0

    reparse_soh_alloc_mb, reparse_loh_alloc_mb = get_alloc_info_for_gc (reparse_file_name, reparse_gc_timestamp_s)

    baseline_soh_alloc_mb = reparse_soh_alloc_mb if (gc_timestamp_s_0 > gc_timestamp_s_1) else soh_alloc_mb_0
    comparison_soh_alloc_mb = reparse_soh_alloc_mb if (gc_timestamp_s_0 < gc_timestamp_s_1) else soh_alloc_mb_1

    print("soh alloc 0: {0:,}mb, 1: {1:,}mb ({2:.2f}%)".format(
        baseline_soh_alloc_mb, comparison_soh_alloc_mb, 
        100.0 * (comparison_soh_alloc_mb - baseline_soh_alloc_mb) / baseline_soh_alloc_mb))

    baseline_loh_alloc_mb = reparse_loh_alloc_mb if (gc_timestamp_s_0 > gc_timestamp_s_1) else loh_alloc_mb_0
    comparison_loh_alloc_mb = reparse_loh_alloc_mb if (gc_timestamp_s_0 < gc_timestamp_s_1) else loh_alloc_mb_1

    print("loh alloc 0: {0:,}mb, 1: {1:,}mb ({2:.2f}%)".format(
        baseline_loh_alloc_mb, comparison_loh_alloc_mb, 
        100.0 * (comparison_loh_alloc_mb - baseline_loh_alloc_mb) / baseline_loh_alloc_mb))

    print("{0:10} | {1:10} | {2:10} | {3:10} | {4:10} | {5:10} | {6:10}".format(
        "size",
        "free0", "free1", "diff",
        "plug0", "plug1", "diff"))

    for i in range(0, total_num_recording_buckets):
        bgc_free_space_bucket_0 = bgc_free_space_bucket_counts_0[i]
        bgc_free_space_bucket_1 = bgc_free_space_bucket_counts_1[i]
        gc1_plug_bucket_0 = gc1_plug_bucket_counts_0[i]
        gc1_plug_bucket_1 = gc1_plug_bucket_counts_1[i]
        free1_is_bigger = (bgc_free_space_bucket_1 > bgc_free_space_bucket_0)
        bgc_free_space_bucket_diff = abs(bgc_free_space_bucket_1 - bgc_free_space_bucket_0)
        gc1_plug1_is_bigger = (gc1_plug_bucket_1 > gc1_plug_bucket_0)
        gc1_plug_bucket_diff = abs(gc1_plug_bucket_1 - gc1_plug_bucket_0)
        print("{0:10} | {1:10} | {2:10} | {3}{4:9} | {5:10} | {6:10} | {7}{8:9}".format(
            recording_bucket_sizes[i],
            bgc_free_space_bucket_0,
            bgc_free_space_bucket_1,
            ("+" if free1_is_bigger else "-"),
            bgc_free_space_bucket_diff,
            gc1_plug_bucket_0,
            gc1_plug_bucket_1,
            ("+" if gc1_plug1_is_bigger else "-"),
            gc1_plug_bucket_diff))

init_recording_buckets()

bgc_gc1_file_name_0 = "C:/exchange/8/8k-ac/gclog.73032.log"
bgc_gc1_file_name_1 = "C:/exchange/8/8k-no-padding-continous-ac/gclog.7428.log"
process_file_bgc_gc1_comparison(bgc_gc1_file_name_0, bgc_gc1_file_name_1)

#%%
import os

# parse the last 3 lines of the lastbuf.txt
# [13596][END][g0]g2:, s: 578459456, frag: 333606624(L: 331827616, O: 1779008), f: 57% (C)   P
# [13596][END][g0]g1:, s: 221992, frag: 0(L: 0, O: 0), f: 0% (C)   P
# [13596]*EGC* 283078(gen0:283078)(0)(GC)(0)(0)
def process_throughput_size(lastbuf_file_name):
    print("processing lastbuf file: {0}".format(lastbuf_file_name))
    with open(lastbuf_file_name, "r") as pause_file:
        lines = pause_file.readlines()
        #for line in pause_file: 
        # for i in range(0, len(lines)):
        #     line = lines[i]

            # if (line.find("]end of bgc sweep: ") != -1):
            #     last_bgc_sweep_line_num = i

        num_lines = len(lines)

        elapsed_time_line = lines[num_lines-4]
        soh_alloc_mb_str, remaining_str = parse_str (elapsed_time_line, "alloc: ", "mb")
        soh_alloc_mb = int(soh_alloc_mb_str)

        loh_alloc_mb_str, remaining_str = parse_str (remaining_str, " ", "mb")
        loh_alloc_mb = int(loh_alloc_mb_str)

        gen2_size_line = lines[num_lines-3]
        gen2_size_str, remaining_str = parse_str(gen2_size_line, "s: ", ",")
        gen2_size = int(gen2_size_str)

        last_gc_end_line = lines[num_lines-1]
        last_gc_index_str, remaining_str = parse_str(last_gc_end_line, "GC* ", "(")
        last_gc_index = int(last_gc_index_str)

    print("soh alloc: {0}mb, loh {1}mb, g2 {2:,}, last gc: {3}".format(
        soh_alloc_mb, loh_alloc_mb, gen2_size, last_gc_index))
    return soh_alloc_mb, loh_alloc_mb, gen2_size, last_gc_index

def process_output(file_name):
    print("processing output file: {0}".format(file_name))
    with open(file_name, "r") as pause_file:
        lines = pause_file.readlines()
        for i in range(0, len(lines)):
            line = lines[i]
            # print(line)
            if (line.find("10min elapsed") != -1):
                num_iterations_str, remaining_str = parse_str(line, "Iter ", ":")
                num_iterations = int(num_iterations_str)
                print("did {0:,} iterations".format(num_iterations))
                return num_iterations
    
    print("didn't find 10min elapsed line!!!!")

# lastbuf_file_name = "C:/exchange/combined/fix8-1k-nopad-nocon-ac-run0-lastbuf.txt"
# output_file_name = "C:/exchange/combined/fix8-1k-nopad-nocon-ac-run0-output.txt"
# process_throughput_size(lastbuf_file_name)
# process_output(output_file_name)

dir_to_process = "C:/exchange/combined/"
files = os.listdir(dir_to_process)
for f in files:
    print(f)
    # get the common part of the name and look for the other one
    common_file_name_str, remaining_str = parse_str(f, "/", ".")
    print(common_file_name_str)
    
    end_index = common_file_name_str.find("lastbuf") 
    str_to_ret = common_file_name_str[0:end_index]
    print(str_to_ret)

    output_file_name = dir_to_process + str_to_ret + "output.txt"
    


#%%
# chart the size inc info

def plot_inc_chart(inc_plt, num_elements, x_inc_data, y_inc_data, 
                 inc_legend, inc_color_index):
    #inc_plt.set_title(inc_title, loc='right')
    inc_plt.plot(x_inc_data, y_inc_data, 
        marker='.', 
        linestyle='-',
        color=total_colors[inc_color_index],
        label=inc_legend)
    #inc_plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
    inc_plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
    inc_plt.grid()

fig = plt.figure()

print("{0} total g1/2 GCs".format(g_num_gen1_gen2_gcs))

num_gc_plts = 4
gc_plts = [None]*num_gc_plts
for plt_index in range (0, num_gc_plts):
    gc_plts[plt_index] = fig.add_subplot(num_gc_plts, 1, (1 + plt_index))

# display GCs whose indices >= start_gc_index and <= end_gc_index
# start_gc_index = 800
# end_gc_index = g_gen2_size_increase_info[g_num_gen1_gen2_gcs - 1].gen_index

start_gc_index = 74000
end_gc_index = 80000

# first plot only gen1 GCs
x_gc_indices = [None]*g_num_gen1_gen2_gcs
y_gc_bgc_state = [None]*g_num_gen1_gen2_gcs
y_gc_gen2_size_inc = [None]*g_num_gen1_gen2_gcs
# on entry, gen2 fl and fl alloc
y_gc_gen2_fl_size = [None]*g_num_gen1_gen2_gcs
y_gc_gen2_fl_ratio = [None]*g_num_gen1_gen2_gcs
num_gcs_to_plot = 0
num_gen1s = 0
num_gen2s = 0
num_gen2_size_increased = 0
gen2_size_increased = 0

# print("{0:>7}|{1:>7}|{2:>5}|{3:>5}|{4:>5}".format(
#     "size", "Free", "Plug", "Unfit", "G0"))

gen0_index_last_bgc = max (g_gen2_size_increase_info[0].gen_index, start_gc_index)
# this is not strictly true...I am also including FGCs, but there are very few of them.
num_gen1s_between_bgc = 0
# this is not correct - but it's only incorrect for the first BGC..
gen2_fl_allocated_between_bgc = 0
gen2_es_allocated_between_bgc = 0
gen2_c_allocated_between_bgc = 0
soh_allocated_mb_last_bgc = g_gen2_size_increase_info[0].soh_allocated_mb_so_far
elapsed_s_last_bgc = g_gen2_size_increase_info[0].elapsed_s

for i in range (0, g_num_gen1_gen2_gcs):
    if ( (g_gen2_size_increase_info[i].gen_index >= start_gc_index) and
       (g_gen2_size_increase_info[i].gen_index <= end_gc_index)):
        x_gc_indices[num_gcs_to_plot] = g_gen2_size_increase_info[i].gen_index
        y_gc_bgc_state[num_gcs_to_plot] = g_gen2_size_increase_info[i].bgc_state
        # if (g_gen2_size_increase_info[i].bgc_state == 0):
        # if (1):
        #     print("GC#{0} bgc state {1}, inc-ed {2:,}".format(
        #         g_gen2_size_increase_info[i].gen_index,
        #         g_gen2_size_increase_info[i].bgc_state,
        #         g_gen2_size_increase_info[i].gen2_size_increase))

        y_gc_gen2_size_inc[num_gcs_to_plot] = g_gen2_size_increase_info[i].gen2_size_increase

        # if (g_gen2_size_increase_info[i].gen2_size_increase > 0):
        if (1):
            if (g_gen2_size_increase_info[i].gen_num == 2):
                num_gen0s_before_bgc = g_gen2_size_increase_info[i].gen_index - gen0_index_last_bgc - num_gen1s_between_bgc
                soh_allocated_mb_during_bgc = g_gen2_size_increase_info[i - 1].soh_allocated_mb_so_far - soh_allocated_mb_last_bgc
                # print("soh alloc during last BGC and {0} is {1} - {2} mb".format(
                #     g_gen2_size_increase_info[i - 1].gen_index,
                #     g_gen2_size_increase_info[i - 1].soh_allocated_mb_so_far,
                #     soh_allocated_mb_last_bgc))

                elapsed_s_during_bgc = g_gen2_size_increase_info[i - 1].elapsed_s - elapsed_s_last_bgc
                print("---------BGC#{0}(FL: {1:10,} bytes {2}%) {3} gen0s, {4} gen1s (g0:g1 {5}:1), {6} mb gen0 alloc, {7}s ({8}min), fla {9:,}, esa {10:,}, ca {11:,} since last bgc--------------".format(
                    g_gen2_size_increase_info[i].gen_index,
                    g_gen2_size_increase_info[i].gen2_fl_size,
                    g_gen2_size_increase_info[i].gen2_fl_ratio,
                    num_gen0s_before_bgc,
                    num_gen1s_between_bgc,
                    (num_gen0s_before_bgc / num_gen1s_between_bgc),
                    soh_allocated_mb_during_bgc,
                    elapsed_s_during_bgc,
                    (elapsed_s_during_bgc / 60),
                    gen2_fl_allocated_between_bgc,
                    gen2_es_allocated_between_bgc,
                    gen2_c_allocated_between_bgc))

                gen0_index_last_bgc = g_gen2_size_increase_info[i].gen_index
                gen2_fl_allocated_between_bgc = 0
                gen2_es_allocated_between_bgc = 0
                gen2_c_allocated_between_bgc = 0
                soh_allocated_mb_last_bgc = g_gen2_size_increase_info[i].soh_allocated_mb_so_far
                elapsed_s_last_bgc = g_gen2_size_increase_info[i].elapsed_s
                # print("setting soh to GC#{0} {1}mb".format(g_gen2_size_increase_info[i].gen_index, 
                #     g_gen2_size_increase_info[i].soh_allocated_mb_so_far))

                num_gen1s_between_bgc = 0
            else:
                num_gen1s_between_bgc = num_gen1s_between_bgc + 1
                gen2_fl_allocated_between_bgc = gen2_fl_allocated_between_bgc + g_gen2_size_increase_info[i].gen2_fl_allocated
                gen2_es_allocated_between_bgc = gen2_es_allocated_between_bgc + g_gen2_size_increase_info[i].gen2_es_allocated
                gen2_c_allocated_between_bgc = gen2_c_allocated_between_bgc + g_gen2_size_increase_info[i].gen2_c_allocated
                if (g_gen2_size_increase_info[i].gen2_size_increase > 0):
                    num_gen2_size_increased = num_gen2_size_increased + 1
                    gen2_size_increased = gen2_size_increased + g_gen2_size_increase_info[i].gen2_size_increase

                    # print("---------GC#{0}(bgc:{1:2}) INC {2:10,} bytes (FL: {3:10,} bytes {4}%)".format(
                    # g_gen2_size_increase_info[i].gen_index,
                    # g_gen2_size_increase_info[i].bgc_state,
                    # g_gen2_size_increase_info[i].gen2_size_increase,
                    # g_gen2_size_increase_info[i].gen2_fl_size,
                    # g_gen2_size_increase_info[i].gen2_fl_ratio))

                    # print("{0:>7}|{1:>7}|{2:>5}|{3:>5}|{4:>5}".format(
                    #     "size", "Free", "Plug", "Unfit", "G0"))
                    # print("{0:>7}|{1:>7}|{2:>5}|{3:>5}".format(
                    #     "size", "Free", "Plug", "Unfit"))

                    # for b_index in range (0, total_num_buckets):
                    #     if (g_gen1_unfit_plugs_info[i][b_index] != 0):
                    #         # print("{0:>7}|{1:>7}|{2:>5}|{3:>5}|{4:>5}".format(
                    #         print("{0:>7}|{1:>7}|{2:>5}|{3:>5}".format(
                    #             size_buckets[b_index],
                    #             g_gen2_free_spaces_info[i][b_index],
                    #             g_gen1_plugs_info[i][b_index],
                    #             g_gen1_unfit_plugs_info[i][b_index]))
                    #             # g_gen0_big_objects_info[i][b_index]))
                    
        if (g_gen2_size_increase_info[i].gen_num == 1): 
            num_gen1s += 1
        else:
            num_gen2s += 1
        y_gc_gen2_fl_size[num_gcs_to_plot] = g_gen2_size_increase_info[i].gen2_fl_size
        y_gc_gen2_fl_ratio[num_gcs_to_plot] = g_gen2_size_increase_info[i].gen2_fl_ratio
        num_gcs_to_plot += 1
    # elif (g_gen2_size_increase_info[i].gen_num == 2):
    #     print("BGC#{0}".format(g_gen2_size_increase_info[i].gen_index))

print("{0} gen1s (gen2 increased in {1} by {2} bytes), {3} gen2s, {4} gcs to plot".format(
        num_gen1s,
        num_gen2_size_increased,
        gen2_size_increased,
        num_gen2s,
        num_gcs_to_plot))

x_gc_indices_to_plot = x_gc_indices[:num_gcs_to_plot]
y_gc_bgc_state_to_plot = y_gc_bgc_state[:num_gcs_to_plot]
y_gc_gen2_size_inc_to_plot = y_gc_gen2_size_inc[:num_gcs_to_plot]
y_gc_gen2_fl_to_plot = y_gc_gen2_fl_size[:num_gcs_to_plot]
y_gc_gen2_fl_ratio_to_plot = y_gc_gen2_fl_ratio[:num_gcs_to_plot]

plot_inc_chart(gc_plts[0], num_gcs_to_plot, x_gc_indices_to_plot, 
                y_gc_bgc_state_to_plot, "bgc state", 1)
plot_inc_chart(gc_plts[1], num_gcs_to_plot, x_gc_indices_to_plot, 
                y_gc_gen2_size_inc_to_plot, "g2 inc", 0)
plot_inc_chart(gc_plts[2], num_gcs_to_plot, x_gc_indices_to_plot, 
                y_gc_gen2_fl_to_plot, "g2 fl", 1)
plot_inc_chart(gc_plts[3], num_gcs_to_plot, x_gc_indices_to_plot, 
                y_gc_gen2_fl_ratio_to_plot, "g2 fl ratio", 0)

#%%

# # this is an attempt to draw a smooth line...but unfortunately
# # the thing gets memory error very easily with a slight large data set.
# from scipy.interpolate import spline
# x = np.array(x_gc_indices_to_plot)
# y = np.array(y_gc_gen0_surv_to_plot)
# # x = np.array([1, 2, 3, 4])
# # y = np.array([4, 10, 8, 11])
# x_smooth = np.linspace(x.min(), x.max(), 100)
# y_smooth = spline(x, y, x_smooth)
# plt.plot(x_smooth, y_smooth)
# # plt.plot(x, y)

def plot_surv_chart(inc_plt, num_elements, x_inc_data, y_inc_data, 
                 inc_legend, inc_color_index):
    #inc_plt.set_title(inc_title, loc='right')
    inc_plt.plot(x_inc_data, y_inc_data, 
        marker='.', 
        linestyle='-',
        color=total_colors[inc_color_index],
        label=inc_legend)
    #inc_plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
    inc_plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
    inc_plt.grid()

fig = plt.figure()

print("{0} total eph GCs".format(g_num_eph_gcs))

num_gc_plts = 4
gc_plts = [None]*num_gc_plts
for plt_index in range (0, num_gc_plts):
    gc_plts[plt_index] = fig.add_subplot(num_gc_plts, 1, (1 + plt_index))

# display GCs whose indices >= start_gc_index and <= end_gc_index
# end_gc_index = g_eph_surv_info[g_num_eph_gcs - 1].gen_index
start_gc_index = 70000
end_gc_index = 80000

# this is my primitive smoothing - there are 
# too many data points, we average every 100 elements
stepping = 500

num_gcs_to_plot = 0

total_num_data_points = g_num_eph_gcs / stepping
x_gc_indices = [0 for i in range(total_num_data_points)]
y_gc_gen0_alloc = [0 for i in range(total_num_data_points)]
y_gc_gen0_surv = [0 for i in range(total_num_data_points)]
y_gc_gen1_alloc = [0 for i in range(total_num_data_points)]
y_gc_gen1_surv = [0 for i in range(total_num_data_points)]

num_data_points = 0
total_num_data_points = 0
gc_indices_sum = 0
gen0_alloc_sum = 0
gen0_surv_sum = 0
gen1_alloc_sum = 0
gen1_surv_sum = 0

for i in range (0, g_num_eph_gcs):
    
    if ( (g_eph_surv_info[i].gen_index >= start_gc_index) and
       (g_eph_surv_info[i].gen_index <= end_gc_index)):

        gc_indices_sum  = gc_indices_sum + g_eph_surv_info[i].gen_index
        gen0_alloc_sum = gen0_alloc_sum + g_eph_surv_info[i].gen0_alloc
        gen0_surv_sum = gen0_surv_sum + g_eph_surv_info[i].gen0_surv
        gen1_alloc_sum = gen1_alloc_sum + g_eph_surv_info[i].gen1_alloc
        gen1_surv_sum = gen1_surv_sum + g_eph_surv_info[i].gen1_surv
        
        # print("GC#{0} gen0 surv {1:,} -> {2:,}".format(
        #     g_eph_surv_info[i].gen_index, 
        #     g_eph_surv_info[i].gen0_surv,
        #     gen0_surv_sum))

        num_data_points = num_data_points + 1
        total_num_data_points = total_num_data_points + 1

        if (num_data_points >= stepping):
            x_gc_indices[num_gcs_to_plot] = gc_indices_sum / stepping
            y_gc_gen0_alloc[num_gcs_to_plot] = gen0_alloc_sum / stepping
            y_gc_gen0_surv[num_gcs_to_plot] = gen0_surv_sum / stepping
            y_gc_gen1_alloc[num_gcs_to_plot] = gen1_alloc_sum / stepping
            y_gc_gen1_surv[num_gcs_to_plot] = gen1_surv_sum / stepping

            num_gcs_to_plot += 1

            num_data_points = 0
            gc_indices_sum = 0
            gen0_alloc_sum = 0
            gen0_surv_sum = 0
            gen1_alloc_sum = 0
            gen1_surv_sum = 0


print("we had {0:,} GCs, plotting {1} data points".format(
    total_num_data_points, num_gcs_to_plot))

x_gc_indices_to_plot = x_gc_indices[:num_gcs_to_plot]
y_gc_gen0_alloc_to_plot = y_gc_gen0_alloc[:num_gcs_to_plot]
y_gc_gen0_surv_to_plot = y_gc_gen0_surv[:num_gcs_to_plot]
y_gc_gen1_alloc_to_plot = y_gc_gen1_alloc[:num_gcs_to_plot]
y_gc_gen1_surv_to_plot = y_gc_gen1_surv[:num_gcs_to_plot]

plot_surv_chart(gc_plts[0], num_gcs_to_plot, x_gc_indices_to_plot, 
                y_gc_gen0_alloc_to_plot, "gen0 alloc", 1)
plot_surv_chart(gc_plts[1], num_gcs_to_plot, x_gc_indices_to_plot, 
                y_gc_gen0_surv_to_plot, "gen0 surv", 0)
plot_surv_chart(gc_plts[2], num_gcs_to_plot, x_gc_indices_to_plot, 
                y_gc_gen1_alloc_to_plot, "gen1 alloc", 1)
plot_surv_chart(gc_plts[3], num_gcs_to_plot, x_gc_indices_to_plot, 
                y_gc_gen1_surv_to_plot, "gen1 surv", 0)

#%%
def plot_fl_fit_chart(inc_plt, num_elements, x_inc_data, y_inc_data, 
                 inc_legend, inc_color_index):
    #inc_plt.set_title(inc_title, loc='right')
    inc_plt.plot(x_inc_data, y_inc_data, 
        marker='.', 
        linestyle='-',
        color=total_colors[inc_color_index],
        label=inc_legend)
    #inc_plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
    inc_plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
    inc_plt.grid()

fig = plt.figure()

print("{0} total eph GCs".format(g_num_eph_gcs))

num_gc_plts = 4
gc_plts = [None]*num_gc_plts
for plt_index in range (0, num_gc_plts):
    gc_plts[plt_index] = fig.add_subplot(num_gc_plts, 1, (1 + plt_index))

# display GCs whose indices >= start_gc_index and <= end_gc_index
start_gc_index = 0
end_gc_index = g_eph_surv_info[g_num_eph_gcs - 1].gen_index
# start_gc_index = 0
# end_gc_index = 70000

# this is my primitive smoothing - there are 
# too many data points, we average every 100 elements
stepping = 30
# stepping = 10

num_gcs_to_plot = 0

# we only look at gen1 GCs with only fl alloc
total_num_data_points = g_num_gen1_gen2_gcs / stepping
x_gc_indices = [0 for i in range(total_num_data_points)]
y_gc_num_plugs_fit_in_gen2 = [0 for i in range(total_num_data_points)]
y_gc_gen1_plan_time = [0 for i in range(total_num_data_points)]
y_gc_gen1_surv = [0 for i in range(total_num_data_points)]
# y_gc_gen1_avg_plug_size = [0 for i in range(total_num_data_points)]
y_gc_gen1_surv_over_plan_ns = [0 for i in range(total_num_data_points)]

# I am not displaying unusally big values for plan so the charts will be easier to look at
total_gen1_gcs = 0
gc_indices_sum = 0
gen1_plugs_tried_in_gen2_sum = 0
gen1_plan_ns_sum = 0
gen2_fl_allocated_sum = 0

total_gen1_surv = 0
total_gen2_inc = 0

num_data_points  = 0

for i in range (0, g_num_gen1_gen2_gcs):
    if ( (g_gen2_size_increase_info[i].gen_index >= start_gc_index) and
       (g_gen2_size_increase_info[i].gen_index <= end_gc_index)):
    
        if (g_gen2_size_increase_info[i].gen_num == 1):
            total_gen1_gcs += 1
                
            gen1_surv = g_gen2_size_increase_info[i].gen2_fl_allocated + g_gen2_size_increase_info[i].gen2_es_allocated + g_gen2_size_increase_info[i].gen2_c_allocated

            total_gen1_surv += gen1_surv
            total_gen2_inc += g_gen2_size_increase_info[i].gen2_size_increase

            if ((g_gen2_size_increase_info[i].gen2_fl_allocated > 0) and 
                (g_gen2_size_increase_info[i].gen2_es_allocated == 0) and 
                (g_gen2_size_increase_info[i].gen2_c_allocated == 0)):

                gc_indices_sum += g_gen2_size_increase_info[i].gen_index
                gen1_plugs_tried_in_gen2_sum += g_gen2_size_increase_info[i].gen1_plugs_tried_in_gen2
                gen1_plan_time_ns = g_gen2_size_increase_info[i].gen1_plan_ns
                if (gen1_plan_time_ns > 4000):
                    print("*GC* {0} plan took {1}ns, bgc state {2}, surv {3:,}, {4:,} plugs!!!".format(
                        g_gen2_size_increase_info[i].gen_index,
                        g_gen2_size_increase_info[i].gen1_plan_ns,
                        g_gen2_size_increase_info[i].bgc_state,
                        g_gen2_size_increase_info[i].gen2_fl_allocated,
                        g_gen2_size_increase_info[i].gen1_plugs_tried_in_gen2))

                    gen1_plan_time_ns = 500

                gen1_plan_ns_sum += gen1_plan_time_ns
                gen2_fl_allocated_sum += g_gen2_size_increase_info[i].gen2_fl_allocated

                # print("GC#{0} surv {1:,} {2:,}ns, ratio: {3}".format(
                #     g_gen2_size_increase_info[i].gen_index,
                #     g_gen2_size_increase_info[i].gen2_fl_allocated,
                #     gen1_plan_time_ns,
                #     (g_gen2_size_increase_info[i].gen2_fl_allocated / gen1_plan_time_ns)))
                
                num_data_points += 1

                if (num_data_points >= stepping):
                    x_gc_indices[num_gcs_to_plot] = gc_indices_sum / stepping
                    y_gc_num_plugs_fit_in_gen2[num_gcs_to_plot] = gen1_plugs_tried_in_gen2_sum / stepping
                    y_gc_gen1_plan_time[num_gcs_to_plot] = gen1_plan_ns_sum / stepping
                    y_gc_gen1_surv[num_gcs_to_plot] = gen2_fl_allocated_sum / gen1_plugs_tried_in_gen2_sum
                    y_gc_gen1_surv_over_plan_ns[num_gcs_to_plot] = gen2_fl_allocated_sum / gen1_plan_ns_sum

                    # print("last {0} GCs total surv {1:,} {2:,}ns, ratio: {3}".format(
                    #     stepping,
                    #     gen2_fl_allocated_sum,
                    #     gen1_plan_ns_sum,
                    #     (gen2_fl_allocated_sum / gen1_plan_ns_sum)))

                    num_data_points = 0
                    gc_indices_sum = 0
                    gen1_plugs_tried_in_gen2_sum = 0
                    gen1_plan_ns_sum = 0
                    gen2_fl_allocated_sum = 0

                    num_gcs_to_plot += 1

print("we had {0:,} GCs, plotting {1:,} data points; total {2:,} gen1 GCs".format(
    total_num_data_points, num_gcs_to_plot, total_gen1_gcs))

print("gen1 GCs surv {0:,}, inc {1:,} avg {2:,}surv/inc".format(
    total_gen1_surv, total_gen2_inc, 
    (total_gen1_surv / total_gen2_inc)))

x_gc_indices_to_plot = x_gc_indices[:num_gcs_to_plot]
y_gc_num_plugs_fit_in_gen2_to_plot = y_gc_num_plugs_fit_in_gen2[:num_gcs_to_plot]
y_gc_gen1_plan_time_to_plot = y_gc_gen1_plan_time[:num_gcs_to_plot]
y_gc_gen1_surv_to_plot = y_gc_gen1_surv[:num_gcs_to_plot]
y_gc_gen1_surv_over_plan_ns_to_plot = y_gc_gen1_surv_over_plan_ns[:num_gcs_to_plot]

plot_surv_chart(gc_plts[0], num_gcs_to_plot, x_gc_indices_to_plot, 
                y_gc_num_plugs_fit_in_gen2_to_plot, "num plugs", 1)
plot_surv_chart(gc_plts[1], num_gcs_to_plot, x_gc_indices_to_plot, 
                y_gc_gen1_plan_time_to_plot, "gen1 plan time", 0)
plot_surv_chart(gc_plts[2], num_gcs_to_plot, x_gc_indices_to_plot, 
                y_gc_gen1_surv_to_plot, "gen1 surv / plugs", 0)
plot_surv_chart(gc_plts[3], num_gcs_to_plot, x_gc_indices_to_plot, 
                y_gc_gen1_surv_over_plan_ns_to_plot, "gen1 surv / plan", 1)

#%%
# the first file - usually I am concentrating on this file
g_file_0 = "C:/bgc-tuning/0906/600-LR1-SS30-LS30-mkp1.0-mki0.016-akp0.00600-aki0.00100-5796-iml21.log"
# g_file_0 = "C:/bgc-tuning/build-0801/gclog-600-LR0-SS-30-kp-2cccccc-ki-753000-0.log"

g_bgc_info = []
g_bgc_detailed_info = []
g_num_gen2s = 0

g_num_gen2s, g_bgc_info, g_bgc_detailed_info, g_total_physical_memory = process_file_bgc_tuning (g_file_0)
print("total {0} gen2s, {1} in info, {2} in detailed info".format(g_num_gen2s, len(g_bgc_info),
                                                                 len(g_bgc_detailed_info)))

print("total physical mem for this analysis is {0:14}".format(g_total_physical_memory))

#%%
# the 2nd file - for comparison
# g_file_1 = "C:/bgc-tuning/build-0801/gclog-600.kp-3800000-ki-3a9800.log"
# g_file_1 = "C:/bgc-tuning/build-0801/gclog-600-LR0-SS-30-kp-2cccccc-ki-753000-0.log"
# g_file_1 = "C:/bgc-tuning/build-0807/new/gclog-600-LR0-SS-30-kp-2cccccc-ki-753000-1.log"
g_file_1 =  "C:/bgc-tuning/0915/600-LR1-SS30-LS30-s0.05-mkp1.0-mki0.016-akp0.00600-aki0.00100-5700-iml24.log"

g_c_bgc_info_1 = []
g_c_bgc_detailed_info_1 = []
g_c_num_gen2s_1 = 0

g_c_num_gen2s_1, g_c_bgc_info_1, g_c_bgc_detailed_info_1, g_total_physical_memory = process_file_bgc_tuning (g_file_1)
# g_c_num_gen2s, g_c_bgc_info, g_c_bgc_detailed_info, g_total_physical_memory = process_file_bgc_tuning ("C:/bgc-tuning/build-0711/gclog.5612.log")
print("total {0} gen2s, {1} in info, {2} in detailed info".format(g_c_num_gen2s_1, len(g_c_bgc_info_1),
                                                                 len(g_c_bgc_detailed_info_1)))

#%%
# the 3rd file - for comparison
# g_file_2 = "C:/bgc-tuning/build-0807/gclog-600-LR0-SS-30-kp-7000000-ki-753000-0.log"
# g_file_2 = "C:/bgc-tuning/build-0801/gclog-800-LR0-SS-30-kp-2cccccc-ki-753000-0.log"
# g_file_2 = "C:/bgc-tuning/build-0807/new/gclog-600-LR0-SS-30-kp-2cccccc-ki-753000-2.log"
g_file_2 = "C:/bgc-tuning/0915/600-LR1-SS30-LS30-s0.03-mkp1.0-mki0.016-akp0.00600-aki0.00100-3920-iml17.log"

g_c_bgc_info_2 = []
g_c_bgc_detailed_info_2 = []
g_c_num_gen2s_2 = 0

g_c_num_gen2s_2, g_c_bgc_info_2, g_c_bgc_detailed_info_2, g_total_physical_memory = process_file_bgc_tuning (g_file_2)
# g_c_num_gen2s, g_c_bgc_info, g_c_bgc_detailed_info, g_total_physical_memory = process_file_bgc_tuning ("C:/bgc-tuning/build-0711/gclog.5612.log")
print("total {0} gen2s, {1} in info, {2} in detailed info".format(g_c_num_gen2s_2, len(g_c_bgc_info_2),
                                                                 len(g_c_bgc_detailed_info_2)))

#%%
# this ploting is for comparison

title_font = {'family': 'verdana',
        'color':  'gray',
        'weight': 'bold',
        'size': 16,
        }
# src0, src1 provides the y_data
def plt_comparison(c_plt, c_title, color_index_0,
                   legend_0, legend_1,  legend_2,
                   src0, src1, src2,
                   field_name, start_index, 
                   num_elements_0, num_elements_1, num_elements_2) :
    max_num_elements = max(num_elements_0, num_elements_1)
    max_num_elements = max(max_num_elements, num_elements_2)
    c_x_data = [None]*max_num_elements
    # print("getting GCs from {0} to {1}".format(start_index, (start_index + num_elements)))
    for c_index in range (start_index, (start_index + max_num_elements)):
        c_x_data[c_index - start_index] = c_index
    # y_data_0 = get_fields(src0, field_name, start_index, num_elements)
    # y_data_1 = get_fields(src1, field_name, start_index, num_elements)
    y_data_0 = get_fields(src0, field_name, start_index, num_elements_0, max_num_elements)
    y_data_1 = get_fields(src1, field_name, start_index, num_elements_1, max_num_elements)
    y_data_2 = get_fields(src2, field_name, start_index, num_elements_2, max_num_elements)

    # c_plt.set_title(c_title, fontdict=title_font, loc='right')
    # c_plt.set_title(c_title, fontdict=title_font, x=1.08, loc='right')
    c_plt.set_title(c_title, fontdict=title_font, x=1.08, loc="left")

    # x_spacing = 5
    # x_minorLocator = MultipleLocator(x_spacing)
    # c_plt.xaxis.set_major_locator(x_minorLocator)
    
    if ((c_title == "ml")):
        y_spacing = 5
        y_minorLocator = MultipleLocator(y_spacing)
        c_plt.yaxis.set_major_locator(y_minorLocator)

    if ((c_title.find("sflr") != -1)):
        y_spacing = 5
        y_minorLocator = MultipleLocator(y_spacing)
        c_plt.yaxis.set_major_locator(y_minorLocator)

    c_plt.plot(c_x_data, y_data_0, 
        marker='.', 
        linestyle='-',
        color=total_colors[color_index_0], 
        label=legend_0)
    c_plt.plot(c_x_data, y_data_1, 
        marker='.', 
        linestyle='-',
        color=total_colors[color_index_0 + 1], 
        label=legend_1)
    # c_plt.plot(c_x_data, y_data_2, 
    #     marker='.', 
    #     linestyle='-',
    #     color=total_colors[color_index_0 + 2], 
    #     label=legend_2)

    c_plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)

    c_plt.grid(which='major')    
    # c_plt.grid()

fig = plt.figure()
plot_legend_0 = g_file_0
plot_legend_1 = g_file_1
plot_legend_2 = g_file_2

total_num_gcs_from_0 = len(g_bgc_info)
total_num_gcs_from_1 = len(g_c_bgc_info_1)
total_num_gcs_from_2 = len(g_c_bgc_info_2)
print("0 has {0} BGCs, 1 has {1} BGCs, 2 has {2} BGCs".format(
    total_num_gcs_from_0, total_num_gcs_from_1, total_num_gcs_from_2))
end_gc_index_0 = total_num_gcs_from_0 - 1
end_gc_index_1 = total_num_gcs_from_1 - 1
end_gc_index_2 = total_num_gcs_from_2 - 1

start_gc_index = 0
# end_gc_index = -1
end_gc_index = 40
if (end_gc_index != -1):
    end_gc_index_0 = min (end_gc_index, end_gc_index_0)
    end_gc_index_1 = min (end_gc_index, end_gc_index_1)
    end_gc_index_2 = min (end_gc_index, end_gc_index_2)

num_gcs_from_0 = end_gc_index_0 - start_gc_index
num_gcs_from_1 = end_gc_index_1 - start_gc_index
num_gcs_from_2 = end_gc_index_2 - start_gc_index

print("displaying GC#{0} to {1} from 0".format(start_gc_index, end_gc_index_0))
print("displaying GC#{0} to {1} from 1".format(start_gc_index, end_gc_index_1))
print("displaying GC#{0} to {1} from 2".format(start_gc_index, end_gc_index_2))

total_plts = 16
c_plts = [None]*total_plts
for plt_index in range (0, total_plts):
    c_plts[plt_index] = fig.add_subplot(total_plts, 1, (1 + plt_index))

color_index = 0
plt_index = 0

plt_comparison(c_plts[plt_index], "reason", color_index,
               plot_legend_0, plot_legend_1, plot_legend_2, 
               g_bgc_info, g_c_bgc_info_1, g_c_bgc_info_2,
               "reason", start_gc_index, num_gcs_from_0, num_gcs_from_1, num_gcs_from_2)

plt_index += 1

plt_comparison(c_plts[plt_index], "ml", color_index,
               plot_legend_0, plot_legend_1, plot_legend_2, 
               g_bgc_info, g_c_bgc_info_1, g_c_bgc_info_2,
               "end_ml", start_gc_index, num_gcs_from_0, num_gcs_from_1, num_gcs_from_2)


plt_index += 1

# plt_comparison(c_plts[plt_index], "g3 v-size", color_index,
#                plot_legend_0, plot_legend_1, plot_legend_2, 
#                g_bgc_info, g_c_bgc_info_1, g_c_bgc_info_2,
#                "gen3_last_bgc_size", start_gc_index, num_gcs_from_0, num_gcs_from_1, num_gcs_from_2)

plt_comparison(c_plts[plt_index], "p-mem", color_index, 
               plot_legend_0, plot_legend_1, plot_legend_2, 
               g_bgc_info, g_c_bgc_info_1, g_c_bgc_info_2,
               "in_use_physical_memory", start_gc_index, num_gcs_from_0, num_gcs_from_1, num_gcs_from_2)

plt_index += 1
plt_comparison(c_plts[plt_index], "ws", color_index, 
               plot_legend_0, plot_legend_1, plot_legend_2, 
               g_bgc_info, g_c_bgc_info_1, g_c_bgc_info_2,
               "end_ws_size", start_gc_index, num_gcs_from_0, num_gcs_from_1, num_gcs_from_2)

# plt_index += 1

# plt_comparison(c_plts[plt_index], "g3 p-mem", color_index, 
#                plot_legend_0, plot_legend_1, plot_legend_2, 
#                g_bgc_detailed_info, g_c_bgc_detailed_info_1, g_c_bgc_detailed_info_2,
#                "gen3_end_physical_size", start_gc_index, num_gcs_from_0, num_gcs_from_1, num_gcs_from_2)

plt_index += 1

plt_comparison(c_plts[plt_index], "g2 v-size", color_index,
               plot_legend_0, plot_legend_1, plot_legend_2, 
               g_bgc_info, g_c_bgc_info_1, g_c_bgc_info_2,
               "gen2_last_bgc_size", start_gc_index, num_gcs_from_0, num_gcs_from_1, num_gcs_from_2)

plt_index += 1

plt_comparison(c_plts[plt_index], "g2 p-mem", color_index, 
               plot_legend_0, plot_legend_1, plot_legend_2, 
               g_bgc_detailed_info, g_c_bgc_detailed_info_1, g_c_bgc_detailed_info_2,
               "gen2_end_physical_size", start_gc_index, num_gcs_from_0, num_gcs_from_1, num_gcs_from_2)

plt_index += 1
plt_comparison(c_plts[plt_index], "g2 alloc", color_index,
               plot_legend_0, plot_legend_1, plot_legend_2, 
               g_bgc_info, g_c_bgc_info_1, g_c_bgc_info_2,
               "gen2_alloc_to_trigger", start_gc_index, num_gcs_from_0, num_gcs_from_1, num_gcs_from_2)

plt_index += 1
plt_comparison(c_plts[plt_index], "g2 alloc kp", color_index,
               plot_legend_0, plot_legend_1, plot_legend_2, 
               g_bgc_detailed_info, g_c_bgc_detailed_info_1, g_c_bgc_detailed_info_2,
               "gen2_alloc_kp", start_gc_index, num_gcs_from_0, num_gcs_from_1, num_gcs_from_2)

plt_index += 1
plt_comparison(c_plts[plt_index], "g2 alloc ki", color_index,
               plot_legend_0, plot_legend_1, plot_legend_2, 
               g_bgc_detailed_info, g_c_bgc_detailed_info_1, g_c_bgc_detailed_info_2,
               "gen2_alloc_ki", start_gc_index, num_gcs_from_0, num_gcs_from_1, num_gcs_from_2)

plt_index += 1

plt_comparison(c_plts[plt_index], "g3 alloc", color_index,
               plot_legend_0, plot_legend_1, plot_legend_2, 
               g_bgc_info, g_c_bgc_info_1, g_c_bgc_info_2,
               "gen3_alloc_to_trigger", start_gc_index, num_gcs_from_0, num_gcs_from_1, num_gcs_from_2)

plt_index += 1
plt_comparison(c_plts[plt_index], "g3 alloc kp", color_index,
               plot_legend_0, plot_legend_1, plot_legend_2, 
               g_bgc_detailed_info, g_c_bgc_detailed_info_1, g_c_bgc_detailed_info_2,
               "gen3_alloc_kp", start_gc_index, num_gcs_from_0, num_gcs_from_1, num_gcs_from_2)

plt_index += 1
plt_comparison(c_plts[plt_index], "g3 alloc ki", color_index,
               plot_legend_0, plot_legend_1, plot_legend_2, 
               g_bgc_detailed_info, g_c_bgc_detailed_info_1, g_c_bgc_detailed_info_2,
               "gen3_alloc_ki", start_gc_index, num_gcs_from_0, num_gcs_from_1, num_gcs_from_2)

# plt_index += 1
# # virtual end flr
# plt_comparison(c_plts[plt_index], "v-eflr", color_index,
#                plot_legend_0, plot_legend_1, plot_legend_2, 
#                g_bgc_info, g_c_bgc_info_1, g_c_bgc_info_2,
#                "gen2_current_bgc_end_flr", start_gc_index, num_gcs_from_0, num_gcs_from_1, num_gcs_from_2)

# plt_index += 1
# plt_comparison(c_plts[plt_index], "p-sflr", color_index,
#                plot_legend_0, plot_legend_1, plot_legend_2, 
#                g_bgc_info, g_c_bgc_info_1, g_c_bgc_info_2,
#                "gen2_current_bgc_physical_sweep_flr", start_gc_index, num_gcs_from_0, num_gcs_from_1, num_gcs_from_2)

plt_index += 1
plt_comparison(c_plts[plt_index], "g2 v-sflr", color_index, 
               plot_legend_0, plot_legend_1, plot_legend_2, 
               g_bgc_info, g_c_bgc_info_1, g_c_bgc_info_2,
               "gen2_current_bgc_sweep_flr", start_gc_index, num_gcs_from_0, num_gcs_from_1, num_gcs_from_2)

plt_index += 1
plt_comparison(c_plts[plt_index], "g3 v-sflr", color_index, 
               plot_legend_0, plot_legend_1, plot_legend_2, 
               g_bgc_info, g_c_bgc_info_1, g_c_bgc_info_2,
               "gen3_current_bgc_sweep_flr", start_gc_index, num_gcs_from_0, num_gcs_from_1, num_gcs_from_2)

plt_index += 1
plt_comparison(c_plts[plt_index], "ml ki+kp", color_index,
               plot_legend_0, plot_legend_1, plot_legend_2, 
               g_bgc_detailed_info, g_c_bgc_detailed_info_1, g_c_bgc_detailed_info_2,
               "ml_pi", start_gc_index, num_gcs_from_0, num_gcs_from_1, num_gcs_from_2)

plt_index += 1
plt_comparison(c_plts[plt_index], "kp", color_index,
               plot_legend_0, plot_legend_1, plot_legend_2, 
               g_bgc_detailed_info, g_c_bgc_detailed_info_1, g_c_bgc_detailed_info_2,
               "ml_kp", start_gc_index, num_gcs_from_0, num_gcs_from_1, num_gcs_from_2)

# plt_index += 1
# plt_comparison(c_plts[plt_index], "ki", color_index,
#                plot_legend_0, plot_legend_1, plot_legend_2, 
#                g_bgc_detailed_info, g_c_bgc_detailed_info_1, g_c_bgc_detailed_info_2,
#                "ml_ki", start_gc_index, num_gcs_from_0, num_gcs_from_1, num_gcs_from_2)

print("total {0} plots".format(plt_index + 1))

#%%
#
# I needed to do a hack for y_data_gen2_actual_gen1_to_trigger since I never actually recorded the bgc end gen1
# index, I needed to do this hack to get an approximate 
#
# start_gc_count = 5
# end_gc_count = 30
start_gc_count = 0
end_gc_count = len(g_bgc_info)

num_gen2s_to_display = end_gc_count - start_gc_count

print("showing data for {0} gen2s, {1} in info".format(num_gen2s_to_display, len(g_bgc_info)))

x_data = [None]*num_gen2s_to_display

# read various fields out for y_data
y_data_gc_indices = [None]*num_gen2s_to_display

y_data_gc_index_delta = [None]*num_gen2s_to_display

y_data_reason = [None]*num_gen2s_to_display
y_data_gen2_panic_ca_plugs_size = [None]*num_gen2s_to_display
y_data_gen2_panic_ca_plugs_count = [None]*num_gen2s_to_display
y_data_gen2_panic_alloc = [None]*num_gen2s_to_display
y_data_gen2_panic_fl = [None]*num_gen2s_to_display
y_data_elapsed_since_last_bgc_s = [None]*num_gen2s_to_display
y_data_elapsed_ms = [None]*num_gen2s_to_display
y_data_beg_ml = [None]*num_gen2s_to_display
y_data_end_ml = [None]*num_gen2s_to_display
y_data_beg_heap_size = [None]*num_gen2s_to_display 
y_data_beg_commit_size = [None]*num_gen2s_to_display 
y_data_beg_ws_size = [None]*num_gen2s_to_display 
y_data_end_heap_size = [None]*num_gen2s_to_display 
y_data_end_commit_size = [None]*num_gen2s_to_display 
y_data_end_ws_size = [None]*num_gen2s_to_display 

y_data_alloc_gen0 = [None]*num_gen2s_to_display
y_data_alloc_gen3 = [None]*num_gen2s_to_display

y_data_gen2_last_bgc_size = [None]*num_gen2s_to_display
y_data_gen2_current_bgc_start_flr = [None]*num_gen2s_to_display
y_data_gen2_current_bgc_sweep_flr = [None]*num_gen2s_to_display
y_data_gen2_current_bgc_physical_sweep_flr = [None]*num_gen2s_to_display
y_data_gen2_current_bgc_end_flr = [None]*num_gen2s_to_display
y_data_gen2_gen_increase_flr = [None]*num_gen2s_to_display
y_data_gen2_bgc_surv_rate = [None]*num_gen2s_to_display
y_data_gen2_actual_gen1_to_trigger = [None]*num_gen2s_to_display
y_data_gen2_gen1_since_last = [None]*num_gen2s_to_display
y_data_gen2_actual_alloc_to_trigger = [None]*num_gen2s_to_display
y_data_gen2_alloc_to_trigger = [None]*num_gen2s_to_display

y_data_gen3_last_bgc_size = [None]*num_gen2s_to_display
y_data_gen3_current_bgc_start_flr = [None]*num_gen2s_to_display
y_data_gen3_current_bgc_sweep_flr = [None]*num_gen2s_to_display
y_data_gen3_current_bgc_physical_sweep_flr = [None]*num_gen2s_to_display
y_data_gen3_current_bgc_end_flr = [None]*num_gen2s_to_display
y_data_gen3_gen_increase_flr = [None]*num_gen2s_to_display
y_data_gen3_bgc_surv_rate = [None]*num_gen2s_to_display
y_data_gen3_actual_gen1_to_trigger = [None]*num_gen2s_to_display
y_data_gen3_gen1_since_last = [None]*num_gen2s_to_display
y_data_gen3_actual_alloc_to_trigger = [None]*num_gen2s_to_display
y_data_gen3_alloc_to_trigger = [None]*num_gen2s_to_display
y_data_in_use_physical_memory = [None]*num_gen2s_to_display

y_data_gen1s_to_trigger = [None]*num_gen2s_to_display

y_data_gen3_end_fl = [None]*num_gen2s_to_display
y_data_gen3_fl_goal = [None]*num_gen2s_to_display
y_data_gen3_path_taken = [None]*num_gen2s_to_display
y_data_gen3_alloc_kp = [None]*num_gen2s_to_display
y_data_gen3_alloc_smoothed = [None]*num_gen2s_to_display
y_data_gen3_alloc_ff = [None]*num_gen2s_to_display

y_data_ml_kp = [None]*num_gen2s_to_display
y_data_ml_ki = [None]*num_gen2s_to_display
# kp + ki
y_data_ml_pi = [None]*num_gen2s_to_display
y_data_pi = [None]*num_gen2s_to_display

y_data_gen2_end_physical_size = [None]*num_gen2s_to_display
y_data_gen2_end_vfl_size = [None]*num_gen2s_to_display
y_data_gen3_end_physical_size = [None]*num_gen2s_to_display
y_data_gen3_end_vfl_size = [None]*num_gen2s_to_display

for gc_index in range (0, num_gen2s_to_display):
    x_data[gc_index] = gc_index + start_gc_count
    y_data_gc_indices[gc_index] = g_bgc_info[gc_index + start_gc_count].gen_index
    #print("GC#{0} r: {1}".format(gc_index, g_bgc_info[gc_index + start_gc_count].reason))
    if (gc_index == 0):
        y_data_gc_index_delta[gc_index] = 0
    else:
        y_data_gc_index_delta[gc_index] = y_data_gc_indices[gc_index] - y_data_gc_indices[gc_index - 1]
        
    y_data_reason[gc_index] = g_bgc_info[gc_index + start_gc_count].reason 
    y_data_gen2_panic_ca_plugs_size[gc_index] = g_bgc_info[gc_index + start_gc_count].gen2_panic_ca_plugs_size
    y_data_gen2_panic_ca_plugs_count[gc_index] = g_bgc_info[gc_index + start_gc_count].gen2_panic_ca_plugs_count
    y_data_gen2_panic_alloc[gc_index] = g_bgc_info[gc_index + start_gc_count].gen2_panic_alloc
    y_data_gen2_panic_fl[gc_index] = g_bgc_info[gc_index + start_gc_count].gen2_panic_fl
    y_data_elapsed_since_last_bgc_s[gc_index] = g_bgc_info[gc_index + start_gc_count].elapsed_since_last_s
    y_data_elapsed_ms[gc_index] = g_bgc_info[gc_index + start_gc_count].elapsed_ms
    y_data_beg_ml[gc_index] = g_bgc_info[gc_index + start_gc_count].beg_ml 
    y_data_end_ml[gc_index] = g_bgc_info[gc_index + start_gc_count].end_ml 
    y_data_beg_heap_size[gc_index] = g_bgc_info[gc_index + start_gc_count].beg_heap_size 
    y_data_beg_commit_size[gc_index] = g_bgc_info[gc_index + start_gc_count].beg_commit_size 
    y_data_beg_ws_size[gc_index] = g_bgc_info[gc_index + start_gc_count].beg_ws_size 
    y_data_end_heap_size[gc_index] = g_bgc_info[gc_index + start_gc_count].end_heap_size 
    y_data_end_commit_size[gc_index] = g_bgc_info[gc_index + start_gc_count].end_commit_size 
    y_data_end_ws_size[gc_index] = g_bgc_info[gc_index + start_gc_count].end_ws_size 
    
    y_data_alloc_gen0[gc_index] = g_bgc_info[gc_index + start_gc_count].alloc_gen0
    y_data_alloc_gen3[gc_index] = g_bgc_info[gc_index + start_gc_count].alloc_gen3 

    y_data_gen2_last_bgc_size[gc_index] = g_bgc_info[gc_index + start_gc_count].gen2_last_bgc_size 
    y_data_gen2_current_bgc_start_flr[gc_index] = g_bgc_info[gc_index + start_gc_count].gen2_current_bgc_start_flr 
    y_data_gen2_current_bgc_sweep_flr[gc_index] = g_bgc_info[gc_index + start_gc_count].gen2_current_bgc_sweep_flr 
    y_data_gen2_current_bgc_physical_sweep_flr[gc_index] = g_bgc_info[gc_index + start_gc_count].gen2_current_bgc_physical_sweep_flr 
    y_data_gen2_current_bgc_end_flr[gc_index] = g_bgc_info[gc_index + start_gc_count].gen2_current_bgc_end_flr 
    y_data_gen2_gen_increase_flr[gc_index] = g_bgc_info[gc_index + start_gc_count].gen2_gen_increase_flr 
    y_data_gen2_bgc_surv_rate[gc_index] = g_bgc_info[gc_index + start_gc_count].gen2_bgc_surv_rate 

    # hack!!! since I didn't record this correctly.
    last_bgc_actual_gen1_to_trigger = 0
    if ((gc_index + start_gc_count) > 0):
        last_bgc_actual_gen1_to_trigger = g_bgc_info[gc_index + start_gc_count - 1].gen2_actual_gen1_to_trigger 
        #print("bgc#{0} gen1 to trigger is {1}".format((gc_index + start_gc_count - 1), last_bgc_actual_gen1_to_trigger))
    y_data_gen2_actual_gen1_to_trigger[gc_index] = g_bgc_info[gc_index + start_gc_count].gen2_actual_gen1_to_trigger - last_bgc_actual_gen1_to_trigger 
    y_data_gen2_gen1_since_last[gc_index] = g_bgc_info[gc_index + start_gc_count].gen2_gen1_since_last 
    y_data_gen2_actual_alloc_to_trigger[gc_index] = g_bgc_info[gc_index + start_gc_count].gen2_actual_alloc_to_trigger 
    y_data_gen2_alloc_to_trigger[gc_index] = g_bgc_info[gc_index + start_gc_count].gen2_alloc_to_trigger 

    y_data_gen3_last_bgc_size[gc_index] = g_bgc_info[gc_index + start_gc_count].gen3_last_bgc_size 
    y_data_gen3_current_bgc_start_flr[gc_index] = g_bgc_info[gc_index + start_gc_count].gen3_current_bgc_start_flr 
    y_data_gen3_current_bgc_sweep_flr[gc_index] = g_bgc_info[gc_index + start_gc_count].gen3_current_bgc_sweep_flr 
    y_data_gen3_current_bgc_physical_sweep_flr[gc_index] = g_bgc_info[gc_index + start_gc_count].gen3_current_bgc_physical_sweep_flr 
    y_data_gen3_current_bgc_end_flr[gc_index] = g_bgc_info[gc_index + start_gc_count].gen3_current_bgc_end_flr 
    y_data_gen3_gen_increase_flr[gc_index] = g_bgc_info[gc_index + start_gc_count].gen3_gen_increase_flr 
    y_data_gen3_bgc_surv_rate[gc_index] = g_bgc_info[gc_index + start_gc_count].gen3_bgc_surv_rate 
    y_data_gen3_actual_gen1_to_trigger[gc_index] = g_bgc_info[gc_index + start_gc_count].gen3_actual_gen1_to_trigger 
    y_data_gen3_gen1_since_last[gc_index] = g_bgc_info[gc_index + start_gc_count].gen3_gen1_since_last 
    y_data_gen3_actual_alloc_to_trigger[gc_index] = g_bgc_info[gc_index + start_gc_count].gen3_actual_alloc_to_trigger 
    y_data_gen3_alloc_to_trigger[gc_index] = g_bgc_info[gc_index + start_gc_count].gen3_alloc_to_trigger     

    y_data_in_use_physical_memory[gc_index] = g_bgc_info[gc_index + start_gc_count].in_use_physical_memory
    
    # hack
    y_data_gen1s_to_trigger[gc_index] = y_data_gen2_actual_gen1_to_trigger[gc_index]

    y_data_gen3_end_fl[gc_index] = g_bgc_detailed_info[gc_index + start_gc_count].gen3_end_fl
    y_data_gen3_fl_goal[gc_index] = g_bgc_detailed_info[gc_index + start_gc_count].gen3_fl_goal 
    y_data_gen3_path_taken[gc_index] = g_bgc_detailed_info[gc_index + start_gc_count].gen3_path_taken 
    y_data_gen3_alloc_kp[gc_index] = g_bgc_detailed_info[gc_index + start_gc_count].gen3_alloc_kp 
    y_data_gen3_alloc_smoothed[gc_index] = g_bgc_detailed_info[gc_index + start_gc_count].gen3_alloc_smoothed
    y_data_gen3_alloc_ff[gc_index] = g_bgc_detailed_info[gc_index + start_gc_count].gen3_alloc_ff 

    y_data_ml_kp[gc_index] = g_bgc_detailed_info[gc_index + start_gc_count].ml_kp
    y_data_ml_ki[gc_index] = g_bgc_detailed_info[gc_index + start_gc_count].ml_ki
    y_data_ml_pi[gc_index] = g_bgc_detailed_info[gc_index + start_gc_count].ml_pi

    y_data_pi[gc_index] = g_bgc_detailed_info[gc_index + start_gc_count].pi

    y_data_gen2_end_physical_size[gc_index] = g_bgc_detailed_info[gc_index + start_gc_count].gen2_end_physical_size
    y_data_gen2_end_vfl_size[gc_index] = g_bgc_detailed_info[gc_index + start_gc_count].gen2_end_vfl_size
    y_data_gen3_end_physical_size[gc_index] = g_bgc_detailed_info[gc_index + start_gc_count].gen3_end_physical_size
    y_data_gen3_end_vfl_size[gc_index] = g_bgc_detailed_info[gc_index + start_gc_count].gen3_end_vfl_size

    avg_plugs_ca_size = 0
    if (y_data_gen2_panic_ca_plugs_count[gc_index] != 0):
        avg_plugs_ca_size = int(y_data_gen2_panic_ca_plugs_size[gc_index] / y_data_gen2_panic_ca_plugs_count[gc_index])
    # print("GC#{0:4}({1:6}(l+{2:4})) r: {3:3} plug c: {4:2}, s: {5:8}({6:5}), panic a: {7:13,}, fl: {8:14,} ".format(gc_index, 
    #     y_data_gc_indices[gc_index], y_data_gc_index_delta[gc_index], y_data_reason[gc_index], 
    #     y_data_gen2_panic_ca_plugs_count[gc_index],
    #     y_data_gen2_panic_ca_plugs_size[gc_index],
    #     avg_plugs_ca_size,
    #     y_data_gen2_panic_alloc[gc_index],
    #     y_data_gen2_panic_fl[gc_index]))

    delta_in_use_phy_mem_ws = y_data_in_use_physical_memory[gc_index] - y_data_end_ws_size[gc_index]
    delta_ws_commit = y_data_end_ws_size[gc_index] - y_data_end_commit_size[gc_index]
    delta_commit_heap =  y_data_end_commit_size[gc_index] - y_data_end_heap_size[gc_index]
    delta_heap_g2_and_g3 =  y_data_end_heap_size[gc_index] - (y_data_gen2_end_physical_size[gc_index]
                                                             + y_data_gen3_end_physical_size[gc_index])
    delta_ws_heap = y_data_end_ws_size[gc_index] -  y_data_end_heap_size[gc_index]

    # print("GC#{0:4}({1:6} ml: {2:2} in_use-ws(mb) {3:7,}, ws-commit(mb): {4:4,}, commit-heap(mb): {5:6,}, heap-g2-g3(mb): {6:4,}, ws-heap(mb): {7:4,}".format(
    #     gc_index, 
    #     y_data_gc_indices[gc_index], 
    #     y_data_end_ml[gc_index],
    #     int(delta_in_use_phy_mem_ws / 1024 / 1024),
    #     delta_ws_commit / 1024 / 1024,
    #     int(delta_commit_heap / 1024 / 1024),
    #     delta_heap_g2_and_g3 / 1024 / 1024,
    #     delta_ws_heap / 1024 / 1024))

    # vs is virtual size
    print("GC#{0:4}({1:6}(l+{2:4} g1)) r: {3:2} g2a {4:16,} vs {5:14,}({6:14,}), sflr: {7:.3}({8:.3}) ml: {9}".format(
        gc_index, 
        y_data_gc_indices[gc_index], 
        y_data_gen1s_to_trigger[gc_index],
        y_data_reason[gc_index], 
        y_data_gen2_alloc_to_trigger[gc_index],
        y_data_gen2_last_bgc_size[gc_index],
        y_data_gen2_end_physical_size[gc_index],
        y_data_gen2_current_bgc_sweep_flr[gc_index],
        y_data_gen2_current_bgc_physical_sweep_flr[gc_index],
        y_data_end_ml[gc_index]))

        # y_data_gen2_last_bgc_size[gc_index], y_data_gen3_last_bgc_size[gc_index]))
#         y_data_beg_heap_size[gc_index], y_data_beg_commit_size[gc_index], y_data_beg_ws_size[gc_index]))                                                                                  

    # print("GC#{0:4}({1:6}(l+{2:4})) r: {3:3} elapsed: {4:6,}s, duration: {5:6,}ms, g2: {6:10,} g3: {7:5,}".format(gc_index, 
    #     y_data_gc_indices[gc_index], y_data_gc_index_delta[gc_index], y_data_reason[gc_index], 
    #     y_data_elapsed_since_last_bgc_s[gc_index], y_data_elapsed_ms[gc_index],
    #     y_data_alloc_gen0[gc_index], y_data_alloc_gen3[gc_index]))

#     print("GC#{0:4}({1:6}) g3: end_fl: {2:10,}, fl_goal: {3:10,}, path: {4:1,}, kp: {5:10,}, s: {6:10,}, ff: {7:10,}".format(
#             y_data_gc_indices[gc_index], 
# #             y_data_gc_index_delta[gc_index],
#             gc_index,
#             y_data_gen3_end_fl[gc_index], 
#             y_data_gen3_fl_goal[gc_index], 
#             y_data_gen3_path_taken[gc_index], 
#             y_data_gen3_alloc_kp[gc_index], 
#             y_data_gen3_alloc_smoothed[gc_index],
#             y_data_gen3_alloc_ff[gc_index]))
    
# for y_data_index in range (0, len(y_data_gen3_alloc_to_trigger)):
#     print("{0}: g3 alloc: {1:,}".format(y_data_index, y_data_gen3_alloc_to_trigger[y_data_index]))

####
# plot some general data
####

fig = plt.figure()
total_plts = 8
bgc_data_plts = [None]*total_plts
for plt_index in range (0, total_plts):
    bgc_data_plts[plt_index] = fig.add_subplot(total_plts, 1, (1 + plt_index))

x_spacing = 100
x_minorLocator = MultipleLocator(x_spacing)

color_index = 0
plt_index = 0

sub_plt = bgc_data_plts[plt_index]
sub_plt.set_title('g2 sflr')

y_spacing = 10
y_minorLocator = MultipleLocator(y_spacing)
sub_plt.yaxis.set_major_locator(y_minorLocator)
sub_plt.xaxis.set_major_locator(x_minorLocator)

y_data = y_data_gen2_current_bgc_sweep_flr
sub_plt.plot(x_data, y_data, 
     marker='.', 
     linestyle='-',
     color=total_colors[color_index], 
     label='sflr')
sub_plt.grid()
y_data = y_data_gen2_current_bgc_physical_sweep_flr
sub_plt.plot(x_data, y_data, 
     marker='.', 
     linestyle='-',
     color=total_colors[color_index + 1], 
     label='phy sflr')
sub_plt.grid(which='minor')
sub_plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)

color_index += 1
plt_index += 1

sub_plt = bgc_data_plts[plt_index]
# sub_plt.set_title('g2 alloc to trigger')
y_data = y_data_gen2_alloc_to_trigger
sub_plt.plot(x_data, y_data, 
     marker='.', 
     linestyle='-',
     color=total_colors[color_index], 
     label='g2 alloc')
sub_plt.grid()
# y_data = y_data_gen2_actual_alloc_to_trigger
# sub_plt.plot(x_data, y_data, 
#      marker='.', 
#      linestyle='-.',
#      color=total_colors[color_index + 1], 
#      label='actual')
sub_plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)

# color_index += 1

# sub_plt = plt_gen3_alloc_to_trigger
# sub_plt.set_title('g3 alloc to trigger')
# y_data = y_data_gen3_alloc_to_trigger
# sub_plt.plot(x_data, y_data, 
#      marker='.', 
#      linestyle='-',
#      color=total_colors[color_index], 
#      label='alloc')
# sub_plt.grid()
# y_data = y_data_gen3_actual_alloc_to_trigger
# sub_plt.plot(x_data, y_data, 
#      marker='.', 
#      linestyle='-.',
#      color=total_colors[color_index + 1], 
#      label='actual')
# sub_plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)

color_index += 1
plt_index += 1

sub_plt = bgc_data_plts[plt_index]
# sub_plt.set_title('g2 physical size')
y_data = y_data_gen2_end_physical_size
sub_plt.plot(x_data, y_data, 
     marker='.', 
     linestyle='-',
     color=total_colors[color_index], 
     label='g2 phy size')
y_spacing = 5000000000
y_minorLocator = MultipleLocator(y_spacing)
sub_plt.yaxis.set_major_locator(y_minorLocator)
sub_plt.xaxis.set_major_locator(x_minorLocator)

sub_plt.grid(which='major')
# sub_plt.grid(which='minor')
# color_index += 1
# plt_index += 1

# sub_plt = bgc_data_plts[plt_index]
# sub_plt.set_title('g2 virtual size')
y_data = y_data_gen2_last_bgc_size
sub_plt.plot(x_data, y_data, 
     marker='.', 
     linestyle='-',
     color=total_colors[color_index + 1], 
     label='g2 virtual size')

y_data = y_data_in_use_physical_memory
sub_plt.plot(x_data, y_data, 
     marker='.', 
     linestyle='-',
     color=total_colors[color_index + 2], 
     label='total p-mem')

# y_spacing = 100000000
# y_minorLocator = MultipleLocator(y_spacing)
# sub_plt.yaxis.set_minor_locator(y_minorLocator)
# sub_plt.xaxis.set_minor_locator(x_minorLocator)

# sub_plt.grid(which='minor')

# y_data = y_data_gen2_end_vfl_size
# sub_plt.plot(x_data, y_data, 
#      marker='.', 
#      linestyle='-',
#      color=total_colors[color_index + 2], 
#      label='g2 vfl')
sub_plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)


color_index += 1
plt_index += 1

sub_plt = bgc_data_plts[plt_index]
# sub_plt.set_title('GC gen3 alloc')
#y_data = y_data_gen3_last_bgc_size
# sub_plt.set_title('kp')
y_data = y_data_ml_kp
sub_plt.plot(x_data, y_data, 
     marker='.', 
     linestyle='-',
     color=total_colors[color_index], 
     label='kp')
sub_plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
sub_plt.grid()

color_index += 1
plt_index += 1

sub_plt = bgc_data_plts[plt_index]
# sub_plt.set_title('pi')
y_data = y_data_ml_ki
sub_plt.plot(x_data, y_data, 
     marker='.', 
     linestyle='-',
     color=total_colors[color_index], 
     label='ki')
sub_plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
sub_plt.grid()

color_index += 1
plt_index += 1

sub_plt = bgc_data_plts[plt_index]
# sub_plt.set_title('pi')
y_data = y_data_ml_pi
sub_plt.plot(x_data, y_data, 
     marker='.', 
     linestyle='-',
     color=total_colors[color_index], 
     label='ml pi')
sub_plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
sub_plt.grid()

color_index += 1
plt_index += 1

sub_plt = bgc_data_plts[plt_index]
y_data = y_data_end_ws_size
sub_plt.plot(x_data, y_data, 
     marker='.', 
     linestyle='-',
     color=total_colors[color_index], 
     label='ws')
sub_plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
sub_plt.grid()

color_index += 1
plt_index += 1

sub_plt = bgc_data_plts[plt_index]
sub_plt.set_title('end ml')
y_data = y_data_end_ml
sub_plt.plot(x_data, y_data, 
     marker='.', 
     linestyle='-',
     color=total_colors[color_index], 
     label='ml')
y_spacing = 10
y_minorLocator = MultipleLocator(y_spacing)
sub_plt.yaxis.set_major_locator(y_minorLocator)
sub_plt.xaxis.set_major_locator(x_minorLocator)

sub_plt.grid(which='major')

# color_index += 1

# # 
# sub_plt = plt_end_commit_size
# sub_plt.set_title('end size')
# y_data = y_data_end_ws_size
# sub_plt.plot(x_data, y_data, 
#      marker='.', 
#      linestyle='-',
#      color=total_colors[color_index], 
#      label='end ws')

# y_spacing = 500000000
# y_minorLocator = MultipleLocator(y_spacing)
# sub_plt.yaxis.set_minor_locator(y_minorLocator)
# sub_plt.xaxis.set_minor_locator(x_minorLocator)

# sub_plt.grid(which='minor')

# y_data = y_data_end_commit_size
# sub_plt.plot(x_data, y_data, 
#      marker='.', 
#      linestyle='-.',
#      color=total_colors[color_index + 1], 
#      label='end commit')

# y_data = y_data_end_heap_size
# sub_plt.plot(x_data, y_data, 
#      marker='.', 
#      linestyle='-.',
#      color=total_colors[color_index + 2], 
#      label='end heap')

# sub_plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)

# color_index += 1

# sub_plt = plt_end_heap_size
# sub_plt.set_title('g2 physical size')
# y_data = y_data_gen2_end_physical_size
# sub_plt.plot(x_data, y_data, 
#      marker='.', 
#      linestyle='-',
#      color=total_colors[color_index], 
#      label='g2 phy size')

# y_spacing = 100000000
# y_minorLocator = MultipleLocator(y_spacing)
# sub_plt.yaxis.set_minor_locator(y_minorLocator)
# sub_plt.xaxis.set_minor_locator(x_minorLocator)

# sub_plt.grid(which='minor')

# # y_data = y_data_end_heap_size
# # sub_plt.plot(x_data, y_data, 
# #      marker='.', 
# #      linestyle='-.',
# #      color=total_colors[color_index + 1], 
# #      label='total heap')

# # y_data = y_data_in_use_physical_memory
# # sub_plt.plot(x_data, y_data, 
# #      marker='.', 
# #      linestyle='-.',
# #      color=total_colors[color_index + 2], 
# #      label='in use phy mem')

# sub_plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)

# color_index += 1

# sub_plt = plt_gen2_alloc_to_trigger 
# sub_plt.set_title('g3 physical size')
# y_data = y_data_gen3_end_physical_size
# sub_plt.plot(x_data, y_data, 
#      marker='.', 
#      linestyle='-',
#      color=total_colors[color_index], 
#      label='g3 phy size')

# y_spacing = 500000000
# y_minorLocator = MultipleLocator(y_spacing)
# sub_plt.yaxis.set_minor_locator(y_minorLocator)
# sub_plt.xaxis.set_minor_locator(x_minorLocator)

# sub_plt.grid(which='minor')

# # y_data = y_data_end_commit_size
# # sub_plt.plot(x_data, y_data, 
# #      marker='.', 
# #      linestyle='-.',
# #      color=total_colors[color_index + 1], 
# #      label='end commit')
# sub_plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)

#%%

# # plot detailed calculations

total_plts = 4
# # total_plts = 3
# plt_fl_info = fig.add_subplot(total_plts, 1, 1)
# plt_path_taken = fig.add_subplot(total_plts, 1, 2)
# plt_goal_calc = fig.add_subplot(total_plts, 1, 3)
# plt_end_ml = fig.add_subplot(total_plts, 1, 4)

# color_index = 0

# sub_plt = plt_fl_info
# sub_plt.set_title('fl info')
# y_data = y_data_gen3_end_fl
# sub_plt.plot(x_data, y_data, 
#      marker='.', 
#      linestyle='-',
#      color=total_colors[color_index], 
#      label='end fl')
# y_data = y_data_gen3_fl_goal
# sub_plt.plot(x_data, y_data, 
#      marker='.', 
#      linestyle=':',
#      color=total_colors[color_index + 1], 
#      label='goal')
# plt_fl_info.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)

# color_index += 1

# sub_plt = plt_path_taken
# sub_plt.set_title('path taken')
# # y_data = y_data_gc_indices
# y_data = y_data_gen3_path_taken

# sub_plt.plot(x_data, y_data, 
#      marker='.', 
#      linestyle='-',
#      color=total_colors[color_index], 
#      label='index')

# color_index += 1

# sub_plt = plt_goal_calc
# sub_plt.set_title('flr')
# y_data = y_data_gen3_current_bgc_start_flr
# sub_plt.plot(x_data, y_data, 
#      marker='.', 
#      linestyle='-',
#      color=total_colors[color_index], 
#      label='start')
# y_data = y_data_gen3_current_bgc_sweep_flr
# sub_plt.plot(x_data, y_data, 
#      marker='.', 
#      linestyle='-',
#      color=total_colors[color_index + 1], 
#      label='sweep')
# y_data = y_data_gen3_current_bgc_end_flr
# sub_plt.plot(x_data, y_data, 
#      marker='.', 
#      linestyle='-',
#      color=total_colors[color_index + 2], 
#      label='end')
# plt_goal_calc.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)

# color_index += 1

# sub_plt = plt_end_ml
# sub_plt.set_title('end ml')
# y_data = y_data_end_ml
# sub_plt.plot(x_data, y_data, 
#      marker='.', 
#      linestyle='-',
#      color=total_colors[color_index], 
#      label='i')

plt.legend()
#plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()

#%%
