import sys, subprocess, os
from io import StringIO
import pandas as pd

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
        sftp.get(str(remoteFilePath), str(localFilePath))
        print("File successfully downloaded ...")


def display_experiment(experiment):
    pass


class Experiment():

    mapping = {'BIRBeam #1' : 'BBeam', 
               'FIRBeam #1' : 'FBeam',
               'Screen_Centre': 'screen center', 
               'Screen_beam' : 'screen beam',  
               'Screen_left' : 'screen left', 
               'Screen_right' : 'screen right' }
    
    def __init__(self, sid, database):
        self.sid = sid
        df = database['tbl_Schedules']
        self.date = df.loc[df['SID'] == self.sid, 'SRunDate'].values[0]
        import datetime
        self.date = datetime.datetime.strptime(self.date, '%m/%d/%y %H:%M:%S')
        self.chamber = df.loc[df['SID'] == 1, 'SEnviro'].values[0]
        df = database['tbl_Schedule_Notes']
        self.animal = df.loc[(df['SID'] == self.sid) & (df['NName'] == 'Animal ID'), 'NValue'].values[0]
        df = database['tbl_Data']
        self.data = df[df['SID'] == self.sid]
        self.duration = self.data['DTime'].values[-1]
        self.inputs = {}
        
        for key, value in self.mapping.items():
            self.inputs[value] = self._get_input_data(key)
    
    def _get_input_data(self, name):
        df = self.data
        on_data = df[(df['DEventText'] == 'Input Transition On Event') & (df['DEffectText'] == name)]   
        return on_data['DTime'].values


class DataBase():
    
    def __init__(self, database_path, verbose=False):
            
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
                    temp_io = StringIO(contents.decode())
                    print(table, temp_io)
                    out_tables[table] = pd.read_csv(temp_io)
            except Exception:
                pass
        self.data = out_tables
        self.database_path = database_path
        self.experiments = self._extract_all_experiments()
    
    def _extract_all_experiments(self):
        #extract_experiments(data):
        all_sid = self.data['tbl_Schedules']['SID'].values
        experiments = []
        for sid in all_sid:
            experiments += [Experiment(sid, self.data)]
        return experiments

    @property
    def nb_experiements(self):
        return len(self.experiments)
    
    @property
    def all_animals(self):
        return set([e.animal for e in self.experiments])

    # def get_sid_per_animal(self, animal='A1'):
    #     data = self.data['tbl_Schedule_Notes']
    #     animals = data[data['NName'] == 'Animal ID']
    #     return animals[animals['NValue'] == animal]['SID'].values

    # def get_experiment(data, SID):
    #     return data[data['SID'] == SID]

    # def get_input_data(data, name='BIRBeam #1'):
    #     on_data = self.data[self.data['DEventText'] == 'Input Transition On Event']
    #     on_data = on_data[on_data['DEffectText'] == name]    
    #     return on_data['DTime'].values