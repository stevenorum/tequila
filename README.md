# tequila
Premade CF stack for forwarding email from SES to your normal account.

Heavily based on [this guide](http://www.daniloaz.com/en/use-gmail-with-your-own-domain-for-free-thanks-to-amazon-ses-lambda/) and [this NodeJS lambda code](https://github.com/arithmetric/aws-lambda-ses-forwarder), so much thanks to the authors of both of those.

## Steps

### Get yoself a domain (manual)

If you don't already have one, go out and buy a domain somewhere.  I recommend either Google or AWS.  (Even though I only use AWS cloud services, I get all of my domains through Google.  That's half because I was doing that before I started doing stuff with domains in AWS, and half because it makes it less likely I'll forget a password or misconfigure something and be completely locked out of an account, as some of them are setup with email addresses through one of the domains that they themselves configure.  Using Google, I can always go and reset the DNS settings to the default to regain access to everything.)

### Add your domain in Route53 (manual)

[Here's a guide on how to add your domain to Route53.](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/CreatingHostedZone.html)  I don't have anything fancy to add, so just use that.

### Add your domain in SES (manual)

Go to [AWS SES in the console](https://console.aws.amazon.com/ses/home?region=us-east-1#verified-senders-domain:), click "Verify a New Domain", and follow the instructions.  Again, I don't have anything fancy to add here, so just follow the instructions and google if you get stuck.

### Create the deployment pipeline (partly manual)

Follow [this guide](https://github.com/stevenorum/cloudformation-templates#codepipeline-githubcfjson) using the codepipeline template in this package.  For ParameterOverrides, put in ```{"EmailDomain":"yournewdomain.org","ForwardTo":"yourname@gmail.com"}``` (obviously with the values replaced with yours).
