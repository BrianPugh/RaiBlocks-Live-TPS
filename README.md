Uses the rai_node/rai_wallet program's callback feature to display the live TPS of your node.

![demo](https://i.imgur.com/a/iChRb.png?raw=true)

run:
    python live_tps.py --help
for user-configurable options

for default parameters, just run:
    python live_tps.py

To configure your rai_node config.json set:
    "callback_address":"<IP address of the computer running this script>",
    "callback_port":"<port you want to use>"
So to use the default paremeters, set
    "callback_address":"127.0.0.1",
    "callback_port":"17076"
