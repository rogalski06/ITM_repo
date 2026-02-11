def determine_progress1(hits, spins):
    if spins == 0:
        return "Get going!"
    
    hits_spins_ratio = hits / spins

    if hits_spins_ratio > 0:
        progress = "On your way!"
        if hits_spins_ratio >= 0.25:
            progress = "Almost there!"
            if hits_spins_ratio >= 0.5:
                if hits < spins:
                    progress = "You win!"
    else:
        progress = "Get going!"

    return progress