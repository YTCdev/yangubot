# YanguBot
 
YanguBot is a Discord bot that integrates with a WooCommerce store that can help stores engage with their customers.

## Features

- Order status checking
- Shipping estimates
- Auto-assigning roles to verified customers
- Custom commands

## Getting Started

0. Install Python 3.7 and prerequisites using `pip install -r requirements.txt`.
1. Make a copy of `config_ex.py` and rename it to `config.py`. Configure the bot as desired. See [Configuration](##Configuration).
2. Run the bot using `python bot.py`.

## Configuration

TODO

## Commands

`!status <order_id>` - Check the status of an order.

`!cc <add/remove/list>` - Manage custom commands. See [Custom Commands](###Custom-Commands). **Requires a staff role.**

`!wcm <order_id>` - Sends a Direct Message to the sender containing a direct link to the order on WooCommerce. **Requires a staff role.**

`!stop_bot` - Stops the bot. **Requires bot owner.**

### Custom Commands

Custom commands allow you to set messages that can be triggered by staff members. Useful for responding to common inquiries.

`!cc add <trigger> <title> <message>` - Creates a new custom command. Titles and messages with multiple words should be surrounded by quotation marks. Note that only one custom command can be assigned to a specific trigger.

`!cc remove <trigger>` - Removes the custom command with the specified trigger.

`!cc list` - Lists all custom commands.

## License

TODO