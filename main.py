import os
import time
from dp_unbounded_knapsack import DP
from bnb_unbounded_knapsack import BnB
# !pip install memory_profiler
from memory_profiler import memory_usage
directory_path = "Datasets/"

file_list = os.listdir(directory_path)

for file_name in file_list:
    file_path = os.path.join(directory_path, file_name)
    with open(file_path, 'r') as file:

        print("Dataset that being proccessed: ", file_path)
        lines = file.readlines()

        wt = lines[1].split()
        wt = [int(i) for i in wt]

        val = lines[3].split()
        val = [int(i) for i in val]

        W = int(0.1 * sum(wt))

        start_time_bnb = time.time()
        start_memory_bnb = memory_usage()[0]
        bnb = BnB(W, wt, val)
        bnb.intialize()
        end_time_bnb = time.time()
        end_memory_bnb = memory_usage()[0]
        execution_time_bnb = end_time_bnb - start_time_bnb
        memory_used_bnb = end_memory_bnb - start_memory_bnb

        print(f"Execution Time BNB: {execution_time_bnb*1000} ms")
        print(f"Memory Usage BNB: {memory_used_bnb*1024} KB")

        start_time_dp = time.time()
        start_memory_dp = memory_usage()[0]

        dp = DP.unboundedKnapsack(W, len(val), val, wt)
        print(dp)

        end_time_dp = time.time()
        end_memory_dp = memory_usage()[0]

        execution_time_dp = end_time_dp - start_time_dp
        memory_used_dp = end_memory_dp - start_memory_dp
        print(f"Execution Time DP: {execution_time_dp*1000} ms")
        print(f"Memory Usage DP: {memory_used_dp*1024} KB")
