from analysis import download_database
from plotting import *
from analysis import DataBase
from pathlib import Path

#download_database()
data = DataBase('equipsy.ABETdb')
all_experiments = data.get_group_experiments()

figures_path = Path('figures')
figures_path.mkdir(exist_ok=True)

filename = figures_path / "weights.png"
display_weights(all_experiments, output=filename)

for date in all_experiments.all_dates:
    mydate = date.replace('/', '_')
    group_experiments = all_experiments.get_experiments_per_date(date)
    filename = figures_path / "time_courses"
    filename.mkdir(exist_ok=True)

    filename = filename / f"{mydate}.png"
    display_group_experiments_over_time(group_experiments, output=filename)

    filename = figures_path / "individuals"
    filename.mkdir(exist_ok=True)
    filename = filename / f"{mydate}.png"
    display_group_experiments(group_experiments, output=filename)

    filename = figures_path / "stats"
    filename.mkdir(exist_ok=True)
    filename = filename / f"{mydate}.png"
    display_stats_group_experiments(group_experiments, output=filename)