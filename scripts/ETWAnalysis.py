import xml.etree.cElementTree as ET
import glob
import os
import clr
import sys
from datetime import date, timedelta

sys.path.append('C:/Users/suwhang/AppData/Local/Programs/Python/Python36/')

clr.AddReference('Microsoft.Diagnostics.Tracing.TraceEvent')


import System.Diagnostics.Tracing
import Microsoft.Diagnostics.Tracing as tracing
from Microsoft.Diagnostics.Tracing.Analysis import TraceLoadedDotNetRuntimeExtensions as ext
from Microsoft.Diagnostics.Tracing.Analysis import *
from Microsoft.Diagnostics.Tracing.Analysis import TraceProcessesExtensions as tpext
from System import Action
import Microsoft.Diagnostics.Tracing.Analysis as analysis

# GC types
NonConcurrentGC = 0
BackgroundGC = 1
ForegroundGC = 2

# Startup flags
CONCURRENT_GC = 0x000001
SERVER_GC = 0x001000 


# GC Stats header
GCSTATS_HEADER = ['GCPauseTimePercentage', 'HeapCount', 'MaxAllocRateMBSec', 'MaxSizePeakMB', 'MaxSuspendDurationMSec', 'MeanCpuMSec', 'MeanPauseDurationMSec', 'MeanSizeAfterMB', 'MeanSizePeakMB', 'NumInduced', 'NumWithPinEvents', 'NumWithPinPlugEvents', 'PinnedObjectPercentage', 'PinnedObjectSizes', 'ProcessDuration', 'TotalAllocatedMB', 'TotalCpuMSec', 'TotalPauseTimeMSec', 'TotalPromotedMB', 'TotalSizeAfterMB', 'TotalSizePeakMB']


def read_trace(file_name):
    source = tracing.ETWTraceEventSource(file_name)
    ext.NeedLoadedDotNetRuntimes(source)
    source.Process()

    statsSummary = {}

    for proc in analysis.TraceProcessesExtensions.Processes(source):
        mang = ext.LoadedDotNetRuntime(proc)
        if mang is None:
            continue

        GCs = mang.GC.GCs

        proc_name_lower_case = proc.Name.lower()
        if (proc_name_lower_case.find("corerun") == -1):
            continue
        

        statsSummary['IsServerGCUsed'] = mang.GC.Stats().IsServerGCUsed

        stats = {}
        stats['GCPauseTimePercentage'] = {'Units': '%', 'Stat': mang.GC.Stats().GetGCPauseTimePercentage()}
        stats['HeapCount'] = {'Units': 'Count', 'Stat': mang.GC.Stats().HeapCount}    
        stats['MaxAllocRateMBSec'] = {'Units': 'MB', 'Stat': mang.GC.Stats().MaxAllocRateMBSec}
        stats['MaxSizePeakMB'] = {'Units': 'MB', 'Stat': mang.GC.Stats().MaxSizePeakMB}
        stats['MaxSuspendDurationMSec'] = {'Units': 'MSec', 'Stat': mang.GC.Stats().MaxSuspendDurationMSec}
        stats['MeanCpuMSec'] = {'Units': 'MSec', 'Stat': mang.GC.Stats().MeanCpuMSec}
        stats['MeanPauseDurationMSec'] = {'Units': 'MSec', 'Stat': mang.GC.Stats().MeanPauseDurationMSec}
        stats['MeanSizeAfterMB'] = {'Units': 'MB', 'Stat': mang.GC.Stats().MeanSizeAfterMB}
        stats['MeanSizePeakMB'] = {'Units': 'MB', 'Stat': mang.GC.Stats().MeanSizePeakMB}
        stats['NumInduced'] = {'Units': 'Count', 'Stat': mang.GC.Stats().NumInduced}
        stats['NumWithPinEvents'] = {'Units': 'Count', 'Stat': mang.GC.Stats().NumWithPinEvents}
        stats['NumWithPinPlugEvents'] = {'Units': 'Count', 'Stat': mang.GC.Stats().NumWithPinPlugEvents}
        stats['PinnedObjectPercentage'] = {'Units': '%', 'Stat': mang.GC.Stats().PinnedObjectPercentage}
        stats['PinnedObjectSizes'] = {'Units': 'Count', 'Stat': mang.GC.Stats().PinnedObjectSizes}
        stats['ProcessDuration'] = {'Units': 'Sec', 'Stat': mang.GC.Stats().ProcessDuration}
        stats['TotalAllocatedMB'] = {'Units': 'MB', 'Stat': mang.GC.Stats().TotalAllocatedMB}
        stats['TotalCpuMSec'] = {'Units': 'MSec', 'Stat': mang.GC.Stats().TotalCpuMSec}
        stats['TotalPauseTimeMSec'] = {'Units': 'MSec', 'Stat': mang.GC.Stats().TotalPauseTimeMSec}
        stats['TotalPromotedMB'] = {'Units': 'MB', 'Stat': mang.GC.Stats().TotalPromotedMB}
        stats['TotalSizeAfterMB'] = {'Units': 'MB', 'Stat': mang.GC.Stats().TotalSizeAfterMB}
        stats['TotalSizePeakMB'] = {'Units': 'MB', 'Stat': mang.GC.Stats().TotalSizePeakMB}


        statsSummary['stats'] = stats
        print ("info for process {0}: {1}".format(proc.ProcessID, proc.Name))
        return statsSummary


def build_stats_xml(statsSummary, test_name):
    # Emit our data as XML
    #test_name = file_name.split('@')[1].split('/')[0]

    root = ET.Element("Scenario", Name=test_name)
    ET.SubElement(root, "Tier").text = "0"
    counters = ET.SubElement(root, "Counters")

    for stat_name in statsSummary['stats']:
        stat_val = statsSummary['stats'][stat_name]
        counter = ET.SubElement(counters, 'Counter', Name=stat_name)
        units = ET.SubElement(counter, 'Units', Inverted='False').text = stat_val['Units']
        results = ET.SubElement(counter, 'Results')
        result = ET.SubElement(results, 'Result').text = str(stat_val['Stat'])
        invalidresults = ET.SubElement(counter, 'InvalidResults')
    return root


def insert_to_xml(root, orig_root):
    
    testcases = orig_root.find('TestCases')
    testcase = testcases.findall('TestCase')[0]
    testcase2 = testcases.findall('TestCase')[1]
    testcases.remove(testcase2)
    scenarios = testcase.find('Scenarios')
    scenarios.insert(0, root)


def find_all_etl(root_dir):
    etl_lst = []
    for filename in glob.iglob(root_dir + '**/*.etl', recursive=True):
        if not os.path.isdir(filename):
            etl_lst.append(filename)
    
    return etl_lst



def main():
    # This is the original tree from Tom's example XML
    orig_root = ET.parse('E:/GC/PerfInfra/PerfLab/PerfResults_T0.xml')
    traces = find_all_etl('E:/GC/Traces/')
    print(traces)

if __name__ == '__main__':
    #main()
    traces = find_all_etl('E:/GC/Traces/suwhang-test-2/')
    csv_file = open('./test.csv', 'w')
    print(traces)
    
    csv_file.write('Test,')  # Test name
    csv_file.write('Date,')  # Date test was taken
    for header in GCSTATS_HEADER:
        csv_file.write(header)
        csv_file.write(',')

    csv_file.write('\n')
    
    stats = {}
    for trace_file in traces:
        stats = read_trace(trace_file)['stats']
        
        test_name = trace_file.split('\\')[1]
        date_diff = int(trace_file.split('\\')[2])
        test_date = date.today() - timedelta(days=date_diff)
        

        csv_file.write('{},{},'.format(test_name, test_date))
        for header in GCSTATS_HEADER:
            csv_file.write(str(stats[header]['Stat']))
            csv_file.write(',')
        csv_file.write('\n')

    for header in GCSTATS_HEADER:
        print('\'{}\': \'{}\''.format(header, stats[header]['Units']))

#ET.dump(orig_root)
#tree = ET.ElementTree(orig_root)

