/*
See logjacks_app.config.constants
for explanations on what
the functions do and their arguments
*/

function input_formulas(input){
    input.style['background-color'] = '';

    if (input.value.startsWith('=')) {
        var row = input.parentElement.parentElement;
        var tbody = row.parentElement;
        var row_idx = Array.prototype.indexOf.call(tbody.children, row);
        var col_idx = Array.prototype.indexOf.call(row.children, input.parentElement);
        var func = input.value.slice(0, 4).toUpperCase();

        if (func == '=SEQ') {
            _sequence(input, tbody, row_idx, col_idx);
        } else if (func == '=REP'){
            _repeat(input, tbody, row_idx, col_idx);
        } else if (func == '=CLR'){
            _clear(input, tbody, row_idx, col_idx);
        }
    }
}

function _extract_args(input_value){
    var reg_exp = /\(([^)]+)\)/;
    var express = reg_exp.exec(input_value)[1];
    var args_list;
    if (express.includes(',')){
        args_list = express.split(',');
    } else {
        args_list = [express];
    }
    return args_list
}


function _sequence(input, tbody, row_idx, col_idx){
    args = _extract_args(input.value);
    var start, stop
    if (args.length > 1){
        start = parseInt(args[0]);
        stop = parseInt(args[1]) - start + 1;

    } else {
        start = 1
        stop = parseInt(args[0]);
    }
    if (isNaN(start) || isNaN(stop)) {
        alert("=SEQ function's arguments must both be integers")
    }
    var inpt_chg;
    for (var i = row_idx; i < row_idx + stop; i++){
        if (i > tbody.children.length - 1) {break;}
        inpt_chg = tbody.children[i].children[col_idx].children[0];
        inpt_chg.value = start;
        start ++
    }

    _change_focus(tbody.children[row_idx + stop].children[col_idx].children[0]);
}


function _repeat(input, tbody, row_idx, col_idx){
    args = _extract_args(input.value);
    var same, stop
    if (args.length < 2){
        alert('=REP function needs to have two arguments:\n1) The value which will be the repeated\n2) The number of rows to update')

    } else {
        same = args[0]
        stop = parseInt(args[1]);
        if (isNaN(stop)){
            alert("=REP function's 2nd argument must be an integer")
        }
    }
    var inpt_chg;
    for (var i = row_idx; i < row_idx + stop; i++){
        if (i > tbody.children.length - 1) {break;}
        inpt_chg = tbody.children[i].children[col_idx].children[0];
        inpt_chg.value = same;
    }

    _change_focus(tbody.children[row_idx + stop].children[col_idx].children[0]);
}


function _clear(input, tbody, row_idx, col_idx){
    args = _extract_args(input.value);

    stop = parseInt(args[0]);
    if (isNaN(stop)){
        alert("=CLR function's argument must be an integer")
    }

    var inpt_chg;
    for (var i = row_idx; i < row_idx + stop; i++){
        if (i > tbody.children.length - 1) {break;}
        inpt_chg = tbody.children[i].children[col_idx].children[0];
        inpt_chg.value = '';
    }

    _change_focus(tbody.children[row_idx + stop].children[col_idx].children[0]);
}

function _change_focus(last_input){
    last_input.focus()
}