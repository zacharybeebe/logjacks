
def _add_date_zeros(val):
    return f"""{'0' * (2 - len(str(val)))}{val}"""


def f_date(dt):
    y = dt.year
    m = _add_date_zeros(dt.month)
    d = _add_date_zeros(dt.day)
    return f'{m}/{d}/{y}'


def h_date(model_date):
    m, d, year = model_date.split('/')
    month = _add_date_zeros(m)
    day = _add_date_zeros(d)
    return f'{year}-{month}-{day}'


# def back_date(val):
#     return datetime(*[int(i) for i in val.split('-')])

def f_price(value):
    if isinstance(value, str):
        value = float(value)
    else:
        value = value
    val_list = [i for i in str(round(value, 2))]
    if '.' not in val_list:
        add_to = ['.', '0', '0']
        for i in add_to:
            val_list.append(i)
    else:
        if len(val_list[-(len(val_list) - val_list.index('.')):]) < 3:
            val_list.append('0')
    temp = [i for i in reversed(val_list)]
    added = 0
    for i in range(3, len(val_list)):
        if i != 3 and i % 3 == 0:
            temp.insert(i + added, ',')
            added += 1
    return f"""${''.join([i for i in reversed(temp)])}"""


def f_round(value):
    str_list = [i for i in str(round(float(value), 1))]
    if len(str_list) <= 5:
        return ''.join(str_list)
    else:
        temp = [0]
        temp += [i for i in reversed(str_list)]
        added = 0
        for i in range(2, len(temp)):
            if i != 3 and i % 3 == 0:
                temp.insert(i + added, ',')
                added += 1
        temp.pop(0)
        return ''.join([i for i in reversed(temp)])


def f_round_or_blank(value):
    f_val = float(value)
    if f_val == 0:
        return '-'
    else:
        str_list = [i for i in str(round(f_val, 1))]
        if len(str_list) <= 5:
            return ''.join(str_list)
        else:
            temp = [0]
            temp += [i for i in reversed(str_list)]
            added = 0
            for i in range(2, len(temp)):
                if i != 3 and i % 3 == 0:
                    temp.insert(i + added, ',')
                    added += 1
            temp.pop(0)
            return ''.join([i for i in reversed(temp)])



if __name__ == '__main__':
    print(f_round_or_blank(0.9652122729998485))