# Land Registry Analysis
A script to do some basic analysis on data downloaded from the HM Land Registry Open Data website.

Current functionality:
- "current_value" Takes input file and the address of a house you want the current value of, and works out what it "should" be, if it has increased from its last sold value by the same amount as the other houses on the list.

Input:
- Takes a csv of values exported from the land registry website, with the "with headers" options.

Example:
- Semi-detached, freehold, not-new houses in Little Paxton in the standard transaction category for all time. Exported 28/01/2023.
- Result: 63 Gordon Way, last sold in June 2003 for £140k, should cost £___k, being listed in Jan 2023 for