# Abir--Python项目配置读取方案，yaml/environ

## 安装
```shell
pip install abir
```

## 快速上手
#### django project

1. 在 `settings.py` 底部添加

```python
import abir  # at the top of settings.py

# another settings

abir.load()
```

2. 在项目首页添加`configure.yaml`
```yaml
DATABASES.default.ENGINE: 'django.db.backends.postgresql'
DATABASES.default.NAME: 'db_name'
CACHE:
  default:
    BACKEND: 'django_redis.cache.RedisCache'
    LOCATION: 'redis://127.0.0.1:6379/1'
    OPTIONS:
      CLIENT_CLASS: 'django_redis.client.DefaultClient'
LANGUAGE_CODE: 'zh-CN'
USE_TZ: true
ALLOWED_HOSTS:
  - *
```
⚠️ 注意：dot`.`将会查询`settings.py`，并更新查询路径下的值。 

3. 启动服务。
```shell
python manmage.py runserver
# or wsgi
```

## environment
```shell
ABIR_USE_TZ:json=false
ABIR_LANGUAGE_CODE=es-us
```
