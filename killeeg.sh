#!/bin/bash
ps axu | grep -E "(pyeeg|myfft)" | awk '{ print $2 }' | xargs kill -SIGKILL 2> /dev/null
