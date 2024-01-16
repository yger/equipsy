import sys, subprocess, os
from io import StringIO
import pandas as pd

def download_data(target_file = 'equipsy.ABETdb'):

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

    def all_animals(self):
        data = self.data['tbl_Schedule_Notes']
        animals = data[data['NName'] == 'Animal ID']
        return animals['NValue'].values

    def get_sid_per_animal(self, animal='A1'):
        data = self.data['tbl_Schedule_Notes']
        animals = data[data['NName'] == 'Animal ID']
        return animals[animals['NValue'] == animal]['SID'].values

    def get_experiment(data, SID):
        return data[data['SID'] == SID]

    def get_input_data(data, name='BIRBeam #1'):
        on_data = self.data[self.data['DEventText'] == 'Input Transition On Event']
        on_data = on_data[on_data['DEffectText'] == name]    
        return on_data['DTime'].values