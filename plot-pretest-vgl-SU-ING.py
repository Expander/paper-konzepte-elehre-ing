import daten
import font
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np
import pandas as pd
import rounding
import style

filename_prefix_SU = 'pretest-sachunterricht'
filename_prefix_ING = 'pretest-ingenieure-all'

bar_colors    = {'SU': 'w'            , 'ING': 'w'             }
bar_fill      = {'SU': True           , 'ING': True            }
bar_hatch     = {'SU': style.my_hatch3, 'ING': style.my_hatch4 }
bar_edgecolor = {'SU': style.my_brown , 'ING': style.my_purple }
bar_textcolor = {'SU': 'w'            , 'ING': 'k'             }
bar_errcolor  = {'SU': 'k'            , 'ING': 'k'             }

# daten einlesen
data_SU  = pd.read_csv(filename_prefix_SU  + '.csv', delimiter=';')
data_ING = pd.read_csv(filename_prefix_ING + '.csv', delimiter=';')
data_all = { 'SU': data_SU, 'ING': data_ING }

for d in data_all:
    g = 'ges'
    data = data_all[d]
    data.set_index('Konzept', inplace=True)
    # Standard-Error
    data['se'  + g] = data['sd' + g]/np.sqrt(data['N' + g])
    # relativer Punkteanteil 
    data['r'   + g] = data['m'  + g]/data['PunkteMax']
    # relativer Standard-Error
    data['rse' + g] = data['se' + g]/data['PunkteMax']

label_locations = np.arange(len(daten.konzepte))
width = style.width
multiplier = 0

fig, ax = plt.subplots(figsize=style.my_figsize)
ax.grid(axis='y', linestyle='-', linewidth=1)
ax.set_axisbelow(True)

# Balken
for d in data_all:
    g = 'ges'
    data = data_all[d]
    dat = data['r' + g]*100
    err = data['rse' + g]*100
    offset = width * multiplier
    x = label_locations + offset
    rects = ax.bar(x, dat, width,
                   label=d,
                   color=bar_colors[d],
                   fill=bar_fill[d],
                   hatch=bar_hatch[d],
                   edgecolor=bar_edgecolor[d])
    ax.bar_label(rects,
                 labels=[f'{r:2.0f}%' for r in [rounding.round_half_up(d) for d in dat]],
                 label_type='center',
                 color='black',
                 backgroundcolor='white',
                 fontsize='small')
    ax.errorbar(x, dat, yerr=err, fmt=' ',
                color=bar_errcolor[d],
                linewidth=2,
                capthick=2,
                capsize=3)
    multiplier += 1

significance = ['sig.', 'sig.', 'n.s.', 'sig.', 'sig.']

# geschweifte Klammern
for xybalken in zip(label_locations + 0.5*width, data_all['ING']['rges']*100 + 7, significance):
    ax.annotate(xybalken[2], xy=(xybalken[0], xybalken[1]), xytext=(xybalken[0], xybalken[1]+5),
                ha='center', va='bottom',
                arrowprops=dict(arrowstyle='-[, widthB=2.5, lengthB=0.75', lw=2))

ax.set_ylabel('erreichte Punktzahl in Prozent')
ax.set_xticks(label_locations + width/2, daten.konzepte_label)
ax.yaxis.set_major_formatter('{x:.0f}%')
ax.yaxis.set_major_locator(plticker.MultipleLocator(base=10))
legend = ax.legend(loc='upper right', ncol=1, edgecolor='k')
legend.get_frame().set_alpha(None)
ax.annotate(r'$\mathdefault{\alpha=0{,}01}$', xy=(4.6,80), ha='right', va='center')
ax.set_ylim(0, 100)

filename_prefix = 'pretest-vgl-SU-ING'
fig.tight_layout()
fig.savefig(filename_prefix + '.pdf')
fig.savefig(filename_prefix + '.png', dpi=300)
