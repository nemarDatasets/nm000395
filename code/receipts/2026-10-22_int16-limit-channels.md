# Receipt: channels at the int16 limits marked bad

**Claim.** Mark channels at the int16 limits as bad (28 `channels.tsv` entries: `Amp6-1`..`Amp6-4` in 7 of 8 recordings).

## Source

- Release: Zenodo record 926082, https://doi.org/10.5281/zenodo.926082 (the only version of concept record
  926081, published 2017-10-19, CC-BY-4.0). The ECoG files are the 8 EDF members of `data_ECoG.rar`
  (395133288 bytes, md5 `e5f36e037abc819d8876d18d10a080ee`, as listed by the Zenodo API in
  `sourcedata/zenodo-926082/zenodo_manifest_926082.tsv`).
- Files read: the 8 `sub-*/ieeg/*_ieeg.edf` of NEMAR `origin/main` at `c83ab075ed7628f7080eca2f3901025ed35b15fb`
  (identical annex keys at the PR parent `33b44c93`). The sha256 the script prints for each file equals its git-annex
  key (`SHA256E-s<bytes>--<sha256>.edf`) and `sha256_bids_file` in `sourcedata/zenodo-926082/b3w1_provenance.json`.
- Match with Zenodo: `b3w1_provenance.json` (in the dataset since its first commit `3422e8b`) gives, for each of the
  8 EDFs, the sha256 of the released member (`sha256_source_file`) and of the BIDS file, with
  `data_section_sha256_equal: true` and `header_change: "start-date day -> 01"`. The data records (everything after
  the header) are therefore byte-identical to the release, so every count below is the same in the released files.
  To redo it: download `data_ECoG.rar`, check the md5 above, extract, compare `sha256_source_file`, then hash the
  bytes after the header of both files.

## Method

- Script: `code/receipts/2026-10-22_int16-limit-channels.py <bids_root>` (mne 1.13.2, numpy 2.5.4, pandas 3.1.0),
  run on Slurm on 2026-10-22 against a read-only copy of NEMAR main.
- EDF calibration (header of every file, all 102 signals identical): physical dimension `uV`, physical min/max
  -500/500, digital min/max -2048/2047, so 1000/4095 = 0.244200 µV per count. The stored counts reach the int16
  limits, beyond the declared digital range; the linear header scaling maps -32768 and 32767 to -8001.83 and
  +8001.83 µV (the "±8001.8 µV" in `status_description`).
- Counts are read unscaled from the EDF data records (header parsed with the standard library, data as little-endian
  int16 via `numpy.memmap`). Per channel: number of samples equal to -32768 and to 32767, fraction of all samples.
- Rule: a channel is `bad` if this fraction is > 10 %; `status_description` gives it rounded to 0.1 %.
- Reader check: for each flagged channel, `mne.io.read_raw_edf` (scaling applied, output in V) returns the same number
  of samples at ±8001.83 µV (within half a count), i.e. MNE applies the header gain and offset without clipping.

## Result

Flagged channels (28 entries). The `status_description` strings the script prints are identical to the 28 `bad`
rows at the PR head (compared programmatically); `origin/main` has no `bad` row.

| file | channel | samples | at -32768 | at 32767 | fraction | MNE same count |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| sub-01 | Amp6-1 | 822000 | 256081 | 275177 | 64.6 % | yes |
| sub-01 | Amp6-2 | 822000 | 256239 | 264078 | 63.3 % | yes |
| sub-01 | Amp6-3 | 822000 | 253952 | 268656 | 63.6 % | yes |
| sub-01 | Amp6-4 | 822000 | 259104 | 276442 | 65.2 % | yes |
| sub-02_run-1 | Amp6-1 | 531600 | 201867 | 110698 | 58.8 % | yes |
| sub-02_run-1 | Amp6-2 | 531600 | 189747 | 204278 | 74.1 % | yes |
| sub-02_run-1 | Amp6-3 | 531600 | 189589 | 204294 | 74.1 % | yes |
| sub-02_run-1 | Amp6-4 | 531600 | 191195 | 204119 | 74.4 % | yes |
| sub-02_run-2 | Amp6-1 | 486000 | 185455 | 101293 | 59.0 % | yes |
| sub-02_run-2 | Amp6-2 | 486000 | 172986 | 186896 | 74.0 % | yes |
| sub-02_run-2 | Amp6-3 | 486000 | 172875 | 186880 | 74.0 % | yes |
| sub-02_run-2 | Amp6-4 | 486000 | 174378 | 187161 | 74.4 % | yes |
| sub-04 | Amp6-1 | 804000 | 220649 | 325051 | 67.9 % | yes |
| sub-04 | Amp6-2 | 804000 | 282351 | 376127 | 81.9 % | yes |
| sub-04 | Amp6-3 | 804000 | 281854 | 376650 | 81.9 % | yes |
| sub-04 | Amp6-4 | 804000 | 281549 | 378565 | 82.1 % | yes |
| sub-05_run-1 | Amp6-1 | 570000 | 174958 | 211116 | 67.7 % | yes |
| sub-05_run-1 | Amp6-2 | 570000 | 187418 | 208372 | 69.4 % | yes |
| sub-05_run-1 | Amp6-3 | 570000 | 186311 | 210181 | 69.6 % | yes |
| sub-05_run-1 | Amp6-4 | 570000 | 189321 | 214536 | 70.9 % | yes |
| sub-05_run-2 | Amp6-1 | 585600 | 120580 | 90880 | 36.1 % | yes |
| sub-05_run-2 | Amp6-2 | 585600 | 115513 | 98366 | 36.5 % | yes |
| sub-05_run-2 | Amp6-3 | 585600 | 108962 | 99484 | 35.6 % | yes |
| sub-05_run-2 | Amp6-4 | 585600 | 129815 | 101879 | 39.6 % | yes |
| sub-06 | Amp6-1 | 498000 | 82996 | 78894 | 32.5 % | yes |
| sub-06 | Amp6-2 | 498000 | 99987 | 94901 | 39.1 % | yes |
| sub-06 | Amp6-3 | 498000 | 99430 | 95415 | 39.1 % | yes |
| sub-06 | Amp6-4 | 498000 | 99314 | 94145 | 38.8 % | yes |

All other channels (fraction ≤ 10 %): per file, number of other ECoG channels with any sample at the limits and the
largest fraction (trigger channels: none in any file).

| file | other ECoG channels | with samples at the limits | max fraction (channel) |
| --- | ---: | ---: | --- |
| sub-01 | 92 | 1 | 0.04 % (Amp2-15) |
| sub-02_run-1 | 92 | 1 | 1.72 % (Amp4-13) |
| sub-02_run-2 | 92 | 1 | 0.79 % (Amp4-13) |
| sub-03 | 96 | 4 | 0.45 % (Amp6-4) |
| sub-04 | 92 | 2 | 4.46 % (Amp2-6) |
| sub-05_run-1 | 92 | 14 | 1.10 % (Amp6-12) |
| sub-05_run-2 | 92 | 13 | 1.31 % (Amp6-5) |
| sub-06 | 92 | 3 | 1.13 % (Amp6-16) |

Largest fraction outside the 28 entries: 4.46 % (`sub-04`, `Amp2-6`), i.e. the README's "at most 4.5%". `sub-03` has
no channel above 10 %.

## Coverage

8 of 8 EDF files, 102 of 102 signals each (816 channel entries); 8 of 8 `channels.tsv` compared.
