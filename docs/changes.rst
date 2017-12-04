Changes
~~~~~~~

v1.3.8
######

* new Reference Class Forecasting analyser

v1.3.7
######

* new financial analysis analyser

v1.3.6
######

* Chart is based on start_date option when using swimlane analysers,
  rather than today's date.
* swimlane charts use 30 as main x axis unit rather than 50 to approximate
  months.

v1.3.5
######

* Bug fixes

v1.3.4
######

* Fixed bug whereby creating an annex from a master containing a project not in
  the compare master threw an error
* Fixes for annex analyser

v1.3.3
######

* new swimlane assurance milestones analyser
* annex analyser now does comparison with previous master document
* fix issues in annex analyser

v1.3.2
######

* Partial fix for final project milestone not ending up on swimlane chart.

v1.3.1
######

* Fixed bug which prevented setting the title of the output sheet from the
  keyword analyser with xlsx output option, to a disallowed character.

v1.3.0
######

* Added keyword analsyer. Search fields in a master file and return the
  values for each field, for each project in the terminal or optionally to
  an xlsx file.

v1.2.2
#######

* Ability to set ``--start_date`` and ``--end_date`` parameters for ``swimlane_milestones``
  analyser.
* Fix bug where date differences not being calculated correctly in
  ``swimlane_milestones`` analyser.
* Fix bug where wrong milestone type was being charted by
  ``swimlane_milestones`` analyser.
* Many more configurations available in ``config.ini`` file relating to
  ``swimlane_analyser``.
* Better logging to ``bcompiler.log`` during ``swimlane_milestones`` analyser.
* Better handling of date objects.
* Various bug fixes

v1.2.1
######

* Added ``annex`` analyser, allowing for easy summarise by project from master.
* Added ASCII art to ``bcompiler --help``!
* Various bug fixes

30 October 2017
###############
- Fix bug where not all columns in master are being processed during swimlane analyser.

17 October 2017
###############

- Changed ERROR log message to WARNING to accommodate dates mixed with free text.

16 October 2017
###############

- Fix bug where cell value in string and datetime value would try to compare arithmetically.

11 October 2017
###############

- Fix bug where `.xlsx` files not being picked up.
- Improved exception handling and bug fixes.

10 October 2017
###############

- Handling cp1252 encoding coming through from Windows
- Added CHANGES.txt
- Minor bugfixes
