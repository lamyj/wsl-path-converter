import re

def convert_w(linux_path):
    """ Convert a Linux path to a Windows path. """

    windows_roots = parse_mounts()[1]
    linux_root = find_root(windows_roots, linux_path, "/")
    linux_leaf = linux_path[len(linux_root):]

    windows_root = windows_roots[linux_root]
    windows_leaf = linux_leaf.replace("/", "\\")

    return "".join([windows_root, windows_leaf])

def convert_m(linux_path):
    """ Convert a Linux path to a Windows path with forward slashes. """
    windows_roots = parse_mounts()[1]
    linux_root = find_root(windows_roots, linux_path, "/")
    linux_leaf = linux_path[len(linux_root):]
    windows_root = windows_roots[linux_root]

    return "".join([windows_root, linux_leaf])

def convert_u(windows_path):
    """ Convert an absolute Windows path to a Linux path. """

    linux_roots = parse_mounts()[0]
    windows_root = find_root(linux_roots, windows_path, "\\")
    windows_leaf = windows_path[len(windows_root):]

    if not windows_leaf.startswith("\\"):
        raise Exception("Cannot convert relative Windows path")

    linux_root = linux_roots[windows_root]
    linux_leaf = windows_leaf.replace("\\", "/")

    return "".join([linux_root, linux_leaf])

def guess_converter(path):
    """ Guess the best converter (to Windows with backslashes or to Linux) for
        a path.
    """

    if re.match(r"^[a-zA-Z]:", path):
        # Drive letter and colon: Windows path
        return convert_u
    elif re.match(r"^\\", path):
        # UNC path: convert to Linux
        return convert_u
    elif re.match(r"^/[^/]", path):
        # Slash followed by non-slash: Linux path
        return convert_w
    else:
        raise Exception("Could not guess converter for \"{}\"".format(path))

def parse_mounts():
    """ Return a map of Windows roots to their corresponding Linux root and a
        map of Linux roots to their corresponding Windows root.

        >>> linux_roots, windows_roots = parse_mounts()
        >>> linux_roots["C:"]
        '/mnt/c'
        >>> windows_roots["/mnt/c"]
        'C:'
    """
    # Map a Windows root to a Linux root
    linux_roots = {}
    # Map a Linux root to a Windows root
    windows_roots = {}
    
    with open("/proc/mounts", "rb") as fd:
        for line in fd.read().splitlines():
            source, target, type_, _ = line.split(b" ", 3)
            
            if type_ not in (b"drvfs", b"9p"):
                continue
            
            # Decode the string (backslash-escaped octal values)
            source = source.decode("unicode-escape")
            # If the root is a fully qualified drive letter, remove the final "\"
            source = re.sub(r"^([a-zA-Z]:)(\\$)", r"\1", source)
            
            target = target.decode("unicode-escape")
            
            linux_roots[source] = target
            windows_roots[target] = source

    return linux_roots, windows_roots

def find_root(roots, path, separator):
    """ Return the root matching the given path followed by a separator. """

    candidates = [
        x for x in roots
        if path == x or path.startswith("{}{}".format(x, separator))]
    if not candidates:
        raise Exception("No root found for {}".format(path))
    elif len(candidates) > 1:
        raise Exception("Multiple roots found for {}".format(path))

    return candidates[0]
