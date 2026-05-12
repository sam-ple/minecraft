import minescript as m

# -------------------------------
# gamerule
# -------------------------------

#m.execute("/gamerule sendCommandFeedback false")  # Disable command feedback

# -------------------------------
# effect
# -------------------------------

#m.execute("/effect give @s health_boost infinite 4 false")  # Give health boost effect

# -------------------------------
# bossbar
# -------------------------------

# 1. Create a Bossbar
#m.execute('/bossbar add <id> "<Display Name>"')

# 2. Change Bossbar name
#m.execute('/bossbar set <id> name "<New Name>"')

# 3. Set players who can see the Bossbar
#m.execute('/bossbar set <id> players @a')  # All players
#m.execute('/bossbar set <id> players @s')  # Only yourself

# 4. Change value
#m.execute('/bossbar set <id> value <value>')  # Set within the maximum

# 5. Change maximum value
#m.execute('/bossbar set <id> max <value>')  # Maximum 1,999,999,999

# 6. Change color (blue, green, pink, purple, red, white, yellow)
#m.execute('/bossbar set <id> color red')

# 7. Change style
#m.execute('/bossbar set <id> style progress')       # No divisions
#m.execute('/bossbar set <id> style notched_6')     # 6 divisions
#m.execute('/bossbar set <id> style notched_10')    # 10 divisions
#m.execute('/bossbar set <id> style notched_12')    # 12 divisions
#m.execute('/bossbar set <id> style notched_20')    # 20 divisions

# 8. Toggle visibility
#m.execute('/bossbar set <id> visible true')   # Show
#m.execute('/bossbar set <id> visible false')  # Hide

# 9. Remove Bossbar
#m.execute('/bossbar remove <id>')

# 10. List all Bossbars
#m.execute('/bossbar list')
