import Random
using DecisionTree
import CSV
using DataFrames

loc = @__DIR__
include(loc * "/prepare_data.jl")
include(loc * "/bootstrap.jl")

results = bootstrap_all(train_matrix, train_res, test_matrix; runs=10000, min_samples_leaf = 2)'
results = results |> DataFrame


results[!,:cutoff] = [0.0, 0.05, 0.10, 0.15, 0.20, 0.30, 0.50, 1.0]
CSV.write("results_no_equal.csv", results)

set_bits = [i[1] for i in (any(train_matrix; dims = 2) |> findall)]

set_bits_tr = train_matrix[set_bits, :]' |> DataFrame
set_bits_tr[!,:yield] = train_res

CSV.write("set_bits_no_equal.csv", set_bits_tr)

set_bits_ts = test_matrix[set_bits, :]' |> DataFrame
CSV.write("set_bits_test_no_equal.csv", set_bits_ts)

