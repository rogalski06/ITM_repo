def determine_progress1(spins, spins_to_complete):
    """
    Determine the progress based on the number of spins and spins to complete.
    """
    if spins == 0:
        return "Get going!"
    elif spins == spins_to_complete:
        return "Completed!"
    elif spins > spins_to_complete:
        return "Almost there!"
    else:
        return "Keep spinning!"

def test_determine_progress1(progress_function):
    """
    Test cases are chosen to cover all possible return values of the function.
    Each case targets a specific branch or output, including edge cases.
    For example:
    - spins = 0: Should return "Get going!" (minimum spins, motivational message)
    - spins = 10: Should return "Keep spinning!" (normal progress)
    - spins = 100: Should return "Almost there!" (near completion)
    - spins = 120: Should return "Completed!" (completion case)
    Adjust these cases based on the actual logic of determine_progress1.
    """

    # Test case 1: spins = 0 returns “Get going!”
    assert progress_function(10, 0) == "Get going!", "Test case 1 failed"

    # Test case 2: spins = 10 returns “Keep spinning!”
    assert progress_function(10, 10) == "Keep spinning!", "Test case 2 failed"

    # Test case 3: spins = 100 returns “Almost there!”
    assert progress_function(10, 100) == "Almost there!", "Test case 3 failed"

    # Test case 4: spins = 120 returns “Completed!”
    assert progress_function(10, 120) == "Completed!", "Test case 4 failed"

    print("All tests passed.")

# How test cases were chosen:
# Each test case targets a unique output of the function, ensuring all possible return values are checked.
# Edge cases (minimum, maximum, and typical values) are included for completeness.

