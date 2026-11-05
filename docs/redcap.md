# REDCap export and local round trip

REDCap uses a data dictionary to define data-entry fields. I follow the [REDCap dictionary column and choice rules documented by UT Dallas](https://atlas.utdallas.edu/TDClient/30/Portal/KB/Article/1142/Editing-the-REDCap-Data-Dictionary): lowercase unique field names, the record ID first, grouped forms, field types and coded choices.

The generated CSV has the standard 18 dictionary columns. `record_id` is the first variable on `dm`, a nonrepeating demographics form. The remaining forms are `vs`, `lb`, `ae`, `ex` and `ds`. Field names have domain prefixes, such as `dm_sex`, so the same SDTM name can appear in multiple forms without colliding. Dropdown choices use integer codes; the codec translates these back to the exact SDTM text. Text fields have date_ymd, integer or number validation when appropriate. Study IDs are synthetic identifiers and are not marked as personal identifiers.

Repeated visits are separate rows with `redcap_repeat_instrument` and `redcap_repeat_instance`. The instance is the original domain sequence number. DM rows have blank repeat fields. There are no longitudinal events in this project.

The pipeline writes the dictionary and records, reads both CSVs back, validates the coded values using that dictionary, reconstructs each domain and compares every released value. The decoder rejects invalid choices, missing required values, invalid dates/numbers, duplicate instances, misplaced fields and mismatched record identities. `roundtrip.json` records the result. This proves the offline codec works against the exported dictionary; it does not prove a particular REDCap server accepted the import.

## Optional manual sandbox check

In a new blank REDCap project that permits repeating instruments:

1. Upload `redcap_dictionary.csv` in the Data Dictionary tool and review its preview.
2. In Project Setup, enable repeating instruments for `vs`, `lb`, `ae`, `ex` and `ds`. Leave `dm` nonrepeating. The dictionary alone does not configure repetition.
3. Import `redcap_records.csv` through Data Import Tool using raw coded values. Review errors before accepting it. Keep this as synthetic test data.
4. Export all records in raw CSV form with repeat-instrument columns. Compare demographic counts, field codes, instances and converted lab values with the original export.

No account, API token or network service is needed for the automated project checks. Server permissions, local REDCap versions, calculated fields, checkbox encodings, surveys and longitudinal events are outside this codec's scope.

## Define-style metadata

`define.xml` uses ODM and Define namespaces for domain groups, variable definitions, origins and code-list references. Its fixed creation timestamp identifies the fictional study metadata baseline, not the time it was run. It is deliberately called Define-XML-style: it is not XSD-validated or complete enough for a regulatory submission. The project does not produce SAS transport files, full value-level metadata, annotated CRFs, external controlled-terminology dictionaries or submission hyperlinks.
