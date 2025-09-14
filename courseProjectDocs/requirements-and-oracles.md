# Requirements and Test Oracles

## Functional Requirements
1. The system shall allow the user to send requests with common HTTP methods (POST, PUT, GET, DELETE).
2. The system shall allow the user to upload/download files.
3. The system shall allow the user to send request in different data formats (JSON, URL Parameters, HTTP Headers).
4. The system shall allow the user to configure their terminal and profile with their preferences.
5. The system shall allow the user to see all responses from the request in printed output to the console.
6. The system shall allow the user to authenticate via username and password before accessing the resource.
7. The system shall allow the user to set and send custom request names.


## Non-Functional Requirements
1. The system shall work consistently across Linux, MacOS, windows and FreeBSD systems.
2. The system shall be accessible on web and mobile devices and desktop CLI.
3. The system shall allow a maximum of n redirects, where n is defined by the user.
4. The system shall timeout stale requests after n milliseconds, where n is defined by the user.
5. The system shall accept no more than one request at a time.

## Test Oracles

| Requirement ID | Requirement Description | Test Oracle (Expected Behavior) |
|-----------------------|-----------------------------------|---------------------------------------------|
| FR-1                   | The system shall allow the user to send requests with common HTTP methods (POST, PUT, GET, DELETE).|When the user sends an HTTP DELETE request, the resource under control should no longer contain those elements.|
| FR-1                   | The system shall allow the user to send requests with common HTTP methods (POST, PUT, GET, DELETE).|When a user sends an HTTP GET request containing Foo:bar, the response must include “Foo”: “bar”.|
| FR-1                   | The system shall allow the user to send requests with common HTTP methods (POST, PUT, GET, DELETE).|When a user sends an HTTP GET request containing Accept: or User-Agent:, those headers shall be absent from the request.|
| FR-1                   | The system shall allow the user to send requests with common HTTP methods (POST, PUT, GET, DELETE).|When the user sends an HTTP POST request with a specified file, then it will be added to the resource under control.|
| NFR-3                  | The system shall allow a maximum of n redirects, where n is defined by the user.|When the redirect count exceeds the limit, the CLI must return ExitStatus.ERROR_TOO_MANY_REDIRECTS.|
| NFR-4                  |The system shall timeout stale requests after n milliseconds, where n is defined by the user.|When the time to process a request exceeds the timeout limit, the CLI must return ExitStatus.ERROR_TIMEOUT.|
| FR-5                   |The system shall allow the user to see all responses from the request in printed output to the console.|When a response is received from any request, the response will be printed to the terminal.|
| FR-7                   |The system shall allow the user to set and send custom request names.|When the user creates a custom HTTP request name, then that name is added to the list of available requests that can successfully be sent.|
