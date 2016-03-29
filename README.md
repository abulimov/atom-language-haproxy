# HAProxy syntax support in Atom

Adds syntax highlighting to [HAProxy](http://www.haproxy.org) configuration files in Atom.
Based on now unavailable [HAProxy.tmbundle](https://github.com/williamsjj/HAProxy.tmbundle).

Syntax highlighting is partially auto-generated with script `generate.py`.
This script parses *configuration.txt* from [haproxy.org](http://www.haproxy.org/#docs)
and generates *haproxy.cson* from *haproxy.cson.template*.
