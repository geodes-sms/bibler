# ![](bibler.png)  BiBler User Manual



## Introduction <a name="intro"></a>
BiBler allows you to manage and manipulate BibTeX entries following the [standard BibTeX rules and formats](http://www.openoffice.org/bibliographic/bibtex-defs.html).



## File menu

##### Open
Import a list of entries from a BibTeX file in a given format and overwrites all existing entries.
See the [Import menu](#import) for teh supported formats. 

##### Save
Overwrites the current file loaded with the list of entries displayed.

##### Save as
Saves list of entries displayed in a new file in BibTeX format.

##### Import from file <a name="import"></a>
Import a list of entries from a file in a given format.
The currently supported formats are EndNote and CSV.
For EndNote, you must have exported your library from EndNote to BibTeX using the `BiBler Export.ens` style provided in the `external/` folder of the BiBler distribution.
For CSV, the data must be formatted in the same way as the export does.
The imported file must follow the [valid syntax](#syntax).
**Make sure the file is encoded in ANSI or UTF-8; special characters may cause some errors.** 

##### Export to file
Export the list of entries to a file in a given format.
The currently supported formats are HTML, CSV, and SQL (for MySQL).

##### Exit
Closes the BiBler application.

## Edit menu

##### Undo
Reverse the last operation performed. When the focus is in the editor, use Ctrl+Z to undo what you typed in.

##### Select all text
Select the entire text in the editor. This enables the Ctrl+A keyboard shortcut in the editor.

##### Filter
Search through the list of entries and display only those that satisfy the query provided.
This searches through all values, not field names and entry types.
The query is not case-sensitive and special characters are simplified (e.g., 'e' will match &eacute;).
By default, an exact match of the query must be found. Regular expressions can be used if the option is enabled in the preferences.
The supported regular expressions follow [Python regex](https://docs.python.org/library/re.html).
Note that the search string cannot start with * since it anyways searches for substrings.

##### Clear Filter
Display the entire list of entries back after a search.

##### Preferences
Set the preferences of BiBler.

* **Bibliography style:** Set the style of the HTML output of entries. This applies for the preview of an entry and the HTML export. The currently supported styles are ACM and a default style.
* **Allow invalid entries:** Only add valid well-formed entries according to the [standard BibTeX rules and formats](http://www.openoffice.org/bibliographic/bibtex-defs.html) and ignore ill-formed entries. This also holds for Open and Import operations.
* **Allow non-standard fields:** Allow to retain non-standard [BibTeX fields](http://www.openoffice.org/bibliographic/bibtex-defs.html) in each entry. This is enabled by default. Otherwise, those fields will be removed from the entries.
* **Override key generation:** When enabled, any new entry added (inserted, opened, or imported) will be assigned a unique BibTeX key, even if one was already provided. This option is diabled by default, however if an entry does not have a key provided, BiBler will assign one automatically.
* **Search query as regular expression:** When enabled, you can specify regular expressions in the search. This is disabled by default.



## Reference menu

##### Add new
Add a new empty entry in the list. To specify the content of the reference, see the update operation. New additions are appended at the end of the list. So you may need to scroll down to see it.

##### Delete
Remove the selected entry from the list.

##### Duplicate
Creates a new entry with the content copied form the selected entry. New additions are appended at the end of the list. So you may need to scroll down to see it.

##### Generate all keys
Generate the BibTeX key of entries in the list. This will override the existiing key even if the option is not enabled in the Preferences.

##### Validate all
Check if all entries in the list are valid with repsect to the [BibTeX rules](http://www.openoffice.org/bibliographic/bibtex-defs.html).
All invalid entries that require your attention are highlighted in red.



## Help menu

##### User manual
Open this document.

##### About BiBler
Display additional information about the distribution of BiBler.



## List of entries
All entries added or loaded from a file are displayed as a table. The list displays minimal information to identify each entry.

Clicking on a column will sort all entries currently displayed in increasing alpha-numerical order.
Columns can be resized, by moving to their header's edge, and can be reordered by drag-n-drop.

Entries in white are correct and valid.
Entries in red are either missing a required field or have an error in one of them.
Entries in light color have a minor error. When you click on a colored entry, the corresponding error is displayed at the bottom of the window.
Note that an entry may have more than one error.

When a paper is linked to an entry, a small PDF icon appears on the left of the of the row of the corresponding entry.
Double-click on the row to open the file.



## Editing an entry

When an entry is selected from the list, its content is displayed at the bottom left of the window.
You can edit each field of the selected entry or the BibTeX directly.
BibTeX entries must be specified in a [valid syntax](#syntax).
When you are done modifying the text, click on Update to apply the changes to the entry.

The fields of the entry are separated between required, optional, and additional fields depending on the entry type (article, inproceedings, etc.).
A missing or erroneous required field will notify an error: entry validation will result in red.
A transgression to the [BibTeX validation rules](http://www.openoffice.org/bibliographic/bibtex-defs.html) will notify a warning: entry validation will result in yellow.
The status bar at the bottom left displays provides more information on the transgressed rule when the entry is selected. 

The additional fields are not part of the BibTeX standard, but they allow you to store more information about each entry.
- `Annote` is the only field supported by BibTeX to add arbitrary notes and comments.
- `Abstract` can be used to store the abstract of the reference.
- `Doi` is the [Digital Object Identifier](https://www.doi.org/) of the reference. All the following are valid and equivalent: `https://doi.org/10.1007/s10270-011-0205-0`    `http://dx.doi.org/10.1007/s10270-011-0205-0`   `10.1007/s10270-011-0205-0`.
- `Paper` is the internal field used by BiBler to store the path or URL to the manuscript of the entry. It is automatically populated if a `Doi` is specified.


## Syntax and validation rules <a name="syntax"></a>

The BibTeX validation rules are described [here](http://www.openoffice.org/bibliographic/bibtex-defs.html).

The general format of a BibTeX entry is:
```
@ENTRYTYPE{key,
  field1 = {value1},
  field2 = {value2}
}
```

White spaces are ignored.
Comments starting with `%` are ignored.
You can use curly brackets `{ }` or double quotes `" "` for values.
If you do not provide a key, make sure the following comma is there.
Here is an example of an article appearing in a journal or magazine:
```
@ARTICLE{article,
  author = {Lastname1, Firstname1 and Lastname2, Firstname2},
  journal = {The name of the journal},
  title = {The title of the work},
  year = {1993},
  month = {aug},
  note = {An optional note},
  number = {2},
  pages = {201--213},
  volume = {4}
}
```

Click on the following link to see some [BibTeX examples](https://verbosus.com/bibtex-style-examples.html).
However, note that some of their fields have values not specified between curly brackets or double quotes, which is invalid.
