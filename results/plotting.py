import pylab as plt
import numpy as np

def _simpleaxis(ax):
    for spine in ['right', 'top']:
        ax.spines[spine].set_visible(False)

def view_group_experiment(experiments, nrows=4):
    ncols = len(experiments) // 4
    fig, axes = plt.subplots(nrows, ncols, squeeze=False)
    for count, e in enumerate(experiments):
        i, j = np.unravel_index(count, (nrows, ncols))
        ax = axes[i, j]
        display_experiment(e, ax)
        ax.set_title(f'{e.animal}')
        _simpleaxis(ax)
        if (i < nrows - 1):
            ax.set_xticks([], [])
            ax.set_xlabel('')
        else:
            ax.set_xlabel('Time (s)')
        if (j < ncols - 1):
            ax.set_yticks([], [])
            ax.set_ylabel('')
        if j== 0:
            ax.set_ylabel('Activation')
    fig.tight_layout()


def display_group_experiments_over_time(group_experiments, nrows=4, to_display=None):
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

def display_experiment_over_time(experiment, axes=None, to_display=None):
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

def display_group_experiments(group_experiments, nrows=4, to_display=None):
    ncols = group_experiments.nb_experiments // 4
    fig, axes = plt.subplots(nrows, ncols, squeeze=False)
    for count, e in enumerate(group_experiments.experiments):
        i, j = np.unravel_index(count, (nrows, ncols))
        ax = axes[i, j]
        _simpleaxis(ax)
        display_experiment(e, ax, to_display)
        ax.set_title(f'{e.animal}')
        if (i < nrows - 1):
            ax.set_xticks([], [])
            ax.set_xlabel('')
        if (j > 0):
            #ax.set_yticks([], [])
            ax.set_ylabel('')
    fig.tight_layout()

def display_experiment(experiment, axes=None, to_display=None):
    if axes is None:
        fig, axes = plt.subplots(1)
    else:
        fig = None
    if to_display is None:
        to_display = experiment.variables_touchscreen
    data = []
    
    for key in to_display:
        data += [experiment.stats[key]]
    xaxis = np.arange(len(data))
    axes.bar(xaxis, data)
    axes.set_xticks(xaxis, to_display, rotation=45)
    axes.set_ylabel('# events')
    _simpleaxis(axes)
    if fig is not None:
        fig.tight_layout()

def display_stats_group_experiment(group_experiment, axes=None, to_display=None):
    if axes is None:
        fig, axes = plt.subplots(1)
    else:
        fig = None
    if to_display is None:
        to_display = group_experiment.experiments[0].variables_touchscreen
    axes.violinplot([group_experiment.stats[i] for i in to_display])
    xaxis = np.arange(len(to_display)) + 1
    axes.set_xticks(xaxis, to_display, rotation=45)
    axes.set_ylabel('# events')
    _simpleaxis(axes)
    if fig is not None:
        fig.tight_layout()

