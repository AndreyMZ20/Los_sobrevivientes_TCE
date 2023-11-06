import numpy as np

def rcosdesign(beta: float, span: float, sps: float, shape='normal'):
    """ Raised cosine FIR filter design
    Calculates square root raised cosine FIR
    filter coefficients with a rolloff factor of `beta`. The filter is
    truncated to `span` symbols and each symbol is represented by `sps`
    samples. rcosdesign designs a symmetric filter. Therefore, the filter
    order, which is `sps*span`, must be even. The filter energy is one.
    Keyword arguments:
    beta  -- rolloff factor of the filter (0 <= beta <= 1)
    span  -- number of symbols that the filter spans
    sps   -- number of samples per symbol
    shape -- `normal` to design a normal raised cosine FIR filter or
             `sqrt` to design a sqre root raised cosine filter
    """

    if beta < 0 or beta > 1:
        raise ValueError("parameter beta must be float between 0 and 1, got {}"
                         .format(beta))

    if span < 0:
        raise ValueError("parameter span must be positive, got {}"
                         .format(span))

    if sps < 0:
        raise ValueError("parameter sps must be positive, got {}".format(span))

    if ((sps*span) % 2) == 1:
        raise ValueError("rcosdesign:OddFilterOrder {}, {}".format(sps, span))

    if shape != 'normal' and shape != 'sqrt':
        raise ValueError("parameter shape must be either 'normal' or 'sqrt'")

    eps = np.finfo(float).eps

    # design the raised cosine filter

    delay = span*sps/2
    t = np.arange(-delay, delay)

    if len(t) % 2 == 0:
        t = np.concatenate([t, [delay]])
    t = t / sps
    b = np.empty(len(t))

    if shape == 'normal':
        # design normal raised cosine filter

        # find non-zero denominator
        denom = (1-np.power(2*beta*t, 2))
        idx1 = np.nonzero(np.fabs(denom) > np.sqrt(eps))[0]

        # calculate filter response for non-zero denominator indices
        b[idx1] = np.sinc(t[idx1])*(np.cos(np.pi*beta*t[idx1])/denom[idx1])/sps

        # fill in the zeros denominator indices
        idx2 = np.arange(len(t))
        idx2 = np.delete(idx2, idx1)

        b[idx2] = beta * np.sin(np.pi/(2*beta)) / (2*sps)

    else:
        # design a square root raised cosine filter

        # find mid-point
        idx1 = np.nonzero(t == 0)[0]
        if len(idx1) > 0:
            b[idx1] = -1 / (np.pi*sps) * (np.pi * (beta-1) - 4*beta)

        # find non-zero denominator indices
        idx2 = np.nonzero(np.fabs(np.fabs(4*beta*t) - 1) < np.sqrt(eps))[0]
        if idx2.size > 0:
            b[idx2] = 1 / (2*np.pi*sps) * (
                np.pi * (beta+1) * np.sin(np.pi * (beta+1) / (4*beta))
                - 4*beta           * np.sin(np.pi * (beta-1) / (4*beta))
                + np.pi*(beta-1)   * np.cos(np.pi * (beta-1) / (4*beta))
            )

        # fill in the zeros denominator indices
        ind = np.arange(len(t))
        idx = np.unique(np.concatenate([idx1, idx2]))
        ind = np.delete(ind, idx)
        nind = t[ind]

        b[ind] = -4*beta/sps * (np.cos((1+beta)*np.pi*nind) +
                                np.sin((1-beta)*np.pi*nind) / (4*beta*nind)) / (
                                np.pi * (np.power(4*beta*nind, 2) - 1))

    # normalize filter energy
    b = b / np.sqrt(np.sum(np.power(b, 2)))
    return b