import getpass
import multiprocessing
import platform


def bootstrap_attributes():
    """初始化配置项，并添加默认配置项"""
    result = {}
    add_attr(result, 'CPU_COUNT', multiprocessing.cpu_count())
    add_attr(result, 'SHELL_USER', getpass.getuser())

    for name in ['machine', 'node', 'processor', 'release', 'system']:
        method = getattr(platform, name)
        add_attr(result, 'OS_{0}'.format(name.upper()), method())

    return result


def add_attr(attributes, name, value):
    """添加配置项"""
    attributes[name] = {
        'value': value
    }
