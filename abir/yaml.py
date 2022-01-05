"""Json/Yaml @Jone"""
import logging
import sys
import os
from .attributes import add_attr


logger = logging.getLogger('abir')


def get_loader(syntax):
    loader = None
    kwargs = {}
    try:
        module = __import__(syntax)
        loader = module.load
        if hasattr(module, "FullLoader"):
            kwargs = {'Loader': getattr(module, "FullLoader")}
    except ImportError as ex:
        logger.error('模块不存在 "%s": %s', syntax, ex)
    except AttributeError as ex:
        logger.error('Loader "%s" 不存在 "load" 方法: %s', syntax, ex)
    return loader, kwargs


def get_settings_dir(settings):
    if hasattr(settings, "__file__"):
        path = settings.__file__
    elif hasattr(settings, "__module__"):
        path = sys.modules[settings.__module__].__file__
    else:
        path = os.getcwd()
    return os.path.dirname(path)


def find_files(base_dir, syntax):
    return [i for i in [f'{base_dir}/config.{syntax}'] if os.path.exists(i)]


def load_attributes(attributes, conf_files, loader, kwargs, skip_exist=False):
    for filename in conf_files:
        with open(filename, "r") as fileObj:
            try:
                data = loader(fileObj, **kwargs)
            except Exception as ex:
                logger.error('配置文件载入失败 "%s": %s', filename, ex)
                return
        if not isinstance(data, dict):
            logger.error(
                '"%s" 应提供 dict 类型: %s',
                filename,
                type(data)
            )
            return
        for name, value in data.items():
            if not (skip_exist and name in attributes):
                add_attr(attributes, name, value)
