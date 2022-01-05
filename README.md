# Abir--Python项目配置方案 yaml/environ

## 安装
```shell
pip install abir
```

## 快速上手
#### django project

1. 在 `settings.py` 中添加

```python
import abir  

# other settings

abir.load() # at the end of settings.py
```

2. 在项目根文件夹下添加`config.yaml`

添加后的项目结构如下：

```shell
├── project
│   ├── project
│   |   ├── __init__.py
│   |   ├── asgi.py
│   |   ├── wsgi.py
│   |   ├── urls.py
│   |   ├── settings.py
│   ├── manange.py
│   ├── config.yaml  # 添加到根下
```

在yaml中添加对应的配置项

```yaml
# settings 中已配置，只希望修改部分配置项时，使用 dot 查询并修改：
DATABASES.default.NAME: 'db_name'
DATABASES.default.HOST: 'dh_host'  # 未配置时，会添加配置项
DATABASES.default.PORT: 'port'
DATABASES.default.USER: 'db_user_name'
DATABASES.default.PASSWORD: 'db_password'

# settings中无配置，或已配置，但希望全部替换，不使用 dot 查询：
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
⚠️ dot`.`将会查询`settings.py`，并更新查询路径下的值。 

3. 启动服务。
```shell
python manmage.py runserver
# or wsgi
```



#### 其他python项目

假设项目结构如下：

```shell
├── project
│   ├── packagges
│   ├── modules 
…… 
```

1. 添加config_module.py (module名称可自定义)

   如下添加代码

   ```python
   import abir
   abir.load(base_dir=BASE_DIR, conf_module='conf_module')  
   # 如果config_module不在根下，输入完整查询路径即可，如：project.packageA.moduleB
   # confi_module 也可以是任何可设置property的对象：getattr and setattr
   ```

   

2. 添加config.yaml

   添加后的项目结构如下：

   ```shell
   ├── project
   │   ├── config_module.py
   │   ├── config.yaml # 添加到根下
   ```

3. 执行应用，即可获取配置

   

## environment 通过环境变量来进行配置

⚠️ 环境变量拥有最高优先级：当yaml/settings中存在配置，且环境变量中也存在，优先取环境变量的配置值，即：`environ > yaml > settings`（当`load()`在conf_module末尾调用时）

### 前缀

abir通过前缀 `ABIR_`捕获环境变量。

##### 1. 字符串类型

```shell
ABIR_LANGUAGE_CODE=es-us
```

##### 2. 其他类型

abir读取环境变量时，会识别 `:`定义，当定义为 :json ，将运行 `json.loads`进行值转换，因此可以通过赋值环境变量为json-string的方式，来满足非字符串类型的配置

```shell
ABIR_LANGUAGE_CODE=zh-CN
ABIR_USE_TZ:json=false
ABIR_TIMEOUT:json=20
ABIR_BLACK_UIDS:json=[101,39,847,11]
ABIR_LIFETIME:json={"days": 1, "key": "some-key"}  # 注意 json-string 与 前端书写json的区别。
```

以上配置，将会被abir解读为：

```python
LANGUAGE_CODE='zh-CN'
USE_TZ=False
TIMEOUT=20
BLACK_UIDS=[101,39,847,11]
LIFETIME={'days': 1, 'key': 'some-key'}
```

