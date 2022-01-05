import pytest
import os


@pytest.fixture(scope='session')
def django_settings_env_ready():
    os.environ.setdefault('ABIR_USE_TZ:json', 'false')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')


def test_django_settings(django_settings_env_ready):
    from django.conf import settings
    assert settings.CACHE['default']['BACKEND'] == 'django_redis.cache.RedisCache', '替换失败'
    assert settings.DATABASES['default']['DB_NAME'] == 'abir', '更新失败'
    assert settings.LOGGING['loggers']['django']['level'] == 'DEBUG', '更新失败'
    assert settings.USE_TZ is False, 'env优先失败'


def test_custom_project():
    from testsuites import conf_module
    assert conf_module.LOGGING['loggers']['django']['level'] == 'DEBUG', '错误的配置'
    assert conf_module.DEBUG is True, '错误的配置'
