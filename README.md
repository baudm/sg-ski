# sg-ski
A solution to RedMart's [Skiing in Singapore](http://geeks.redmart.com/2015/01/07/skiing-in-singapore-a-coding-diversion/) coding diversion

In order to minimize the execution time, a simple 2-dimensional list containing int objects is used. The chosen solution is recursive in nature, so memoization is employed to avoid recomputation of previously calculated values. The *expensive* section of get_length_and_elevation() is called only as many times as the total number of elements in the map grid.
