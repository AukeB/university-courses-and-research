# Stellar Structure & Evolution 2020: Practical Assignment.
# Auke Bruinsma (s1594443).

 ### Import packages ###

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.ticker import FuncFormatter
import math
import matplotlib.cm as cmx
import pandas as pd
import os
from decimal import Decimal
import regimes


 ### Global constants ###

n1 = 76 # Number of .data files which is the same as the number of time instances of the star.
n2 = 125 # For M_1
figsize=(13,6.5)

 ### Set up paths and directories ###

# General data directory.
#data_dir = '/data2/bruinsma/SSE/data'
data_dir = '/home/auke/Desktop/temp2/data'

# Two different paths for the two different simulations.
sim_1 = '/1m_sun/LOGS/'
sim_2 = '/2m_sun/LOGS/'
numpy_arrays = '/numpy_arrays/'

 ### Load all parameters so that you only have to go once through all time instances ###

star_age_1 = np.load(data_dir+numpy_arrays+'star_age_1.npy')
star_age_2 = np.load(data_dir+numpy_arrays+'star_age_2.npy')
num_zones_1 = np.load(data_dir+numpy_arrays+'num_zones_1.npy')
num_zones_2 = np.load(data_dir+numpy_arrays+'num_zones_2.npy')
Teff_1 = np.load(data_dir+numpy_arrays+'Teff_1.npy')
Teff_2 = np.load(data_dir+numpy_arrays+'Teff_2.npy')
photosphere_L_1 = np.load(data_dir+numpy_arrays+'photosphere_L_1.npy')
photosphere_L_2 = np.load(data_dir+numpy_arrays+'photosphere_L_2.npy')
logT_1 = np.load(data_dir+numpy_arrays+'logT_1.npy')
logT_2 = np.load(data_dir+numpy_arrays+'logT_2.npy')
logRho_1 = np.load(data_dir+numpy_arrays+'logRho_1.npy')
logRho_2 = np.load(data_dir+numpy_arrays+'logRho_2.npy')
logR_1 = np.load(data_dir+numpy_arrays+'logR_1.npy')
logR_2 = np.load(data_dir+numpy_arrays+'logR_2.npy')
grada_1 = np.load(data_dir+numpy_arrays+'grada_1.npy')
grada_2 = np.load(data_dir+numpy_arrays+'grada_2.npy')
gradr_1 = np.load(data_dir+numpy_arrays+'gradr_1.npy')
gradr_2 = np.load(data_dir+numpy_arrays+'gradr_2.npy')

#print(logR_1[35].iloc[354]) # Test.
#print(star_age_1)

 ### PLOT: Evolution of the core in the log T_c - log Rho_c plane ###

def make_plot_1():
	def inspect_arrays():
		for i in range(n1):
			print(f'{i} {logT_1[i]} {logRho_1[i]} {star_age_1[i]:.2e}')
		for i in range(n2):
			print(f'{i} {logT_2[i]} {logRho_2[i]} {star_age_2[i]:.2e}')

	#inspect_arrays()

	fig, ax = plt.subplots(1,1,figsize=figsize)

	ax.set_title(r'Evolution of the core in the $\log T_c$ - $\log \rho_c$ plane',fontsize=20)
	ax.set_xlabel(r'$\log T_c$ (K)',fontsize=16)
	ax.set_ylabel(r'$\log \rho_c$ (g cm$^{-3}$)',fontsize=16)

	jet = plt.get_cmap('jet') 
	cNorm_1  = colors.Normalize(vmin = 0, vmax = len(logT_1) - 1)
	cNorm_2 = colors.Normalize(vmin = 0, vmax = len(logT_2) - 1)
	scalarMap_1 = cmx.ScalarMappable(norm = cNorm_1, cmap = jet)
	scalarMap_2 = cmx.ScalarMappable(norm = cNorm_2, cmap = jet)

	for i in range(n1-1):
		colorVal_1 = scalarMap_1.to_rgba(i)

		x_1 = [logT_1[i], logT_1[i+1]]
		y_1 = [logRho_1[i], logRho_1[i+1]]

		if i == 1:
			ax.plot(x_1, y_1, color = colorVal_1,lw=0.7,ls='--',label=r'$1M_{Sun}$ $(Z = 0.02)$')
			ax.scatter(logT_1[i],logRho_1[i],color=colorVal_1,s=1.4)

		ax.plot(x_1, y_1, color = colorVal_1,lw=0.7,ls='--')
		ax.scatter(logT_1[i],logRho_1[i],color=colorVal_1,s=1.4)

	for i in range(n2-1):
		colorVal_2 = scalarMap_2.to_rgba(i)	

		x_2 = [logT_2[i], logT_2[i+1]]
		y_2 = [logRho_2[i], logRho_2[i+1]]

		if i == 1:
			ax.plot(x_2, y_2, color = colorVal_2,lw=0.7,label=r'$2M_{Sun}$ $(Z = 0.02)$')
			ax.scatter(logT_2[i],logRho_2[i],color=colorVal_2,s=1.4)

		ax.plot(x_2, y_2, color = colorVal_2,lw=0.7)
		ax.scatter(logT_2[i],logRho_2[i],color=colorVal_2,s=1.4)

		annotate_fs = 7

		# Pre-main sequence.
		if i == 0: plt.annotate(s='A',xy=(logT_2[i],logRho_2[i]),
			xytext=(logT_2[i],logRho_2[i]),fontsize=annotate_fs)
		# Landing on the ZAMS.
		if i == 4: plt.annotate(s='B',xy=(logT_2[i],logRho_2[i]),
			xytext=(logT_2[i],logRho_2[i]),fontsize=annotate_fs)
		# Overall contraction phase near the end of the MS.
		if i == 7: plt.annotate(s='C',xy=(logT_2[i],logRho_2[i]),
			xytext=(logT_2[i],logRho_2[i]),fontsize=annotate_fs)
		# Exhaustion of Hydrogen in the center and disappearance of the convective core.
		if i == 9: plt.annotate(s='D',xy=(logT_2[i],logRho_2[i]),
			xytext=(logT_2[i],logRho_2[i]),fontsize=annotate_fs)
		# Thick shell burning.
		if i == 10: plt.annotate(s='E',xy=(logT_2[i],logRho_2[i]),
			xytext=(logT_2[i],logRho_2[i]),fontsize=annotate_fs)
		# Red Giant.
		if i == 11: plt.annotate(s='F',xy=(logT_2[i],logRho_2[i]),
			xytext=(logT_2[i],logRho_2[i]),fontsize=annotate_fs)
		# Helium flash ???
		if i == 26: plt.annotate(s='G',xy=(logT_2[i],logRho_2[i]),
			xytext=(logT_2[i],logRho_2[i]),fontsize=annotate_fs)
		# Helium flash ???
		if i == 35: plt.annotate(s='H',xy=(logT_2[i],logRho_2[i]),
			xytext=(logT_2[i],logRho_2[i]),fontsize=annotate_fs)
		# Early AGB.
		if i == 39: plt.annotate(s='I',xy=(logT_2[i],logRho_2[i]),
			xytext=(logT_2[i],logRho_2[i]),fontsize=annotate_fs)
		# Thermal Pulsating AGB.
		if i == 45: plt.annotate(s='J',xy=(logT_2[i],logRho_2[i]),
			xytext=(logT_2[i],logRho_2[i]),fontsize=annotate_fs)
		# Post-AGB.
		if i == 106: plt.annotate(s='K',xy=(logT_2[i],logRho_2[i]),
			xytext=(logT_2[i],logRho_2[i]),fontsize=annotate_fs)
		# White dwarf
		if i == 122: plt.annotate(s='L',xy=(logT_2[i],logRho_2[i]),
			xytext=(logT_2[i],logRho_2[i]),fontsize=annotate_fs)

	sm = plt.cm.ScalarMappable(cmap = jet, norm = plt.Normalize(vmin=np.min(star_age_1), vmax=np.max(star_age_1)))
	sm._A = []
	cb = plt.colorbar(sm)
	cb.set_label('Age [yr]')

	#ax.plot(logT_1,logRho_1,label=r'$1M_{Sun}$',ls='--', lw=0.8, marker='o', ms=4, color='brown')
	#ax.plot(logT_2,logRho_2,label=r'$2M_{Sun}$',ls='--', lw=0.8, marker='o', ms=4, color='k')

	# Regimes.
	ax.plot(np.log10(regimes.T_rad_ig),regimes.log_rho,':',label='Radiation | Ideal gas',lw=0.7)
	ax.plot(np.log10(regimes.T_ig_NR[0:regimes.b3]),regimes.log_rho[0:regimes.b3],':',label='Ideal gas | NR degenerate',lw=0.7)
	ax.plot(regimes.log_rho[0:regimes.b1],np.log10(regimes.T_NR_ER[0:regimes.b1]),':',label='NR degenerate | ER degenerate',lw=0.7)
	ax.plot(np.log10(regimes.T_ig_ER[regimes.b2:-1]),regimes.log_rho[regimes.b2:-1],':',label='Ideal gas | ER degenerate',lw=0.7)

	ax.text(7.7,-2,s='Radiation',fontsize=12)
	ax.text(6,0,s='Ideal gas',fontsize=12)
	ax.text(5.7,4.3,s='Degenerate NR',fontsize=12)
	ax.text(6,6.4,s='Degenerate ER',fontsize=12)

	# Theoretical tracks.
	dif_1 = np.log10(regimes.rad_ig(10**logRho_1[0],regimes.mu)) - logT_1[0]
	dif_2 = np.log10(regimes.rad_ig(10**logRho_2[0],regimes.mu)) - logT_2[0]
	dif_3 = np.log10(regimes.T_NR_ER)-5.45467
	dif_4 = np.log10(regimes.T_NR_ER)-6.05019

	b1 = 773
	b2 = 802
	b3 = 920
	b4 = 939

	ax.plot(np.log10(regimes.T_rad_ig[0:b1])-dif_1,regimes.log_rho[0:b1],'--',
		label=r'Theoretical track $1M_{Sun}$',lw=0.7,c='gray')
	ax.plot(np.log10(regimes.T_rad_ig[0:b2])-dif_2,regimes.log_rho[0:b2],'-',
		label=r'Theoretical track $2M_{Sun}$',lw=0.7,c='gray')

	ax.plot(regimes.log_rho[0:b3],np.log10(
		regimes.T_NR_ER[0:b3])-dif_3[0:b3],'--',lw=0.7,c='gray')
	ax.plot(regimes.log_rho[0:b4],np.log10(
		regimes.T_NR_ER[0:b4])-dif_4[0:b4],'-',lw=0.7,c='gray')





	# Position solar core.
	ax.scatter(np.log10(15e6), np.log10(150), marker = '*', color = 'orange',label='Solar core current position')
	ax.legend(loc='lower left', bbox_to_anchor=(0.55, 0))
	ax.set_xlim(5.2,8.9)
	ax.set_ylim(-4.5,7)

	
	#ax.grid()

	plt.savefig('figs/plot1.png')
	#plt.show()
	plt.close()

 ### PLOT: Hertzsprung-Russel diagram ###

def make_plot_2():
	def inspect_arrays():
		for i in range(n1):
			print(i,Teff_1[i],photosphere_L_1[i])
		for i in range(n2):
			print(i,Teff_2[i],photosphere_L_2[i])

	#inspect_arrays()

	fig, ax = plt.subplots(1,1,figsize=figsize)

	ax.set_title(r'Hertzsprung-Russel Diagram',fontsize=20)
	ax.set_xlabel(r'$\log T_{eff}$ (K)',fontsize=16)
	ax.set_ylabel(r'$\log (L/L_{Sun})$',fontsize=16)

	ax.set_xscale('log')
	ax.set_yscale('log')
	plt.gca().invert_xaxis()
	plt.gca().yaxis.set_major_formatter(FuncFormatter(
		lambda x,y: '{}'.format(np.round(math.log(x, 10),decimals=0))))
	plt.gca().xaxis.set_major_formatter(FuncFormatter(
		lambda x,y: '{}'.format(np.round(math.log(x, 10),decimals=0))))


	jet = plt.get_cmap('jet') 
	cNorm_1  = colors.Normalize(vmin = 0, vmax = len(Teff_1) - 1)
	cNorm_2 = colors.Normalize(vmin = 0, vmax = len(Teff_2) - 1)
	scalarMap_1 = cmx.ScalarMappable(norm = cNorm_1, cmap = jet)
	scalarMap_2 = cmx.ScalarMappable(norm = cNorm_2, cmap = jet)

	for i in range(n1-1):
		colorVal_1 = scalarMap_1.to_rgba(i)

		x_1 = [Teff_1[i], Teff_1[i+1]]
		y_1 = [photosphere_L_1[i], photosphere_L_1[i+1]]

		if i == 0:
			ax.plot(x_1, y_1, color = colorVal_1,lw=0.7,ls='--',label=r'$1M_{Sun}$ $(Z = 0.02)$')
			ax.scatter(Teff_1[i],photosphere_L_1[i],color=colorVal_1,s=1.4)

		ax.plot(x_1, y_1, color = colorVal_1,lw=0.7,ls='--')
		ax.scatter(Teff_1[i],photosphere_L_1[i],color=colorVal_1,s=1.4)

	for i in range(n2-1):
		colorVal_2 = scalarMap_2.to_rgba(i)	

		x_2 = [Teff_2[i], Teff_2[i+1]]
		y_2 = [photosphere_L_2[i], photosphere_L_2[i+1]]

		if i == 0: 
			ax.plot(x_2, y_2, color = colorVal_2,lw=0.7,label=r'$2M_{Sun}$ $(Z = 0.02)$')
			ax.scatter(Teff_2[i],photosphere_L_2[i],color=colorVal_2,s=1.4)

		annotate_fs = 7

		# Pre-main sequence.
		if i == 0: plt.annotate(s='A',xy=(Teff_2[i],photosphere_L_2[i]),
			xytext=(Teff_2[i],photosphere_L_2[i]),fontsize=annotate_fs)
		# Landing on the ZAMS.
		if i == 4: plt.annotate(s='B',xy=(Teff_2[i],photosphere_L_2[i]),
			xytext=(Teff_2[i],photosphere_L_2[i]),fontsize=annotate_fs)
		# Overall contraction phase near the end of the MS.
		if i == 7: plt.annotate(s='C',xy=(Teff_2[i],photosphere_L_2[i]),
			xytext=(Teff_2[i],photosphere_L_2[i]),fontsize=annotate_fs)
		# Exhaustion of Hydrogen in the center and disappearance of the convective core.
		if i == 9: plt.annotate(s='D',xy=(Teff_2[i],photosphere_L_2[i]),
			xytext=(Teff_2[i],photosphere_L_2[i]),fontsize=annotate_fs)
		# Thick shell burning.
		if i == 10: plt.annotate(s='E',xy=(Teff_2[i],photosphere_L_2[i]),
			xytext=(Teff_2[i],photosphere_L_2[i]),fontsize=annotate_fs)
		# Red Giant.
		if i == 11: plt.annotate(s='F',xy=(Teff_2[i],photosphere_L_2[i]),
			xytext=(Teff_2[i],photosphere_L_2[i]),fontsize=annotate_fs)
		# Helium flash ???
		if i == 26: plt.annotate(s='G',xy=(Teff_2[i],photosphere_L_2[i]),
			xytext=(Teff_2[i],photosphere_L_2[i]),fontsize=annotate_fs)
		#
		if i == 35: plt.annotate(s='H',xy=(Teff_2[i],photosphere_L_2[i]),
			xytext=(Teff_2[i],photosphere_L_2[i]),fontsize=annotate_fs)
		# Early AGB.
		if i == 39: plt.annotate(s='I',xy=(Teff_2[i],photosphere_L_2[i]),
			xytext=(Teff_2[i],photosphere_L_2[i]),fontsize=annotate_fs)
		# Thermal Pulsating AGB.
		if i == 45: plt.annotate(s='J',xy=(Teff_2[i],photosphere_L_2[i]),
			xytext=(Teff_2[i],photosphere_L_2[i]),fontsize=annotate_fs)
		# Post-AGB.
		if i == 106: plt.annotate(s='K',xy=(Teff_2[i],photosphere_L_2[i]),
			xytext=(Teff_2[i],photosphere_L_2[i]),fontsize=annotate_fs)
		# White dwarf
		if i == 122: plt.annotate(s='L',xy=(Teff_2[i],photosphere_L_2[i]),
			xytext=(Teff_2[i],photosphere_L_2[i]),fontsize=annotate_fs)

		ax.plot(x_2, y_2, color = colorVal_2,lw=0.7)
		ax.scatter(Teff_2[i],photosphere_L_2[i],color=colorVal_2,s=1.4)


	sm = plt.cm.ScalarMappable(cmap = jet, norm = plt.Normalize(vmin=np.min(star_age_1), vmax=np.max(star_age_1)))
	sm._A = []
	cb = plt.colorbar(sm)
	cb.set_label('Age [yr]')

	#ax.plot(logT_1,logRho_1,label=r'$1M_{Sun}$',ls='--', lw=0.8, marker='o', ms=4, color='brown')
	#ax.plot(logT_2,logRho_2,label=r'$2M_{Sun}$',ls='--', lw=0.8, marker='o', ms=4, color='k')

	ax.legend()
	#ax.grid()
	
	plt.savefig('figs/plot2.png')
	plt.show()
	plt.close()

 ### Convection ###

def make_plot_3_and_4():
	for i in range(n2):
		if i == 7:
			#print(i)

			fig, (ax1, ax2) = plt.subplots(1,2,figsize=(10,5))
			
			if i == 3: 
				fig.suptitle('Convection in the pre-main sequence phase.',fontsize = 18)
				ax1.text(x=-1,y=1e4,s='Convection')
				ax2.text(x=-0.7,y=0.6*1e4,s='Convection')
			if i == 7: 
				fig.suptitle('Convection in the main sequence phase.',fontsize = 18)
				ax1.axvline(x=-0.132382)
				ax2.axvline(x=-0.755303)
				ax1.text(x=-2.5,y=1*10**1,s='Radiation')
				ax2.text(x=-2.3,y=0.7,s='Convection')

			ax1.set_title(r'$1M_{Sun}$',fontsize=18)
			ax1.set_xlabel(r'$\log (R/R_{Sun})$',fontsize=16)
			ax1.set_ylabel(r'$\log \nabla$',fontsize=16)

			ax2.set_title(r'$2M_{Sun}$',fontsize=18)
			ax2.set_xlabel(r'$\log (R/R_{Sun})$',fontsize=16)
			ax2.set_ylabel(r'$\log \nabla$',fontsize=16)

			fig.tight_layout(pad=1.0)

			ax2.set_yscale('log')
			ax1.set_yscale('log')

			ax1.plot(logR_1[i],grada_1[i],color='brown',lw=1,ls='--',label=r'$\nabla_{ad}$')
			ax1.plot(logR_1[i],gradr_1[i],color='k',lw=1,ls='--',label=r'$\nabla_{rad}$')
			
			ax2.plot(logR_2[i],grada_2[i],c='brown',lw=1,ls='-',label=r'$\nabla_{ad}$')
			ax2.plot(logR_2[i],gradr_2[i],c='k',lw=1,ls='-',label=r'$\nabla_{rad}$')

			ax1.legend()
			ax2.legend()

			fig.tight_layout()
			fig.subplots_adjust(top=0.85)

			plt.savefig(f'figs/convection_plots/plot_convection_profile_{i}.png')
			plt.show()
			plt.close()

def main():
	#make_plot_1()
	make_plot_2()
	#make_plot_3_and_4()

main()