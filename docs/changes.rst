Changes
~~~~~~~

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
