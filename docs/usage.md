# Usage

## Basics

Tabs are created, using a `tab` directive. Consecutive `tab` directives create a single set of tabs.

```rst
This is text before the tabs.

.. tab:: One

   One is an interesting number.

.. tab:: Two

   Two is the even prime.

.. tab:: Three

   Three is an odd prime.

.. tab:: Four

   Four is not a perfect number.

This is text after the tabs, which seems to flow right through, which avoids breaking the flow of the document.
```

This is text before the tabs.

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

This is text after the tabs, which seems to flow right through. There is no visual difference for content that's within a tab vs outside it -- adding tabs doesn't disrupt the flow of the document.

## Multiple Tab Sets

It is possible to start a new set from a tab, by having some content between sets or by providing `:new-set:` option to the `tab` directive.

```rst
.. tab:: One

   One is an interesting number.

.. tab:: Two

   Two is the even prime.

This will break the tab set!

.. tab:: Three

   Three is an odd prime.

.. tab:: Four

   Four is not a perfect number.

.. tab:: Five
   :new-set:

   Five is a nice number.

.. tab:: Six

   Six is also nice.
```

```{eval-rst}
.. tab:: One

   One is an interesting number.

.. tab:: Two

   Two is the even prime.

This will break the tab set!

.. tab:: Three

   Three is an odd prime.

.. tab:: Four

   Four is not a perfect number.

.. tab:: Five
   :new-set:

   Five is a nice number.

.. tab:: Six

   Six is also nice.
```

## Code Tabs

The first code block in a tab content will "join" with the tabs, making things fairly clean for language snippets and OS-based command suggestions.

````{tab} Python
```python
print("Hello World!")
```

It's pretty simple!
````

````{tab} C++
```cpp
#include <iostream>

int main() {
  std::cout << "Hello World!" << std::endl;
}
```

More code, but it works too!
````

## Synchronisation

Tabs across multiple sets are synchronised according to the label, unconditionally. This requires JavaScript to be enabled on the end user's browser and, thus, should be considered a progressive enhancement.

```{hint}
Nearly all usage of tabbed content in documentation is based on something about the user which stays consistent throughout the reading (like their OS, or preferred language etc). That's why this behaviour is unconditional.
```

````{tab} Windows
```console
$ py -m pip install sphinx
```
````

````{tab} Unix (MacOS / Linux)
```console
$ python -m pip install sphinx
```
````

````{tab} Windows
:new-set:
```console
$ make.bat html
```
````

````{tab} Unix (MacOS / Linux)
```console
$ make html
```
````
