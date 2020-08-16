from processing import *
from readers import *
from post import *
from contextlib import redirect_stdout
from tempfile import mkdtemp
import uuid
from werkzeug.utils import secure_filename


class Session(object):
    def __init__(self):
        self.calendar = self.studies = self.classes = self.teachers = self.mat = self.curriculum = self.pairs = self.metric = None
        self.tmp = mkdtemp()
        self.id = str(uuid.uuid4())

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __hash__(self):
        return self.id.__hash__()

    def gen_name(self, filename=None):
        if filename is None:
            filename = str(uuid.uuid4())
        return self.tmp + '/' + secure_filename(filename)

    def load_presets(self):
        self.calendar = read_1()
        self.studies, self.classes, self.teachers = read_2()
        self.mat = read_5(year, self.teachers)

    def load_calendar(self, calendar_name):
        self.calendar = read_1(calendar_name)

    def load_source(self, source_name):
        self.calendar = read_6(source_name)

    def load_facilities(self, fac_name):
        self.studies, self.classes, self.teachers = read_2(fac_name)

    def load_mat(self, graph_name):
        self.mat = read_5(year, self.teachers, graph_name)

    def compute(self):
        pairs = gen_pairs(year, self.calendar, self.studies, self.classes, self.teachers, self.mat)
        pairs = divide_classes(pairs, self.studies, self.classes)
        self.pairs = divide_teachers(pairs, self.teachers)
        self.metric = metrics(pairs, self.calendar, self.classes, self.teachers)

    def export(self, out_name):
        save_file(self.pairs, out_name)

    def metrics(self, out_name):
        with open(out_name, 'w') as f, redirect_stdout(f):
            print_metric(self.metric)


class Sessions(object):
    def __init__(self):
        self.sessions = {}

    def new(self):
        session = Session()
        self.sessions[session.id] = session
        return session.id

    def has(self, other):
        return other in self.sessions

    def get(self, other):
        return self.sessions[other]
