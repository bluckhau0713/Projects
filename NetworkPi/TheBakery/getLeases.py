import matplotlib.pyplot as plt


colors = {'totalClients': 'palegreen',
          'QUCONSOLES': '#d1f7ff', 'QUGuest': 'slateblue', 'QUINCY': 'cornflowerblue',
          'border': '#ff2a6d',
          'font': '#05d9e8', 'background': '#01012b',
          'deniedPackets': 'lightcoral', 'allowedPackets': 'lightgreen', 'reset-both': 'tan',
          'water': '#00bce1', 'land': 'darkgreen', 'source': 'yellow', 'destination': 'pink', 'both': 'magenta',
          'gauge': 'lightcoral',
          'buildings': 'palegreen'}

with open("C:/PythonScripts/NetworkPi/leases.txt", 'r', encoding='utf-16') as file:
    leases = file.read().strip()

# Create a figure and axis
fig, ax = plt.subplots(figsize=(1, 1), dpi=400)
fig.patch.set_alpha(0)
# Add text to the axis
ax.text(0.5, 0.5, f'Current active DHCP leases: {leases}', color=colors['font'], fontsize=12, ha='center', va='center')

# Customize text properties
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')  # Hide axis

# Save the figure as an image
plt.savefig('//transporter/PiReporting/toPi/dhcpLeases/leases.png', bbox_inches='tight', pad_inches=0, transparent=True)

