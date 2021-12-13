from logjacks_app.timber.log import Log
from logjacks_app.timber.constants import (
    math,
    TAPER_EQ,
    TAPER_HEIGHTS_EQ
)
from time import perf_counter


def timer(func):
    def wrapper(*args, **kwargs):
        now = perf_counter()
        x = func(*args, **kwargs)
        after = perf_counter()
        print(f'{func.__name__} took {round(after-now, 10)} seconds\n')
        return x
    return wrapper


class Timber(object):
    def __init__(self, plot_factor: float, species: str, dbh: float, total_height: float):
        self.plot_factor = plot_factor
        self.species = species
        self.dbh = dbh
        self.total_height = total_height

        self.hdr = self.total_height / (self.dbh / 12)
        self.ba = self.dbh ** 2 * 0.005454
        self.rd = self.ba / math.sqrt(self.dbh)

        self.tpa, self.ba_ac, self.rd_ac = self._get_tpa_ba_ac_rd_ac()
        self.stem_dibs = TAPER_HEIGHTS_EQ[self.species](self.dbh, self.total_height)
        self.dib_heights = self._bucket_stem_dibs()

        self.merch_dib = math.floor(0.40 * self.stem_dibs[17][0])
        self.merch_height = self.dib_heights[self.merch_dib][-1]

    def __getitem__(self, item):
        return self.__dict__[item]

    def get_any_dib(self, stem_height: int):
        """Returns the diameter inside bark (DIB) at any given stem height"""
        return TAPER_EQ[self.species](self.dbh, self.total_height, stem_height)

    def _bucket_stem_dibs(self):
        dib_heights = {}
        for stem_height in self.stem_dibs:
            dib_int = self.stem_dibs[stem_height][0]
            if dib_int not in dib_heights:
                dib_heights[dib_int] = []
            dib_heights[dib_int].append(stem_height)

        return dib_heights

    def _get_tpa_ba_ac_rd_ac(self):
        """Calculates the Trees per Acre, Basal Area per Acre and Relative Density per Acre
           based on the plot factor"""
        if self.plot_factor == 0:
            return 0, 0, 0
        else:
            if self.plot_factor > 0:
                tpa = self.plot_factor / self.ba
                ba_ac = self.plot_factor
                rd_ac = tpa * self.rd

            else:
                tpa = abs(self.plot_factor)
                ba_ac = abs(self.plot_factor) * self.ba
                rd_ac = tpa * self.rd
            return tpa, ba_ac, rd_ac


class TimberQuick(Timber):
    """TimberQuick is a class that will virtually cruise a tree based on it's
       species, DBH, total height and plot factor. For fixed-area plots use the negative inverse of the plot size (1/30th ac = -30),
       for variable-area plots use the Basal Area Factor (BAF) (40 BAF = 40).

       Preferred Log Length and Minimum Log Length are needed
       but set at the default industry standard of 40 foot preferred and 16 foot minimum.

       TimberQuick uses stem-taper equations from Czaplewski, Kozak, or Wensel
       (depending on species) to calculate the DIB (diameter inside bark) at any stem height.

       TimberQuick will instantiate the tree with common individual and per acre metrics based on the input args.

       To cruise the tree, first TimberQuick determines the merchantable DIB of the tree, this is calculated from
       40% of the DIB at a stem height of 17 feet (the FORM height). This is industry standard.

       TimberQuick then correlates that Merch DIB to a merchantable height. The tree is then split up into logs,
       based on this Merch Height with priority given to the preferred log length and if preferred log length
       cannot be achieved, then if the remaining length up to Merch Height is greater than or equal to the minimum log length,
       that final log is added.

       Log metrics are sent to the Log Class, to which their volumes in Board Feet
       (using Scribner Coefficients based on Log Length and top DIB) and Cubic Feet (based on the Two-End Conic Cubic Foot Rule).
       Log grades are determined by species, minimum log lengths and minimum top DIBs set forth by the
       Official Rules for the Log Scaling and Grading Bureaus. Log defect is always 0%

       For inventories, this class is meant to be added to the Plot Class using the Plot Class method of add_tree"""

    def __init__(self, plot_factor: float, species: str, dbh: float, total_height: float,
                 preferred_log_length: int = 40, minimum_log_length: int = 16, utility_log_dib=3):
        super(TimberQuick, self).__init__(plot_factor, species, dbh, total_height)

        self.pref_log = int(preferred_log_length)
        self.min_log = int(minimum_log_length)
        self.utility_log_dib = utility_log_dib

        self.bf = 0
        self.cf = 0
        self.bf_ac = 0
        self.cf_ac = 0
        self.vbar = 0

        self.logs = self._get_volume_and_logs()

    def _get_volume_and_logs(self):
        """Method for cruising the tree, this will determine the stem heights and lengths of the logs, which are sent to
           the Log Class for volume calculations, return a dictionary of the logs by log number"""
        stem_heights = self._calc_stem_heights()
        lengths = [self._calc_log_length(stem_heights[i - 1], stem_heights[i]) for i in range(1, len(stem_heights))]
        stem_heights.pop(0)

        logs = {}
        bf = 0
        cf = 0
        for i, (stem_height, length) in enumerate(zip(stem_heights, lengths), 1):
            log = Log(self, stem_height, length)
            bf += log.bf
            cf += log.cf
            logs[i] = log

        self.bf = bf
        self.cf = cf
        self.bf_ac = self.bf * self.tpa
        self.cf_ac = self.cf * self.tpa
        self.vbar = self.bf / self.ba
        return logs

    def _calc_stem_heights(self):
        """Starting at stem height of 1 (stump height), master is updated with the log stem height calculated from
           self._calc_log_stem, if self._calc_log_stem returns None, all logs have been found and iteration is complete"""
        master = [1]
        for i in range(401):
            log_stem = self._calc_log_stem(master[i])
            if not log_stem[0]:
                if log_stem[1]:
                    master.append(log_stem[1])
                break
            else:
                master.append(log_stem[1])
        return master

    def _calc_log_stem(self, previous_log_stem_height):
        """Using the previous_log_stem_height arg, it will check if the minimum log length added to previous stem height plus
           1 foot of in-between is greater than the merch height, if it is, it will return None and no more logs can be added. If not
           it will check if the preferred log length added to the previous stem height plus 1 foot of in-between is less than
           or equal to the merch height, if it is then the new stem height is returned and a 40 foot (or user defined preferred length)
           log will added. If not then the merch height is the returned and a final log is added with a length determined by the difference
           between the merch height and previous stem height"""
        min_log_check = previous_log_stem_height + self.min_log + 1

        if min_log_check > self.merch_height - 2:
            try:
                utility_height = self.dib_heights[self.utility_log_dib][-1]
            except KeyError:
                utility_height = self.dib_heights[self.utility_log_dib + 1][-1]
            if utility_height - previous_log_stem_height - 1 >= self.min_log:
                return False, utility_height
            else:
                return False, None
        else:
            if previous_log_stem_height + 1 + self.pref_log <= self.merch_height:
                return True, previous_log_stem_height + self.pref_log + 1
            else:
                return True, self.merch_height

    @staticmethod
    def _calc_log_length(previous_log_stem_height, current_log_stem_height):
        """Returns a log length in multiples of 2 (24, 26, 28... feet)"""
        return (current_log_stem_height - previous_log_stem_height - 1) // 2 * 2


class TimberFull(Timber):
    """TimberFull is a class that will cruise a tree based on it's based on the user-cruised logs. These logs can be manually
       added to the class using the add_log method. Required arguments for add_log are stem height (int), log length (int),
       log grade (str), and log defect (int). Log defect should be the whole number value of the estimated percent defect 10% = 10.

       Like TimberQuick, TimberFull uses stem-taper equations from Czaplewski, Kozak, or Wensel
       (depending on species) to calculate the DIB (diameter inside bark) at any stem height.

       TimberFull will instantiate the tree with common individual and per acre metrics based on the input args.

       When the user adds a log using the add_log method, the log metrics are sent to the Log Class,
       to which their volumes in Board Feet (using Scribner Coefficients based on Log Length and top DIB)
       and Cubic Feet (based on the Two-End Conic Cubic Foot Rule) are calculated.

       For inventories, this class is meant to be added to the Plot Class using the Plot Class method of add_tree"""

    def __init__(self, plot_factor: float, species: str, dbh: float, total_height: float):
        super(TimberFull, self).__init__(plot_factor, species, dbh, total_height)

        self.bf = 0
        self.cf = 0
        self.bf_ac = 0
        self.cf_ac = 0
        self.vbar = 0

        self.logs = {}

    def add_log(self, stem_height, length, grade, defect):
        """Adds Log Class to the logs dictionary of TimberFull and recalculates the tree's volumes and
           volume-related metrics"""
        if not self.logs:
            self.logs[1] = Log(self, stem_height, length, grade=grade.upper(), defect_pct=defect)
        else:
            num = max(self.logs) + 1
            self.logs[num] = Log(self, stem_height, length, grade=grade.upper(), defect_pct=defect)
        self._calc_volume_and_logs()

    def _calc_volume_and_logs(self):
        """Calcuates the tree's volume and volume-related metrics based on the log volumes"""
        if not self.logs:
            return
        else:
            bf = 0
            cf = 0
            for lnum in self.logs:
                log = self.logs[lnum]
                bf += log.bf
                cf += log.cf

            self.bf = bf
            self.cf = cf
            self.bf_ac = self.bf * self.tpa
            self.cf_ac = self.cf * self.tpa
            self.vbar = self.bf / self.ba


if __name__ == '__main__':
    pf = 40
    spp = 'DF'
    dbh = 24.5
    hgt = 122

    # @timer
    # def hunnit(rng, obj, pf, spp, dbh, hgt):
    #     for i in range(rng):
    #         obj(pf, spp, dbh, hgt)
    #
    # hunnit(100000, Tree, pf, spp, dbh, hgt)
    # hunnit(100000, TimberQuick, pf, spp, dbh, hgt)

    y = TimberFull(pf, spp, dbh, hgt)
    print(f'{y.merch_dib=}')
    print(f'{y.merch_height=}')
    # for log_n in y.logs:
    #     print(f'{log_n}:')
    #     log = y.logs[log_n]
    #     for i in log.__dict__:
    #         print(f'\t{i}: {log.__dict__[i]}')
    #     print()