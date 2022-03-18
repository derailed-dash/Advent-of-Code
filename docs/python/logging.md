---
title: Logging
tags: 
  - name: Python Logging
    link: https://docs.python.org/3/library/logging.html
---
Rather than simply using `print()` statements, I tend to use the [logging](https://docs.python.org/3/library/logging.html){:target="_blank"} module for generating console output.

It has a number of advantages over `print()` statements. The first is that we can specify a logging threshold `level`. 
- There are various levels, such as DEBUG, INFO, WARN, ERROR.
- When you write a logging statement, you decide the level of that statement.
- Any logging statements that are above the threshold will be printed. But any that are below the threshold will not be printed.
- Thus, if we want to see less logging, we can simply increase the threshold.  And if we want to see more logging, we decrease the threshold.

For example:

```python
import logging

# initialise the Root logger
logging.basicConfig(format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", datefmt='%H:%M:%S')
# now get a named instance of the logger for our application
logger = logging.getLogger(__name__) 

# Set the logging threshold of our logging instance to DEBUG
logger.setLevel(logging.DEBUG) 

# print some stuff
logger.debug("We'll see this.")
logger.info("And this.")

# now set threshold to INFO; everything below INFO is now suppressed
logger.setLevel(logging.INFO) 

# print some more stuff
logger.debug("We will NOT see this.")
logger.info("But we will see this.")
```

The output from the above looks like this:
```text
09:08:46.929:DEBUG:__main__:    We'll see this.
09:08:46.929:INFO:__main__:     And this
09:08:46.929:INFO:__main__:     But we will see this.
```

Note that we must first `import` the `logging` module.

Another advantage is that you can customise what appears in the console messages.  For example, this initial configuration tells the logger to print the time, the logging level, the name of the logger, and then the message.

```python
# It will print the time (including milliseconds), the logging level, and the logger name
logging.basicConfig(format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", datefmt='%H:%M:%S')
```

We can also configure our logger to print logging messages to a file, rather than to the console.  For example:

```python
logging.basicConfig(
        filename='example.log', 
        encoding='utf-8', 
        level=logging.DEBUG, 
        format='%(asctime)s:%(levelname)s:\t%(message)s')
logging.debug('This message should go to the log file')
```

The logging configuration itself can also be placed externalised to a file, rather than coded into the program.

It's worth noting how we can pass varaibles into a logging statement. This is a typical example:

```python
import logging

# setup
logging.basicConfig(format="%(asctime)s.%(msecs)03d:%(levelname)s:%(name)s:\t%(message)s", 
                    datefmt='%H:%M:%S')
logger = logging.getLogger("FooBar-App")
logger.setLevel(logging.INFO)

my_key = "foo"
my_val = "bar"
logger.info("My key is named %s, and it's value is %s", my_key, my_val)
```

Here, each `%s` within the string message itself is a placeholder for a variable.  The variables are passed after the string message, as a comma-separated list.

The output looks like this:

```text
08:41:25.172:INFO:FooBar-App:   My key is named foo, and it's value is bar
```

To wrap up: the Python **logging** module is pretty sophisticated.  I've only touched the surface here. Check the documentation for more details.

