from logjacks_app.timber.constants import ALL_SPECIES_NAMES, GRADE_NAMES
import json


class Cell:
    def __init__(self, label, value, type_, required, non_negative):
        self.label = label
        self.name = f'cell|{self.label}'
        self.val = value
        self.type = type_
        self.required = required
        self.non_negative = non_negative
        self.err = False

    def __json__(self):
        master = {}
        for key, value in self.__dict__.items():
            if value in [True, False, None]:
                master[key] = json.dumps(value)
            else:
                master[key] = value
        return master

    def error_func(self):
        pass

    def error_check(self):
        return self.error_func()


class FloatCell(Cell):
    def __init__(self, label, value, required=True, non_negative=True):
        super(FloatCell, self).__init__(label, value, 'number', required, non_negative)

    def error_func(self):
        if not self.required and self.val == '':
            return None
        else:
            if ''.join(filter(lambda x: False if x == '.' else True, self.val)).isdigit():
                self.val = float(self.val)
                if self.non_negative and self.val < 0:
                    return False
                else:
                    return self.val
            else:
                return False


class IntegerCell(Cell):
    def __init__(self, label, value, required=False):
        super(IntegerCell, self).__init__(label, value, 'number', required, True)

    def error_func(self):
        if not self.required and self.val == '':
            return None
        else:
            if self.val.isnumeric():
                self.val = int(self.val)
                if self.val < 0:
                    return False
                else:
                    return self.val
            else:
                return False


class LogGradeCell(Cell):
    def __init__(self, label, value):
        super(LogGradeCell, self).__init__(label, value, 'text', False, True)

    def error_func(self):
        if self.val.upper() in GRADE_NAMES:
            self.val = self.val.upper()
            return self.val
        else:
            return False


class SpeciesCell(Cell):
    def __init__(self, value):
        super(SpeciesCell, self).__init__('Species', value, 'text', True, True)

    def error_func(self):
        if self.val.upper() in ALL_SPECIES_NAMES:
            self.val = self.val.upper()
            return self.val
        else:
            return False


class StandCell(Cell):
    def __init__(self, value):
        super(StandCell, self).__init__('Stand ID', value, 'text', True, True)

    def error_func(self):
        if self.val == '':
            return False
        else:
            return self.val

