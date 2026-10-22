import hashlib
import sys
from pathlib import Path

import mne
import numpy as np
import pandas as pd

LIMITS = (-32768, 32767)
BAD_FRACTION = 0.10
FIELDS = [("label", 16), ("transducer", 80), ("dim", 8), ("pmin", 8), ("pmax", 8)]
FIELDS += [("dmin", 8), ("dmax", 8), ("prefilter", 80), ("nsamp", 8)]


def read_header(path: Path) -> tuple[int, int, pd.DataFrame]:
    with path.open("rb") as f:
        fixed = f.read(256)
        ns = int(fixed[252:256])
        raw = f.read(ns * 256).decode("latin1")
    signals, off = {}, 0
    for key, w in FIELDS:
        signals[key] = [raw[off + i * w : off + (i + 1) * w].strip() for i in range(ns)]
        off += ns * w
    return int(fixed[184:192]), int(fixed[236:244]), pd.DataFrame(signals)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(1 << 24):
            h.update(chunk)
    return h.hexdigest()


def scan(path: Path) -> tuple[dict, list[dict]]:
    header_bytes, n_records, sig = read_header(path)
    calib = sig[["dim", "pmin", "pmax", "dmin", "dmax"]].drop_duplicates()
    assert len(calib) == 1, f"{path.name}: several calibrations\n{calib}"
    dim, pmin, pmax, dmin, dmax = calib.iloc[0]
    gain = (float(pmax) - float(pmin)) / (int(dmax) - int(dmin))
    rails = [float(pmin) + (lim - int(dmin)) * gain for lim in LIMITS]  # µV
    nsamp = sig.nsamp.astype(int).to_numpy()
    data = np.memmap(path, dtype="<i2", mode="r", offset=header_bytes)
    data = data.reshape(n_records, nsamp.sum())
    starts = np.concatenate([[0], np.cumsum(nsamp)])
    raw = mne.io.read_raw_edf(path, preload=False, verbose="error")
    channels = []
    for k, label in enumerate(sig.label):
        counts = np.asarray(data[:, starts[k] : starts[k + 1]]).ravel()
        n_low, n_high = (int((counts == lim).sum()) for lim in LIMITS)
        fraction = (n_low + n_high) / counts.size
        row = {"file": path.name, "channel": label, "n_samples": counts.size}
        row |= {"n_at_-32768": n_low, "n_at_32767": n_high, "fraction": fraction}
        row["bad"] = fraction > BAD_FRACTION
        if row["bad"]:
            volts = raw.get_data(picks=[label])[0] * 1e6
            n_mne = sum(int((np.abs(volts - r) < gain / 2).sum()) for r in rails)
            row["mne_same_count"] = n_mne == n_low + n_high
            row["status_description"] = (
                f"at the int16 limits (±{rails[1]:.1f} µV) "
                f"for {100 * fraction:.1f}% of samples"
            )
        channels.append(row)
    info = {"file": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)}
    info |= {"n_records": n_records, "n_signals": len(sig), "dim": dim}
    info |= {"pmin": pmin, "pmax": pmax, "dmin": dmin, "dmax": dmax}
    info["uV_per_count"] = f"{gain:.6f}"
    info["rails_uV"] = "/".join(f"{r:.2f}" for r in rails)
    return info, channels


def main(root: Path) -> None:
    edfs = sorted(root.glob("sub-*/ieeg/*_ieeg.edf"))
    print(f"mne {mne.__version__}, numpy {np.__version__}, pandas {pd.__version__}")
    print(f"{len(edfs)} EDF files under {root}")
    infos, channels = zip(*(scan(p) for p in edfs))
    files = pd.DataFrame(infos)
    chans = pd.DataFrame([c for cs in channels for c in cs])
    chans["type"] = np.where(chans.channel.str.endswith("trigger"), "TRIG", "ECOG")
    bad, good = chans[chans.bad], chans[~chans.bad]
    print("## files\n" + files.to_csv(sep="\t", index=False))
    cols = ["file", "channel", "n_samples", "n_at_-32768", "n_at_32767", "fraction"]
    cols += ["mne_same_count", "status_description"]
    print(
        "## channels above the threshold\n"
        + bad[cols].to_csv(sep="\t", index=False, float_format="%.4f")
    )
    top = good.sort_values("fraction").groupby(["file", "type"]).tail(1)
    others = good.groupby(["file", "type"]).agg(
        n_channels=("channel", "size"),
        n_channels_above_0=("fraction", lambda f: (f > 0).sum()),
    )
    others = others.join(top.set_index(["file", "type"])[["channel", "fraction"]])
    print(
        "## other channels: max fraction per file and type\n"
        + others.to_csv(sep="\t", float_format="%.4f")
    )
    print(
        f"## summary: {len(bad)} entries > {BAD_FRACTION:.0%} in {bad.file.nunique()} "
        f"of {len(edfs)} files, channels {sorted(bad.channel.unique())}; "
        f"max elsewhere {good.fraction.max():.4f}"
    )


if __name__ == "__main__":
    main(Path(sys.argv[1]))
