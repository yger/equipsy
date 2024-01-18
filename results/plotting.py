import pylab as plt
import numpy as np

def _simpleaxis(ax):
    for spine in ['right', 'top']:
        ax.spines[spine].set_visible(False)


def display_variables(group_experiments, variables=None, show_stats=True, axes=None, output=None):

    if variables is None:
        variables = list(group_experiments.experiments[0].variables.keys())

    if len(variables) == 1:
        display_variable(group_experiments, variables[0], show_stats, output=output)
    else:
        ncols = 2
        nrows = len(variables) // ncols
        
        if axes is None:
            fig, axes = plt.subplots(nrows, ncols, figsize=(15, 10), squeeze=False)
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

    all_animals = group_experiments.all_animals
    all_dates = list(group_experiments.all_dates)
    
    res = {}
    for animal in group_experiments.all_animals:
        data = group_experiments.get_experiments_per_animals(animal)
        res[animal] = []
        for e in data.experiments:
            res[e.animal] += [e.stats[variable]]

    all_res = []
    
    for animal in res.keys():
        res[animal] = np.array(res[animal])
        all_res += [res[animal]]
        axes.plot(res[animal], label=animal)

    m = np.mean(all_res, 0)
    s = np.std(all_res, 0)
    axes.plot(m, lw=2, c='k')
    axes.fill_between(np.arange(len(m)), m-s, m+s, color='k', alpha=0.1)
    axes.set_ylabel(f'{variable}')
    axes.set_xticks(np.arange(len(all_dates)), all_dates, rotation=45)
    axes.legend()
    _simpleaxis(axes)
    if fig is not None:
        fig.tight_layout()
    if output is not None:
        plt.savefig(output)



def display_weights(group_experiments, show_stats=True, axes=None, output=None):
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
        to_display = experiment.variables_touchscreen
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
    fig, axes = plt.subplots(nrows, ncols, squeeze=False)

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
        to_display = experiment.variables_touchscreen
    data = []
    
    for key in to_display:
        data += [experiment.stats[key]]

    if stats is not None:
        shown_stats = [stats[i] for i in to_display]
    
    xaxis = np.arange(1, len(data)+1)
    axes.scatter(xaxis, data, c='k', s=20)
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
        fig, axes = plt.subplots(1)
    else:
        fig = None
    if to_display is None:
        to_display = group_experiments.experiments[0].variables_touchscreen
    axes.violinplot([group_experiments.stats[i] for i in to_display])
    xaxis = np.arange(len(to_display)) + 1
    axes.set_xticks(xaxis, to_display, rotation=45)
    axes.set_ylabel('# events')
    _simpleaxis(axes)
    if fig is not None:
        fig.tight_layout()
    if output is not None:
        plt.savefig(output)


