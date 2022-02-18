HIGHLIGHT = '#B0F9F5';


function toggle_table(t_row, table_id){
    var table = document.getElementById(table_id);

    if (table.style.visibility == 'collapse'){
        table.style.visibility = 'visible';
        t_row.style.backgroundColor = HIGHLIGHT;
    } else {
        table.style.visibility = 'collapse';
        t_row.style.backgroundColor = '';
    }

}
