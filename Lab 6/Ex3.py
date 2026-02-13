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

def determine_progress2(hits, spins):
    if spins == 0:
        return "Get going!"
    hits_spins_ratio = hits / spins
    progress = "Get going!"
    if hits_spins_ratio > 0:
        progress = "On your way!"
    if hits_spins_ratio >= 0.25:
        progress = "Almost there!"
    if hits_spins_ratio >= 0.5 and hits < spins:
        progress = "You win!"
    return progress

def determine_progress3(hits, spins):
    if spins == 0:
        return "Get going!"
    hits_spins_ratio = hits / spins
    if hits_spins_ratio == 0:
        return "Get going!"
    elif hits_spins_ratio >= 0.5 and hits < spins:
        return "You win!"
    elif hits_spins_ratio >= 0.25:
        return "Almost there!"
    else:
        return "On your way!"

def test_determine_progress1(progress_function):

    # Test case 1: spins = 0 returns “Get going!”
    assert progress_function(10,0) == "Get going!", "Test case 1 failed"
    # Test case 2: hits/spins = 0 returns “Get going!”
    assert progress_function(0,10) == "Get going!", "Test case 2 failed"
    # Test case 3: hits/spins = 0.1 (0 < returns < 0.25) returns “On your way!”
    assert progress_function(1,10) == "On your way!", "Test case 3 failed"
    # Test case 4: hits/spins = 0.25 (ratio >= 0.25) returns “Almost there!”
    assert progress_function(1,4) == "Almost there!", "Test case 4 failed"
    # Test case 5: hits/spins >= 0.5 with hits < spins returns “You win!”
    assert progress_function(6,10) == "You win!", "Test case 5 failed"
    # Test case 6: hits/spins = 0.5 with hits >= spins returns “Almost there!”
    assert progress_function(11,10) == "Almost there!", "Test case 6 failed"

    print("All tests passed!")

def test_determine_progress2(progress_function):

    # Test case 1: spins = 0 returns “Get going!”
    assert progress_function(10,0) == "Get going!", "Test case 1 failed"
    # Test case 2: hits/spins = 0 returns “Get going!”
    assert progress_function(0,10) == "Get going!", "Test case 2 failed"
    # Test case 3: hits/spins = 0.1 (0 < returns < 0.25) returns “On your way!”
    assert progress_function(1,10) == "On your way!", "Test case 3 failed"
    # Test case 4: hits/spins = 0.25 (ratio >= 0.25) returns “Almost there!”
    assert progress_function(1,4) == "Almost there!", "Test case 4 failed"
    # Test case 5: hits/spins >= 0.5 with hits < spins returns “You win!”
    assert progress_function(6,10) == "You win!", "Test case 5 failed"
    # Test case 6: hits/spins = 0.5 with hits >= spins returns “Almost there!”
    assert progress_function(11,10) == "Almost there!", "Test case 6 failed"

    print("All tests passed!")

def test_determine_progress3(progress_function):
    # Test case 1: spins = 0 returns “Get going!”
    assert progress_function(10,0) == "Get going!", "Test case 1 failed"
    # Test case 2: hits/spins = 0 returns “Get going!”
    assert progress_function(0,10) == "Get going!", "Test case 2 failed"
    # Test case 3: hits/spins = 0.1 (0 < returns < 0.25) returns “On your way!”
    assert progress_function(1,10) == "On your way!", "Test case 3 failed"
    # Test case 4: hits/spins = 0.25 (ratio >= 0.25) returns “Almost there!”
    assert progress_function(1,4) == "Almost there!", "Test case 4 failed"
    # Test case 5: hits/spins >= 0.5 with hits < spins returns “You win!”
    assert progress_function(6,10) == "You win!", "Test case 5 failed"
    # Test case 6: hits/spins = 0.5 with hits >= spins returns “Almost there!”
    assert progress_function(11,10) == "Almost there!", "Test case 6 failed"

    print("All tests passed!")

# Run the test
test_determine_progress1(determine_progress1)

# Run the test for determine_progress2
test_determine_progress2(determine_progress2)

# Run the test for determine_progress3
test_determine_progress3(determine_progress3)