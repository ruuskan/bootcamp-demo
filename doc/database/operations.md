Module bootcamp-demo.database.operations
========================================

Functions
---------

    
`get_all()`
:   Returns sqlalchemy query object
    
    Query all data.

    
`insert_row(date, primary, secondary, tertiary, share_count, share_amount, tier_name)`
:   Return id of the inserted row
    
    Insert new row with supplied data in the database
    
    Parameters:
    date:           datetime object of the draw time
    primary:        stringified list of primary numbers
    secondary:      stringified list of secondary numbers
    tertiary:       stringified list of tertiary numbers
    share_count:    stringified list of winners of each prize tier
    share_amount:   stringified list of winnings per winner of each prize tier
    tier_name:      stringified list of tier names

    
`search_between(startdate, enddate)`
:   Returns sqlalchemy query object
    
    Query result between starting and ending datetimes.
    
    Parameters:
    startdate:  datetime.datetime type time object specifying starting date for the query
    enddate:    datetime.datetime type time object specifying ending date for the query