import acoular as ac
import numpy as np
import spharpy as sph
import matplotlib.pyplot as plt


def plot_directivities() -> None:
    sh_order = 8
    coords = sph.samplings.equalarea(sh_order)
    directivities = ac.directivity.Directivity.__subclasses__()
    fig = plt.figure()
    for directivity in directivities:
        ax = fig.add_subplot(1, len(directivities), directivities.index(directivity) + 1, projection="3d", title=directivity.__name__)
        coeffs = directivity(target_directions=coords.cartesian).coefficients
        sph.plot.balloon(coords, coeffs, ax=ax)

    return fig


if __name__ == "__main__":
    fig = plot_directivities()
    plt.show()
