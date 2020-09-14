# homeassistant使用教程

* [1.在rk3288上下载及安装docker](#index1)
* [2.在rk3288上使用docker下载及运行homeassistant容器](#index2)
* [3.homeassistant配置集成在线编辑](#index3)
* [4.homeassistant配置集成地图](#index4)
* [5.homeassistant配置mqtt](#index5)
* [6.homeassistant配置modbus](#index6)

<span id="index1"></span>

## 在rk3288上下载及安装docker

* 使用官方安装脚本自动安装

```shell script
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
```

* 也可以使用国内 daocloud 一键安装命令：

```shell script
curl -sSL https://get.daocloud.io/docker | sh
```

<span id="index2"></span>

## 在rk3288上使用docker下载及运行homeassistant容器

* docker run -d --name="home-assistant" -v /你的/config路径:/config -v /etc/localtime:/etc/localtime:ro --net=host homeassistant/home-assistant
* 在浏览器中访问 <http://192.168.207.51:8123>，ip为rk3288的地址
* 创建账号密码


<span id="index3"></span>
## homeassistant配置集成在线编辑
* 查看docker 容器 查找出名称为 home-assistant 的 CONTAINER ID
```
 sudo docker ps -a
```
![avatar](./image/docker_ps_a.png)
* 进入容器内部 安装 hass-configurator
```
docker exec -ti 2c0ddfbed370 /bin/bash
pip install hass-configurator
```
![avatar](./image/install_hass_configurator.png)
* 运行插件 hass-configurator
```angular2
hass-configurator &
```
![avatar](./image/run_hass_configurator.png)
* 在home-assistant的配置文件 configuration.yaml 中添加 (这个地方的IP就是 网关的ip，端口是固定的)
```angular2
panel_iframe:
  configurator:
    title: HASS配置器
    icon: mdi:wrench
    url: 'http://192.168.207.234:3218/'
```
![avatar](./image/hass_config.png)
* 重启服务
![avatar](./image/restart_hass_1.png)
![avatar](./image/restart_hass_2.png)

* 怎么编辑配置文件
![avatar](./image/update_settings_1.png)
![avatar](./image/update_settings_2.png)


<span id="index4"></span>

## homeassistant配置集成地图

* 获取高德地图api key
去<https://lbs.amap.com/>高德开放者平台注册用户，并创建Web端（不是Web服务），获取应用的apikey备用。

* 下载插件inkwavemap
在<https://github.com/5high/ha-inkwavemap>下载解压文件，并把解压出来的全放在ha配置根目录下

* 创建并添加长期访问令牌和apiKey
  * 在ha界面上，点击左侧用户名，拉到最下面，创建一个长期密钥；
  * cd到ha配置目录的www/custom_ui/inkwavemap目录下，在LongTimeToken=中添加上一步创建好的长期访问令牌到Bearer 后面，注意中间有一个空格，最终效果如下：

    ```text
    GaodeMapKey="e968872c767507a9504b90418f791b69"
    LongTimeToken="Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI4NzUyNTNlMDE1MTA0YTc1OGJmZjI0NWMxZjg5ZDU1ZCIsImlhdCI6MTYwMDA0NTE2OCwiZXhwIjoxOTE1NDA1MTY4fQ.ob_B8uLFynvYAHyV9AZOYOkkx12BOcI7EMacDgP10so"
    ```

* 重启ha
  * 如果提示如遇到Unauthorized报错，请清理浏览器缓存和cookie之后重新访问。
  * 如遇家庭位置不准确请到<http://www.gpsspg.com/maps.htm>这里获取准确的GPS信息（切记取回谷歌地球的GPS数据），并修改configration.yaml里的家的GPS信息，并重启Home Assistant。

    ```yaml
    homeassistant:
    latitude: 26.024079
    longitude: 119.415892
    #elevation: 430
    unit_system: metric
    time_zone: Asia/Shanghai
    name: Home
    ```


