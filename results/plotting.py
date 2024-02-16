import pylab as plt
import numpy as np
import matplotlib

def _simpleaxis(ax):
    for spine in ['right', 'top']:
        ax.spines[spine].set_visible(False)


def display_variables(group_experiments, variables=None, show_stats=True, axes=None, output=None):

    if variables is None:
        variables = list(group_experiments.experiments[0].stats.keys())

    if len(variables) == 1:
        display_variable(group_experiments, variables[0], show_stats, output=output)
    else:
        ncols = 3
        nrows = len(variables) // ncols
        
        if axes is None:
            fig, axes = plt.subplots(nrows, ncols, figsize=(15, 5), squeeze=False)
        else:
            fig = None
    
        count = 0
        for i in range(nrows):
            for j in range(ncols):
                display_variable(group_experiments, variables[count], show_stats, axes=axes[i,j])
                count += 1
                axes[i,j].get_legend().remove()
    
        if fig is not None:
            fig.tight_layout()
        if output is not None:
            plt.savefig(output)


def display_variable(group_experiments, variable, show_stats=True, axes=None, output=None):
    if axes is None:
        fig, axes = plt.subplots(1)
    else:
        fig = None

    my_cmap = plt.cm.get_cmap('tab20')
    
    all_animals = group_experiments.all_animals
    all_dates = list(group_experiments.all_dates)

    cNorm = matplotlib.colors.Normalize(vmin=0, vmax=20)
    scalarMap = plt.cm.ScalarMappable(norm=cNorm, cmap=my_cmap)

    res = {}
    for animal in group_experiments.all_animals:
        data = group_experiments.get_experiments_per_animals(animal)
        res[animal] = []
        for e in data.experiments:
            res[e.animal] += [e.stats[variable]]

    all_res = []
    
    for count, animal in enumerate(res.keys()):
        res[animal] = np.array(res[animal])
        all_res += [res[animal]]
        colorVal = scalarMap.to_rgba(count)
        axes.plot(res[animal], label=animal, c=colorVal)

    m = np.mean(all_res, 0)
    s = np.std(all_res, 0)
    axes.plot(m, lw=2, c='k')
    axes.fill_between(np.arange(len(m)), m-s, m+s, color='k', alpha=0.1)
    axes.set_ylabel(f'{variable}')
    axes.set_xticks(np.arange(len(all_dates)), all_dates, rotation=45)
    axes.legend()
    if variable == 'Correct_Percentage':
        axes.plot(np.arange(len(m)), 50*np.ones(len(m)), 'k--')
        axes.set_ylim(0, 100)
    _simpleaxis(axes)
    if fig is not None:
        fig.tight_layout()
    if output is not None:
        plt.savefig(output)



def display_weights(group_experiments, show_stats=True, axes=None, output=None):
    if axes is None:
        fig, axes = plt.subplots(1, figsize=(15, 5))
    else:
        fig = None

    my_cmap = plt.cm.get_cmap('tab20')
    all_animals = group_experiments.all_animals
    all_dates = list(group_experiments.all_dates)
    cNorm = matplotlib.colors.Normalize(vmin=0, vmax=20)
    scalarMap = plt.cm.ScalarMappable(norm=cNorm, cmap=my_cmap)
    
    res = {}
    for animal in group_experiments.all_animals:
        data = group_experiments.get_experiments_per_animals(animal)
        res[animal] = []
        for e in data.experiments:
            res[e.animal] += [e.weight]

    all_res = []
    
    for count, animal in enumerate(res.keys()):
        res[animal] = np.array(res[animal])
        all_res += [res[animal]]
        colorVal = scalarMap.to_rgba(count)
        axes.plot(res[animal], label=animal, c=colorVal)

    m = np.mean(all_res, 0)
    s = np.std(all_res, 0)
    axes.plot(m, lw=2, c='k')
    axes.fill_between(np.arange(len(m)), m-s, m+s, color='k', alpha=0.1)
    axes.set_ylabel('Weight (g)')
    axes.set_xticks(np.arange(len(all_dates)), all_dates, rotation=45)
    axes.legend()
    _simpleaxis(axes)
    if fig is not None:
        fig.tight_layout()
    if output is not None:
        plt.savefig(output)


def display_stats(group_experiments, show_stats=True, axes=None, output=None):
    if axes is None:
        fig, axes = plt.subplots(1)
    else:
        fig = None

    all_animals = group_experiments.all_animals
    all_dates = list(group_experiments.all_dates)
    
    res = {}
    for animal in group_experiments.all_animals:
        data = group_experiments.get_experiments_per_animals(animal)
        res[animal] = []
        for e in data.experiments:
            res[e.animal] += [e.weight]

    all_res = []
    
    for animal in res.keys():
        res[animal] = np.array(res[animal])
        all_res += [res[animal]]
        axes.plot(res[animal], label=animal)

    m = np.mean(all_res, 0)
    s = np.std(all_res, 0)
    axes.plot(m, lw=2, c='k')
    axes.fill_between(np.arange(len(m)), m-s, m+s, color='k', alpha=0.1)
    axes.set_ylabel('Weight (g)')
    axes.set_xticks(np.arange(len(all_dates)), all_dates, rotation=45)
    axes.legend()
    _simpleaxis(axes)
    if fig is not None:
        fig.tight_layout()
    if output is not None:
        plt.savefig(output)


def display_group_experiments_over_time(group_experiments, nrows=4, to_display=None, output=None):
    ncols = group_experiments.nb_experiments // 4
    fig, axes = plt.subplots(nrows, ncols, squeeze=False)
    for count, e in enumerate(group_experiments.experiments):
        i, j = np.unravel_index(count, (nrows, ncols))
        ax = axes[i, j]
        display_experiment_over_time(e, ax, to_display)
        if count < group_experiments.nb_experiments - 1:
            ax.get_legend().remove()
        ax.set_title(f'{e.animal}')
        _simpleaxis(ax)
        if (i < nrows - 1):
            ax.set_xticks([], [])
            ax.set_xlabel('')
        if (j > 0):
            #ax.set_yticks([], [])
            ax.set_ylabel('')
    fig.tight_layout()
    if output is not None:
        plt.savefig(output)


def display_experiment_over_time(experiment, axes=None, to_display=None, output=None):
    if axes is None:
        fig, axes = plt.subplots(1)
    else:
        fig = None
    if to_display is None:
        to_display = experiment.stats.keys()
    for count, key in enumerate(to_display):
        data = experiment.variables[key]
        axes.plot(data, np.zeros(len(data)), c=f'C{count}', marker='|', mew=1,
                    markersize=10, ls="", label=key)

    axes.legend()
    axes.set_xlabel('Time (s)')
    axes.set_ylabel('Activation')
    axes.set_yticks([], [])
    _simpleaxis(axes)
    if fig is not None:
        fig.tight_layout()
    if output is not None:
        plt.savefig(output)


def display_group_experiments(group_experiments, nrows=4, to_display=None, show_stats=True, output=None):
    ncols = group_experiments.nb_experiments // 4
    fig, axes = plt.subplots(nrows, ncols, squeeze=False, figsize=(10, 10))

    if show_stats:
        stats = group_experiments.stats
    else:
        stats = None
    
    for count, e in enumerate(group_experiments.experiments):
        i, j = np.unravel_index(count, (nrows, ncols))
        ax = axes[i, j]
        _simpleaxis(ax)
        display_experiment(e, ax, to_display, stats=stats)
        ax.set_title(f'{e.animal}')
        if (i < nrows - 1):
            ax.set_xticks([], [])
            ax.set_xlabel('')
        if (j > 0):
            #ax.set_yticks([], [])
            ax.set_ylabel('')
    fig.tight_layout()
    if output is not None:
        plt.savefig(output)


def display_experiment(experiment, axes=None, to_display=None, stats=None, output=None):
    if axes is None:
        fig, axes = plt.subplots(1)
    else:
        fig = None
    if to_display is None:
        to_display = experiment.stats.keys()
    data = []
    
    for key in to_display:
        data += [experiment.stats[key]]

    if stats is not None:
        shown_stats = [stats[i] for i in to_display]

    z_score = (np.abs(data - np.mean(shown_stats, 1)))/np.std(shown_stats, 1)
    xaxis = np.arange(1, len(data)+1)
    data = np.array(data)
    z_limit = 2
    idx = np.where(z_score > z_limit)        
    axes.scatter(xaxis[idx], data[idx], c='r', s=20)
    idx = np.where(z_score <= z_limit)
    axes.scatter(xaxis[idx], data[idx], c='k', s=20)
    axes.set_xticks(xaxis, to_display, rotation=45)
    axes.set_ylabel('# events')
    if stats is not None:
        violin_parts = axes.violinplot(shown_stats, showmedians=True)
        # Make the violin body blue with a red border:
        for partname in ('cbars','cmins','cmaxes','cmedians'):
            vp = violin_parts[partname]
            vp.set_edgecolor('k')
            vp.set_linewidth(0.5)
        for vp in violin_parts['bodies']:
            vp.set_facecolor('0.5')
            vp.set_linewidth(0.5)
            vp.set_alpha(0.5)
    _simpleaxis(axes)
    if fig is not None:
        fig.tight_layout()
    if output is not None:
        plt.savefig(output)

def display_stats_group_experiments(group_experiments, axes=None, to_display=None, output=None):
    if axes is None:
        fig, axes = plt.subplots(1, figsize=(15, 5))
    else:
        fig = None
    if to_display is None:
        to_display = group_experiments.experiments[0].stats.keys()

    axes.violinplot([group_experiments.stats[i] for i in to_display], showmeans=True)
    xaxis = np.arange(len(to_display)) + 1
    axes.set_xticks(xaxis, to_display, rotation=45)
    axes.set_ylabel('# events')
    _simpleaxis(axes)
    if fig is not None:
        fig.tight_layout()
    if output is not None:
        plt.savefig(output)

def plot_correlations(group_experiments):
    mean_responses = {'time' : [], 'angle' : []}
    corrcoeffs = {'time' : [], 'angle' : []}
    all_perfs = []
    all_types = []
    for type in ['Theta 1', 'Theta 2']:
        a = group_experiments.get_experiments_per_types(type)
        for e in a.experiments:
            tmp_reaction = e.get_reaction_times()
            tmp_angles = e.get_angular_differences()
            tmp_responses = e.get_responses()
            corrcoeffs['time'] += [np.corrcoef(tmp_reaction, tmp_responses)[0, 1]]
            mean_responses['time'] += [tmp_reaction.mean()]
            if len(tmp_angles)!= len(tmp_responses):
                tmp_angles = tmp_angles[:-1]
            corrcoeffs['angle'] += [np.corrcoef(tmp_angles, tmp_responses)[0, 1]]
            mean_responses['angle'] += [tmp_angles.mean()]
            all_perfs += [e.stats['Correct_Percentage']]
            if e.type == 'Theta 1':
                all_types += [1]
            else:
                all_types += [2]

    all_types = np.array(all_types)

    for key in ['time', 'angle']:
        mean_responses[key] = np.nan_to_num(mean_responses[key])
        corrcoeffs[key] = np.nan_to_num(corrcoeffs[key])
            
    fix, axes = plt.subplots(ncols=2, nrows=2, figsize=(15, 5))
    
    experiment = group_experiments.get_experiments_per_types('Theta 1').experiments[1]
    tmp_responses = e.get_responses()
    tmp_reaction = np.nan_to_num(experiment.get_reaction_times())
    tmp_angles = e.get_angular_differences()
    
    axes[0, 0].set_ylabel('reaction time (s)')   
    axes[0, 0].set_xlabel('# Trial')

    axes[0, 0].plot(tmp_reaction)
    ax2 = axes[0, 0].twinx() 
    ax2.plot(tmp_responses, c='0.8')
    bins =np.linspace(corrcoeffs['time'].min(), corrcoeffs['time'].max(), 20)
    axes[0, 1].hist(corrcoeffs['time'][all_types == 1], bins, label='Theta 1', alpha=0.25)
    axes[0, 1].hist(corrcoeffs['time'][all_types == 2], bins, label='Theta 2', alpha=0.25)
    axes[0, 1].hist(corrcoeffs['time'], bins, label='All', alpha=0.25)
    axes[0, 1].set_xlabel('corrcoeff')
    axes[0, 1].set_ylabel('# Sessions')
    axes[0, 1].legend()
    
    if len(tmp_angles)!= len(tmp_responses):
        tmp_angles = tmp_angles[:-1]
    
    axes[1, 0].set_ylabel('angular difference (°)')
    axes[1, 0].set_xlabel('# Trial')
    axes[1, 0].plot(tmp_angles)
    ax2 = axes[1, 0].twinx() 
    ax2.plot(tmp_responses, c='0.8')
    bins =np.linspace(corrcoeffs['angle'].min(), corrcoeffs['angle'].max(), 20)
    axes[1, 1].hist(corrcoeffs['angle'][all_types == 1], bins, label='Theta 1', alpha=0.25)
    axes[1, 1].hist(corrcoeffs['angle'][all_types == 2], bins, label='Theta 2', alpha=0.25)
    axes[1, 1].hist(corrcoeffs['angle'], bins, label='All', alpha=0.25)
    axes[1, 1].set_xlabel('corrcoeff')
    axes[1, 1].set_ylabel('# Sessions')
    axes[1, 1].legend()
    

def plot_nb_trials_vs_performances(group_experiments):
    nb_trials = {}
    stats = {}
    all_types = []
    fig, axes = plt.subplots(ncols=3, figsize=(15,5))
    for type in ['Theta 1', 'Theta 2']:
        a = group_experiments.get_experiments_per_types(type)
        for e in a.experiments:
            if e.animal in nb_trials:
                nb_trials[e.animal] += [e.nb_trials]
                stats[e.animal] += [e.stats['Correct_Percentage']]
            else:
                nb_trials[e.animal] = [e.nb_trials]
                stats[e.animal] = [e.stats['Correct_Percentage']]
        if e.type == 'Theta 1':
            all_types += [1]
        else:
            all_types += [2]

    for animal in nb_trials.keys():
        nb_trials[animal] = np.array(nb_trials[animal])
        stats[animal] = np.array(stats[animal])
        
    n = group_experiments.get_experiments_per_types('Theta 1').nb_experiments // 16
    
    all_types = np.array(all_types)

    for count in range(3):

        if count == 0:
            total_nb_trials = np.array([np.sum(i[:n]) for i in nb_trials.values()])
            mean_perfs = np.array([np.mean(i[:n]) for i in stats.values()])
        elif count == 1:
            total_nb_trials = np.array([np.sum(i[n:]) for i in nb_trials.values()])
            mean_perfs = np.array([np.mean(i[n:]) for i in stats.values()])
        elif count == 2:
            total_nb_trials = np.array([np.sum(i) for i in nb_trials.values()])
            mean_perfs = np.array([np.mean(i) for i in stats.values()])
        
        axes[count].plot(total_nb_trials, mean_perfs, '.')
        axes[count].plot([min(total_nb_trials), max(total_nb_trials)], [50, 50], 'k--')
        import scipy
        slope, intercept, r, p, se = scipy.stats.linregress(total_nb_trials, mean_perfs)
        axes[count].plot(total_nb_trials, intercept + slope*total_nb_trials, f'C{1}', label='fitted line')
        axes[count].set_xlabel('# trials')
        axes[count].set_ylabel('#Average performance')
    
                