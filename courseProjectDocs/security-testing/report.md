# Test Scope and Coverage

We examined vulnerabilities inside of the `/httpie` directory. This does not include documentation, test cases, or some execution scripts found in other files. The `/httpie` folder holds the core logic of the application and is where all of the source code resides. All types of vulnerabilites were targeted.

# Vulnerability Summary

| Title                                            | Type                                    | Severity | Recommended Fix                                                                                                                                                                                                                                                                                                                                                          |
| ------------------------------------------------ | --------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [B101:assert_used] (CWE-703)                     | Improper check or handling of exception | Low      | Replace the `assert` keyword with a simple `if` statement. In certain configurations when running the source code, the `assert` flag can be turned off, which can cause certain parts of the code to always pass or always fail, which in turn can cause unintended consequences                                                                                         |
| [B113:request_without_timeout] (CWE-400)         | Uncontrolled Resource Consumption       | Medium   | Add in a simple timeout, where the request fails if the response takes too long. By not doing this, the system expends resources by sitting and doing nothing, in this case, it could be for an infinite amount of time. So, by adding in a simple timeout, the code can continue if it takes too long, this could in theory be set by the user when they make a request |
| [B501:request_with_no_cert_validation] (CWE-295) | Improper Certificate Validatio          | High     | Remove verify = false to rely on the default certification validation, or, use a direct path to the users certificate. By not having this, the system allows for anyone to make requests which might not be ideal.                                                                                                                                                       |

# Execution and Results

To analyze the program we used a tool called `Bandit`. This is a CLI vulnerability scanning tool which is able to statically analyze python source code to find potential issues. After the `Bandit` tool is run, a report is printed to the console detailing which vulnerabilites were found (low / medium / high) and how confident the tools is in that analysis (low / medium / high). What this told us is which vulnerabilites the tool was certain are in the code and how bad they were, from there we could continue to filter and address the highest priority ones.

To run `Bandit`, first type `pip install bandit` into the project root. Once installed run the command `bandit -r .\httpie\` from the project root. The tool will run and the report will generate.

There were no failed scans or unexpected behavior, the tool took around 1-2 seconds to run.

Of note, we expected there to be minimal security issues in the program, in total there were 32, with only 4 different CWE numbers. This is because `httpie` is simple an HTTP interface, it does the routing and requests and makes the process easier for users to work with HTTP. It and of itself doesn't perform much logic it just routes the requests, gets the responses, and returns them to the user, it assumes that the endpoint they want to interact with is performing the security checks.

# Group Contributions

| Member   | Task                                                                                                         | Notes |
| -------- | ------------------------------------------------------------------------------------------------------------ | ----- |
| Vinayaka | Ran the bandit tool, found the MEDIUM vulnerability, added findings to the report                            | None  |
| Chris    | Found and determined how to setup the bandit tool, found the LOW vulnerability, added findings to the report | None  |
| Dan      | Ran the bandit tool, found the HIGH vulnerability, added findings to the report                              | None  |
