# Sphinx Inline Tabs

```{include} ../README.md
:start-after: <!-- start-include-here -->
:end-before: <!-- end-include-here -->
```

## Demo

```{tab} One
One is an interesting number.
```

```{tab} Two
Two is the even prime.
```

```{tab} Three
Three is an odd prime.
```

```{tab} Four
Four is not a perfect number.
```

This is text after the tabs, which seems to flow right through, which avoids breaking the flow of the document. And, if JavaScript is enabled, the next set of tabs will be synchronised.

````{tab} One
```
print(1)
```
````

````{tab} Two
```
print(2)
```
````

````{tab} Three
```
print(3)
```
````

````{tab} Four
```
print(4)
```
````

To know more, take a look at the [Usage](usage) documentation of this project.

```{toctree}
:hidden:
usage
```

```{toctree}
:caption: Useful Links
:hidden:
PyPI page <https://pypi.org/project/sphinx-inline-tabs>
GitHub Repository <https://github.com/pradyunsg/sphinx-inline-tabs>
```
