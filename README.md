django-undodelete
=================

Django-undodelete combines soft-delete technology and background tasks to perform delayed archiving and hard-deleting data. It also gives the possibility of undoing delete action, at first by user, later by admin.


Basic motivation
----------------

- Real delete is slow, cascade delete is very slow.
- People do mistakes. Undo is standard.
- Data is more valuable than the program.

Advanced motivation
----------------

- Naive solution of permanent softdelete via additionally column(s) and adjusted queries is uncomfortable and has integrity issues. Often leads to unexpected  side effects.
- Raising nonused data over database is dangerous and leads to unexpected problems in future.

Solution
----------------

- Divide and rule
- first step is softdelete - fast, easy undoable action, side effects are acceptable in short time.
- second step is partitioning data, softdeleted data are optionally moved and then hard-deleted from original table. It can be implemented as background task.



