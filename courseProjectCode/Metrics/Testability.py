import subprocess # Import subprocess to run shell commands from Python

def run_command(command): # function to execute shell command and returns its output as a string
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def count_test_cases(): # Fucntion to count total test cases by collecting pytest functions
    output = run_command("pytest --collect-only | grep '<Function' | wc -l")
    return int(output) if output else 0

def count_test_suites():# Fucntion to count total test suites by collecting pytest modules
    output = run_command("pytest --collect-only | grep '<Module' | wc -l")
    return int(output) if output else 0

def run_coverage(): # Runs pytest with coverage to measure code coverage and display the report
    print("\nRunning tests with coverage...")
    subprocess.run("coverage run --source=httpie -m pytest || true", shell=True)
    print("\nCoverage Report:")
    subprocess.run("coverage report", shell=True)

if __name__ == "__main__":
    print("Collecting Testability Metrics for HTTPie...\n")
    run_coverage()
    total_tests = count_test_cases()
    total_suites = count_test_suites()
    print(f"Total test cases: {total_tests}")
    print(f"Total test suites (modules): {total_suites}")