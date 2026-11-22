#!/usr/bin/env python3
"""Skim and repair the LPHY2131 ntuples.

This is an optional, instructor-side tool. It copies the WeakBosonsAnalysis tree of an
ntuple into a new file and

  * keeps only events with at least N leptons (muons + electrons), if --min-leptons N is given;
  * optionally drops branches that no lab uses (--drop, e.g. --drop JetsPt JetsEta JetsPhi);
  * fixes the isolation branches of the CMS ntuples: there the branch "MuonIsolation" holds a
    leaf named "muonIsolation" (same for electrons), which ROOT's RDataFrame cannot read.
    In the output, every leaf has the same name as its branch. Branch names are unchanged,
    so the notebooks work as before.

The tree path (LPHY2131analysis/WeakBosonsAnalysis) and the branch names are kept, so a
skimmed file can replace the original one without changing the notebooks.

The number of events in the input file is saved in the tree LPHY2131analysis/SkimInfo.

WARNING: the notebooks compute the selection efficiency as
    len(selected_simu) / simutree.num_entries
Skimming a *simulation* file with --min-leptons > 0 reduces num_entries and makes that
efficiency wrong. For simulation, only use the default (--min-leptons 0), which repairs the
branch names without removing events.

The skim must be looser than any cut the students may try. Suggested settings:
    Z (doubleMu / doubleEl data):  --min-leptons 2
    W (singleMu / singleEl data):  --min-leptons 1

Examples:
    python skim.py doubleMu2011_ntuple.root doubleMu2011_skim.root --min-leptons 2
    python skim.py ppChargedCurrentFullsim_ntuple.root ppChargedCurrentFullsim_fixed.root
"""

import argparse
import os
import sys
import time

import numpy as np
import uproot

DIRECTORY = "LPHY2131analysis"
TREE = "WeakBosonsAnalysis"

COMPRESSION = {
    "zlib": lambda level: uproot.ZLIB(level),
    "lzma": lambda level: uproot.LZMA(level),
    "lz4": lambda level: uproot.LZ4(level),    # needs the lz4 and xxhash packages to read
    "zstd": lambda level: uproot.ZSTD(level),  # needs the zstandard package to read
}


def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input", help="input ntuple (ROOT file)")
    parser.add_argument("output", help="output ROOT file (must not exist yet)")
    parser.add_argument("--min-leptons", type=int, default=0,
                        help="keep events with nMuons + nElectrons >= N (default: 0, keep all events)")
    parser.add_argument("--drop", nargs="+", default=[], metavar="BRANCH",
                        help="branches to leave out of the output")
    parser.add_argument("--compression", choices=sorted(COMPRESSION), default="zlib",
                        help="compression algorithm (default: zlib, readable everywhere)")
    parser.add_argument("--level", type=int, default=4, help="compression level (default: 4)")
    parser.add_argument("--step-size", default="100 MB", help="amount of input read at once (default: 100 MB)")
    parser.add_argument("--max-entries", type=int, default=None,
                        help="only process the first N input events (for testing)")
    return parser.parse_args()


def main():
    args = parse_arguments()
    if os.path.exists(args.output):
        sys.exit(f"Output file {args.output} already exists; refusing to overwrite it.")
    if os.path.abspath(args.input) == os.path.abspath(args.output):
        sys.exit("Input and output must be different files.")

    intree = uproot.open(args.input)[f"{DIRECTORY}/{TREE}"]
    unknown = set(args.drop) - set(intree.keys())
    if unknown:
        sys.exit(f"Unknown branch(es) in --drop: {', '.join(sorted(unknown))}")
    branches = [name for name in intree.keys() if name not in args.drop]
    for needed in ("nMuons", "nElectrons"):
        if args.min_leptons > 0 and needed not in branches:
            sys.exit(f"--min-leptons needs the {needed} branch; do not drop it.")

    # For each variable-length branch, the branch holding its length (e.g. MuonIsolation -> nMuons).
    # Branches sharing a counter in the input share it in the output too.
    counters = {name: intree[name].count_branch.name
                for name in branches if intree[name].count_branch is not None}
    for name, counter in counters.items():
        if counter not in branches:
            sys.exit(f"Branch {name} needs its counter {counter}; do not drop it.")

    entry_stop = intree.num_entries if args.max_entries is None else min(args.max_entries, intree.num_entries)
    print(f"Input : {args.input}  ({entry_stop} events, {len(branches)} branches kept)")

    start = time.time()
    n_out = 0
    with uproot.recreate(args.output, compression=COMPRESSION[args.compression](args.level)) as outfile:
        outtree = None
        for events in intree.iterate(branches, step_size=args.step_size, entry_stop=entry_stop):
            if args.min_leptons > 0:
                events = events[events.nMuons + events.nElectrons >= args.min_leptons]
            data = {name: events[name] for name in branches}
            if outtree is None:
                outtree = outfile.mktree(f"{DIRECTORY}/{TREE}",
                                         {name: array.type.content for name, array in data.items()},
                                         title=intree.title,
                                         counter_name=lambda name: counters[name])
            if len(events) > 0:
                outtree.extend(data)
            n_out += len(events)
            print(f"\r  {n_out} events written", end="", flush=True)
        print()

        info = outfile.mktree(f"{DIRECTORY}/SkimInfo",
                              {"inputEntries": np.int64, "outputEntries": np.int64, "minLeptons": np.int32},
                              title=f"skim of {os.path.basename(args.input)}")
        info.extend({"inputEntries": np.array([entry_stop], dtype=np.int64),
                     "outputEntries": np.array([n_out], dtype=np.int64),
                     "minLeptons": np.array([args.min_leptons], dtype=np.int32)})

    size_in, size_out = os.path.getsize(args.input), os.path.getsize(args.output)
    print(f"Output: {args.output}  ({n_out} events, {100 * n_out / max(entry_stop, 1):.1f}% kept)")
    print(f"Size  : {size_in / 1e6:.0f} MB -> {size_out / 1e6:.0f} MB, in {time.time() - start:.0f} s")


if __name__ == "__main__":
    main()
