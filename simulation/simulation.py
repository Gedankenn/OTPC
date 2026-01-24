import matplotlib.pyplot as plt
import numpy as np
import mplcyberpunk

plt.style.use("cyberpunk")

def cria_func(x, x2, A1, A2, intervalo):
    delta = (x - x2)
    a = (A1 - A2) / delta
    b = A2 - a * x2

    vet = []
    for k in np.arange(x, x2, intervalo):
        vet.append(a * k + b)

    return vet


def ref_signal(step):
    x1 = np.arange(0, 2, step)
    y1 = cria_func(0, 2, 0, 5, step)
    x2 = np.arange(2, 5, step)
    y2 = cria_func(2, 5, 5, 5, step)
    x3 = np.arange(5, 7, step)
    y3 = cria_func(5, 7, 5, 0, step)

    # Concatenate segments
    x = np.concatenate((x1, x2, x3))
    y = np.concatenate((y1, y2, y3))

    fig, ax = plt.subplots()
    ax.plot(x, y, label="Reference")
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Amplitude")
    ax.set_title("Reference Signal")
    ax.legend()

    mplcyberpunk.add_glow_effects()
    plt.show()


ref_signal(0.005)

