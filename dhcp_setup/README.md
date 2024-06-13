# Настройка DHCP сервера

## Мои файлы

Директория `backup_files` - изначальные файлы с моего ПК

Директория `changed_files` - файлы настройки с моего ПК

## Установка библиотек

Установка библиотеки dhcp сервера

```(bash)
sudo apt-get update
sudo apt-get install isc-dhcp-server
```

## Определить ip адрес сетевого интерфейса

Первоначально требуется соединить два устройства с помощью кабеля `ethernet`.

Для определения `ip` адреса можно использовать следующие команды

```bash
ip a
```

Пример вывода

```bash
3: enx00e04c360050: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 00:e0:4c:36:00:50 brd ff:ff:ff:ff:ff:ff
    inet 169.254.234.211/16 brd 169.254.255.255 scope link noprefixroute enx00e04c360050
       valid_lft forever preferred_lft forever
    inet6 fe80::2e0:4cff:fe36:50/64 scope link 
       valid_lft forever preferred_lft forever
```

При использовании данной команды, в выводе, нам необходимо увидеть параметр `inet` у сетевого интерфейса, если его нету, потребуется добавить настройки, чтобы ОС самостоятельно определила ему `ip` из заранее заготовленного списка адресов. Алгоритм добавления настроек будет рассмотрен в следующем параграфе.

Как мы видим в текущем примере нам выделили `ip` адрес из специального региона `inet 169.254.234.211/16`.

Из полученного адреса, нужно выделить `subnet` и `netmask`.

`netmask` можно получить из `ip` адреса, а именно после слэша мы видим сколько битов используется в маске

```(bash)
inet 169.254.234.211/ ->16<-  ==> 16 битов
netmask = 255.255.0.0
```

Следовательно, чтобы получить 'subnet' нужно:

```(bash)
subnet = ip & netmask = 169.254.234.211 & 255.255.0.0 = 169.254.0.0
```

## Присвоить сетевому интерфейсу статический ip

Менеджер сетевых интерфейсов в разных система может быть различный

### 1. ifupdown (not tested)

Проверить используется ли он можно командой

```bash
ls /etc/network/interfaces
```

Если директория есть и в ней есть файл, значит используется он.

ChatGPT ниже:

Нужно создать файл конфигурации для сетевого интерфейса в каталоге `/etc/network/interfaces.d/`.

```bash
# /etc/network/interfaces.d/enx00e04c360050

auto enx00e04c360050
iface enx00e04c360050 inet dhcp
```

Вставьте содержимое и сохраните файл. После этого перезапустите сетевой интерфейс или перезагрузите систему:

```bash
sudo ifdown enx00e04c360050
sudo ifup enx00e04c360050
```

### 2. netplan

В дистрибутивах Ubuntu с GUI обычно используется библиотека `netplan`

Чтобы добавить новое правило нужно:

1. Перейти в директорию `cd /etc/netplan`
2. Просмотреть файлы `ls -la`

Пример вывода

```bash
01-network-manager-all.yaml  90-NM-1dd12b67-a47e-402b-a99b-5486db4322f4.yaml  90-NM-677e1a26-ad2d-489c-a07c-edc1b9a9014a.yaml
90-NM-5cdfc0eb-a240-4981-995a-092a363f4f74.yaml  90-NM-9d5495b0-732b-3360-84ab-163fd483de08.yaml
```

3. Открыть файл `01-network-manager-all.yaml` либо создать новый в стиле `02-name.yaml`

И добавить аналогичную настройку

```yaml
# 02-ethernet-locallink.yaml

network:
   ethernets:
     enx00e04c360050:
       dhcp4: no
```

4. `sudo netplan apply`

## Настройка файлов конфигурации DHCP

Перед началом работы необходимо создать файлы бэкапа, вот как можно сохранить файлы.

```bash
sudo mv /etc/dhcp/dhcpd.conf{,.backup}
```

Перейдем к настройке.

```yaml
# /etc/default/isc-dhcp-server

 # Defaults for isc-dhcp-server (sourced by /etc/init.d/isc-dhcp-server)
 
 # Path to dhcpd's config file (default: /etc/dhcp/dhcpd.conf).
 #DHCPDv4_CONF=/etc/dhcp/dhcpd.conf
 #DHCPDv6_CONF=/etc/dhcp/dhcpd6.conf
 
 # Path to dhcpd's PID file (default: /var/run/dhcpd.pid).
 #DHCPDv4_PID=/var/run/dhcpd.pid
 #DHCPDv6_PID=/var/run/dhcpd6.pid
 
 # Additional options to start dhcpd with.
 #   Don't use options -cf or -pf here; use DHCPD_CONF/ DHCPD_PID instead
 #OPTIONS=""
 
 # On what interfaces should the DHCP server (dhcpd) serve DHCP requests?
 #   Separate multiple interfaces with spaces, e.g. "eth0 eth1".
 INTERFACESv4="enx00e04c360050"
 INTERFACESv6=""
```

```yaml
# /etc/dhcp/dhcpd.conf

 INTERFACESv4="enx00e04c360050";
 
 authoritative;
 subnet 169.254.0.0 netmask 255.255.0.0 {
   range 169.254.0.2 169.254.255.254;
   option routers 169.254.0.1;
   option broadcast-address 169.254.255.255;
   default-lease-time 600;
   max-lease-time 7200;
 }
```

`INTERFACESv4` в файле `/etc/dhcp/dhcpd.conf` я вставил на всякий случай.

## Как проверить

Чтобы запустить сервис нужно использовать команду.

```bash
sudo systemctl restart isc-dhcp-server.service
```

Чтобы проверить статус нужно использовать команду

```bash
sudo systemctl status isc-dhcp-server.service
```

Тогда на ПК клиента нужно написать следующую команду (UNIX | WSL)

```bash
sudo dhclient -v <interface_name>
```

При удачном запуске, если снова вывести команду `status`, можно увидеть

```bash
● isc-dhcp-server.service - ISC DHCP IPv4 server
     Loaded: loaded (/lib/systemd/system/isc-dhcp-server.service; enabled; preset: enabled)
     Active: active (running) since Mon 2024-01-15 20:46:23 MSK; 1min 38s ago
       Docs: man:dhcpd(8)
   Main PID: 4044 (dhcpd)
      Tasks: 1 (limit: 8697)
     Memory: 24.8M
        CPU: 60ms
     CGroup: /system.slice/isc-dhcp-server.service
             └─4044 dhcpd -user dhcpd -group dhcpd -f -4 -pf /run/dhcp-server/dhcpd.pid -cf /etc/dhcp/dhcpd.conf enx00e04c360050

Jan 15 20:46:23 asus sh[4044]: Listening on LPF/enx00e04c360050/00:e0:4c:36:00:50/169.254.0.0/16
Jan 15 20:46:23 asus sh[4044]: Sending on   LPF/enx00e04c360050/00:e0:4c:36:00:50/169.254.0.0/16
Jan 15 20:46:23 asus sh[4044]: Sending on   Socket/fallback/fallback-net
Jan 15 20:46:23 asus dhcpd[4044]: Sending on   LPF/enx00e04c360050/00:e0:4c:36:00:50/169.254.0.0/16
Jan 15 20:46:23 asus dhcpd[4044]: Sending on   Socket/fallback/fallback-net
Jan 15 20:46:23 asus dhcpd[4044]: Server starting service.
Jan 15 20:46:24 asus dhcpd[4044]: DHCPDISCOVER from b4:2e:99:4f:e0:96 via enx00e04c360050
```

Ниже видно, что мы получили запрос на получение ip от клиентского пк.

```bash
Jan 15 20:46:25 asus dhcpd[4044]: DHCPOFFER on 169.254.0.2 to b4:2e:99:4f:e0:96 (HomePC) via enx00e04c360050
Jan 15 20:46:25 asus dhcpd[4044]: DHCPREQUEST for 169.254.0.2 (169.254.234.211) from b4:2e:99:4f:e0:96 (HomePC) via enx00e04c360050
Jan 15 20:46:25 asus dhcpd[4044]: DHCPACK on 169.254.0.2 to b4:2e:99:4f:e0:96 (HomePC) via enx00e04c360050
```
