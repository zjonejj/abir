import os
import sys
import traceback
import logging

from abir.attributes import bootstrap_attributes
from abir.environ import load_env
from abir.yaml import (
    get_loader,
    get_settings_dir,
    find_files, load_attributes
)


logger = logging.getLogger('abir')


def get_conf_module(module_name=None):
    """获取配置模块"""
    module_name = module_name or os.environ.get('DJANGO_SETTINGS_MODULE') or \
        "{0}.settings".format(os.path.basename(os.path.dirname(
            traceback.extract_stack(limit=3)[0][0]
        )))

    return sys.modules[module_name]


def inject_attr(attributes, conf_module):
    """将attribute添加入config module"""
    for attr in attributes.keys():
        value = attributes[attr]['value']
        if '.' in attr:
            # 嵌套属性 (属性节点在config module里面)
            master_key, *nodes = attr.split(".")
            if not (target := getattr(conf_module, master_key, None)):
                setattr(conf_module, master_key, {})
                target = getattr(conf_module, master_key)
            for key in nodes[0:-1]:
                if key not in target:
                    target[key] = {}
                target = target[key]
            if isinstance(target, dict):
                target[nodes[-1]] = value
        elif ':' not in attr:
            # 有形如 (:raw, :hide, etc) 的属性，不会设置到config_module
            setattr(conf_module, attr, value)


def load(syntax="yaml", conf_module=None, base_dir=None):
    """load properties 主流程"""
    loader, kwargs = get_loader(syntax)

    if isinstance(conf_module, str):
        conf_module = get_conf_module(conf_module)
    elif conf_module is None:
        conf_module = get_conf_module()
    # else:

    # conf_module = conf_module or get_conf_module()
    base_dir = base_dir or os.path.dirname(get_settings_dir(conf_module))
    attributes = bootstrap_attributes()

    load_env(attributes)
    load_attributes(attributes, find_files(base_dir, syntax), loader, kwargs,
                    skip_exist=True)

    inject_attr(attributes, conf_module)
    logger.info('attributes injected %s', attributes)
