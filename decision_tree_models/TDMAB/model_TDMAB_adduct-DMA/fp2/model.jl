using Flux
using CSV
using MLBase
# using CuArrays

all_data = CSV.read("all.csv")

all_matrix = hcat([decode(fp) for fp in all_data[:fingerprint]]...) |> gpu
all_res = all_data[:yield] |> Vector{Float64} |> gpu
all_hot = Flux.onehotbatch(all_res .> 0.9, [true,false]) |> gpu

function validate(folds)

    function make_model(train, train_hot)
        d = Dense(2048, 2) |> gpu
        loss(x,y) = Flux.crossentropy(model(d,x), y)
        for i in 1:1000
            Flux.train!(loss, params(d), ((train, train_hot),), ADAM())
        end

        println(loss(train,train_hot))

        d
    end

    results = []

    for i in folds
        train = all_matrix[:, i]
        train_hot = all_hot[:, i]

        test = all_matrix[:, filter(x -> !(x in i), 1:length(all_res))]
        test_hot = all_hot[:, filter(x -> !(x in i), 1:length(all_res))]
        m = make_model(train, train_hot)

        test_pred = cpu(Flux.onecold(model(m, test)))
        ground_tr = cpu(Flux.onecold(test_hot))

        @show(test_pred, ground_tr)

        roc_s = MLBase.roc(ground_tr .- 1, test_pred .- 1)
        s = f1score(roc_s)
        append!(results,s)
    end

    results
end

