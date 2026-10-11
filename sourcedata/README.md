# sourcedata

Original release files of the source dataset, as far as they can be redistributed.

## Release files stored under their release names (added 2026-10-11)

24 release files of Zenodo record 926082 (https://doi.org/10.5281/zenodo.926082) are listed under `sourcedata/zenodo-926082/` with their release paths.
They take no extra storage: each is a git-annex pointer to the same content as the BIDS file named in
`sourcedata/SOURCEDATA_POINTERS.tsv`.

- 16 are `identical`: byte for byte the released file.
- 8 are `scrubbed`: the privacy-scrubbed copy used in the BIDS part, not the released bytes. The ECoG EDFs (members of `data_ECoG.rar`) differ from the release only in the header start date (day of month set to 01). The stimulus WAV files (members of the two stimulus `.rar`) are identical. The `.rar` archives themselves (member timestamps hold recording dates) and the MRI/CT volumes (faces) are not included.

The unscrubbed originals are not redistributed here; they remain available from the public source.
