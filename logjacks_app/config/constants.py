HELPFUL_SHEET_FUNCTIONS = """
<p>
    These Functions will help with data entry, type them into the table cell you wish to start at and click Enter.<br>
    The function name is not case-sensitive, but you do need to type the "=" sign before the function name.
</p>
<p><b>=REP(Arg1, Arg2)</b> [Repeating the Same Value]<br>
    Arg1 is the value to be repeated<br>
    Arg2 is how many rows it will be repeated in<br><br>
    For example:<br>
    <b>=REP(1, 4)</b><br>
    1<br>
    1<br>
    1<br>
    1<br><br>
    <b>=REP(DF, 3)</b><br>
    DF<br>
    DF<br>
    DF<br>
</p>
<br><br>

<p><b>=SEQ(Arg1, Arg2)</b> [Sequential Numbers]<br>
    Arg1 is starting number in the sequence<br>
    Arg2 is the stopping number in the sequence<br>* Arg1 may be omitted and will default to 1 *<br><br>
    For example:<br>
    <b>=SEQ(4)</b><br>
    1<br>
    2<br>
    3<br>
    4<br><br>
    <b>=SEQ(3, 6)</b><br>
    3<br>
    4<br>
    5<br>
    6<br>
</p>
<br><br>

</p>
<p><b>=CLR(Arg1)</b> [Clearing a subset of data]<br>
    Arg1 is the number of rows within the column to clear<br><br>
    For example:<br>
    <b>=CLR(4)</b><br>
    *blank*<br>
    *blank*<br>
    *blank*<br>
    *blank*<br>
</p>

"""

FLASH_UNABLE_TO_IMPORT = """
<b>Unable to Import Sheet</b><br>
LogJacks looks for many variations of column names while importing, but unfortunately <br> 
it could not locate the required columns from this sheet.<br><br>
If you have column names that are standard for your business and would like to get them<br>
added to the list of column names LogJacks searches for, please contact us.<br><br>
Required Columns for Import are:<br>
<b>Stand ID<br>
Plot Factor<br>
Plot Number<br>
Tree Number<br>
Species<br>
DBH<br>
Total Height</b>
"""