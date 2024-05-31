import matplotlib.pyplot as plt

## Installation of Atkinson Hyperlegible
# rm -rf ~/.cache/matplotlib/
# from matplotlib import font_manager
# font_manager.findSystemFonts(fontpaths=None, fontext="ttf")
# font_manager.findfont("Atkinson Hyperlegible")

## Installation of Times New Roman
# rm -rf ~/.cache/matplotlib/
# sudo apt install msttcorefonts -qq

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ["Times New Roman"] + plt.rcParams["font.serif"]

## for Atkinson Hyperlegible use:
# plt.rcParams['font.family'] = 'sans-serif'
# plt.rcParams['font.sans-serif'] = 'Atkinson Hyperlegible'
