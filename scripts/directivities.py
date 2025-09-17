import acoular as ac
import numpy as np
import spharpy as sph
import matplotlib.pyplot as plt
import argparse


def plot_directivities() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--plot_resolution', default= 8, type=int,
                        help='resolution of the directivity plot - in spherical harmonic order')
    parser.add_argument('--sh_order', default = 1, type=int, help='max order of spherical harmonics to plot for sh directivity')
    args = parser.parse_args()
    sh_order = args.plot_resolution
    coords = sph.samplings.equalarea(sh_order)
    directivities = ac.directivity.Directivity.__subclasses__()
    fig = plt.figure()

    # Separate out SphericalHarmonicDirectivity
    normal_directivities = [d for d in directivities if d != ac.SphericalHarmonicDirectivity]

    # Get SH coefficients
    sh_max_order = args.sh_order
    sh_instance = ac.SphericalHarmonicDirectivity(target_directions=coords.cartesian, n=sh_max_order)
    sh_coeffs = sh_instance.coefficients

    # Set up plot layout - normal directivities on top, SH below
    cols = max(len(normal_directivities), sh_max_order*2+1)
    rows = 1 + sh_max_order + 1
    fig = plt.figure(figsize=(4 * cols, 4 * rows))

    for directivity in normal_directivities:
        ax = fig.add_subplot(rows, cols, directivities.index(directivity) + 1, projection="3d", title=directivity.__name__)
        coeffs = directivity(target_directions=coords.cartesian).coefficients
        sph.plot.balloon(coords, coeffs, ax=ax)

    sh_coeff_i = 0
    centre = cols // 2
    for n in range(sh_max_order + 1):
        for m in range(-n, n + 1):
            coeff = sh_coeffs[sh_coeff_i]
            plot_index = cols + (n * cols) + 1 + centre + m
            ax = fig.add_subplot(rows, cols, plot_index, projection="3d", title=f"SphHarm n:{n} m:{m}")
            sph.plot.balloon(coords, coeff, ax=ax)
            sh_coeff_i += 1

    return fig


if __name__ == "__main__":
    fig = plot_directivities()
    plt.show()
