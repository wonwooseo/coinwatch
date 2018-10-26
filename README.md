# coinwatch
Watch coin price and buy / sell on user-set point.
Uses Coinone API.

## Price Monitor
Monitor for each currency works with 2 threads, one for GUI loop and one for 
data fetching via Coinone API. Those threads communicate using a queue.
Global flag is used to signal exit.

## Transactions
Not implemented yet.

## TODOs
- [x] Price monitoring loop
- [x] GUI to show monitoring results
- [x] Multiple monitors via threading
- [x] Config INI for monitor settings
- [ ] In-GUI menu to change options of monitor
- [ ] Send alert to user when preset price is met

... and more to come...

## Possible features in future
- Make transactions based on monitoring results
- Expand to stocks
- ML-based prediction?