# Gun Violence Data
Looking through this (gun violence dataset)[https://github.com/jamesqo/gun-violence-data] for patterns. Current functionality is to input a month, and then return a bar chart of number of gun-caused deaths grouped by state.

## Built With:
- Pandas
- jQuery
- d3.js

## Next steps:
- Add labels
- Figure out smooth animated transition between months
- Track a particular state month-by-month in a line chart
- Animate the transition from January to December all in one go
- Figure out how to groupby month *WITHOUT* having to add month as a column manually every time the server spins up. I guess we could just re-save it as a new CSV and use *that* one. That's probably easiest.
- Add a stacked bar chart; and maybe stacked histograms?
