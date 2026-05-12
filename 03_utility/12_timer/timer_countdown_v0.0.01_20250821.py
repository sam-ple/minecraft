import minescript as m
import sys
import time

# --- Parse argument ---
# Example: "timer 120" → sys.argv[1] = "120"
if len(sys.argv) > 1:
    try:
        num = int(sys.argv[1])
    except ValueError:
        m.echo("❌ Please enter a valid number (example: timer 120)")
        sys.exit()
else:
    num = 300  # Default = 300 seconds (5 minutes)

m.echo(f"Countdown start ({num} seconds)")

# --- Create the bossbar ---
m.execute('bossbar add timer "Countdown"')
m.execute('bossbar set timer color blue')
m.execute(f'bossbar set timer max {num}')
m.execute(f'bossbar set timer value {num}')
m.execute('bossbar set timer players @a')

# --- Countdown loop ---
for t in range(num, 0, -1):
    minutes = t // 60
    seconds = t % 60
    time_text = f"{minutes:02d}:{seconds:02d}"

    m.execute(f'bossbar set timer name "{time_text}"')
    m.execute(f'bossbar set timer value {t}')
    time.sleep(1)

# --- Remove bossbar when finished ---
m.execute('bossbar remove timer')
m.echo("Countdown stop")
m.execute('title @a title "Time Up!"')
#m.execute('title @a subtitle "⏰"')
