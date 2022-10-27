import uproot
import awkward as ak
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import mplhep as hep
import scipy
import iminuit
from inspect import signature, stack, Parameter
from functools import wraps

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
        if index is not None: # if there is an index, we select that column
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
            
    def plot(self,binedges):
        plt.hist(self.events, binedges, color=self.color, label=self.label,weights = self.norm)

# The curve class is a simple helper built from a function and display options.
class curve:
    def __init__(self,func, label, color='g', linewidth=4):
        self.func = func
        self.label = label
        self.color = color
        self.linewidth = linewidth
        
    def plot(self,linspace):
        plt.plot(linspace,np.array([self.func(xi) for xi in linspace]), 
                     label=self.label, color=self.color, lw=self.linewidth)

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
# TODO: this function can soon be dropped or made into a proxy for Plotter
def plot(data, simu, curves, xlim, xlabel, ylabel='Probability', nbins=100, islog=True, color='g', density=True):
    fig, ax = plt.subplots(figsize=(10, 10))
    hep.style.use(hep.style.CMS)
    hep.cms.text("Open Data")
    ax.set_xlim(*xlim)
    bin_width = (xlim[1]-xlim[0])/nbins
    bin_edges = np.arange(xlim[0],xlim[1]+bin_width,bin_width)
    bin_centers = (bin_edges+bin_width/2)[:-1]
   
    if type(simu) is ak.highlevel.Array:
        ax.hist(simu, bins=bin_edges, density=density, facecolor=color, alpha=0.75, label='MC'); # simulation
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

class Plotter:
    def __init__(self, cost, xlabel="Var", ylabel="Events", text = True, logscale = False, legend = False, fill = True, density = True, color='g'):
        self.cost = cost
        self.cmsText = text
        self.simu = None
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.logscale = logscale
        self.legend = legend
        self.fill = fill
        self.curves = None
        self.simu = None
        self.density = density
        self.color = color
        self.xe = cost.xe if cost is not None else np.array([]) # bin edges
        self.cx = 0.5 * (self.xe[1:] + self.xe[:-1]) # bin centers
        
    def setSimulation(self,simu):
        self.simu = simu
    
    def setText(self,text = True):
        self.cmsText = text
        
    def setCurves(self,curves):
        self.curves = curves
        
    def setHistograms(self,simu):
        self.simu = simu
        
    def plotSimu(self):
        if type(self.simu) is ak.highlevel.Array:
            plt.hist(self.simu, bins=self.xe, density=self.density, facecolor=self.color, alpha=0.75, label='MC'); # simulation
        else:
            assert(type(self.simu) is list)
            if len(self.simu)>0:
                samples = [ s.events for s in self.simu ]
                label = [ s.label for s in self.simu ]
                norm = [ [s.norm]*len(s.events) for s in self.simu ]
                color = [ s.color for s in self.simu ]
                plt.hist(samples, self.xe, density=self.density, alpha=0.75, 
                         stacked=True, color=color, label=label,weights = norm)

    def plotCurves(self):
        for curve in self.curves:
            curve.plot(self.cx)
            #plt.plot(self.cx,np.array([curve.func(xi) for xi in self.cx]), 
            #         label=curve.label, color=curve.color, lw=curve.linewidth)

    def __call__(self, args=None,data=None):
        hep.style.use(hep.style.CMS)
        if self.cmsText:
            hep.cms.text("Open Data")
        if data is None:
            xe = self.xe
            cx = self.cx
        else:
            xe = data[1]
            cx = 0.5 * (xe[1:] + xe[:-1])
            self.xe = xe
            
        plt.xlim(xe[0],xe[-1])
        
        # data
        n = self.cost.data if data is None else data[0]
        if self.density:
            plt.errorbar(cx, n, n*0, fmt="ok", label='Data')
        else:
            plt.errorbar(cx, n, n ** 0.5, fmt="ok", label='Data')
        
        # fit 
        if args is not None and self.cost is not None:
            if isinstance(self.cost,iminuit.cost.ExtendedBinnedNLL):
                    sm = np.diff(self.cost.scaled_cdf(xe, args[0], 0, *args[2:]))
                    bm = np.diff(self.cost.scaled_cdf(xe, 0, args[1], *args[2:]))
                    tm = sm+bm
                    plt.stairs(sm+bm, xe, fill=self.fill, color="C0", label = "S+B fit", lw=4)
                    plt.stairs(bm, xe, fill=self.fill, color="C1", label = "bkg shape", lw=4)


            if isinstance(self.cost,iminuit.cost.Template):
                shapes = [a*b for a,b in zip(self.cost._bbl_data[0],args)]
                plt.stairs(shapes[0]+shapes[1], xe, fill=True, color="C0", label = "S+B fit", lw=4)
                plt.stairs(shapes[1], xe, fill=True, color="C1", label = "bkg shape", lw=4)
                #plt.stairs(mu + mu_err, xe, baseline=mu - mu_err, fill=True, color="C0")

        # Monte Carlo histograms
        if self.simu is not None:
            self.plotSimu()

        # other curves
        if self.curves is not None:
            self.plotCurves()
        
        if self.logscale:
            plt.yscale('log')
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)  
        if self.legend:
            plt.legend();
    
    
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
        
# Normalized Relativistic Breit-Wigner
def breitwigner(x, m, gamma):
    """
    Normalized Relativistic Breit-Wigner
    .. math::
        f(x; m, \Gamma) = N\\times \\frac{1}{(x^2-m^2)^2+m^2\Gamma^2}
    where
    .. math::
        N = \\frac{2 \sqrt{2} m \Gamma  \gamma }{\pi \sqrt{m^2+\gamma}}
    and
    .. math::
        \gamma=\sqrt{m^2\left(m^2+\Gamma^2\\right)}
    .. seealso::
        :func:`cauchy`
    .. plot:: pyplots/pdf/cauchy_bw.py
        :class: lightbox
    """
    mm = m*m
    xm = x*x-mm
    gg = gamma*gamma
    s = sqrt(mm*(mm+gg))
    N = (2*sqrt(2)/pi)*m*gamma*s/sqrt(mm+s)
    return N/(xm*xm+mm*gg)

# Decorator to make the definition of s+b more natural. 
# This creates a significant overhead in the calculation, but we can afford it.
def signalbackground(background,signal):
    """Decorator factory that makes a function with 
       combined arguments from signal and background pdf functions"""

    def decorator(f):
        @wraps(f)
        def wrapper(x,s,b,*args,**kwargs):
            # get signatures for signal and background functions
            f1_sig = signature(background)
            f2_sig = signature(signal)
            # ignore the first parameter (x), concatenate the rest
            parameters=tuple(list(f1_sig.parameters.values())[1:])+tuple(list(f2_sig.parameters.values())[1:])
            # first args are fixed: 
            f_args={'x':x,'s':s,'b':b}
            # loop over other args and store them
            for n,arg in enumerate(args):
                f_args[parameters[n].name] = arg
            for name, arg in kwargs.items():
                if name in f_args:
                    raise TypeError(f"{stack()[0][3]}() got multiple values for argument '{name}'")
                f_args[name]=arg
            # now prepare the arguments for the function, i.e. split between signal and backgorund parameters
            bkg_params = {}
            signal_params = {}
            for arg in list(f1_sig.parameters.values())[1:]:
                bkg_params[arg.name] = f_args[arg.name]
            for arg in list(f2_sig.parameters.values())[1:]:
                signal_params[arg.name] = f_args[arg.name]
            
            return f(x,s,b,bkg_params,signal_params)

        # Override signature
        f1_sig = signature(background)
        f2_sig = signature(signal)
        parameters=tuple(list(f1_sig.parameters.values())[1:])+tuple(list(f2_sig.parameters.values())[1:])
        sig = signature(f)
        sig = sig.replace(parameters=(Parameter("x",Parameter.POSITIONAL_OR_KEYWORD),Parameter("s",Parameter.POSITIONAL_OR_KEYWORD),Parameter("b",Parameter.POSITIONAL_OR_KEYWORD))+parameters)
        wrapper.__signature__ = sig
        
        return wrapper
    
    return decorator
