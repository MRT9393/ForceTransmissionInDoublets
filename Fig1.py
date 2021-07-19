# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 21:56:01 2021

@author: Artur Ruppel

"""
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import matplotlib as mpl
import pickle
import seaborn as sns
import pandas as pd
import statannot
import os

# import pylustrator

# mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['font.size'] = 8

# chose an example for force maps
doublet_example = 1
singlet_example = 5

# %% load data for plotting
folder = "C:/Users/Balland/Documents/_forcetransmission_in_cell_doublets_alldata/"
AR1to1d_fullstim_long = pickle.load(open(folder + "analysed_data/AR1to1d_fullstim_long.dat", "rb"))
AR1to1s_fullstim_long = pickle.load(open(folder + "analysed_data/AR1to1s_fullstim_long.dat", "rb"))
AR1to1d_fullstim_short = pickle.load(open(folder + "analysed_data/AR1to1d_fullstim_short.dat", "rb"))
AR1to1s_fullstim_short = pickle.load(open(folder + "analysed_data/AR1to1s_fullstim_short.dat", "rb"))
# AR1to2d_halfstim =        pickle.load(open(folder + "analysed_data/AR1to2d_halfstim.dat", "rb"))
AR1to1d_halfstim = pickle.load(open(folder + "analysed_data/AR1to1d_halfstim.dat", "rb"))
AR1to1s_halfstim = pickle.load(open(folder + "analysed_data/AR1to1s_halfstim.dat", "rb"))
# AR2to1d_halfstim =        pickle.load(open(folder + "analysed_data/AR2to1d_halfstim.dat", "rb"))

# define some colors for the plots
colors_parent = ['#026473', '#E3CC69', '#77C8A6', '#D96248']

figfolder = "C:/Users/Balland/Documents/_forcetransmission_in_cell_doublets_alldata/_Figure1/"
if not os.path.exists(figfolder):
    os.mkdir(figfolder)

# %% prepare dataframe for boxplots

# initialize empty dictionaries
concatenated_data_1to1d = {}
concatenated_data_1to1s = {}
concatenated_data = {}

# loop over all keys
for key1 in AR1to1d_fullstim_long:  # keys are the same for all dictionaries so I'm just taking one example here
    for key2 in AR1to1d_fullstim_long[key1]:
        if AR1to1d_fullstim_long[key1][key2].ndim == 1:  # only 1D data can be stored in the data frame

            # concatenate values from different experiments
            concatenated_data_1to1d[key2] = np.concatenate(
                (AR1to1d_halfstim[key1][key2], AR1to1d_fullstim_short[key1][key2], AR1to1d_fullstim_long[key1][key2]))
            concatenated_data_1to1s[key2] = np.concatenate(
                (AR1to1s_halfstim[key1][key2], AR1to1s_fullstim_short[key1][key2], AR1to1s_fullstim_long[key1][key2]))

            # concatenate doublet and singlet data to create pandas dataframe
            concatenated_data[key2] = np.concatenate((concatenated_data_1to1d[key2], concatenated_data_1to1s[key2]))
key2 = 'spreadingsize_baseline'
# get number of elements for both condition
n_doublets = concatenated_data_1to1d[key2].shape[0]
n_singlets = concatenated_data_1to1s[key2].shape[0]

# create a list of keys with the same dimensions as the data
keys1to1d = ['AR1to1d' for i in range(n_doublets)]
keys1to1s = ['AR1to1s' for i in range(n_singlets)]
keys = np.concatenate((keys1to1d, keys1to1s))

# add keys to dictionary with concatenated data
concatenated_data['keys'] = keys

# Creates DataFrame
df = pd.DataFrame(concatenated_data)

# convert to more convenient units for plotting
df_plot_units = df  # all units here are in SI units
df_plot_units['Es_baseline'] *= 1e12  # convert to fJ
df_plot_units['spreadingsize_baseline'] *= 1e12  # convert to µm²
df_plot_units['sigma_xx_baseline'] *= 1e3  # convert to mN/m
df_plot_units['sigma_yy_baseline'] *= 1e3  # convert to mN/m

# %% plot figure 1C, force maps

# prepare data first

# concatenate TFM maps from different experiments and calculate average maps over first 20 frames and all cells to get average maps
Tx_1to1d_average = np.nanmean(np.concatenate((AR1to1d_halfstim["TFM_data"]["Tx"][:, :, 0:20, :],
                                              AR1to1d_fullstim_short["TFM_data"]["Tx"][:, :, 0:20, :],
                                              AR1to1d_fullstim_long["TFM_data"]["Tx"][:, :, 0:20, :]), axis=3),
                              axis=(2, 3))
Ty_1to1d_average = np.nanmean(np.concatenate((AR1to1d_halfstim["TFM_data"]["Ty"][:, :, 0:20, :],
                                              AR1to1d_fullstim_short["TFM_data"]["Ty"][:, :, 0:20, :],
                                              AR1to1d_fullstim_long["TFM_data"]["Ty"][:, :, 0:20, :]), axis=3),
                              axis=(2, 3))
Tx_1to1s_average = np.nanmean(np.concatenate((AR1to1s_halfstim["TFM_data"]["Tx"][:, :, 0:20, :],
                                              AR1to1s_fullstim_short["TFM_data"]["Tx"][:, :, 0:20, :],
                                              AR1to1s_fullstim_long["TFM_data"]["Tx"][:, :, 0:20, :]), axis=3),
                              axis=(2, 3))
Ty_1to1s_average = np.nanmean(np.concatenate((AR1to1s_halfstim["TFM_data"]["Ty"][:, :, 0:20, :],
                                              AR1to1s_fullstim_short["TFM_data"]["Ty"][:, :, 0:20, :],
                                              AR1to1s_fullstim_long["TFM_data"]["Ty"][:, :, 0:20, :]), axis=3),
                              axis=(2, 3))

# get one example
Tx_1to1d_example = AR1to1d_halfstim["TFM_data"]["Tx"][:, :, 0, doublet_example]
Ty_1to1d_example = AR1to1d_halfstim["TFM_data"]["Ty"][:, :, 0, doublet_example]
Tx_1to1s_example = AR1to1s_halfstim["TFM_data"]["Tx"][:, :, 0, singlet_example]
Ty_1to1s_example = AR1to1s_halfstim["TFM_data"]["Ty"][:, :, 0, singlet_example]

# calculate amplitudes
T_1to1d_average = np.sqrt(Tx_1to1d_average ** 2 + Ty_1to1d_average ** 2)
T_1to1s_average = np.sqrt(Tx_1to1s_average ** 2 + Ty_1to1s_average ** 2)
T_1to1d_example = np.sqrt(Tx_1to1d_example ** 2 + Ty_1to1d_example ** 2)
T_1to1s_example = np.sqrt(Tx_1to1s_example ** 2 + Ty_1to1s_example ** 2)

# crop maps 
crop_start = 8
crop_end = 84

Tx_1to1d_average_crop = Tx_1to1d_average[crop_start:crop_end, crop_start:crop_end] * 1e-3  # convert to kPa
Ty_1to1d_average_crop = Ty_1to1d_average[crop_start:crop_end, crop_start:crop_end] * 1e-3
T_1to1d_average_crop = T_1to1d_average[crop_start:crop_end, crop_start:crop_end] * 1e-3

Tx_1to1d_example_crop = Tx_1to1d_example[crop_start:crop_end, crop_start:crop_end] * 1e-3
Ty_1to1d_example_crop = Ty_1to1d_example[crop_start:crop_end, crop_start:crop_end] * 1e-3
T_1to1d_example_crop = T_1to1d_example[crop_start:crop_end, crop_start:crop_end] * 1e-3

Tx_1to1s_average_crop = Tx_1to1s_average[crop_start:crop_end, crop_start:crop_end] * 1e-3
Ty_1to1s_average_crop = Ty_1to1s_average[crop_start:crop_end, crop_start:crop_end] * 1e-3
T_1to1s_average_crop = T_1to1s_average[crop_start:crop_end, crop_start:crop_end] * 1e-3

Tx_1to1s_example_crop = Tx_1to1s_example[crop_start:crop_end, crop_start:crop_end] * 1e-3
Ty_1to1s_example_crop = Ty_1to1s_example[crop_start:crop_end, crop_start:crop_end] * 1e-3
T_1to1s_example_crop = T_1to1s_example[crop_start:crop_end, crop_start:crop_end] * 1e-3

# set up plot parameters
# *****************************************************************************
n = 4  # every nth arrow will be plotted
pixelsize = 0.864  # in µm
pmax = 2  # kPa

# create x- and y-axis for plotting maps
x_end = np.shape(T_1to1d_average_crop)[1]
y_end = np.shape(T_1to1d_average_crop)[0]
extent = [0, x_end * pixelsize, 0, y_end * pixelsize]

# create mesh for vectorplot    
xq, yq = np.meshgrid(np.linspace(0, extent[1], x_end), np.linspace(0, extent[3], y_end))

fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(3, 2.5))

im = axes[0, 0].imshow(T_1to1d_example_crop, cmap=plt.get_cmap("turbo"), interpolation="bilinear", extent=extent,
                       vmin=0, vmax=pmax, aspect='auto')
axes[0, 0].quiver(xq[::n, ::n], yq[::n, ::n], Tx_1to1d_example_crop[::n, ::n], Ty_1to1d_example_crop[::n, ::n],
                  angles='xy', scale=10, units='width', color="r")
# axes[0,0].set_title('n=1', pad=-400, color='r')

axes[0, 1].imshow(T_1to1d_average_crop, cmap=plt.get_cmap("turbo"), interpolation="bilinear", extent=extent, vmin=0,
                  vmax=pmax, aspect='auto')
axes[0, 1].quiver(xq[::n, ::n], yq[::n, ::n], Tx_1to1d_average_crop[::n, ::n], Ty_1to1d_average_crop[::n, ::n],
                  angles='xy', scale=10, units='width', color="r")

axes[1, 0].imshow(T_1to1s_example_crop, cmap=plt.get_cmap("turbo"), interpolation="bilinear", extent=extent, vmin=0,
                  vmax=pmax, aspect='auto')
axes[1, 0].quiver(xq[::n, ::n], yq[::n, ::n], Tx_1to1s_example_crop[::n, ::n], Ty_1to1s_example_crop[::n, ::n],
                  angles='xy', scale=10, units='width', color="r")

axes[1, 1].imshow(T_1to1s_average_crop, cmap=plt.get_cmap("turbo"), interpolation="bilinear", extent=extent, vmin=0,
                  vmax=pmax, aspect='auto')
axes[1, 1].quiver(xq[::n, ::n], yq[::n, ::n], Tx_1to1s_average_crop[::n, ::n], Ty_1to1s_average_crop[::n, ::n],
                  angles='xy', scale=10, units='width', color="r")

# adjust space in between plots
plt.subplots_adjust(wspace=0.02, hspace=-0.02)

# remove axes
for ax in axes.flat:
    ax.axis('off')
    aspectratio = 1.0
    ratio_default = (ax.get_xlim()[1] - ax.get_xlim()[0]) / (ax.get_ylim()[1] - ax.get_ylim()[0])
    ax.set_aspect(ratio_default * aspectratio)

# add colorbar
cbar = fig.colorbar(im, ax=axes.ravel().tolist())
cbar.ax.set_title('kPa')

# add title
plt.suptitle('Traction forces', y=0.94, x=0.44)

# % start: automatic generated code from pylustrator
plt.figure(1).ax_dict = {ax.get_label(): ax for ax in plt.figure(1).axes}

plt.figure(1).axes[0].set_position([0.125000, 0.505253, 0.306931, 0.368181])
plt.figure(1).axes[1].set_position([0.438069, 0.505253, 0.306931, 0.368181])
plt.figure(1).axes[2].set_position([0.125000, 0.131566, 0.306931, 0.368181])
plt.figure(1).axes[3].set_position([0.438069, 0.131396, 0.306931, 0.368521])
plt.figure(1).text(0.5, 0.5, 'New Text', transform=plt.figure(1).transFigure,
                   color='w')  # id=plt.figure(1).texts[1].new
plt.figure(1).texts[1].set_position([0.252433, 0.838137])
plt.figure(1).texts[1].set_text("n=1")
plt.figure(1).text(0.5, 0.5, 'New Text', transform=plt.figure(1).transFigure,
                   color='w')  # id=plt.figure(1).texts[2].new
plt.figure(1).texts[2].set_position([0.252433, 0.464523])
plt.figure(1).texts[2].set_text("n=1")
plt.figure(1).text(0.5, 0.5, 'New Text', transform=plt.figure(1).transFigure,
                   color='w')  # id=plt.figure(1).texts[3].new
plt.figure(1).texts[3].set_position([0.557647, 0.464523])
plt.figure(1).texts[3].set_text('n=' + str(n_singlets))
plt.figure(1).text(0.5, 0.5, 'New Text', transform=plt.figure(1).transFigure,
                   color='w')  # id=plt.figure(1).texts[4].new
plt.figure(1).texts[4].set_position([0.549791, 0.838137])
plt.figure(1).texts[4].set_text('n=' + str(n_doublets))
# % end: automatic generated code from pylustrator
plt.show()
fig.savefig(figfolder + 'C.png', dpi=300, bbox_inches="tight")

# %% plot figure 1D_1, xx-stress maps

# prepare data first

# concatenate MSM maps from different experiments and calculate average maps over first 20 frames and all cells to get average maps
sigma_xx_1to1d_average = np.nanmean(np.concatenate((AR1to1d_halfstim["MSM_data"]["sigma_xx"][:, :, 0:20, :],
                                                    AR1to1d_fullstim_short["MSM_data"]["sigma_xx"][:, :, 0:20, :],
                                                    AR1to1d_fullstim_long["MSM_data"]["sigma_xx"][:, :, 0:20, :]),
                                                   axis=3), axis=(2, 3))
sigma_xx_1to1s_average = np.nanmean(np.concatenate((AR1to1s_halfstim["MSM_data"]["sigma_xx"][:, :, 0:20, :],
                                                    AR1to1s_fullstim_short["MSM_data"]["sigma_xx"][:, :, 0:20, :],
                                                    AR1to1s_fullstim_long["MSM_data"]["sigma_xx"][:, :, 0:20, :]),
                                                   axis=3), axis=(2, 3))

# get one example
sigma_xx_1to1d_example = AR1to1d_halfstim["MSM_data"]["sigma_xx"][:, :, 0, doublet_example]
sigma_xx_1to1s_example = AR1to1s_halfstim["MSM_data"]["sigma_xx"][:, :, 0, singlet_example]

# convert NaN to 0 to have black background
sigma_xx_1to1d_average[np.isnan(sigma_xx_1to1d_average)] = 0
sigma_xx_1to1s_average[np.isnan(sigma_xx_1to1s_average)] = 0
sigma_xx_1to1d_example[np.isnan(sigma_xx_1to1d_example)] = 0
sigma_xx_1to1s_example[np.isnan(sigma_xx_1to1s_example)] = 0

# crop maps 
crop_start = 8
crop_end = 84

sigma_xx_1to1d_average_crop = sigma_xx_1to1d_average[crop_start:crop_end, crop_start:crop_end] * 1e3  # convert to mN/m
sigma_xx_1to1d_example_crop = sigma_xx_1to1d_example[crop_start:crop_end, crop_start:crop_end] * 1e3
sigma_xx_1to1s_average_crop = sigma_xx_1to1s_average[crop_start:crop_end, crop_start:crop_end] * 1e3
sigma_xx_1to1s_example_crop = sigma_xx_1to1s_example[crop_start:crop_end, crop_start:crop_end] * 1e3

# set up plot parameters
# *****************************************************************************
n = 4  # every nth arrow will be plotted
pixelsize = 0.864  # in µm
pmax = 10  # mN/m

# create x- and y-axis for plotting maps
x_end = np.shape(sigma_xx_1to1d_average_crop)[1]
y_end = np.shape(sigma_xx_1to1d_average_crop)[0]
extent = [0, x_end * pixelsize, 0, y_end * pixelsize]

# create mesh for vectorplot    
xq, yq = np.meshgrid(np.linspace(0, extent[1], x_end), np.linspace(0, extent[3], y_end))

fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(3, 2.5))

im = axes[0, 0].imshow(sigma_xx_1to1d_example_crop, cmap=plt.get_cmap("turbo"), interpolation="bilinear", extent=extent,
                       vmin=0, vmax=pmax, aspect='auto')

axes[0, 1].imshow(sigma_xx_1to1d_average_crop, cmap=plt.get_cmap("turbo"), interpolation="bilinear", extent=extent,
                  vmin=0, vmax=pmax, aspect='auto')

axes[1, 0].imshow(sigma_xx_1to1s_example_crop, cmap=plt.get_cmap("turbo"), interpolation="bilinear", extent=extent,
                  vmin=0, vmax=pmax, aspect='auto')

axes[1, 1].imshow(sigma_xx_1to1s_average_crop, cmap=plt.get_cmap("turbo"), interpolation="bilinear", extent=extent,
                  vmin=0, vmax=pmax, aspect='auto')

# adjust space in between plots
plt.subplots_adjust(wspace=0.02, hspace=-0.02)

# remove axes
for ax in axes.flat:
    ax.axis('off')
    aspectratio = 1.0
    ratio_default = (ax.get_xlim()[1] - ax.get_xlim()[0]) / (ax.get_ylim()[1] - ax.get_ylim()[0])
    ax.set_aspect(ratio_default * aspectratio)

# add colorbar
cbar = fig.colorbar(im, ax=axes.ravel().tolist())
cbar.ax.set_title('mN/m')

# add title
plt.suptitle('xx-Stress', y=0.94, x=0.44)

# % start: automatic generated code from pylustrator
plt.figure(1).ax_dict = {ax.get_label(): ax for ax in plt.figure(1).axes}

plt.figure(1).axes[0].set_position([0.125000, 0.505253, 0.306931, 0.368181])
plt.figure(1).axes[1].set_position([0.438069, 0.505253, 0.306931, 0.368181])
plt.figure(1).axes[2].set_position([0.125000, 0.131566, 0.306931, 0.368181])
plt.figure(1).axes[3].set_position([0.438069, 0.131396, 0.306931, 0.368521])
plt.figure(1).text(0.5, 0.5, 'New Text', transform=plt.figure(1).transFigure,
                   color='w')  # id=plt.figure(1).texts[1].new
plt.figure(1).texts[1].set_position([0.252433, 0.838137])
plt.figure(1).texts[1].set_text("n=1")
plt.figure(1).text(0.5, 0.5, 'New Text', transform=plt.figure(1).transFigure,
                   color='w')  # id=plt.figure(1).texts[2].new
plt.figure(1).texts[2].set_position([0.252433, 0.464523])
plt.figure(1).texts[2].set_text("n=1")
plt.figure(1).text(0.5, 0.5, 'New Text', transform=plt.figure(1).transFigure,
                   color='w')  # id=plt.figure(1).texts[3].new
plt.figure(1).texts[3].set_position([0.557647, 0.464523])
plt.figure(1).texts[3].set_text('n=' + str(n_singlets))
plt.figure(1).text(0.5, 0.5, 'New Text', transform=plt.figure(1).transFigure,
                   color='w')  # id=plt.figure(1).texts[4].new
plt.figure(1).texts[4].set_position([0.549791, 0.838137])
plt.figure(1).texts[4].set_text('n=' + str(n_doublets))
# % end: automatic generated code from pylustrator

# save figure
fig.savefig(figfolder + 'D1.png', dpi=300, bbox_inches="tight")
plt.show()

# %% plot figure 1D_2, yy-stress maps

# prepare data first

# concatenate MSM maps from different experiments and calculate average maps over first 20 frames and all cells to get average maps
sigma_yy_1to1d_average = np.nanmean(np.concatenate((AR1to1d_halfstim["MSM_data"]["sigma_yy"][:, :, 0:20, :],
                                                    AR1to1d_fullstim_short["MSM_data"]["sigma_yy"][:, :, 0:20, :],
                                                    AR1to1d_fullstim_long["MSM_data"]["sigma_yy"][:, :, 0:20, :]),
                                                   axis=3), axis=(2, 3))
sigma_yy_1to1s_average = np.nanmean(np.concatenate((AR1to1s_halfstim["MSM_data"]["sigma_yy"][:, :, 0:20, :],
                                                    AR1to1s_fullstim_short["MSM_data"]["sigma_yy"][:, :, 0:20, :],
                                                    AR1to1s_fullstim_long["MSM_data"]["sigma_yy"][:, :, 0:20, :]),
                                                   axis=3), axis=(2, 3))

# get one example
sigma_yy_1to1d_example = AR1to1d_halfstim["MSM_data"]["sigma_yy"][:, :, 0, doublet_example]
sigma_yy_1to1s_example = AR1to1s_halfstim["MSM_data"]["sigma_yy"][:, :, 0, singlet_example]

# convert NaN to 0 to have black background
sigma_yy_1to1d_average[np.isnan(sigma_yy_1to1d_average)] = 0
sigma_yy_1to1s_average[np.isnan(sigma_yy_1to1s_average)] = 0
sigma_yy_1to1d_example[np.isnan(sigma_yy_1to1d_example)] = 0
sigma_yy_1to1s_example[np.isnan(sigma_yy_1to1s_example)] = 0

# crop maps 
crop_start = 8
crop_end = 84

sigma_yy_1to1d_average_crop = sigma_yy_1to1d_average[crop_start:crop_end, crop_start:crop_end] * 1e3
sigma_yy_1to1d_example_crop = sigma_yy_1to1d_example[crop_start:crop_end, crop_start:crop_end] * 1e3
sigma_yy_1to1s_average_crop = sigma_yy_1to1s_average[crop_start:crop_end, crop_start:crop_end] * 1e3
sigma_yy_1to1s_example_crop = sigma_yy_1to1s_example[crop_start:crop_end, crop_start:crop_end] * 1e3

# set up plot parameters
# *****************************************************************************
n = 4  # every nth arrow will be plotted
pixelsize = 0.864  # in µm
pmax = 10  # mN/m

# create x- and y-axis for plotting maps
x_end = np.shape(sigma_xx_1to1d_average_crop)[1]
y_end = np.shape(sigma_xx_1to1d_average_crop)[0]
extent = [0, x_end * pixelsize, 0, y_end * pixelsize]

# create mesh for vectorplot    
xq, yq = np.meshgrid(np.linspace(0, extent[1], x_end), np.linspace(0, extent[3], y_end))

fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(3, 2.5))

im = axes[0, 0].imshow(sigma_yy_1to1d_example_crop, cmap=plt.get_cmap("turbo"), interpolation="bilinear", extent=extent,
                       vmin=0, vmax=pmax, aspect='auto')

axes[0, 1].imshow(sigma_yy_1to1d_average_crop, cmap=plt.get_cmap("turbo"), interpolation="bilinear", extent=extent,
                  vmin=0, vmax=pmax, aspect='auto')

axes[1, 0].imshow(sigma_yy_1to1s_example_crop, cmap=plt.get_cmap("turbo"), interpolation="bilinear", extent=extent,
                  vmin=0, vmax=pmax, aspect='auto')

axes[1, 1].imshow(sigma_yy_1to1s_average_crop, cmap=plt.get_cmap("turbo"), interpolation="bilinear", extent=extent,
                  vmin=0, vmax=pmax, aspect='auto')

# adjust space in between plots
plt.subplots_adjust(wspace=0.02, hspace=-0.02)

# remove axes
for ax in axes.flat:
    ax.axis('off')
    aspectratio = 1.0
    ratio_default = (ax.get_xlim()[1] - ax.get_xlim()[0]) / (ax.get_ylim()[1] - ax.get_ylim()[0])
    ax.set_aspect(ratio_default * aspectratio)

# add colorbar
cbar = fig.colorbar(im, ax=axes.ravel().tolist())
cbar.ax.set_title('mN/m')

# add title
plt.suptitle('yy-Stress', y=0.94, x=0.44)

# % start: automatic generated code from pylustrator
plt.figure(1).ax_dict = {ax.get_label(): ax for ax in plt.figure(1).axes}

plt.figure(1).axes[0].set_position([0.125000, 0.505253, 0.306931, 0.368181])
plt.figure(1).axes[1].set_position([0.438069, 0.505253, 0.306931, 0.368181])
plt.figure(1).axes[2].set_position([0.125000, 0.131566, 0.306931, 0.368181])
plt.figure(1).axes[3].set_position([0.438069, 0.131396, 0.306931, 0.368521])
plt.figure(1).text(0.5, 0.5, 'New Text', transform=plt.figure(1).transFigure,
                   color='w')  # id=plt.figure(1).texts[1].new
plt.figure(1).texts[1].set_position([0.252433, 0.838137])
plt.figure(1).texts[1].set_text("n=1")
plt.figure(1).text(0.5, 0.5, 'New Text', transform=plt.figure(1).transFigure,
                   color='w')  # id=plt.figure(1).texts[2].new
plt.figure(1).texts[2].set_position([0.252433, 0.464523])
plt.figure(1).texts[2].set_text("n=1")
plt.figure(1).text(0.5, 0.5, 'New Text', transform=plt.figure(1).transFigure,
                   color='w')  # id=plt.figure(1).texts[3].new
plt.figure(1).texts[3].set_position([0.557647, 0.464523])
plt.figure(1).texts[3].set_text('n=' + str(n_singlets))
plt.figure(1).text(0.5, 0.5, 'New Text', transform=plt.figure(1).transFigure,
                   color='w')  # id=plt.figure(1).texts[4].new
plt.figure(1).texts[4].set_position([0.549791, 0.838137])
plt.figure(1).texts[4].set_text('n=' + str(n_doublets))
# % end: automatic generated code from pylustrator

# save figure
fig.savefig(figfolder + 'D2.png', dpi=300, bbox_inches="tight")
plt.show()

# %% plot figure 1E boxplots

# define plot parameters
fig = plt.figure(2, figsize=(9, 2))  # figuresize in inches
gs = gridspec.GridSpec(1, 5)  # sets up subplotgrid rows by columns
gs.update(wspace=0.5, hspace=0.25)  # adjusts space in between the boxes in the grid
colors = [colors_parent[1], colors_parent[2]]  # defines colors
sns.set_palette(sns.color_palette(colors))  # sets colors
linewidth_bp = 0.7  # linewidth of boxplot borders
width = 0.3  # width of boxplots
dotsize = 1.8  # size of datapoints in swarmplot
linewidth_sw = 0.3  # linewidth of boxplot borders
alpha_sw = 1  # transparency of dots in swarmplot
alpha_bp = 0.8  # transparency of boxplots
ylabeloffset = 1.4  # adjusts distance of ylabel to the plot
titleoffset = 3  # adjusts distance of title to the plot

##############################################################################
# Generate first panel
##############################################################################

# extract data from dataframe to test if their distribution is gaussian
data_1to1d = df[df["keys"] == "AR1to1d"]["spreadingsize_baseline"].to_numpy()
data_1to1s = df[df["keys"] == "AR1to1s"]["spreadingsize_baseline"].to_numpy()

test = 'Mann-Whitney'

ymin = 500
ymax = 2000
stat_annotation_offset = 0.22

# the grid spec is rows, then columns
fig_ax = fig.add_subplot(gs[0, 0])

# set plot variables
x = 'keys'
y = 'spreadingsize_baseline'

# create box- and swarmplots
sns.swarmplot(x=x, y=y, data=df, ax=fig_ax, alpha=alpha_sw, linewidth=linewidth_sw, zorder=0, size=dotsize)
bp = sns.boxplot(x=x, y=y, data=df, ax=fig_ax, linewidth=linewidth_bp, notch=True, showfliers=False, width=width)

order = ['AR1to1d', 'AR1to1s']
statannot.add_stat_annotation(bp, data=df, x=x, y=y, order=order, box_pairs=[('AR1to1d', 'AR1to1s')],
                              line_offset_to_box=stat_annotation_offset, test=test, text_format='star', loc='inside', verbose=2)

# make boxplots transparent
for patch in bp.artists:
    r, g, b, a = patch.get_facecolor()
    patch.set_facecolor((r, g, b, alpha_bp))

plt.setp(bp.artists, edgecolor='k')
plt.setp(bp.lines, color='k')

# set labels
fig_ax.set_xticklabels(['Doublet', 'Singlet'])
fig_ax.set_xlabel(xlabel=None)
fig_ax.set_ylabel(ylabel='A [$\mathrm{\mu m^2}$]', labelpad=ylabeloffset)
fig_ax.set_title(label='Spreading size', pad=titleoffset)
fig_ax.set()

# Define where you want ticks
yticks = np.arange(500, 2001, 250)
plt.yticks(yticks)

# provide info on tick parameters
plt.minorticks_on()
plt.tick_params(direction='in', which='minor', length=3, bottom=False, top=False, left=True, right=True)
plt.tick_params(direction='in', which='major', length=6, bottom=False, top=False, left=True, right=True)

# set limits
fig_ax.set_ylim(ymin=ymin)
fig_ax.set_ylim(ymax=ymax)

##############################################################################
# Generate second panel
##############################################################################

# extract data from dataframe to test if their distribution is gaussian
data_1to1d = df[df["keys"] == "AR1to1d"]["Es_baseline"].to_numpy()
data_1to1s = df[df["keys"] == "AR1to1s"]["Es_baseline"].to_numpy()

test = 'Mann-Whitney'

ymin = 0
ymax = 2
stat_annotation_offset = -0.09  # adjust y-position of statistical annotation

# the grid spec is rows, then columns
fig_ax = fig.add_subplot(gs[0, 1])

# set plot variables
x = 'keys'
y = 'Es_baseline'

sns.swarmplot(x=x, y=y, data=df, ax=fig_ax, alpha=alpha_sw, linewidth=linewidth_sw, zorder=0, size=dotsize)
bp = sns.boxplot(x=x, y=y, data=df, ax=fig_ax, linewidth=linewidth_bp, notch=True, showfliers=False, width=width)

order = ['AR1to1d', 'AR1to1s']
statannot.add_stat_annotation(bp, data=df, x=x, y=y, order=order, box_pairs=[('AR1to1d', 'AR1to1s')],
                              line_offset_to_box=stat_annotation_offset, test=test, text_format='star', loc='inside', verbose=2)

# make boxplots transparent
for patch in bp.artists:
    r, g, b, a = patch.get_facecolor()
    patch.set_facecolor((r, g, b, alpha_bp))

plt.setp(bp.artists, edgecolor='k')
plt.setp(bp.lines, color='k')

# set labels
fig_ax.set_xticklabels(['Doublet', 'Singlet'])
fig_ax.set_xlabel(xlabel=None)
fig_ax.set_ylabel(ylabel='$\mathrm{E_s}$ [pJ]', labelpad=ylabeloffset)
fig_ax.set_title(label='Strain energy', pad=titleoffset)
fig_ax.set()

# Define where you want ticks
yticks = np.arange(0, 2.1, 0.5)
plt.yticks(yticks)

# provide info on tick parameters
plt.minorticks_on()
plt.tick_params(direction='in', which='minor', length=3, bottom=False, top=False, left=True, right=True)
plt.tick_params(direction='in', which='major', length=6, bottom=False, top=False, left=True, right=True)

# set limits
fig_ax.set_ylim(ymin=ymin)
fig_ax.set_ylim(ymax=ymax)

##############################################################################
# Generate third panel
##############################################################################

# extract data from dataframe to test if their distribution is gaussian
data_1to1d = df[df["keys"] == "AR1to1d"]["sigma_xx_baseline"].to_numpy()
data_1to1s = df[df["keys"] == "AR1to1s"]["sigma_xx_baseline"].to_numpy()

test = 'Mann-Whitney'

ymin = 0
ymax = 14
stat_annotation_offset = -0.07  # adjust y-position of statistical annotation

# the grid spec is rows, then columns
fig_ax = fig.add_subplot(gs[0, 2])

# set plot variables
x = 'keys'
y = 'sigma_xx_baseline'

sns.swarmplot(x=x, y=y, data=df, ax=fig_ax, alpha=alpha_sw, linewidth=linewidth_sw, zorder=0, size=dotsize)
bp = sns.boxplot(x=x, y=y, data=df, ax=fig_ax, linewidth=linewidth_bp, notch=True, showfliers=False, width=width)

order = ['AR1to1d', 'AR1to1s']
statannot.add_stat_annotation(bp, data=df, x=x, y=y, order=order, box_pairs=[('AR1to1d', 'AR1to1s')],
                              line_offset_to_box=stat_annotation_offset, test=test, text_format='star', loc='inside', verbose=2)

# make boxplots transparent
for patch in bp.artists:
    r, g, b, a = patch.get_facecolor()
    patch.set_facecolor((r, g, b, alpha_bp))

plt.setp(bp.artists, edgecolor='k')
plt.setp(bp.lines, color='k')

# set labels
fig_ax.set_xticklabels(['Doublet', 'Singlet'])
fig_ax.set_xlabel(xlabel=None)
fig_ax.set_ylabel(ylabel='$\mathrm{\sigma _{xx}}$ [mN/m]', labelpad=ylabeloffset)
fig_ax.set_title(label='xx-Stress', pad=titleoffset)
fig_ax.set()

# Define where you want ticks
yticks = np.arange(0, 15, 2)
plt.yticks(yticks)

# provide info on tick parameters
plt.minorticks_on()
plt.tick_params(direction='in', which='minor', length=3, bottom=False, top=False, left=True, right=True)
plt.tick_params(direction='in', which='major', length=6, bottom=False, top=False, left=True, right=True)

# set limits
fig_ax.set_ylim(ymin=ymin)
fig_ax.set_ylim(ymax=ymax)

##############################################################################
# Generate fourth panel
##############################################################################

# extract data from dataframe to test if their distribution is gaussian
data_1to1d = df[df["keys"] == "AR1to1d"]["sigma_yy_baseline"].to_numpy()
data_1to1s = df[df["keys"] == "AR1to1s"]["sigma_yy_baseline"].to_numpy()

test = 'Mann-Whitney'

ymin = 0
ymax = 14
stat_annotation_offset = 1.03  # adjust y-position of statistical annotation

# the grid spec is rows, then columns
fig_ax = fig.add_subplot(gs[0, 3])

# set plot variables
x = 'keys'
y = 'sigma_yy_baseline'

sns.swarmplot(x=x, y=y, data=df, ax=fig_ax, alpha=alpha_sw, linewidth=linewidth_sw, zorder=0, size=dotsize)
bp = sns.boxplot(x=x, y=y, data=df, ax=fig_ax, linewidth=linewidth_bp, notch=True, showfliers=False, width=width)

order = ['AR1to1d', 'AR1to1s']
statannot.add_stat_annotation(bp, data=df, x=x, y=y, order=order, box_pairs=[('AR1to1d', 'AR1to1s')],
                              line_offset_to_box=stat_annotation_offset, test=test, text_format='star', loc='inside', verbose=2)

# make boxplots transparent
for patch in bp.artists:
    r, g, b, a = patch.get_facecolor()
    patch.set_facecolor((r, g, b, alpha_bp))

plt.setp(bp.artists, edgecolor='k')
plt.setp(bp.lines, color='k')

# set labels
fig_ax.set_xticklabels(['Doublet', 'Singlet'])
fig_ax.set_xlabel(xlabel=None)
fig_ax.set_ylabel(ylabel='$\mathrm{\sigma _{yy}}$ [mN/m]', labelpad=ylabeloffset)
fig_ax.set_title(label='yy-Stress', pad=titleoffset)
fig_ax.set()

# Define where you want ticks
yticks = np.arange(0, 15, 2)
plt.yticks(yticks)

# provide info on tick parameters
plt.minorticks_on()
plt.tick_params(direction='in', which='minor', length=3, bottom=False, top=False, left=True, right=True)
plt.tick_params(direction='in', which='major', length=6, bottom=False, top=False, left=True, right=True)

# set limits
fig_ax.set_ylim(ymin=ymin)
fig_ax.set_ylim(ymax=ymax)

##############################################################################
# Generate fifth panel
##############################################################################
ymin = -1
ymax = 1
stat_annotation_offset = 0.03  # adjust y-position of statistical annotation
ylabeloffset = -2

# extract data from dataframe to test if their distribution is gaussian
data_1to1d = df[df["keys"] == "AR1to1d"]["AIC_baseline"].to_numpy()
data_1to1s = df[df["keys"] == "AR1to1s"]["AIC_baseline"].to_numpy()

test = 'Mann-Whitney'

# the grid spec is rows, then columns
fig_ax = fig.add_subplot(gs[0, 4])

# set plot variables
x = 'keys'
y = 'AIC_baseline'

sns.swarmplot(x=x, y=y, data=df, ax=fig_ax, alpha=alpha_sw, linewidth=linewidth_sw, zorder=0, size=dotsize)
bp = sns.boxplot(x=x, y=y, data=df, ax=fig_ax, linewidth=linewidth_bp, notch=True, showfliers=False, width=width)

order = ['AR1to1d', 'AR1to1s']
statannot.add_stat_annotation(bp, data=df, x=x, y=y, order=order, box_pairs=[('AR1to1d', 'AR1to1s')],
                              line_offset_to_box=stat_annotation_offset, test=test, text_format='star', loc='inside', verbose=2)

# make boxplots transparent
for patch in bp.artists:
    r, g, b, a = patch.get_facecolor()
    patch.set_facecolor((r, g, b, alpha_bp))

plt.setp(bp.artists, edgecolor='k')
plt.setp(bp.lines, color='k')

# set labels
fig_ax.set_xticklabels(['Doublet', 'Singlet'])
fig_ax.set_xlabel(xlabel=None)
fig_ax.set_ylabel(ylabel='AIC', labelpad=ylabeloffset)
fig_ax.set_title(label='Anisotropy coefficient', pad=titleoffset)
fig_ax.set()

# Define where you want ticks
yticks = np.arange(-1, 1.1, 0.5)
plt.yticks(yticks)

# provide info on tick parameters
plt.minorticks_on()
plt.tick_params(direction='in', which='minor', length=3, bottom=False, top=False, left=True, right=True)
plt.tick_params(direction='in', which='major', length=6, bottom=False, top=False, left=True, right=True)

# set limits
fig_ax.set_ylim(ymin=ymin)
fig_ax.set_ylim(ymax=ymax)

# save plot to file
plt.savefig(figfolder + 'E.png', dpi=300, bbox_inches="tight")
plt.show()
