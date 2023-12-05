# Returns the maximum value 
# with knapsack of W capacity 
def unboundedKnapsack(W, n, val, wt): 

	# dp[i] is going to store maximum 
	# value with knapsack capacity i. 
	dp = [0 for i in range(W + 1)] 

	ans = 0

	# Fill dp[] using above recursive formula 
	for i in range(W + 1): 
		for j in range(n): 
			if (wt[j] <= i): 
				dp[i] = max(dp[i], dp[i - wt[j]] + val[j]) 

	return dp[W] 

file_path = "Datasets/dataset_10000.txt"


with open(file_path, 'r') as file:
    lines = file.readlines()

    wt = (lines[1].split())
    wt = [int(i) for i in wt]
    val = (lines[3].split())
    val = [int(i) for i in val]

    W = int(0.1 * sum(wt))
        
    bnb = unboundedKnapsack(W, len(val), val, wt)
    print(bnb)

