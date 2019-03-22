# pyplugins
Plugin system fro python applications

## How to install

If you clone this repo, you can install with below command:

```bash
python setup.py install
```

Also, you can install this package with below command:

```bash
pip install pyplugins
```

## Creating my first plugin

First, you should create a directory with your _.py_ plugins. These plugins **must inherits** from the class **IPlugin** and the class name must be **Plugin**

An example plugin is showed below:

```python

from pyplugins import IPlugin

class Plugin(IPlugin):

    NAME = "My Plugin"
    VERSION = "1.0"
    DESCRIPTION = "This is my first plugin"

    def run(self):
        print("This method will be executed dynamically later")
        # The return will be stored into `PluginLoader`
        return 0
```

# How to use

If you want execute an certain method from each plugin into your plugins dir, you can use below code:

```python
from pyplugins import PluginLoader

loader = PluginLoader(path = "/path/to/my/plugins")

# If no args, will execute the `run` method into each plugin (whitout method params)
loader.run()
```

You can change the method to run

```python
loader.run(method="custom_method")
```

Also, you can set method args
```python
# This code will run `custom_method(foo = bar)` into each plugin
loader.run(method="custom_method", args={"foo": "bar"})
```

# Getting responses

The response from each method will be returned in a dict which will be returned by the _run_ method from _PluginLoader_ class.

For example, suppose you have two files into folder **/tmp/plugins**

```
/tmp/plugins
├── plugin1.py
└── plugin2.py
```


```python
# plugin1.py

from pyplugins import IPlugin

class Plugin(IPlugin):

    NAME = "Plugin 1"
    VERSION = "1.0"
    DESCRIPTION = "Hello world!"

    def run(self):
        return "Plugin 1 output"
```

```python
# plugin2.py

from pyplugins import IPlugin

class Plugin(IPlugin):

    NAME = "Plugin 2"
    VERSION = "0.2"
    DESCRIPTION = "This is a description"

    def run(self):
        return [1,5,8,7]
```

When you execute the _run method_, yoy will get the response (returned via _return_) into a dict:

```python
from pyplugins import PluginLoader

loader = PluginLoader(path = "/tmp/plugins")

responses = loader.run()

# {'Plugin 1': 'Plugin 1 output', 'Plugin 2': [1, 5, 8, 7]}
```

Note that the dict keys are the plugin _NAME_