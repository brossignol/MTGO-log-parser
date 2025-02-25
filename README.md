This project extracts standings of challenges of MTGO based on logs parsing.

Usage:
* Log into MTGO Client (to update the logs).
* Run `python main.py` -> Standings of events starting within the same day are extracted.
* You can re-run main.py to update the standings after any round finish.

Notes:
* Filter on the formats you are interested in by using the `filters` list inside main.py. Example `filters = ['Legacy']`
* The client doesn't need to run for the parser to work, the logs are frozen at the time of the last MTGO logout.
* The logs are cleaned each time the client starts up, but challenges data of the day are re-downloaded by the Client.