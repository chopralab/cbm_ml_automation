using CodecBase

function decode(a :: AbstractString)
    dec = transcode(Base64Decoder(), a)
    reint = reinterpret(Int32, dec[1:12])
    len = reint[2]
    nOn = reint[3]
    dec = dec[13:end]

    ret = BitVector(undef, len)
    ret[1:len] .= false

    current = 1
    position = 0

    for i in 1:nOn

        # Read current position and determine number of others to read
        offset = Int32(0)
        tmp = UInt32(dec[position+=1])
        val = UInt32(tmp)
        if (val & 1) == 0
            shift = 1
        elseif (val & 3) == 1
            tmp = UInt32(dec[position+=1])
            val |= (tmp << 8)
            shift = 2
            offset = 1 << 7
        elseif (val & 7) == 3
            tmp = UInt32(dec[position+=1])
            val |= tmp << 8
            tmp = UInt32(dec[position+=1])
            val |= tmp << 16
            shift = 3
            offset = (1 << 7) + (1 << 14)
        else
            tmp = UInt32(dec[position+=1])
            val |= tmp << 8
            tmp = UInt32(dec[position+=1])
            val |= tmp << 16
            tmp = UInt32(dec[position+=1])
            val |= tmp << 24
            shift = 3
            offset = (1 << 7) + (1 << 14) + (1 << 21)
        end
        num = (val >> shift) + offset

        # Update return vector
        current += num
        ret[current] = true
        current += 1
    end

    ret
end

