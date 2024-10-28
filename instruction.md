# README - Инструкция по настройке почтового сервера

## Описание
Этот файл содержит инструкции по настройке почтового сервера. Включены шаги для установки и настройки Postfix, Dovecot, DKIM, SPF, DMARC, и антивирусной/антиспам фильтрации (ClamAV и SpamAssassin). Это руководство ориентировано на использование виртуальной машины на VirtualBox.

## Предварительные требования
- Установленная виртуальная машина с Linux (Ubuntu или CentOS) на VirtualBox
- Права суперпользователя на сервере

## Шаги для выполнения задач

### 1. Обновление системы и установка необходимых пакетов

Обновите систему и установите необходимые пакеты:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install postfix dovecot-core dovecot-imapd dovecot-pop3d opendkim opendkim-tools spamassassin clamav-daemon -y
```

### 2. Настройка Postfix

Измените конфигурацию Postfix в файле `/etc/postfix/main.cf`:

```ini
myhostname = mail.local
mydomain = local
inet_interfaces = all
mydestination = $myhostname, $mydomain, localhost.localdomain, localhost
```

Перезапустите Postfix, чтобы применить изменения:

```bash
sudo systemctl restart postfix
```

### 3. Настройка Dovecot

Измените конфигурацию Dovecot в файле `/etc/dovecot/conf.d/10-mail.conf`:

```ini
mail_location = maildir:~/Maildir
```

Создайте директорию Maildir для каждого пользователя:

```bash
sudo -u username maildirmake /home/username/Maildir
```

Перезапустите Dovecot:

```bash
sudo systemctl restart dovecot
```

### 4. Настройка OpenDKIM

Настройте OpenDKIM, отредактировав файл `/etc/opendkim.conf`:

```ini
AutoRestart             Yes
AutoRestartRate         10/1h
Syslog                  Yes
UMask                   002
Domain                  mail.local
KeyFile                 /etc/opendkim/keys/mail.local/mail.private
```

Перезапустите OpenDKIM:

```bash
sudo systemctl restart opendkim
```

### 5. Проверка работы почтового сервера

- Убедитесь, что Postfix и Dovecot работают корректно:
  ```bash
  sudo systemctl status postfix
  sudo systemctl status dovecot
  ```
- Используйте команду `swaks` для тестирования отправки писем:
  ```bash
  swaks --to user1@mail.local --from root@mail.local --server mail.local
  ```

### 6. Проверка входящих писем

- Для пользователей с `Maildir` письма будут находиться в директории `/home/username/Maildir/new`.
- Используйте следующую команду для просмотра письма:
  ```bash
  cat /home/username/Maildir/new/имя_файла
  ```
