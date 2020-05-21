import random
import pandas as pd
import datetime
import os


class Teachers:
    def __init__(self, csv_path):
        self.csv_path = csv_path

    def get_df(self):
        self.df = pd.read_csv(self.csv_path, index_col='Grade')
        return self.df

    def group_df(self):
        self.grouped_df = self.df.groupby('Grade')
        return self.grouped_df

    def get_grade(self):
        self.grades = self.grouped_df.groups.keys()
        return self.grades

    def grades_group(self):

        for grade in self.grades:
            self.grade_group = self.grouped_df.get_group(grade)
            Class_object = GradesClass(grade, self.grade_group)
            Class_object.run()

    def run(self):
        Teachers.get_df(self)
        Teachers.group_df(self)
        Teachers.get_grade(self)
        Teachers.grades_group(self)


class GradesClass(Teachers):
    busy_periods = {}

    def __init__(self, grade, grade_group):
        self.Week_Days = pd.read_csv('resources/Weekdays.csv', index_col='Days')
        self.grade_group = grade_group
        self.grade = grade
        self.teacher_subject_periods_list = [tuple(self.grade_group.iloc[index]) for index in range(len(grade_group))]

    def teachers_names_generator(self):
        for i in self.teacher_subject_periods_list:
            name = i[0]
            try:
                _ = GradesClass.busy_periods[name]
            except KeyError:
                GradesClass.busy_periods[name] = []

    def loop(self, period, teacher_name, subject, periods):
        while True:
            days = self.Week_Days.index
            periods = self.Week_Days.columns
            day = random.choice(days)
            period = random.choice(periods)
            busy_period = self.Week_Days.loc[day, period]
            if pd.isna(busy_period) and (day, period) not in GradesClass.busy_periods[teacher_name]:
                self.Week_Days.loc[day, period] = subject
                GradesClass.busy_periods[teacher_name].append((day, period))
                break
            else:
                continue

    def Week_Schedule(self):
        for teacher in self.teacher_subject_periods_list:
            teacher_name, subject, periods = teacher
            for period in range(periods):
                GradesClass.loop(self, period, teacher_name, subject, periods)

    def path_generator(self):
        if not os.path.exists(GradesClass.today()):
            os.mkdir(GradesClass.today())
        else:
            pass
        self.Week_Days.to_csv(f'{GradesClass.today()}/Grade {self.grade}.csv')

    @staticmethod
    def today():
        return datetime.datetime.today().strftime('%Y-%m-%d')

    def run(self):
        GradesClass.teachers_names_generator(self)
        GradesClass.Week_Schedule(self)
        GradesClass.path_generator(self)
