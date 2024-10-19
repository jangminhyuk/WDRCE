#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file generates Figure 2(a), (b)

import numpy as np
import matplotlib.pyplot as plt
import argparse
import pickle
import os
import re
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
import matplotlib.ticker as ticker
from matplotlib import cm
from scipy.interpolate import interp1d

def summarize_theta_w(lqg_theta_w_values, lqg_theta_v_values, lqg_cost_values ,wdrc_theta_w_values, wdrc_theta_v_values, wdrc_cost_values , drce_theta_w_values, drce_theta_v_values, drce_cost_values, drlqc_theta_w_values, drlqc_theta_v_values, drlqc_cost_values, dist, noise_dist, infinite, use_lambda, path):
    
    surfaces = []
    labels = []
    # Create 3D plot
    plt.rcParams.update({
    "text.usetex": True,
    "text.latex.preamble": r"\usepackage{amsmath}",
    })
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
     # Collect all cost values to determine z-limits
    all_cost_values = np.concatenate([lqg_cost_values, wdrc_cost_values, drce_cost_values, drlqc_cost_values])
    z_min = 0.999 * np.min(all_cost_values)
    z_max = 1.001 * np.max(all_cost_values)
    # -------------------
    # LQG
    # Interpolate cost values for smooth surface - LQG
    theta_w_grid_lqg, theta_v_grid_lqg = np.meshgrid(
        np.linspace(min(lqg_theta_w_values), max(lqg_theta_w_values), 100),
        np.linspace(min(lqg_theta_v_values), max(lqg_theta_v_values), 100)
    )
    cost_grid_lqg = griddata(
        (lqg_theta_w_values, lqg_theta_v_values), lqg_cost_values,
        (theta_w_grid_lqg, theta_v_grid_lqg), method='cubic'
    )

    # Plot smooth surface - LQG
    surface_lqg =ax.plot_surface(theta_w_grid_lqg, theta_v_grid_lqg, cost_grid_lqg, alpha=0.5, color='red', label='LQG')
    surfaces.append(surface_lqg)
    labels.append('LQG')
    #-------------------------
    # Repeat the process for WDRC
    # Interpolate cost values for smooth surface - WDRC
    theta_w_grid_wdrc, theta_v_grid_wdrc = np.meshgrid(
    np.linspace(min(wdrc_theta_w_values), max(wdrc_theta_w_values), 100),
    np.linspace(min(wdrc_theta_v_values), max(wdrc_theta_v_values), 100)
    )
    cost_grid_wdrc = griddata(
        (wdrc_theta_w_values, wdrc_theta_v_values), wdrc_cost_values,
        (theta_w_grid_wdrc, theta_v_grid_wdrc), method='linear'  # Use linear interpolation
    )

    # Plot smooth surface - WDRC
    surface_wdrc =ax.plot_surface(theta_w_grid_wdrc, theta_v_grid_wdrc, cost_grid_wdrc, alpha=0.6, color='blue', label='WDRC')
    surfaces.append(surface_wdrc)
    labels.append('WDRC [12]')
    #--------------

    # Interpolate cost values for smooth surface - DRLQC
    theta_w_grid_drlqc, theta_v_grid_drlqc = np.meshgrid(
        np.linspace(min(drlqc_theta_w_values), max(drlqc_theta_w_values), 100),
        np.linspace(min(drlqc_theta_v_values), max(drlqc_theta_v_values), 100)
    )
    cost_grid_drlqc = griddata(
        (drlqc_theta_w_values, drlqc_theta_v_values), drlqc_cost_values,
        (theta_w_grid_drlqc, theta_v_grid_drlqc), method='cubic'
    )
    
    # Plot smooth surface - DCE
    surface_drlqc = ax.plot_surface(theta_w_grid_drlqc, theta_v_grid_drlqc, cost_grid_drlqc, alpha=0.6, color='gold', label='DRLQC', antialiased=False)
    surfaces.append(surface_drlqc)
    labels.append('DRLQC [14]')
    
    #--------------
    # Interpolate cost values for smooth surface - DRCE
    theta_w_grid_drce, theta_v_grid_drce = np.meshgrid(
        np.linspace(min(drce_theta_w_values), max(drce_theta_w_values), 100),
        np.linspace(min(drce_theta_v_values), max(drce_theta_v_values), 100)
    )
    cost_grid_drce = griddata(
        (drce_theta_w_values, drce_theta_v_values), drce_cost_values,
        (theta_w_grid_drce, theta_v_grid_drce), method='cubic'
    )
    
    # Plot smooth surface - DCE
    surface_drce = ax.plot_surface(theta_w_grid_drce, theta_v_grid_drce, cost_grid_drce, alpha=0.5, color='green', label='WDR-CE', antialiased=False)
    surfaces.append(surface_drce)
    labels.append('WDR-CE [Ours]')
    
    #---------------
    legend = fig.legend(
    handles=surfaces,
    labels=labels,
    bbox_to_anchor=(0.8, 0.7),
    loc='center right',
    frameon=True,
    framealpha=1.0,
    facecolor='white'
    )
    legend.get_frame().set_alpha(1.0) 
    legend.get_frame().set_facecolor('white')
    
    # Set labels
    ax.set_xlabel(r'$\theta_w$', fontsize=16)
    ax.set_ylabel(r'$\theta_v$', fontsize=16)
    ax.set_zlabel(r'Total Cost', fontsize=16, labelpad=3)
    # Set z-axis limits
    ax.set_zlim(z_min, z_max)
    
    ax.view_init(elev=14, azim=35)
    ax.zaxis.set_rotate_label(False)
    a = ax.zaxis.label.get_rotation()
    if a<180:
        a += 90
    ax.zaxis.label.set_rotation(a)
    a = ax.zaxis.label.get_rotation()
    ax.set_zlabel(r'Total Cost', fontsize=16, labelpad=3)
    plt.show()
    fig.savefig(path + 'params_{}_{}_zeromean.pdf'.format(dist, noise_dist), dpi=300, bbox_inches="tight", pad_inches=0.3)
    #plt.clf()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--dist', required=False, default="normal", type=str) #disurbance distribution (normal or uniform or quadratic)
    parser.add_argument('--noise_dist', required=False, default="normal", type=str) #noise distribution (normal or uniform or quadratic)
    parser.add_argument('--infinite', required=False, action="store_true") #infinite horizon settings if flagged
    parser.add_argument('--use_lambda', required=False, action="store_true") #DEPRECATED !! (use lambda results if flagged)
    args = parser.parse_args()
    
    
    if args.use_lambda:
        path = "./results/{}_{}/finite/multiple/DRLQC/params_lambda/zero/".format(args.dist, args.noise_dist)
    else:
        path = "./results/{}_{}/finite/multiple/DRLQC/params_thetas/zero/".format(args.dist, args.noise_dist)

    #Load data
    drlqc_theta_w_values =[]
    drlqc_lambda_values = []
    drlqc_theta_v_values = []
    drlqc_cost_values = []
    
    drce_theta_w_values =[]
    drce_lambda_values = []
    drce_theta_v_values = []
    drce_cost_values = []
    
    wdrc_theta_w_values = []
    wdrc_lambda_values = []
    wdrc_theta_v_values = []
    wdrc_cost_values = []
    
    lqg_theta_w_values =[]
    lqg_lambda_values = []
    lqg_theta_v_values = []
    lqg_cost_values = []
    
    drlqc_optimal_theta_w, drlqc_optimal_theta_v, drlqc_optimal_cost = 0, 0, 99999999
    drce_optimal_theta_w, drce_optimal_theta_v, drce_optimal_cost = 0, 0, 99999999
    wdrc_optimal_theta_w, wdrc_optimal_cost = 0, 99999999
    # TODO : Modify the theta_v_list and lambda_list below to match your experiments!!! 
    
    theta_v_list = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0] # radius of noise ambiguity set
    theta_w_list = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0] # radius of disturbance ambiguity set
    
    if args.dist=='normal':
        lambda_list = [12, 15, 20, 25, 30, 35, 40, 45, 50] # disturbance distribution penalty parameter
        theta_v_list = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
        theta_w_list = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
    else:
        lambda_list = [15, 20, 25, 30, 35, 40, 45, 50] # disturbance distribution penalty parameter
        theta_v_list = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
        theta_w_list = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
        
    # Regular expression pattern to extract numbers from file names
    
    if args.use_lambda:
        pattern_drce = r"drce_(\d+)and_(\d+(?:\.\d+)?)_?(\d+(?:_\d+)?)?"
        pattern_drlqc = r"drlqc_(\d+)and_(\d+(?:\.\d+)?)_?(\d+(?:_\d+)?)?"
        pattern_wdrc = r"wdrc_(\d+)"
    else:
        pattern_drlqc = r"drlqc_(\d+(?:\.\d+)?)_?(\d+(?:_\d+)?)?and_(\d+(?:\.\d+)?)_?(\d+(?:_\d+)?)?"
        pattern_drce = r"drce_(\d+(?:\.\d+)?)_?(\d+(?:_\d+)?)?and_(\d+(?:\.\d+)?)_?(\d+(?:_\d+)?)?"
        pattern_wdrc = r"wdrc_(\d+(?:\.\d+)?)_?(\d+(?:_\d+)?)?"
    pattern_lqg = r"lqg.pkl"
    
    print(path)
    # Iterate over each file in the directory
    for filename in os.listdir(path):
        match = re.search(pattern_drce, filename)
        if match:
            if args.use_lambda:
                lambda_value = float(match.group(1))  # Extract lambda
                theta_v_value = float(match.group(2))   # Extract theta_v value
                theta_v_str = match.group(3)
                theta_v_value += float(theta_v_str)/10
                #changed _1_5_ to 1.5!
                # Store theta_w and theta values
                drce_lambda_values.append(lambda_value)
                drce_theta_v_values.append(theta_v_value)
            else:
                theta_w_value = float(match.group(1))  # Extract theta_w value
                theta_w_str = match.group(2)
                theta_w_value += float(theta_w_str)/10
                theta_v_value = float(match.group(3))   # Extract theta_v value
                theta_v_str = match.group(4)
                theta_v_value += float(theta_v_str)/10
                #changed _1_5_ to 1.5!
                # Store theta_w and theta values
                drce_theta_w_values.append(theta_w_value)
                drce_theta_v_values.append(theta_v_value)
            
            drce_file = open(path + filename, 'rb')
            drce_cost = pickle.load(drce_file)
            if drce_cost[0]<drce_optimal_cost:
                drce_optimal_cost = drce_cost[0]
                drce_optimal_theta_w = theta_w_value
                drce_optimal_theta_v = theta_v_value
            drce_file.close()
            drce_cost_values.append(drce_cost[0])  # Store cost value
        else:
            match_drlqc = re.search(pattern_drlqc, filename)
            if match_drlqc:
                if args.use_lambda:
                    lambda_value = float(match_drlqc.group(1))  # Extract lambda
                    theta_v_value = float(match_drlqc.group(2))   # Extract theta_v value
                    theta_v_str = match_drlqc.group(3)
                    theta_v_value += float(theta_v_str)/10
                    #changed _1_5_ to 1.5!
                    # Store theta_w and theta values
                    drlqc_lambda_values.append(lambda_value)
                    drlqc_theta_v_values.append(theta_v_value)
                else:
                    theta_w_value = float(match_drlqc.group(1))  # Extract theta_w value
                    theta_w_str = match_drlqc.group(2)
                    theta_w_value += float(theta_w_str)/10
                    theta_v_value = float(match_drlqc.group(3))   # Extract theta_v value
                    theta_v_str = match_drlqc.group(4)
                    theta_v_value += float(theta_v_str)/10
                    #changed _1_5_ to 1.5!
                    # Store theta_w and theta values
                    drlqc_theta_w_values.append(theta_w_value)
                    drlqc_theta_v_values.append(theta_v_value)
                
                drlqc_file = open(path + filename, 'rb')
                drlqc_cost = pickle.load(drlqc_file)
                if drlqc_cost[0]<drlqc_optimal_cost:
                    drlqc_optimal_cost = drlqc_cost[0]
                    drlqc_optimal_theta_w = theta_w_value
                    drlqc_optimal_theta_v = theta_v_value
                drlqc_file.close()
                drlqc_cost_values.append(drlqc_cost[0])  # Store cost value
            else:
                match_wdrc = re.search(pattern_wdrc, filename)
                if match_wdrc: # wdrc
                    if args.use_lambda:
                        lambda_value = float(match_wdrc.group(1))  # Extract lambda
                    else:
                        theta_w_value = float(match_wdrc.group(1))  # Extract theta_w value
                        theta_w_str = match_wdrc.group(2)
                        theta_w_value += float(theta_w_str)/10
                    wdrc_file = open(path + filename, 'rb')
                    wdrc_cost = pickle.load(wdrc_file)
                    if wdrc_cost[0] < wdrc_optimal_cost:
                        #print("WDRC!!!{} & {}".format(wdrc_cost[0], theta_w_value))
                        wdrc_optimal_cost = wdrc_cost[0]
                        wdrc_optimal_theta_w = theta_w_value
                    wdrc_file.close()
                    for aux_theta_v in theta_v_list:
                        if args.use_lambda:
                            wdrc_lambda_values.append(lambda_value)
                        else:
                            wdrc_theta_w_values.append(theta_w_value)
                        wdrc_theta_v_values.append(aux_theta_v) # since wdrc not affected by theta v, just add auxilary theta for plot
                        wdrc_cost_values.append(wdrc_cost[0])
                else:
                    match_lqg = re.search(pattern_lqg, filename)
                    if match_lqg:
                        lqg_file = open(path + filename, 'rb')
                        lqg_cost = pickle.load(lqg_file)
                        
                        lqg_file.close()
                        if args.use_lambda:
                            for aux_lambda in lambda_list:
                                for aux_theta_v in theta_v_list:
                                    lqg_lambda_values.append(aux_lambda)
                                    lqg_theta_v_values.append(aux_theta_v)
                                    lqg_cost_values.append(lqg_cost[0])
                        else:
                            for aux_theta_w in theta_w_list:
                                for aux_theta_v in theta_v_list:
                                    lqg_theta_w_values.append(aux_theta_w)
                                    lqg_theta_v_values.append(aux_theta_v)
                                    lqg_cost_values.append(lqg_cost[0])
                
                    
    # We obtained the best-parameters for each method (within the examined region)
    # DRLQC
    print("Best parameters & Cost within the examined region")
    print("-------------------------")
    print("DRLQC")
    print("Best theta_w: {}, Best theta_v: {}, Best cost: {}".format(drlqc_optimal_theta_w, drlqc_optimal_theta_v, drlqc_optimal_cost))
    print("-------------------------")
    print("DRCE")
    print("Best theta_w: {}, Best theta_v: {}, Best cost: {}".format(drce_optimal_theta_w, drce_optimal_theta_v, drce_optimal_cost))
    print("-------------------------")
    print("WDRC")
    print("Best theta_w: {},  Best cost: {}".format(wdrc_optimal_theta_w, wdrc_optimal_cost))
    print("-------------------------")
    print("LQG")
    print("Cost: {}".format(lqg_cost[0]))               

    exit()
    # Convert lists to numpy arrays
    if args.use_lambda:
        drlqc_lambda_values = np.array(drlqc_lambda_values)
        drce_lambda_values = np.array(drce_lambda_values)
        wdrc_lambda_values = np.array(wdrc_lambda_values)
        lqg_lambda_values = np.array(lqg_lambda_values)
    else:
        drlqc_theta_w_values = np.array(drlqc_theta_w_values)
        drce_theta_w_values = np.array(drce_theta_w_values)
        wdrc_theta_w_values = np.array(wdrc_theta_w_values)
        lqg_theta_w_values = np.array(lqg_theta_w_values)
    
    drlqc_theta_v_values = np.array(drlqc_theta_v_values)
    drlqc_cost_values = np.array(drlqc_cost_values)
    
    drce_theta_v_values = np.array(drce_theta_v_values)
    drce_cost_values = np.array(drce_cost_values)

    wdrc_theta_v_values = np.array(wdrc_theta_v_values)
    wdrc_cost_values = np.array(wdrc_cost_values)
    
    lqg_theta_v_values = np.array(lqg_theta_v_values)
    lqg_cost_values = np.array(lqg_cost_values)
    
    summarize_theta_w(lqg_theta_w_values, lqg_theta_v_values, lqg_cost_values ,wdrc_theta_w_values, wdrc_theta_v_values, wdrc_cost_values , drce_theta_w_values, drce_theta_v_values, drce_cost_values, drlqc_theta_w_values, drlqc_theta_v_values, drlqc_cost_values, args.dist, args.noise_dist, args.infinite, args.use_lambda, path)

