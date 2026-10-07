# Categorical processing of Chinese lexical tone (ECoG, auditory oddball)

Electrocorticography (ECoG) from 6 patients with medically intractable epilepsy (S1-S6) listening passively to a
two-deviant auditory oddball sequence of Mandarin syllables, released with:

> Si X, Zhou W, Hong B (2017). Cooperative cortical network for categorical processing of Chinese lexical tone.
> *PNAS* 114(46):12303-12308. https://doi.org/10.1073/pnas.1710752114

Source record: Zenodo https://doi.org/10.5281/zenodo.926082 (CC-BY-4.0, published 2017-10-19).

## Task (from the paper)

A synthesized rising-level-falling (T2-T1-T4) tone continuum of the Mandarin syllable /i/ was built. In the ECoG
experiment, token 5 (level tone T1) was the frequent standard; tokens 2 (rising, T2) and 8 (level, T1) were the
infrequent deviants. Both deviants are the same physical distance from the standard, giving a cross-category pair
(2 vs 5) and a within-category pair (8 vs 5). 500 trials (S6: 250), onset-to-onset interval 1100 ms with 5% jitter.
The patients watched a silent movie. Electrode placement was decided by clinical need only; no seizure occurred
within 1 h before or after the test. The study was approved by the Ethics Committees of Yuquan Hospital,
Tsinghua University, and patients gave written informed consent.

## Data

- `sub-01` ... `sub-06`, task `toneoddball`. S2 and S5 were exported as two parts (`run-1`, `run-2`).
- EDF, 1200 Hz, 96 ECoG inputs + 6 trigger inputs per file, named by amplifier input (`Amp<k>-<n>`,
  `Amp<k>-trigger`) as released. The mapping of inputs to electrode contacts is not part of the release.
- EDF prefilter field: `HP:0.1Hz LP:0Hz notch HP:48Hz LP:52Hz` (hardware high-pass 0.1 Hz and 50 Hz notch).
- `*_events.tsv`: pulses of the `Amp1-trigger` channel, decoded to digital codes (1, 2, 3; occasionally 255).
  The release does not document which code is which stimulus. Code 1 accounts for about 80% of pulses (the
  standard). The stimulus files are numbered `01standard_flat_yi5`, `02deviant_cross_rise_yi2` and
  `03deviant_within_flat_yi8`, which suggests codes 1/2/3 = standard / cross-category deviant / within-category
  deviant. This is our inference and is labelled as such in `task-toneoddball_events.json`.
- `stimuli/`: the release's stimulus files, unchanged (`stimuli_ECoG_MMN`: the three oddball sounds;
  `stimuli_BehaviorContinumm`: the 13-step continuum used in the behavioural pre-test with healthy volunteers).

## Changes from the release

- EDF header start date: day set to 01 (year and month kept). No other byte of the EDF files changed (SHA-256 of
  the data sections of the source and BIDS files are equal; recorded in `sourcedata/zenodo-926082/b3w1_provenance.json`).
  The EDF patient and recording fields are empty in the release.
- Not redistributed: `data_MRI.rar` (FreeSurfer `orig.mgz` T1 per patient) and `data_CT.rar` (raw CT per patient).
  A surface render of these volumes shows reconstructable facial features, so they are left out; they remain
  available from the CC-BY-4.0 source record. The original `.rar` archives are also not copied because their
  member timestamps carry full recording dates.
- Age and sex are not in the release (`n/a`).

## Licence

CC-BY-4.0, as the source record. Please cite the paper and the Zenodo record.
