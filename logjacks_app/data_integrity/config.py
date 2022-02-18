from logjacks_app.data_integrity.table_cells import IntegerCell, FloatCell, LogGradeCell, SpeciesCell, StandCell


INVENTORY_ROW = [
    StandCell(''),
    FloatCell('Plot Factor', '', non_negative=False),
    IntegerCell('Plot Number', '', required=True),
    IntegerCell('Tree Number', '', required=True),
    SpeciesCell(''),
    FloatCell('DBH', ''),
    FloatCell('Total Height', '', required=False),
    IntegerCell('Pref Log Length', 40),
    IntegerCell('Min Log Length', 16),
    IntegerCell('Utility Log DIB', 3),
    IntegerCell('Stump Height', 1),
    IntegerCell('Log 1 Length', ''),
    LogGradeCell('Log 1 Grade', ''),
    IntegerCell('Log 1 Defect', ''),
    IntegerCell('Between Logs', 0),
    IntegerCell('Log 2 Length', ''),
    LogGradeCell('Log 2 Grade', ''),
    IntegerCell('Log 2 Defect', ''),
    IntegerCell('Between Logs', 0),
    IntegerCell('Log 3 Length', ''),
    LogGradeCell('Log 3 Grade', ''),
    IntegerCell('Log 3 Defect', ''),
    IntegerCell('Between Logs', 0),
    IntegerCell('Log 4 Length', ''),
    LogGradeCell('Log 4 Grade', ''),
    IntegerCell('Log 4 Defect', ''),
    IntegerCell('Between Logs', 0),
    IntegerCell('Log 5 Length', ''),
    LogGradeCell('Log 5 Grade', ''),
    IntegerCell('Log 5 Defect', ''),
    IntegerCell('Between Logs', 0),
    IntegerCell('Log 6 Length', ''),
    LogGradeCell('Log 6 Grade', ''),
    IntegerCell('Log 6 Defect', '')
]


POSSIBLE_COL_NAMES_FROM_UPLOAD = {
    'Stand ID': {
        'names': ['S NAME', 'S ID', 'S CN', 'S NM', 'ST NAME', 'ST ID', 'ST CN', 'ST NM', 'STD NAME', 'STD ID', 'STD CN', 'STD NM',
                  'STND NAME', 'STND ID', 'STND CN', 'STND NM', 'STAND NAME', 'STAND ID', 'STAND CN', 'STAND NM',
                  'ST', 'STND', 'STAND', 'PUNIT_NAME'],
        'required': True,
        'cruise': 'base',
        'fill': False
    },

    'Plot Factor': {
        'names': ['P FACTOR', 'P FACT', 'P FAC', 'P F', 'PT FACTOR', 'PT FACT', 'PT FAC', 'PT F', 'PLT FACTOR', 'PLT FACT', 'PLT FAC', 'PLT F',
                  'PLOT FACTOR', 'PLOT FACT', 'PLOT FAC',
                  'E FACTOR', 'E FACT', 'E FAC', 'E F', 'EX FACTOR', 'EX FACT', 'EX FAC', 'EX F', 'EXP FACTOR', 'EXP FACT', 'EXP FAC', 'EXP F',
                  'EXPANSION FACTOR', 'EXPANSION FACT', 'EXPANSION FAC'],
        'required': True,
        'cruise': 'base',
        'fill': False
    },

    'Plot Number': {
        'names': ['P NUMBER', 'P NUM', 'P #', 'PT NUMBER', 'PT NUM', 'PT #', 'PLT NUMBER', 'PLT NUM', 'PLT #', 'PLOT NUMBER', 'PLOT NUM', 'PLOT #',
                  'PLOT', 'PLT', 'PT'],
        'required': True,
        'cruise': 'base',
        'fill': False
    },

    'Tree Number': {
        'names': ['T NUMBER', 'T NUM', 'T #', 'T N', 'TR NUMBER', 'TR NUM', 'TR #', 'TR N', 'TRE NUMBER', 'TRE NUM', 'TRE #', 'TRE N',
                  'TREE NUMBER', 'TREE NUM', 'TREE #', 'TREE N', 'TREE', 'TRE', 'TR'],
        'required': True,
        'cruise': 'base',
        'fill': False
    },

    'Species': {
        'names': ['SP', 'SPP', 'SPC', 'SPECIE', 'SPECIES', 'SP CD', 'SPP CD', 'SPC CD', 'SPECIE CD', 'SPECIES CD',
                  'SP CODE', 'SPP CODE', 'SPC CODE', 'SPECIE CODE', 'SPECIES CODE'],
        'required': True,
        'cruise': 'base',
        'fill': False
    },

    'DBH': {
        'names': ['D', 'DB', 'DBH', 'DIA', 'DIAM', 'DIAMETER', 'DIAMETER BREAST HEIGHT'],
        'required': True,
        'cruise': 'base',
        'fill': False
    },

    'Total Height': {
        'names': ['HT', 'HGT', 'HEIGHT', 'T HT', 'T HGT', 'T HEIGHT', 'TOT HT', 'TOT HGT', 'TOT HEIGHT', 'TTL HT', 'TTL HGT', 'TTL HEIGHT',
                  'TOTAL HT', 'TOTAL HGT', 'TOTAL HEIGHT'],
        'required': True,
        'cruise': 'base',
        'fill': False
    },

    'Pref Log Length': {
        'names': ['P L', 'P LG', 'P LOG', 'PREF L', 'PREF LG', 'PREF LOG', 'PREFERRED L', 'PREFERRED LG', 'PREFERRED LOG',
                  'P L LGT', 'P LG LGT', 'P LOG LGT', 'PREF L LGT', 'PREF LG LGT', 'PREF LOG LGT', 'PREFERRED L LGT',
                  'PREFERRED LG LGT', 'PREFERRED LOG LGT', 'P L LENGTH', 'P LG LENGTH', 'P LOG LENGTH',
                  'PREF L LENGTH', 'PREF LG LENGTH', 'PREF LOG LENGTH', 'PREFERRED L LENGTH', 'PREFERRED LG LENGTH', 'PREFERRED LOG LENGTH',
                  'PLOG LGT', 'PLOG LENGTH'],
        'required': False,
        'cruise': 'q',
        'fill': False,
        'default': 40
    },

    'Min Log Length': {
        'names': ['M L', 'M LG', 'M LOG', 'MIN L', 'MIN LG', 'MIN LOG', 'MINIMUM L', 'MINIMUM LG', 'MINIMUM LOG',
                  'M L LGT', 'M LG LGT', 'M LOG LGT', 'MIN L LGT', 'MIN LG LGT', 'MIN LOG LGT', 'MINIMUM L LGT',
                  'MINIMUM LG LGT', 'MINIMUM LOG LGT', 'M L LENGTH', 'M LG LENGTH', 'M LOG LENGTH',
                  'MIN L LENGTH', 'MIN LG LENGTH', 'MIN LOG LENGTH', 'MINIMUM L LENGTH', 'MINIMUM LG LENGTH', 'MINIMUM LOG LENGTH',
                  'MLOG LGT', 'MLOG LENGTH'],
        'required': False,
        'cruise': 'q',
        'fill': False,
        'default': 16
    },

    'Utility Log DIB': {
        'names': ['UT D', 'UT DIB', 'UTIL D', 'UTIL DIB', 'UTILITY D', 'UTILITY DIB',
                  'PL D', 'PL DIB', 'PLP D', 'PLP DIB', 'PULP D', 'PULP DIB',
                  'UT LG D', 'UT LG DIB', 'UT LOG D', 'UT LOG DIB', 'UTIL LG D', 'UTIL LG DIB', 'UTIL LOG D', 'UTIL LOG DIB',
                  'UTILITY LG D', 'UTILITY LG DIB', 'UTILITY LOG D', 'UTILITY LOG DIB',
                  'PL LG D', 'PL LG DIB', 'PL LOG D', 'PL LOG DIB', 'PLP LG D', 'PLP LG DIB', 'PLP LOG D', 'PLP LOG DIB',
                  'PULP LG D', 'PULP LG DIB', 'PULP LOG D', 'PULP LOG DIB'],
        'required': False,
        'cruise': 'q',
        'fill': False,
        'default': 3
    },

    'Stump Height': {
        'names': ['S H', 'S HT', 'S HGT', 'S HEIGHT', 'ST H', 'ST HT', 'ST HGT', 'ST HEIGHT',
                  'STP H', 'STP HT', 'STP HGT', 'STP HEIGHT', 'STMP H', 'STMP HT', 'STMP HGT', 'STMP HEIGHT',
                  'STUMP H', 'STUMP HT', 'STUMP HGT', 'STUMP HEIGHT'],
        'required': False,
        'cruise': 'f',
        'fill': False,
        'default': 1
    },

    'Log {} Length': {
        'names': ['L {} LGT', 'L {} LENGTH', 'LG {} LGT', 'LG {} LENGTH', 'LOG {} LGT', 'LOG {} LENGTH',
                  'L LGT {}', 'L LENGTH {}', 'LG LGT {}', 'LG LENGTH {}', 'LOG LGT {}', 'LOG LENGTH {}',
                  'SG {} LGT', 'SG {} LENGTH', 'SEG {} LGT', 'SEG {} LENGTH', 'SEGMENT {} LGT', 'SEGMENT {} LENGTH',
                  'SG LGT {}', 'SG LENGTH {}', 'SEG LGT {}', 'SEG LENGTH {}', 'SEGMENT LGT {}', 'SEGMENT LENGTH {}'],
        'required': False,
        'cruise': 'f',
        'fill': True,
        'default': 'UTF'
    },

    'Log {} Grade': {
        'names': ['L {} GRD', 'L {} GRADE', 'LG {} GRD', 'LG {} GRADE', 'LOG {} GRD', 'LOG {} GRADE',
                  'L GRD {}', 'L GRADE {}', 'LG GRD {}', 'LG GRADE {}', 'LOG GRD {}', 'LOG GRADE {}',
                  'L {} GR', 'LG {} GR', 'LOG {} GR', 'L GR {}', 'LG GR {}', 'LOG GR {}',
                  'SG {} GRD', 'SG {} GRADE', 'SEG {} GRD', 'SEG {} GRADE', 'SEGMENT {} GRD', 'SEGMENT {} GRADE',
                  'SG GRD {}', 'SG GRADE {}', 'SEG GRD {}', 'SEG GRADE {}', 'SEGMENT GRD {}', 'SEGMENT GRADE {}',
                  'SG {} GR', 'SEG {} GR', 'SEGMENT {} GR', 'SEGMENT {} GR', 'SG GR {}', 'SEG GR {}', 'SEGMENT GR {}'],
        'required': False,
        'cruise': 'f',
        'fill': True,
        'default': 'UTF'
    },

    'Log {} Defect': {
        'names': ['L {} DFT', 'L {} DEFECT', 'LG {} DFT', 'LG {} DEFECT', 'LOG {} DFT', 'LOG {} DEFECT',
                  'L DFT {}', 'L DEFECT {}', 'LG DFT {}', 'LG DEFECT {}', 'LOG DFT {}', 'LOG DEFECT {}',
                  'L {} DF', 'LG {} DF', 'LOG {} DF', 'L DF {}', 'LG DF {}', 'LOG DF {}',
                  'SG {} DFT', 'SG {} DEFECT', 'SEG {} DFT', 'SEG {} DEFECT', 'SEGMENT {} DFT', 'SEGMENT {} DEFECT',
                  'SG DFT {}', 'SG DEFECT {}', 'SEG DFT {}', 'SEG DEFECT {}', 'SEGMENT DFT {}', 'SEGMENT DEFECT {}',
                  'SG {} DF', 'SEG {} DF', 'SEGMENT {} DF', 'SEGMENT {} DF', 'SG DF {}', 'SEG DF {}', 'SEGMENT DF {}'],
        'required': False,
        'cruise': 'f',
        'fill': True,
        'default': 0
    },

    'Between Logs': {
        'names': ['BTW L', 'BTW LG', 'BTW LGS', 'BTW LOG', 'BTW LOGS'
                  'BETWEEN L', 'BETWEEN LG', 'BETWEEN LGS', 'BETWEEN LOG', 'BETWEEN LOGS'],
        'required': False,
        'cruise': 'f',
        'fill': False,
        'default': 0
    }
}