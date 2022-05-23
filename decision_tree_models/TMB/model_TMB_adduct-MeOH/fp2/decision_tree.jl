using DecisionTree
using CSV: read
using DataFrames

include("decode.jl")

using Random
Random.seed!(12345)
rand(12)

all_data = read("train.csv", DataFrame)

all_matrix = hcat([decode(fp) for fp in all_data[!,:fingerprint]]...)
all_res = all_data[!,:yield] |> Vector{Float64}
all_hot = Int.(all_res .> 0.2) .+ 1

h = ["hit", "nohit"]

# Performs 6-fold cross validation
cv = nfoldCV_tree(h[all_hot], all_matrix' |> Matrix, 6)

println(cv)

# Obtain a tree to analyze

tree = build_tree(h[all_hot], all_matrix' |> Matrix)

print_tree(tree)

# Sample tree (boolean):
#Feature 428, Threshold true
#L-> Feature 1018, Threshold true
#    L-> Feature 574, Threshold true
#        L-> hit : 28/28        
#        R-> nohit : 1/1         
#    R-> nohit : 1/1              
#R-> Feature 1948, Threshold true  
#    L-> nohit : 3/3                
#    R-> Feature 2018, Threshold true
#        L-> hit : 2/2 
#        R-> nohit : 1/1

# Sample tree (numeric):
#Feature 428, Threshold 0.5
#L-> Feature 464, Threshold 0.5
#    L-> Feature 1039, Threshold 0.5
#        L-> Feature 1059, Threshold 0.5
#            L-> Feature 1422, Threshold 0.5
#                L-> nohit : 24/24
#                R-> hit : 1/1
#            R-> hit : 1/1
#        R-> hit : 1/1
#    R-> hit : 3/3
#R-> Feature 1367, Threshold 0.5
#    L-> hit : 5/5
#    R-> nohit : 1/1

