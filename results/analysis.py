import sys, subprocess, os
from io import StringIO
import pandas as pd
import numpy as np


variables_of_interest = {'Habituation' : ['Reward_First',
                                          'Screen_Centre',
                                          'Screen_First',
                                          'Screen_beam',
                                          'Screen_left',
                                          'Screen_right',
                                          'reward_beam',
                                          'reward_to_screen',
                                          'screen_to_reward'],
                         'Initial Touch' : ['Correct_Counter'],
                         'Must Initiate' : ['Correct_Counter'],
                         'Must Touch' : ['Correct_Counter', 'Blank_Touch_Counter'],
                         'Punish Incorrect' : ['Correct_Counter', 'Blank_Touch_Counter'],
                         'Theta 1' : ['Correct_Counter', 'Blank_Touch_Counter'],
                         'Theta 2' : ['Correct_Counter', 'Blank_Touch_Counter']
                        }


def download_database(target_file = 'equipsy.ABETdb'):

    import pysftp, os
    from pathlib import Path
    Hostname = "pr-pfcomporte.univ-lille.fr"
    Username = "pierre.yger"
    Password = "gFdp*DabQBVm5Pn"
    
    cnopts = pysftp.CnOpts(knownhosts=os.path.expanduser(os.path.join('~', '.ssh', 'known_hosts')))
    cnopts.hostkeys = None
    with pysftp.Connection(host=Hostname, username=Username, password=Password, cnopts=cnopts) as sftp:
        print("Connection successfully established ... ")
        remoteFilePath = Path('rat') / 'touchscreen'/ 'ABET System Folder'/ 'equipsy.ABETdb'
        localFilePath = Path(f'./{target_file}')
        # Use get method to download a file
        info = sftp.stat(str(remoteFilePath))
        if info.st_size != os.stat(str(localFilePath)).st_size:
            sftp.get(str(remoteFilePath), str(localFilePath))
            print("File successfully downloaded ...")
        else:
            print("File has not changed ...")

    

class GroupExperiments():

    def __init__(self, experiments):
        self.experiments = experiments

    @property
    def nb_experiments(self):
        return len(self.experiments)

    @property
    def all_animals(self):
        return sorted(set([e.animal for e in self.experiments]))

    @property
    def all_types(self):
        return sorted(set([e.type for e in self.experiments]))

    @property
    def all_dates(self):
        from datetime import datetime, date
        lst = [e.date.strftime('%d/%m/%y') for e in self.experiments]
        lst.sort(key=lambda x: datetime.strptime(x, '%d/%m/%y'))
        res = []
        for i in lst:
            if i not in res:
                res +=[i]
        return res
    
    @property
    def stats(self):
        res = {}
        for e in self.experiments:
            for key, value in e.stats.items():
                if not key in res:            
                    res[key] = [value]
                else:
                    res[key] += [value]

        for key in res.keys():
            res[key] = np.array(res[key])
        return res

    def get_experiments_per_dates(self, dates, sorted=True):
        experiments = []
        if not np.iterable(dates):
            animals = [dates]
        
        for e in self.experiments:
            if e.date.strftime('%d/%m/%y') in dates:
                experiments += [e]
        if sorted:
            sorted_experiments = []
            idx = np.argsort([e.animal for e in experiments])
            for i in idx:
                sorted_experiments += [experiments[i]]
            return GroupExperiments(sorted_experiments)
        else:
            return GroupExperiments(experiments)
    
    def get_experiments_per_animals(self, animals, sorted=True):
        experiments = []
        if not np.iterable(animals):
            animals = [animals]
        
        for e in self.experiments:
            if e.animal in animals:           
                experiments += [e]
                
        if sorted:
            sorted_experiments = []
            idx = np.argsort([e.date for e in experiments])
            for i in idx:
                sorted_experiments += [experiments[i]]
            return GroupExperiments(sorted_experiments)
        else:
            return GroupExperiments(experiments)
        return GroupExperiments(experiments)

    def get_experiments_per_types(self, types, sorted=True):
        experiments = []
        if not np.iterable(types):
            animals = [types]
        for e in self.experiments:
            if e.type in types:
                experiments += [e]
        if sorted:
            sorted_experiments = []
            idx = np.argsort([e.date for e in experiments])
            for i in idx:
                sorted_experiments += [experiments[i]]
            return GroupExperiments(sorted_experiments)
        else:
            return GroupExperiments(experiments)
        return GroupExperiments(experiments)


# class SingleTrial():

#     def __init__(self, database):
#         self.data = database

class SingleExperiment():
    
    def __init__(self, sid, database):
        self.sid = sid
        df = database['tbl_Schedules']
        self.date = df.loc[df['SID'] == self.sid, 'SRunDate'].values[0]
        import datetime
        self.date = datetime.datetime.strptime(self.date, '%m/%d/%y %H:%M:%S')
        self.chamber = df.loc[df['SID'] == self.sid, 'SEnviro'].values[0]

        experiment_type = df.loc[df['SID'] == self.sid, 'SName'].values[0]        
        if experiment_type.find('Habituation') > -1:
            experiment_type = 'Habituation'
        elif experiment_type.find('Initial Touch') > -1:
            experiment_type = 'Initial Touch'
        elif experiment_type.find('Must Touch') > -1:
            experiment_type = 'Must Touch'
        elif experiment_type.find('Must Initiate') > -1:
            experiment_type = 'Must Initiate'
        elif experiment_type.find('Punish Incorrect') > -1:
            experiment_type = 'Punish Incorrect'
        elif experiment_type.find('Theta 1 fixed') > -1:
            experiment_type = 'Theta 1'
        elif experiment_type.find('Theta 2 fixed') > -1:
            experiment_type = 'Theta 2'

        self.type = experiment_type
        df = database['tbl_Schedule_Notes']
        self.animal = df.loc[(df['SID'] == self.sid) & (df['NName'] == 'Animal ID'), 'NValue'].values[0]

        if self.sid == 309:
            self.animal = 'E1'

        df = database['tbl_Data']
        self.data = df[df['SID'] == self.sid]
        try:
            self.duration = self.data['DTime'].values[-1]
        except Exception:
            print(self.chamber, self.animal)
            self.duration = 0
        self.inputs = {}
        self.variables = {}

        self.variables_touchscreen = variables_of_interest[self.type]
        
        for key in self.variables_touchscreen:
            self.variables[key] = self._get_variable_data(key)
    
    def _get_variable_data(self, name):
        df = self.data
        on_data = df[(df['DEventText'] == 'Variable Event') & (df['DEffectText'] == name)] 
        return on_data['DTime'].values
    
    @property
    def stats(self):
        res = {}
        for key in self.variables:
            res[key] = len(self.variables[key])
        if 'Correct_Counter' in self.variables and 'Blank_Touch_Counter' in self.variables:
            res['Correct_Percentage'] = 100*res['Correct_Counter'] / (res['Correct_Counter'] + res['Blank_Touch_Counter'])
        return res

    @property
    def nb_trials(self):
        du = self.data.loc[self.data['DEffectText'] == '_Trial_Counter', ['DTime', 'DValue1']]
        return len(du) - 1
    
    def get_trial(self, target_trial):
        assert target_trial < self.nb_trials
        du = self.data.loc[self.data['DEffectText'] == '_Trial_Counter', ['DTime', 'DValue1']]
        nb_trials = len(du) - 1
        trial_start = du.loc[du['DValue1'] == target_trial, 'DTime'].values[0]
        trial_stop = du.loc[du['DValue1'] == target_trial + 1, 'DTime'].values[0]
        du = self.data[(self.data['DTime'] >= trial_start) & (self.data['DTime'] < trial_stop)]
        return du

    def get_reaction_times(self, trials=None):
        res = []
        
        if trials is None:
            trials = range(self.nb_trials)
            
        for trial in trials:
            try:
                df = self.get_trial(trial)
                t_start = df[(df['DEventText'] == 'Group Change Event') & (df['DGroup'] == 5)]['DTime'].values[0]
                t_stop = df[(df['DEventText'] == 'Clear Image by Position') & (df['DGroup'] == 6)]['DTime'].values[0]
                res += [t_stop - t_start]
            except Exception:
                pass
                #print(f'{trial} can not be properly parsed')
        return np.array(res)

    def get_angular_differences(self, trials=None):
        res = []

        if self.type == 'Theta 1':
            ref = 45
            mapping = {1:0, 2:22.5, 3:67.5, 4:90, 5:112.5, 6:135, 7:157.5}
        elif self.type == 'Theta 2':
            ref = 135
            mapping = {1:0, 2:22.5, 3:45, 4:67.5, 5:90, 6:112.5, 7:157.5}
        
        if trials is None:
            trials = range(self.nb_trials)
            
        for trial in trials:
            try:
                df = self.get_trial(trial)
                image = df[(df['DEventText'] == 'Variable Event') & (df['DEffectText'] == 'Incorrect_Image')]['DValue1'].values[0]
                res += [np.abs(mapping[image] - ref)]
            except Exception:
                pass
                #print(f'{trial} can not be properly parsed')
        return np.array(res)

    def get_responses(self, trials=None):
        res = []
        
        if trials is None:
            trials = range(self.nb_trials)
            
        for trial in trials:
            try:
                df = self.get_trial(trial)
                correct_position = df[(df['DEventText'] == 'Variable Event') & (df['DEffectText'] == 'Correct_Grid_Position')]['DValue1'].values[0]
                image = df[(df['DText1'] == 'Position') & (df['DGroup'] == 6) & (df['DValue2'] != -1)]['DValue1'].values[0]    
                res += [image == correct_position]
            except Exception:
                pass
                #print(f'{trial} can not be properly parsed')
        return np.array(res)

class DataBase():
    
    def __init__(self, database_path, verbose=False):

        self.database_path = database_path
        subprocess.call(["mdb-schema", database_path, "mysql"])
        # Get the list of table names with "mdb-tables"
        table_names = subprocess.Popen(["mdb-tables", "-1", database_path],
                                           stdout=subprocess.PIPE).communicate()[0]
        tables = table_names.splitlines()
        sys.stdout.flush()
        # Dump each table as a stringio using "mdb-export",
        out_tables = {}
        for rtable in tables:
            try:
                table = rtable.decode()
                if verbose: print('running table:',table)
                if table != '':
                    if verbose: print("Dumping " + table)
                    contents = subprocess.Popen(["mdb-export", database_path, table],
                                                stdout=subprocess.PIPE).communicate()[0]
                    sys.stdout.flush()
                    temp_io = StringIO(contents.decode())
                    out_tables[table] = pd.read_csv(temp_io, low_memory=False)
            except Exception:
                pass
        self.data = out_tables
        
    def get_group_experiments(self):
        self.database_path = self.database_path
        all_sid = self.data['tbl_Schedules']['SID'].values
        
        self.experiments = []
        for sid in all_sid:
            if sid not in [33]:
                self.experiments += [SingleExperiment(sid, self.data)]
            if sid == [34]:
                self.experiments[-1].animal = 'G1'
        try:
            self._get_weights_from_google_drive()
        except Exception:
            pass
        return GroupExperiments(self.experiments)

    def _get_weights_from_google_drive(self, sheet_id = "1i3MCAurk3bOyVAwBfm3RZ4-Qxb2mTa18bwoezFktiG4",
                                       sheet_name = "Poids"):
        import pandas as pd        
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        df = pd.read_csv(url)
        for e in self.experiments:
            target_date = e.date.strftime('%d/%m')
            target_animal = e.animal
            data = df.loc[df['# RAT'] == target_animal, target_date].values[0]
            data = float(data)
            e.weight = data
