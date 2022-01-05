import os
import logging
import json
from .attributes import add_attr


logger = logging.getLogger('abir')
CONF_PRE = 'ABIR_'
_JSON_MARKER = ':json'


def load_env(attributes):
    """
    从环境变量中获取
    """
    for name, value in os.environ.items():
        if name.startswith(CONF_PRE):
            attr = name.replace(CONF_PRE, "")
            if attr.endswith(_JSON_MARKER):
                attr = attr.replace(_JSON_MARKER, "")
                try:
                    value = json.loads(value)
                except json.decoder.JSONDecodeError as exc:
                    logger.error(
                        '对 "%s" JSON 解码失败, 环境变量："%s", %s',
                        value, attr, str(exc)
                    )
            add_attr(attributes, attr, value)
