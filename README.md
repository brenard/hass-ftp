# FTP Backup agent for Home-Assistant

This a _custom component_ for [Home Assistant](https://www.home-assistant.io/).
This integration allows you to store your backups on FTP server.

**Note:** This integration was initially based on official Home Assistant
[webdav](https://www.home-assistant.io/integrations/webdav/) integration.

## Installation

### Using HACS

Firstly, you have to add the following custom repository :

- Repository : `https://github.com/brenard/hass-ftp`
- Category : _Integration_

After, click on _Explore & download repositories_, search and install _FTP_
integration. Finally, go to _Settings_, _Devices & services_, click on _+ Add integration_ button
and search for _FTP_.

### Manually

Put the `custom_components/ftp` directory in your Home Assistant `custom_components` directory
and restart Home Assistant. You can now add this integration (look for _"FTP"_) and provide the
required connection information to your FTP server.

**Note:** The `custom_components` directory is located in the same directory of the
`configuration.yaml`. If it doesn't exists, create it.

## Run development environment

A development environment is provided with this integration if you want to contribute. The `manage`
script at the root of the repository permit to create and start a Home Assistant docker container
with a pre-installation of this integration (linked to sources).

Start by create the container by running the command `./manage create` and start it by running
`./manage start` command. You can now access to Home Assistant web interface on
[http://localhost:8123](http://localhost:8123) and follow the initialization process of the Home
Assistant instance.

## Debugging

To enable debug log, edit the `configuration.yaml` file and locate the `logger` block. If it does not
exists, add it with the following content :

```yaml
logger:
  default: warn
  logs:
    custom_components.ftp: debug
    aioftp.client: debug
```

Don't forget to restart Home Assistant after.

**Note:** In development environment and you will be able to follow docker container logs by running
the `./manage logs` command.

## Roadmap

- Manually trigger an exceptional heating cycle (by temporarily modifying the timer parameter)
