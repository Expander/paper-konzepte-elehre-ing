import daten
import font
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np
import pandas as pd
import rounding
import style
import sys

if len(sys.argv) != 2:
    raise "Error: 1 argument expected"

filename_prefix = sys.argv[1]

print(f'filename_prefix = {filename_prefix}')

bar_colors    = {'ges': style.my_blue  , 'int': 'w'            , 'kon': 'w'             }
bar_fill      = {'ges': True           , 'int': True           , 'kon': True            }
bar_hatch     = {'ges': None           , 'int': style.my_hatch1, 'kon': style.my_hatch2 }
bar_edgecolor = {'ges': style.my_blue  , 'int': style.my_red   , 'kon': style.my_green  }
bar_textcolor = {'ges': 'w'            , 'int': 'k'            , 'kon': 'k'             }
bar_errcolor  = {'ges': style.my_orange, 'int': 'k'            , 'kon': 'k'             }

# daten einlesen
data = pd.read_csv(filename_prefix + '.csv', delimiter=';')

for g in daten.gruppen:
    # Standard-Error
    data['se'  + g] = data['sd' + g]/np.sqrt(data['N' + g])
    # relativer Punkteanteil 
    data['r'   + g] = data['m'  + g]/data['PunkteMax']
    # relativer Standard-Error
    data['rse' + g] = data['se' + g]/data['PunkteMax']

data.set_index('Konzept', inplace=True)
print(data)

label_locations = np.arange(len(daten.konzepte))
width = style.width
multiplier = 0

fig, ax = plt.subplots(figsize=style.my_figsize)
ax.grid(axis='y', linestyle='-', linewidth=1)
ax.set_axisbelow(True)

# Balken
for g in daten.gruppen:
    dat = data['r' + g]*100
    err = data['rse' + g]*100
    # print(dat)
    offset = width * multiplier
    x = label_locations + offset
    rects = ax.bar(x, dat, width,
                   label=data[g].loc['ogSK'],
                   color=bar_colors[g],
                   fill=bar_fill[g],
                   hatch=bar_hatch[g],
                   edgecolor=bar_edgecolor[g])
    ax.bar_label(rects,
                 labels=[f'{r:2.0f}%' for r in [rounding.round_half_up(d) for d in dat]],
                 label_type='center',
                 color='black',
                 backgroundcolor='white',
                 fontsize='small')
    ax.errorbar(x, dat, yerr=err, fmt=' ',
                color=bar_errcolor[g],
                linewidth=2,
                capthick=2,
                capsize=3)
    multiplier += 1

# geschweifte Klammern
for xybalken in zip(label_locations + 1.5*width, (data['rint'] + data['rseint'])*100 + 5, data['sig']):
    ax.annotate(xybalken[2], xy=(xybalken[0], xybalken[1]), xytext=(xybalken[0], xybalken[1]+5),
                ha='center', va='bottom',
                arrowprops=dict(arrowstyle='-[, widthB=2.5, lengthB=0.75', lw=2))

ax.set_ylabel('erreichte Punktzahl in Prozent')
# ax.set_title('Studierende ' + data['studiengang'].loc['ogSK'] + ' (Pretest)')
ax.set_xticks(label_locations + width, daten.konzepte_label)
ax.yaxis.set_major_formatter('{x:.0f}%')
ax.yaxis.set_major_locator(plticker.MultipleLocator(base=10))
legend = ax.legend(loc='upper right', ncol=1, edgecolor='k')
legend.get_frame().set_alpha(None)
ax.annotate(r'$\mathdefault{\alpha=0{,}01}$', xy=(4.9,73), ha='right', va='center')
ax.set_ylim(0, 100)

fig.tight_layout()
fig.savefig(filename_prefix + '.pdf')
fig.savefig(filename_prefix + '.png', dpi=style.dpi_resolution)
