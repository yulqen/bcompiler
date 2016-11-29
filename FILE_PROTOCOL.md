# bcompiler: File Storage, Version Control and Naming Convention

## Naming Conventions

* no spaces in file names; use underscores as separators
* filenames containing **_NO_STEP_** are not to be altered ('NO_STEP' is a reference to 'being trampled-on'; if they are  available to change, they should have an MS Office filetype '_TC_ONLY_..' equivalent;
* filenames containing **_TC_ONLY_** are an MS Office filetype to be used for Track Changes;
* filenames containing **_TC_ONLY_** should also contain identifier of person who last made any change, as initials, and the date of the last save (e.g. '_ML_231116');

## Version Control

Files whose name contains '__TC_ONLY_' may be edited by anybody. Track Change mode MUST be activated before any changes are saved. Once significant changes have been made, the editor must edit the Version Control Table within the file (this is found at the top of **datamap-master-to-returns** and on a separate sheet in **bicc_template**) to include details of the change. Once these changes have been approved, the '_NO_STEP_' version of the file will be edited to match the '_TC_ONLY_' version and its version will be changed to match.

So, an example workflow would be:

* Decision that changes are required to **datamap-master-to-returns**.
* Change proposer (the editor) opens **datamap-master-to-returns_TC_ONLY_[..INITIALS_DATE_VERSION..]** file and makes changes.
* Whilst editing, the file can be saved but **NO CHANGES TO FILENAME OR VERSION CONTROL TABLE SHOULD BE MADE**.
* When changes are final, editor should increment version number in Version Control Table inside the document (0.1 to 0.2, 0.9 to 1.0, and so on), add their name, date and notes about what has changed and why, and make the appropriate changes to the filename.
* Editor informs ML of a change to be applied.
* ML applies the change tracking and converts the '_TC_ONLY_' file to a '_NO_STEP_' file.
* ML applies all Track Changes in '_TC_ONLY_' file. If a '_TC_ONLY_' file still has outstanding Track Changes, that indicates that changes have not been migrated to '_NO_STEP_' file.
* ML increments the version of the '_NO_STEP_' file as appropriate.

## Files in this directory (so far)

(Please note, the version numbers and editor initials indicated here are likely to be different)

* bicc_template_NO_STEP_[v0.1] (Excel XLSX): this is the file that bcompiler uses as the template for the return
* bicc_template_TC_ONLY_[ML_231116_v0.1] (Excel XLSX): this is the file that is available to be changed by anybody, as long as Track Change mode is used.
* datamap-master-to-returns_NO_STEP_v0.1 (Text file): this is the file that bcompiler uses to migrate data from the MASTER to the RETURN template
* datamap-master-to-returns_TC_ONLY_[ML_231116_v0.1] (Excel XLSX): this is the file that is available to be changed by anybody, as long as Track Change mode is used.
* various files named 'archive_' that are archives of previous or current working files that should not be changed or deleted.
