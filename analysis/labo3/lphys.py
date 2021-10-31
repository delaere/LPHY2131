import uproot
import awkward as ak
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import mplhep as hep
import scipy
import iminuit
import probfit

# This file contains a set of helper functions used in the various Notebooks.


def analyzeTree(tree, branch, simpleselection=None, selection=None, index=None, step_size="10 MB"):
    selected = ak.Array([])
    for batch in tree.iterate(step_size=step_size):
        if simpleselection:
            batchsel = batch[simpleselection(batch)][branch]
        elif selection:
            batchsel = selection(batch,branch)
        else:
            batchsel = batch[branch]
        if index: # if there is an index, we select that column
            batchsel = batchsel[:,index]
        elif (type(branch) is str): # otherwise, we flatten the selection
            batchsel = ak.flatten(batchsel, axis=None)
        else: # unless branch is a list, in which case we do nothing.
            pass
        selected = ak.concatenate([selected,batchsel])
    return selected

# Two classes are introduced to describe respectively the binned samples and the parametric curves for the plot function.

# The sample class is a simple helper built from events (Numpy array) and display options
class sample:
    def __init__(self,events, label, color='g', norm=None, integral=None):
        self.events = events
        self.label = label
        self.color = color
        self.norm = norm if norm else 1.
        if integral:
            self.norm = integral/len(events)

# The curve class is a simple helper built from a function and display options.
class curve:
    def __init__(self,func, label, color='g', linewidth=4):
        self.func = func
        self.label = label
        self.color = color
        self.linewidth = linewidth

# this function allows to plot two simple histograms side by side, for simulation and data
def sidePlot(data, simu, xlim, xlabel, ylabel='Probability', nbins=100, islog=True, color='g', density=True):
    fig, axs = plt.subplots(1, 2, figsize=(10, 5), sharey=True)
    axs[0].hist(data, nbins, range=xlim, density=density, facecolor=color, alpha=0.75);
    axs[0].set_xlabel(xlabel)
    axs[0].set_ylabel(ylabel)
    axs[0].set_xlim(*xlim)
    if islog: axs[0].set_yscale('log')
    textxpos = xlim[0] + (xlim[1]-xlim[0])/5
    textypos = axs[0].get_ylim()[1]/10. if islog else axs[0].get_ylim()[1]*0.8
    axs[0].text(textxpos, textypos, r'data')
    axs[0].grid(True)
    axs[1].hist(simu, nbins, range=xlim, density=density, facecolor=color, alpha=0.75);
    axs[1].set_xlabel(xlabel)
    axs[1].set_xlim(*xlim)
    axs[1].text(textxpos, textypos, r'MC')
    axs[1].grid(True)

# this function allows to plot simulations (one or several), data, and parametric curves.
# the default mode is to use the helper classes for samples and curves.
# In the special case where only one sample is needed, options can be passed directly as arguments.
def plot(data, simu, curves, xlim, xlabel, ylabel='Probability', nbins=100, islog=True, color='g', density=True):
    fig, ax = plt.subplots(figsize=(10, 10))
    hep.set_style(hep.style.CMS)
    hep.cms.text("Open Data")
    ax.set_xlim(*xlim)
    bin_width = (xlim[1]-xlim[0])/nbins
    bin_edges = np.arange(xlim[0],xlim[1]+bin_width,bin_width)
    bin_centers = (bin_edges+bin_width/2)[:-1]
   
    if type(simu) is ak.highlevel.Array:
        ax.hist(simu, nbins, density=density, facecolor=color, alpha=0.75, label='MC'); # simulation
    else:
        assert(type(simu) is list)
        if len(simu)>0:
            samples = [ s.events for s in simu ]
            label = [ s.label for s in simu ]
            norm = [ [s.norm]*len(s.events) for s in simu ]
            color = [ s.color for s in simu ]
            ax.hist(samples, bin_edges, density=density, alpha=0.75, stacked=True, color=color, label=label,weights = norm)

    data_x,_ = np.histogram(ak.to_numpy(data), bins=bin_edges, density=density ) # histogram the data
    plt.errorbar(x=bin_centers, y=data_x, yerr=np.sqrt(data_x*len(data))/len(data),
                 fmt='ko', # 'k' means black and 'o' is for circles 
                 label='Data')
    
    x = np.arange(xlim[0],xlim[1],(xlim[1]-xlim[0])/(nbins*10))
    for curve in curves:
        plt.plot(x,np.array([curve.func(xi) for xi in x]), label=curve.label, color=curve.color, lw=curve.linewidth)
    
    if islog: ax.set_yscale('log')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend();
    
# build an histogram of a function
def histogram(model,bin_centers, norm=True):
    values = np.array([ model(x) for x in bin_centers ])
    if norm: 
        tot = np.sum(values)
        values = values / tot
    return values

# draw random numbers from an arbitrary function, given a set of bin centers.
def randomValues(model,bin_centers,size):
    hist = histogram(model,bin_centers)
    cdf = np.cumsum(hist)
    cdf = cdf / cdf[-1]
    values = np.random.rand(size)
    value_bins = np.searchsorted(cdf, values)
    random_from_cdf = bin_centers[value_bins]
    return random_from_cdf

# draw random numbers from a function for a given binning (xlim, nbins).
def randomSample(model,xlim,nbins,size):
    bin_width = (xlim[1]-xlim[0])/nbins
    bin_edges = np.arange(xlim[0],xlim[1]+bin_width,bin_width)
    bin_centers = (bin_edges+bin_width/2)[:-1]
    return randomValues(model,bin_centers,size)

# compute the correlation matrix from the covariance matrix.
def correlation_from_covariance(covariance):
    v = np.sqrt(np.diag(covariance))
    outer_v = np.outer(v, v)
    correlation = covariance / outer_v
    correlation[covariance == 0] = 0
    return correlation

# make a plot of a matrix with labels.
def matrixPlot(fig,ax,correlationMatrix,labels,colormap="viridis",mrange=(-1,1)):
    assert(len(correlationMatrix.shape)==2 and correlationMatrix.shape[0]==correlationMatrix.shape[0] and len(labels)== correlationMatrix.shape[0])
    if mrange=="log":
        cax = ax.matshow(correlationMatrix, cmap=plt.get_cmap(colormap), norm=mpl.colors.SymLogNorm(1,1,base=10))
    else:
        cax = ax.matshow(correlationMatrix, vmin=mrange[0], vmax=mrange[1], cmap=plt.get_cmap(colormap))
    fig.colorbar(cax,ax=ax)
    ticks = np.arange(0,len(labels),1)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)
    ax.set_xticklabels(labels,rotation=45)
    for (i, j), z in np.ndenumerate(correlationMatrix):
        ax.text(j, i, '{:0.1e}'.format(z), ha='center', va='center',  fontsize='small')
