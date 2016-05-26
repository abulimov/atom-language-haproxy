# HAProxy syntax support in Atom

Adds syntax highlighting to [HAProxy](http://www.haproxy.org) configuration files in Atom.
Based on now unavailable [HAProxy.tmbundle](https://github.com/williamsjj/HAProxy.tmbundle).

Syntax highlighting is partially auto-generated with script `generate.py`.
This script parses *configuration.txt* from [haproxy.org](http://www.haproxy.org/#docs)
and generates *haproxy.cson* from *haproxy.cson.template*.

## Updating grammars

### Manual update

Update `grammars/haproxy.cson`. When done, make same changes in
`haproxy.cson.template`, which is used for generating grammars from
HAProxy docs.

### Updating from docs

Make changes in `haproxy.cson.template` or (in case of new HAProxy release)
provide new HAProxy docs.
Download HAProxy *configuration.txt* for latest stable version from
[haproxy.org](http://www.haproxy.org/#docs),
and run `python3 ./generate.py -d path/to/configuration.txt --out grammars/haproxy.cson`.
