import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np

filename_prefix = 'ingenieure'

# rm -rf ~/.cache/matplotlib/
# from matplotlib import font_manager
# font_manager.findSystemFonts(fontpaths=None, fontext="ttf")
# font_manager.findfont("Atkinson Hyperlegible")

atkinson = 'Atkinson Hyperlegible'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = atkinson

my_blue   = '#00e'
my_red    = '#c00'
my_green  = '#090'
my_orange = '#e80'

gruppen = ['ges', 'int', 'kon']

gruppen_label    = {'ges': 'gesamt' , 'int': 'EnWi,ST', 'kon': 'MB,BLVT' }
bar_colors       = {'ges': my_blue  , 'int': 'w'      , 'kon': 'w'       }
bar_fill         = {'ges': True     , 'int': True     , 'kon': True      }
bar_hatch        = {'ges': None     , 'int': '////'   , 'kon': '\\\\\\\\'}
bar_edgecolor    = {'ges': my_blue  , 'int': my_red   , 'kon': my_green  }
bar_textcolor    = {'ges': 'w'      , 'int': 'k'      , 'kon': 'k'       }
bar_errcolor     = {'ges': my_orange, 'int': 'k'      , 'kon': 'k'       }

# daten einlesen
data = pd.read_csv(filename_prefix + '.csv', delimiter=';')

for g in gruppen:
    # Standard-Error
    data['se'  + g] = data['sd' + g]/np.sqrt(data['N' + g])
    # relativer Punkteanteil 
    data['r'   + g] = data['m'  + g]/data['PunkteMax']
    # relativer Standard-Error
    data['rse' + g] = data['se' + g]/data['PunkteMax']

konzepte = data['Konzept']
konzepte_label = ['offene und geschl.\nStromkreise', 'Reihen- u.\nParallelschaltungen', 'elektr.\nStromstärke', 'elektr.\nWiderstand', 'elektr.\nSpannung']

data.set_index('Konzept', inplace=True)
print(data)

label_locations = np.arange(len(konzepte))
width = 0.28
multiplier = 0

cm = 1/2.54
fig, ax = plt.subplots(layout='constrained', figsize=(20*cm, 10*cm))
ax.grid(axis='y', linestyle='-', linewidth=0.1)
ax.set_axisbelow(True)

# Balken
for g in gruppen:
    dat = data['r' + g]*100
    err = data['rse' + g]*100
    # print(dat)
    offset = width * multiplier
    x = label_locations + offset
    rects = ax.bar(x, dat, width,
                   label=gruppen_label[g],
                   color=bar_colors[g],
                   fill=bar_fill[g],
                   hatch=bar_hatch[g],
                   edgecolor=bar_edgecolor[g])
    ax.bar_label(rects,
                 labels=[f'{d:2.0f}%' for d in dat],
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
for xybalken in zip(label_locations + 1.5*width, data['rint']*100 + 7, data['sig']):
    ax.annotate(xybalken[2], xy=(xybalken[0], xybalken[1]), xytext=(xybalken[0], xybalken[1]+5),
                ha='center', va='bottom',
                arrowprops=dict(arrowstyle='-[, widthB=2.5, lengthB=0.75', lw=2))

ax.set_ylabel('Erreichte Punktzahl in Prozent')
ax.set_title('Studierende Ingenieurwissenschaften (Pretest)')
ax.set_xticks(label_locations + width, konzepte_label)
ax.yaxis.set_major_formatter('{x:.0f}%')
ax.yaxis.set_major_locator(plticker.MultipleLocator(base=10))
legend = ax.legend(loc='upper right', ncols=1, edgecolor='k')
legend.get_frame().set_alpha(None)
ax.set_ylim(0, 100)

fig.tight_layout()
fig.savefig(filename_prefix + '.pdf')
fig.savefig(filename_prefix + '.png', dpi=300)
