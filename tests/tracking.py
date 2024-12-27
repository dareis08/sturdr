

## copied originally from signal_test.ipynb
import numpy as np
import os
import matplotlib.pyplot as plt
from sturdr.channel.gps_l1ca_channel import gps_l1ca_code


if __name__ == "__main__":

    print(f"{os.path.basename(__file__)} startup\n")

    TWO_PI = 2 * np.pi

    # signal parameters
    CODE_LEN = 1023                             # chips
    CODE_FREQ = 1.023e6                         # chips/s
    CARRIER_FREQ = 1.57542e9                    # Hz
    KAPPA = CODE_FREQ / CARRIER_FREQ
    SAMP_FREQ = 20e6                             # samples/s
    IF_FREQ = TWO_PI * 5e6                    # rad/s
    T_S = 1 / SAMP_FREQ                         # s

    # test parameters
    init_carrier_doppler = 1800.0                    # Hz
    init_code_doppler = KAPPA * init_carrier_doppler # chips/s
    init_code_phase = 100.0                          # chips
    init_carrier_phase = 0.0                         # rad

    # simulate 1 seconds of signal
    total_time = int(1 * 10)              # ms
    samples_per_ms = int(SAMP_FREQ / 1000)  # samples/ms
    total_len = total_time * samples_per_ms # samples
    gps_code = gps_l1ca_code(1)

    signal = np.zeros(total_len, dtype=np.complex128)
    carrier_phase = np.zeros(total_len, dtype=np.double)
    code_phase = np.zeros(total_len, dtype=np.double)
    carrier_doppler = np.zeros(total_len, dtype=np.double)
    code_doppler = np.zeros(total_len, dtype=np.double)
    for k in range(total_len):
        t_k = k * T_S
        if k == 0:
            carrier_phase[k] = init_carrier_phase
            code_phase[k] = init_code_phase
        else:
            carrier_doppler[k] = init_carrier_doppler + 10*t_k
            code_doppler[k] = KAPPA * carrier_doppler[k]
            carrier_phase[k] = carrier_phase[k-1] + (IF_FREQ + TWO_PI*carrier_doppler[k]) * T_S
            code_phase[k] = code_phase[k-1] + (CODE_FREQ + code_doppler[k]) * T_S
        signal[k] = np.exp(1j * carrier_phase[k]) * gps_code[int(np.mod(code_phase[k], 1023))]


    plt.figure()
    plt.plot(sample_count, np.mod(code_phase[sample_count],1023), label='true', linewidth=2)
    plt.plot(sample_count, np.mod(track_code_phase,1023)+init_code_phase-1023, '--', label='est')
    plt.legend()
    plt.title('Code Phase')

    plt.figure()
    plt.plot(sample_count, carrier_doppler[sample_count], label=True, linewidth=2)
    plt.plot(sample_count, track_doppler, '--', label='est')
    plt.legend()
    plt.title('Doppler')

    plt.figure()
    plt.plot(sample_count, code_doppler[sample_count], label=True, linewidth=2)
    plt.plot(sample_count, track_code_doppler, '--', label='est')
    plt.legend()
    plt.title('Code Doppler')

    plt.show()

    print(carrier_doppler[0], carrier_doppler[-1])
    print(track_doppler[0], track_doppler[-1])
    # print(code_doppler[0], code_doppler[-1])
    # print(code_doppler[0] / track_code_doppler[0])
