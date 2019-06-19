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

def get_data_from_userlists(lines):
    keywords = []
    found_paragraph = False
    started = False
    for line in lines:
        if line.startswith("3.4. Userlists"):
            found_paragraph = True
            continue
        if line.startswith("3.5. Peers"):
            break
        if found_paragraph:
            if line.startswith("userlist <listname>"):
                started = True
        if started:
            stripped = line.strip()
            if stripped and not line.startswith(" "):
                keywords.append(stripped.split()[0])
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
        if line.startswith("3.7. Programs"):
            break
        if found_paragraph:
            if line.startswith("mailers <mailersect>"):
                started = True
        if started:
            stripped = line.strip()
            if stripped and not line.startswith(" "):
                keywords.append(stripped.split()[0])
    return keywords

def get_data_from_programs(lines):
    keywords = []
    found_paragraph = False
    started = False
    for line in lines:
        if line.startswith("3.7. Programs"):
            found_paragraph = True
            continue
        if line.startswith("4. Proxies"):
            break
        if found_paragraph:
            if line.startswith("program <name>"):
                started = True
        if started:
            stripped = line.strip()
            if stripped and not line.startswith(" "):
                keywords.append(stripped.split()[0])
    return keywords

def get_data_from_resolvers(lines):
    keywords = []
    found_paragraph = False
    started = False
    for line in lines:
        if line.startswith("5.3.2. The resolvers section"):
            found_paragraph = True
            continue
        if line.startswith("6. HTTP header manipulation"):
            break
        if line.startswith("A resolvers section accept the following parameters:"):
            continue
        if found_paragraph:
            if line.startswith("resolvers <resolvers id>"):
                started = True
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
            if line.startswith("5.2"):
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

def get_data_from_converters(lines):
    keywords = []
    found_paragraph = False
    started = False
    for line in lines:
        if line.startswith("7.3.1. Converters"):
            found_paragraph = True
            continue
        if line.startswith("7.3.2. Fetching samples from internal states"):
            break
        if found_paragraph:
            if line.startswith("51d.single"):
                started = True
        if started:
            stripped = line.strip()
            if stripped and not line.startswith(" "):
                keyword = stripped.split()[0] # split by space
                keywords.append(keyword.split('(')[0]) # split by opening parentheses
    return keywords

def get_data_from_fetches_internal_state(lines):
    keywords = []
    found_paragraph = False
    started = False
    for line in lines:
        if line.startswith("7.3.2. Fetching samples from internal states"):
            found_paragraph = True
            continue
        if line.startswith("7.3.3. Fetching samples at Layer 4"):
            break
        if found_paragraph:
            if line.startswith("always_false"):
                started = True
        if started:
            stripped = line.strip()
            if stripped and not line.startswith(" "):
                keyword = stripped.split()[0] # split by space
                keywords.append(keyword.split('(')[0]) # split by opening parentheses
    return keywords

def get_data_from_fetches_layer4(lines):
    keywords = []
    found_paragraph = False
    started = False
    for line in lines:
        if line.startswith("7.3.3. Fetching samples at Layer 4"):
            found_paragraph = True
            continue
        if line.startswith("7.3.4. Fetching samples at Layer 5"):
            break
        if found_paragraph:
            if line.startswith("bc_http_major"):
                started = True
        if started:
            stripped = line.strip()
            if stripped and not line.startswith(" "):
                keyword = stripped.split()[0] # split by space
                keywords.append(keyword.split('(')[0]) # split by opening parentheses
    return keywords

def get_data_from_fetches_layer5(lines):
    keywords = []
    found_paragraph = False
    started = False
    for line in lines:
        if line.startswith("7.3.4. Fetching samples at Layer 5"):
            found_paragraph = True
            continue
        if line.startswith("7.3.5. Fetching samples from buffer contents"):
            break
        if found_paragraph:
            if line.startswith("51d.all"):
                started = True
        if started:
            stripped = line.strip()
            if stripped and not line.startswith(" "):
                keyword = stripped.split()[0] # split by space
                keywords.append(keyword.split('(')[0]) # split by opening parentheses
    return keywords

def get_data_from_fetches_layer6(lines):
    keywords = []
    found_paragraph = False
    started = False
    for line in lines:
        if line.startswith("7.3.5. Fetching samples from buffer contents"):
            found_paragraph = True
            continue
        if line.startswith("7.3.6. Fetching HTTP sample"):
            break
        if found_paragraph:
            if line.startswith("payload"):
                started = True
        if started:
            stripped = line.strip()
            if stripped and not line.startswith(" "):
                keyword = stripped.split()[0] # split by space
                keywords.append(keyword.split('(')[0]) # split by opening parentheses
    return keywords

def get_data_from_fetches_layer7(lines):
    keywords = []
    found_paragraph = False
    started = False
    for line in lines:
        if line.startswith("7.3.6. Fetching HTTP sample"):
            found_paragraph = True
            continue
        if line.startswith("7.4. Pre-defined ACLs"):
            break
        if found_paragraph:
            if line.startswith("base"):
                started = True
        if started:
            stripped = line.strip()
            if stripped and not line.startswith(" "):
                keyword = stripped.split()[0] # split by space
                keywords.append(keyword.split('(')[0]) # split by opening parentheses
    return keywords

def get_data_from_http_request(lines):
    keywords = []
    found_paragraph = False
    started = False
    for line in lines:
        if line.startswith("http-request <action>"):
            found_paragraph = True
            continue
        if found_paragraph:
            if line.startswith("http-request"):
                started = True
            if line.startswith("http-response <action>"):
                break
            if started:
                stripped = line.strip()
                if stripped and not line.startswith(" "):
                    keyword = stripped.split()[1] # split by space
                    keywords.append(keyword.split('(')[0]) # split by opening parentheses
    return keywords

def get_data_from_http_response(lines):
    keywords = []
    found_paragraph = False
    started = False
    for line in lines:
        if line.startswith("http-response <action>"):
            found_paragraph = True
            continue
        if found_paragraph:
            if line.startswith("http-response"):
                started = True
            if line.startswith("http-reuse"):
                break
            if started:
                stripped = line.strip()
                if stripped and not line.startswith(" "):
                    keyword = stripped.split()[1] # split by space
                    keywords.append(keyword.split('(')[0]) # split by opening parentheses
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

    userlists_options = list(set(get_data_from_userlists(lines)))
    userlists_options.sort()

    peers_options = list(set(get_data_from_peers(lines)))
    peers_options.sort()

    mailers_options = list(set(get_data_from_mailers(lines)))
    mailers_options.sort()

    programs_options = list(set(get_data_from_programs(lines)))
    programs_options.sort()

    resolvers_options = list(set(get_data_from_resolvers(lines)))
    resolvers_options.sort()

    double_first = list(set(double_params.keys()))
    double_first.sort()

    double_second = list(set(chain.from_iterable(double_params.values())))
    double_second.sort()

    bind_options = list(set(get_data_from_bind(lines)))
    bind_options.sort()

    server_options = list(set(get_data_from_server(lines)))
    server_options.sort()

    http_request_options = list(set(get_data_from_http_request(lines)))
    http_request_options.sort()

    http_response_options = list(set(get_data_from_http_response(lines)))
    http_response_options.sort()

    converters = list(set(get_data_from_converters(lines)))
    converters.sort()

    internal_state_fetches = list(set(get_data_from_fetches_internal_state(lines)))
    internal_state_fetches.sort()

    layer4_fetches = list(set(get_data_from_fetches_layer4(lines)))
    layer4_fetches.sort()

    layer5_fetches = list(set(get_data_from_fetches_layer5(lines)))
    layer5_fetches.sort()

    layer6_fetches = list(set(get_data_from_fetches_layer6(lines)))
    layer6_fetches.sort()

    layer7_fetches = list(set(get_data_from_fetches_layer7(lines)))
    layer7_fetches.sort()

    keywords_string = r"^\\s*({0})\\b".format("|".join(keywords))
    global_keywords_string = r"^\\s*({0})\\b".format("|".join(global_keywords))
    double_first_string = r"^\\s*({0})\\b".format("|".join(double_first))
    double_second_string = r"\\s+({0})(?=\\s+|$)".format("|".join(double_second))
    server_options_string = r"\\s+({0})(?=\\s+|$)".format("|".join(server_options))
    http_request_options_string = r"\\s+({0})(?=\\s+|$)".format("|".join(http_request_options))
    http_response_options_string = r"\\s+({0})(?=\\s+|$)".format("|".join(http_response_options))
    bind_options_string = r"\\s+({0})(?=\\s+|$)".format("|".join(bind_options))
    mailers_options_string = r"\\s+({0})(?=\\s+|$)".format("|".join(mailers_options))
    userlists_options_string = r"\\s+({0})(?=\\s+|$)".format("|".join(userlists_options))
    peers_options_string = r"\\s+({0})(?=\\s+|$)".format("|".join(peers_options))
    programs_options_string = r"\\s+({0})(?=\\s+|$)".format("|".join(programs_options))
    resolvers_options_string = r"\\s+({0})(?=\\s+|$)".format("|".join(resolvers_options))
    converters_string = r"\\s+({0})(?=\\s+|$)".format("|".join(converters))
    internal_state_fetches_string = r"\\s+({0})(?=\\s+|$)".format("|".join(internal_state_fetches))
    layer4_fetches_string = r"\\s+({0})(?=\\s+|$)".format("|".join(layer4_fetches))
    layer5_fetches_string = r"\\s+({0})(?=\\s+|$)".format("|".join(layer5_fetches))
    layer6_fetches_string = r"\\s+({0})(?=\\s+|$)".format("|".join(layer6_fetches))
    layer7_fetches_string = r"\\s+({0})(?=\\s+|$)".format("|".join(layer7_fetches))

    with open(args.template, "r") as f:
        template = f.read()

    output = template \
        .replace("{keywords}", keywords_string) \
        .replace("{global_keywords}", global_keywords_string) \
        .replace("{double_first}", double_first_string) \
        .replace("{double_second}", double_second_string) \
        .replace("{server_options}", server_options_string) \
        .replace("{http_request_options}", http_request_options_string) \
        .replace("{http_response_options}", http_response_options_string) \
        .replace("{bind_options}", bind_options_string) \
        .replace("{mailers_options}", mailers_options_string) \
        .replace("{userlists_options}", userlists_options_string) \
        .replace("{peers_options}", peers_options_string) \
        .replace("{programs_options}", programs_options_string) \
        .replace("{resolvers_options}", resolvers_options_string) \
        .replace("{converters}", converters_string) \
        .replace("{internal_state_fetches}", internal_state_fetches_string) \
        .replace("{layer4_fetches}", layer4_fetches_string) \
        .replace("{layer5_fetches}", layer5_fetches_string) \
        .replace("{layer6_fetches}", layer6_fetches_string) \
        .replace("{layer7_fetches}", layer7_fetches_string)

    with open(args.out, "w") as f:
        f.write(output)

if __name__ == "__main__":
    main()
