This project extracts standings of challenges of MTGO based on logs parsing.

Usage:
* Log into MTGO Client (to update the log)
* Run main.py -> Standings of Challenges starting within the same day are extracted.
* Re-run main.py to update the standings after any round finish.

The MTGO logs are cleaned each time the client starts up, but challenges data of the day are re-downloaded by the Client.