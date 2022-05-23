
loc = @__DIR__

include(loc * "/decode.jl")
train_data = CSV.read("train.csv")

train_matrix = hcat([decode(fp) for fp in train_data[:fingerprint]]...)
train_res = train_data[:yield] |> Vector{Float64}

test = CSV.read("test.csv")[:fingerprint]

test_matrix = hcat(decode.(test)...)

nothing
