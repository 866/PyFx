import processing.mathalgs as mt

class template_processor:
    def __init__(self, _templates=None):
        self.templates = _templates

    def find_all_fragments(self, tf, beg_end):
        pass

    def generate_all_templates(self, beg_end, db=None, tf = None):
        """
        :param beg_end: a list with begin and end. They show the position relative to anchor point(can be negative)
        :param db: database
            OR
        :param tf: timeframe
        :return: all templates
        """
        if (db is None and tf is None) or (db is not None and tf is not None):
            return None
        lows, highs = []
        if db is not None:
            for tf in db.items():
                low, high = find_all_fragments(tf, beg_end)
                lows += low
                high += high
            else:
                source = find_all_fragments(tf, beg_end)
