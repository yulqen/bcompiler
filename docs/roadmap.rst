Roadmap
-------

``bcompiler`` makes use of `semantic versioning <http://semver.org/>`_
and therefore follows the MAJOR.MINOR.PATH version pattern.

1.2 - Plugins
*************

- Allow integration of own analysers written in Python
- Simple plugin management interface through commandline

1.1 - Analysers
***************

- Commandline analysers for simple features
- API for analysers to be customised and used outside
  bcompiler
- ``bcompiler-init`` wrapper for auxiliary files repository so user doesn't
  have to push, pull and merge in git

Commandline analysers
=====================

==================== ===================  ===========
Analyser             Product              Status
==================== ===================  ===========
swimlane_milestones  Excel chart          Implemented
financial_analysis   Excel spreadsheet    
report_annex         Excel spreadsheet 
project_list         terminal output
sro_list             terminal output
rag_ratings          terminal output
==================== ===================  ===========


API
===

==================== ===================  ===========
Analyser             Product              Status
==================== ===================  ===========
swimlane_milestones  SwimlaneChart()
others...
==================== ===================  ===========


1.0 - Stability
*****************

- Compile master from populated templates
- Populate templates from master
- Commandline interface
- Test suite
- Clean data in both directions
- Integrate with auxiliary files repository
- ``bcompiler-init`` to set up project
- Documentation
