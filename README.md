Using this tool and CloudFlare you can have a DDNS like domain.
just set the script to run every x minutes in cron so it keeps CloudFlare up to date.

Each time the script runs it will check the current IP address and compare that with what's already configured on CloudFlare. If it's the same then it leaves it as is, otherwise it updates CloudFlare with the correct IP address and sends a notification to your Pushover application.

I would recommend taking a backup of your DNS setup in CloudFlare in the case of any unintended consequences. Once it's run the first time you can check the correct record has been updated.

Get an account with CloudFlare and configure your domain if not done so already.
Also enable the API on your account. Note the key and copy it into the script along with the email address.

Create a new application with Pushover and copy the keys into the script.

Setup to run in cron and you should be good to go.
