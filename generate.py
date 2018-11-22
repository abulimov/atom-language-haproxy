#!/usr/bin/env python3
# quick-and-dirty script to generate haproxy.cson from haproxy docs

import argparse
from itertools import chain

def get_data_from_global(lines):
    keywords = []
    started = False
    for line in lines:
        if line.startswith("3. Global parameters"):
            started = True
            continue
        if line.startswith("3.1. Process management and security"):
            break
        if started:
            stripped = line.strip()
            if stripped.startswith("- "):
                keywords.append(stripped.lstrip("- "))
    return keywords

def get_data_from_peers(lines):
    keywords = []
    found_paragraph = False
    started = False
    for line in lines:
        if line.startswith("3.5. Peers"):
            found_paragraph = True
            continue
        if line.startswith("3.6. Mailers"):
            break
        if found_paragraph:
            if line.startswith("peers <peersect>"):
                started = True
                continue
        if started:
            stripped = line.strip()
            if stripped and not line.startswith(" "):
                keywords.append(stripped.split()[0])
    return keywords

def get_data_from_mailers(lines):
    keywords = []
    found_paragraph = False
    started = False
    for line in lines:
        if line.startswith("3.6. Mailers"):
            found_paragraph = True
            continue
        if line.startswith("3.7. Modules"):
            break
        if found_paragraph:
            if line.startswith("mailers <mailersect>"):
                started = True
                continue
        if started:
            stripped = line.strip()
            if stripped and not line.startswith(" "):
                keywords.append(stripped.split()[0])
    return keywords

def get_data_from_table(lines):
    keywords = []
    double = []
    next_words = ["(deprecated)", "(*)", "-", "X"]
    started = False
    for line in lines:
        if line.startswith("4.1. Proxy keywords matrix"):
            started = True
            continue
        if line.startswith("4.2. Alphabetically sorted keywords reference"):
            break
        if started:
            splitted = line.split()
            if len(splitted) < 3:
                continue
            if splitted[1] in next_words:
                keywords.append(splitted[0])
            elif splitted[2] in next_words:
                double.append(splitted[0] + " " + splitted[1])
    return keywords, double

def get_data_from_bind(lines):
    keywords = []
    found_paragraph = False
    started = False
    for line in lines:
        if line.startswith("5.1. Bind options"):
            found_paragraph = True
            continue
        if found_paragraph:
            if line.startswith("The currently supported settings are the following ones"):
                started = True
                continue
            if line.startswith("5.2. Server and default-server options"):
                break
            if started:
                stripped = line.strip()
                if not line.startswith(" "):
                    if stripped:
                        keywords.append(stripped.split()[0])
    return keywords

def get_data_from_server(lines):
    keywords = []
    found_paragraph = False
    started = False
    for line in lines:
        if line.startswith("5.2. Server and default-server options"):
            found_paragraph = True
            continue
        if found_paragraph:
            if line.startswith("The currently supported settings are the following ones"):
                started = True
                continue
            if line.startswith("5.3"):
                break
            if started:
                stripped = line.strip()
                if not line.startswith(" "):
                    if stripped:
                        keywords.append(stripped.split()[0])
    return keywords

def parse_doubles(double):
    m = dict()
    for d in double:
        splitted = d.split()
        if splitted[0] in m:
            m[splitted[0]].append(splitted[1])
        else:
            m[splitted[0]] = [splitted[1]]
    return m

def main():
    parser = argparse.ArgumentParser(description='Generate HAProxy grammars for Atom.')
    parser.add_argument('-o', '--out', dest='out',
                        default="haproxy.cson",
                        help='write grammars to this file')
    parser.add_argument('-t', '--template', dest='template',
                        default="haproxy.cson.template",
                        help='grammars template file')
    parser.add_argument('-d', '--docs', dest='docs',
                        default="configuration.txt",
                        help='HAProxy docs file')

    args = parser.parse_args()
    with open(args.docs, "r") as f:
        lines = f.readlines()

    keywords, double = get_data_from_table(lines)
    global_keywords = get_data_from_global(lines)
    double_params = parse_doubles(double)

    keywords.sort()
    global_keywords.sort()

    peers_options = list(set(get_data_from_peers(lines)))
    peers_options.sort()

    mailers_options = list(set(get_data_from_mailers(lines)))
    mailers_options.sort()

    double_first = list(set(double_params.keys()))
    double_first.sort()

    double_second = list(set(chain.from_iterable(double_params.values())))
    double_second.sort()

    bind_options = list(set(get_data_from_bind(lines)))
    bind_options.sort()

    server_options = list(set(get_data_from_server(lines)))
    server_options.sort()

    keywords_string = r"^\\s*({0})\\b".format("|".join(keywords))
    global_keywords_string = r"^\\s*({0})\\b".format("|".join(global_keywords))
    double_first_string = r"^\\s*({0})\\b".format("|".join(double_first))
    double_second_string = r"\\s+({0})(?=\\s+|$)".format("|".join(double_second))
    server_options_string = r"\\s+({0})(?=\\s+|$)".format("|".join(server_options))
    bind_options_string = r"\\s+({0})(?=\\s+|$)".format("|".join(bind_options))
    mailers_options_string = r"\\s+({0})(?=\\s+|$)".format("|".join(mailers_options))
    peers_options_string = r"\\s+({0})(?=\\s+|$)".format("|".join(peers_options))

    with open(args.template, "r") as f:
        template = f.read()

    output = template \
        .replace("{keywords}", keywords_string) \
        .replace("{global_keywords}", global_keywords_string) \
        .replace("{double_first}", double_first_string) \
        .replace("{double_second}", double_second_string) \
        .replace("{server_options}", server_options_string) \
        .replace("{bind_options}", bind_options_string) \
        .replace("{mailers_options}", mailers_options_string) \
        .replace("{peers_options}", peers_options_string)

    with open(args.out, "w") as f:
        f.write(output)

if __name__ == "__main__":
    main()
