SPECIES = ['SF', 'GF', 'NF', 'WL', 'LP', 'PP', 'DF', 'WH', 'RA', 'BM',
'SS', 'ES', 'AS', 'WP', 'RC', 'CW', 'JP', 'SP', 'WF', 'RF', 'RW', 'IC'];

GRADES = ['PL', 'P1', 'P2', 'P3', 'SM', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'UT', 'CR'];

RED = '#FB866D';

MASTER = {};

F_IDX_START = 7;
F_IDX_STOP = 10;
F_REMOVE = 3;
SETBACK_TOG = 8;
SETBACK_INIT = 24;
SKIP_STAND = 1;

ON_TOGGLE = null;
QUICK_CRUISE = true;


function today(){
    Date.prototype.toDateInputValue = (function() {
        var local = new Date(this);
        local.setMinutes(this.getMinutes() - this.getTimezoneOffset());
        return local.toJSON().slice(0,10);
    });
    return new Date().toDateInputValue();
}

function update_flash(visibility, innerHTML){
    var flash = document.getElementById('flash_p');
    flash.style.visibility = visibility;
    flash.innerHTML = innerHTML
    flash.style.fontWeight = 'bold';
    flash.style.color = RED;
}

function toggle_buttons(visibility){
    document.getElementById('open_dialog').style.visibility = visibility;
    document.getElementById('submit_data').style.visibility = visibility;
    document.getElementById('clear_data').style.visibility = visibility;
    document.getElementById('add_row_but').style.visibility = visibility;
}


function clear_alert() {
    var warning = 'Are you sure you would like to clear your data?';
    if (confirm(warning)) {
        var table = document.getElementById('blank_inventory_table').children[0];
        var tbody = table.children[1];
        for (var row_idx = 0; row_idx < tbody.children.length; row_idx ++){
            var row  = tbody.children[row_idx];
            for (var col_idx = 1; col_idx < row.children.length; col_idx ++){
                inpt = row.children[col_idx].firstChild;
                inpt.value = '';
                inpt.style['background-color'] = '';
            }
        }
    }
}


function add_row(blank_row){
    var tbody = document.getElementById('blank_inventory_table').children[0].children[1];
    var row_len = tbody.children[0].children.length + 2;
    var row_idx = tbody.children.length + 1;
    var tr, td;

    if (QUICK_CRUISE) {
        tr = _create_tbody_row(row_idx, blank_row);
        tbody.appendChild(tr);
    } else {
        tr = _create_tbody_row(row_idx, blank_row);
        for (var i = 0; i < F_REMOVE; i++){
            tr.removeChild(tr.lastChild);
        }
        for (var i = F_IDX_STOP; i < row_len; i++){
            td = _create_tbody_td(row_idx, blank_row[i]);
            tr.appendChild(td);
        }
        tbody.appendChild(tr);
    }
}


function toggle_cruise(toggle, blank_row){
    var toggle_switch;

    if (toggle.id.slice(-1) == '1'){
        toggle_switch = '2';
        QUICK_CRUISE = true;
    } else {
        toggle_switch = '1';
        QUICK_CRUISE = false;
    }
    var off_toggle = document.getElementById(toggle.id.slice(0, -1) + toggle_switch);
    off_toggle.checked = false;

    if (ON_TOGGLE != toggle ) {
        ON_TOGGLE = toggle;
        var table = document.getElementById('blank_inventory_table').children[0];
        var thead_row = table.children[0].children[0];
        var thead_row_removals = thead_row.children.length - SETBACK_TOG;
        var tbody = table.children[1];

        var row, row_len, th, td;
        if (toggle_switch == '2') {
            for (var col_idx = 0; col_idx < thead_row_removals; col_idx ++) {
                thead_row.removeChild(thead_row.lastChild);
            }
            for (var col_idx = F_IDX_START; col_idx < F_IDX_STOP; col_idx ++){
                th = _create_thead_th(blank_row[col_idx].label);
                thead_row.appendChild(th);
            }
            for (var row_idx = 0; row_idx < tbody.children.length; row_idx ++){
                row = tbody.children[row_idx];
                row_removals = row.children.length - SETBACK_TOG;
                for (var col_idx = 0; col_idx < row_removals; col_idx ++) {
                    row.removeChild(row.lastChild);
                }
                for (var col_idx = F_IDX_START; col_idx < F_IDX_STOP; col_idx ++){
                    td = _create_tbody_td(row_idx + 1, blank_row[col_idx]);
                    row.appendChild(td);
                }
            }
        } else {
            for (var col_idx = 0; col_idx < F_REMOVE; col_idx ++) {
                thead_row.removeChild(thead_row.lastChild);
            }
            for (var col_idx = F_IDX_STOP; col_idx < blank_row.length; col_idx ++) {
                th = _create_thead_th(blank_row[col_idx].label);
                thead_row.appendChild(th);
            }

            for (var row_idx = 0; row_idx < tbody.children.length; row_idx ++){
                row = tbody.children[row_idx];
                for (var col_idx = 0; col_idx < F_REMOVE; col_idx ++) {
                    row.removeChild(row.lastChild);
                }
                for (var col_idx = F_IDX_STOP; col_idx < blank_row.length; col_idx ++) {
                    td = _create_tbody_td(row_idx + 1, blank_row[col_idx]);
                    row.appendChild(td);
                }
            }
        }
    }
}


function _create_radio(radio_id, is_checked, label, blank_row) {
    radio = document.createElement('input');
    radio.type = 'radio';
    radio.id = radio_id;
    radio.className = 'form-check-input';
    radio.checked = is_checked;
    if (is_checked){ON_TOGGLE = radio;}
    radio.onclick = function(){toggle_cruise(this, blank_row)};

    radio_lab = document.createElement('label');
    radio_lab.className = 'form-check-label';
    radio.htmlFor = radio_id
    radio_lab.innerHTML = label;

    return [radio, radio_lab]
}

function _create_thead_row(blank_row) {
    // Starting Table Head and Adding Row Number at the beginning
    var tr = document.createElement('tr');
    tr.style.textAlign = 'center';
    var th = document.createElement('th');
    th.style.width = '20px'
    th.innerHTML = '&emsp;';
    tr.appendChild(th);

    //Constructing Table Head
    for (var i = 0; i < blank_row.length - SETBACK_INIT; i ++){
        th = _create_thead_th(blank_row[i].label);
        tr.appendChild(th);
    }
    return tr
}

function _create_thead_th(label){
    var th = document.createElement('th');
    th.innerHTML = label;
    return th
}

function _create_tbody_row(row_idx, blank_row){
    var tr, td, sml
    var tr = document.createElement('tr');
    var td = document.createElement('td');
    var sml = document.createElement('small');

    td.style.textAlign = 'center';
    sml.innerHTML = row_idx;
    sml.style.width = '20px'
    td.appendChild(sml);
    tr.appendChild(td);

    for (var i = 0; i < blank_row.length - SETBACK_INIT; i++){
        td = _create_tbody_td(row_idx, blank_row[i]);
        tr.appendChild(td);
    }
    return tr
}

function _create_tbody_td(row_idx, elem) {
    var td = document.createElement('td');
    var inpt = document.createElement('input');
    inpt.type = 'text';
    inpt.name = elem.name + `_${row_idx}`;
    inpt.value = elem.val;
    inpt.required = elem.required;
    inpt.onchange = function(){input_formulas(this)}
    inpt.style.width = '125px';

    td.appendChild(inpt);
    return td
}


function create_new_table(button, blank_row, alert_clear=false){
    QUICK_CRUISE = true;
    update_flash('hidden', '')

    var b_div = document.getElementById('blank_inventory_table');

    if (alert_clear){
        var warning = 'Are you sure you would like to clear your data and start a blank sheet?';
        if (confirm(warning)) {
            b_div.innerHTML = '';
        } else {
            return
        }
    }

    button.disabled = true;
    toggle_buttons('visible');

    var t_div = document.getElementById('cruise_toggle');
    var radios = [['&emsp;Quick Cruise', true], ['&emsp;Full Cruise', false]];
    var p_tag, radio, radio_lab, radio_id;

    for (var i = 0; i < radios.length; i++){
        radio_id = `cruise_radio_${i + 1}`
        p_tag = document.createElement('p');
        [radio, radio_lab] = _create_radio(radio_id, radios[i][1], radios[i][0], blank_row)

        p_tag.appendChild(radio);
        p_tag.appendChild(radio_lab)
        t_div.appendChild(p_tag);
    }

    var table, thead, tbody, tr;

    table = document.createElement('table');
    thead = document.createElement('thead');

    tbody = document.createElement('tbody');
    tbody.style.overflow = 'scroll';

    tr = _create_thead_row(blank_row);
    thead.appendChild(tr);
    table.appendChild(thead);

    for (var i = 1; i < 51; i++){
        tr = _create_tbody_row(i, blank_row)
        tbody.appendChild(tr);
    }
    table.appendChild(tbody);
    b_div.append(table);
}


function create_imported_table(table_data){
    if (table_data[0].length > 10){
        QUICK_CRUISE = false;
    }

    toggle_buttons('visible');

    SETBACK_INIT = 0;

    var b_div, table, thead, tbody, tr;

    b_div = document.getElementById('blank_inventory_table');

    table = document.createElement('table');
    thead = document.createElement('thead');
    tbody = document.createElement('tbody');
    tbody.style.overflow = 'scroll'

    tr = _create_thead_row(table_data[0]);
    thead.appendChild(tr);
    table.appendChild(thead);

    for (var i = 0; i < table_data.length; i++){
        tr = _create_tbody_row(i + 1, table_data[i])
        tbody.appendChild(tr);
    }
    table.appendChild(tbody);
    b_div.append(table);

    SETBACK_INIT = 24;
}


function _check_float(value, non_negative=true, required=true){
    if (!required && value == ''){
        return value
    } else {
        var x = parseFloat(value);
        if (isNaN(x)) {
            return false
        } else if (non_negative && x < 0) {
            return false
        } else {
            return x
        }
    }
}

function _check_int(value, required=true){
    if(!required && value == '') {
        return value
    } else {
        var x = parseInt(value);
        if (isNaN(x)) {
            return false
        } else if (x < 0) {
            return false
        } else {
            return x
        }
    }
}

function _check_val_in_list(value, check_list, required=true, check_reverse=false) {
    if (!required && value == ''){
        return value
    } else {
        var x = value.toUpperCase();
        if (check_list.includes(x)){
            return x
        } else {
            if (check_reverse){
                var y = _reverse_str(x);
                if (check_list.includes(y)) {
                    return y
                }
            }
            return false
        }
    }
}

function _reverse_str(value){
    arr = value.split('');
    return arr.reverse().join('');
}


CHECKS = {
    2: function(value){return _check_float(value, non_negative=false)},
    3: function(value){return _check_int(value)},
    4: function(value){return _check_int(value)},
    5: function(value){return _check_val_in_list(value, SPECIES)},
    6: function(value){return _check_float(value)},
    7: function(value){return _check_float(value, non_negative=true, required=false)},
}

QUICK_CHECKS = {
    8: function(value){return _check_int(value)},
    9: function(value){return _check_int(value)},
    10: function(value){return _check_int(value)}
}

FULL_CHECKS = {
    1: function(value){return _check_int(value, required=false)},
    2: function(value){return _check_val_in_list(value, GRADES, required=false, check_reverse=true)},
    3: function(value){return _check_int(value, required=false)},
    0: function(value){return _check_int(value, required=false)},
}

function _get_table_head_vals(){
    var thead_cols = document.getElementById('blank_inventory_table').children[0].children[0].firstChild.children;
    var thead_vals = []
    for (var i = 0; i < thead_cols.length; i ++){
        thead_vals.push(thead_cols[i].innerHTML)
    }
    return thead_vals
}

function _create_label(value){
    label = document.createElement('label');
    label.innerHTML = value
    label.style = 'width: 200px; text-align: left; font-weight: bold;'
    return label
}

function _create_input(dtype, value){
    inpt = document.createElement('input');
    inpt.type = dtype;
    inpt.value = value;
    inpt.style.width = '200px'
    inpt.onchange = function(){this.style['background-color'] = ''}
    if (dtype == 'text'){
        inpt.disabled = true;
    }
    return inpt
}

function submit_stands(){
    var div = document.getElementById('multiple_stands_div');
    var master_table = document.getElementById('master|master_table');

    var errors = false;
    var valid_stand_id = true;

    var current_stand, inpt, lab;
    for (var i = 0; i < div.children.length; i++){
        child = div.children[i];
        if (child.tagName == 'P'){
            if (child.children.length == 2){
                inpt = child.lastChild;
                if (inpt.type == 'text') {
                    current_stand = inpt.value.toUpperCase();
                } else {
                    if (inpt.type == 'number'){
                        val = _check_float(inpt.value, non_negative=true, required=false);
                    } else {
                        val = inpt.value;
                    }

                    if (val === false) {
                        errors = true;
                        inpt.style['background-color'] = RED;
                    } else {
                        if (val == '') {
                            val = 0
                        }
                        lab = child.firstChild.innerHTML.slice(0, -1);
                        MASTER[current_stand][lab] = val;
                    }
                }
            }
        }
    }

    if (errors){
        update_flash('visible', 'Errors in form...')

    } else {
        master_table.value = JSON.stringify(MASTER);
        document.getElementById('form_new_sale').submit();
    }
}


function stands_block(stands){
    var b_div = document.getElementById('blank_inventory_table');
    b_div.innerHTML = '';

    update_flash('hidden', '')
    toggle_buttons('hidden');

    var form = document.getElementById('form_new_sale');
    var div = document.createElement('div');
    div.id = 'multiple_stands_div';

    var p, h6, inpts, lab, inpt, i, j

    p = document.createElement('p');
    h6 = document.createElement('h6');
    h6.innerHTML = 'Enter Stand Data'
    p.appendChild(h6);
    div.appendChild(p);

    for (i = 0; i < stands.length; i++){
        inpts = [['Stand ID:', 'text', stands[i]], ['Acres:', 'number', ''], ['Date of Inventory:', 'date', today()]]
        for (j = 0; j < inpts.length; j ++){
            p = document.createElement('p');
            lab = _create_label(inpts[j][0]);
            inpt = _create_input(inpts[j][1], inpts[j][2]);
            p.appendChild(lab);
            p.appendChild(inpt);
            div.appendChild(p);
        }
        p = document.createElement('p');
        p.innerHTML = '&emsp;'
        div.appendChild(p);
    }
    p = document.createElement('p');
    submit = document.createElement('input');
    submit.type = 'button';
    submit.value = 'Submit'
    submit.className = 'btn btn-sm btn-info';
    submit.onclick = submit_stands;
    p.appendChild(submit);

    div.appendChild(p);

    b_div.appendChild(div);
}


function check_table_cells(){
    var form = document.getElementById('form_new_sale');
    var flash = document.getElementById('flash_p');

    var master_table = document.getElementById('master|master_table');
    var thead_vals = _get_table_head_vals()
    var tbody = document.getElementById('blank_inventory_table').children[0].children[1];
    var rows_len = tbody.children[0].children.length;
    var no_errors = true
    var valid_stand_id = true
    var row, row_idx, col_idx, current_stand, check_val, head_val, inner, inpt, inner_inpt, check_blanks, current_log;

    MASTER = {}
    var stands = []
    for (row_idx = 0; row_idx < tbody.children.length; row_idx ++) {
        row = tbody.children[row_idx];

        for (col_idx = 1; col_idx < row.children.length; col_idx ++) {
            inpt = row.children[col_idx].firstChild;
            if (col_idx == 1){
                if (inpt.value == '') {
                    check_blanks = [];
                    for (inner = 2; inner < 8; inner ++){
                        inner_inpt = row.children[inner].firstChild.value;
                        if (inner_inpt != '') {
                            check_blanks.push(inner_inpt);
                        }
                    }
                    if (check_blanks.length == 0){
                        if (no_errors) {
                            if (Object.keys(MASTER).length > 0){
                                stands_block(stands);
                            } else {
                                update_flash('visible', 'Please enter some stand data before submitting')
                            }
                        }
                        return
                    } else {
                        no_errors = false
                        valid_stand_id = false
                        inpt.style['background-color'] = RED;
                    }
                } else {
                    valid_stand_id = true
                    current_stand = inpt.value.toUpperCase();
                    if (!MASTER.hasOwnProperty(current_stand)){
                        MASTER[current_stand] = {}
                        stands.push(current_stand);
                    }
                }
            } else {
                if (col_idx > 7) {
                    if (QUICK_CRUISE){
                        check_val = QUICK_CHECKS[col_idx](inpt.value);
                    } else {
                        check_val = FULL_CHECKS[col_idx % 4](inpt.value);
                    }
                } else {
                    check_val = CHECKS[col_idx](inpt.value);
                }

                if (check_val === false) {
                    no_errors = false;
                    inpt.style['background-color'] = RED;
                } else {
                    head_val = thead_vals[col_idx];

                    if (head_val.startsWith('Log')) {
                        current_log = head_val.slice(4, 5);
                    }

                    if (head_val.startsWith('Between')){
                        head_val = head_val + current_log;
                    }

                    if (valid_stand_id) {
                        if(!MASTER[current_stand].hasOwnProperty(head_val)){
                            MASTER[current_stand][head_val] = []
                        }
                        MASTER[current_stand][head_val].push(check_val);
                    }
                }

            }
        }
    }
    if (no_errors){
        stands_block(stands);
    } else {
        update_flash('visible', 'Errors within table...')
    }
}

















