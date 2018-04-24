# tequila
Premade CF stack for forwarding email from SES to your normal account.

Heavily based on [this guide](http://www.daniloaz.com/en/use-gmail-with-your-own-domain-for-free-thanks-to-amazon-ses-lambda/) and [this NodeJS lambda code](https://github.com/arithmetric/aws-lambda-ses-forwarder), so much thanks to the authors of both of those.

This stack should work pretty much out-of-the-box if all you want to do is forward all email to a domain to a single email address.  If you aren't doing anything fancy with email and just want to let yourself receive emails to a domain that you're managing in Route 53, this will do the trick.  If you want to do fancy stuff with email (automatically sending/replying/filtering or something like that), this should serve as a good starting point 

## Steps

### Get yoself a domain (manual)

If you don't already have one, go out and buy a domain somewhere.  I recommend either Google or AWS.  (Even though I only use AWS cloud services, I get all of my domains through Google.  That's half because I was doing that before I started doing stuff with domains in AWS, and half because it makes it less likely I'll forget a password or misconfigure something and be completely locked out of an account, as some of them are setup with email addresses through one of the domains that they themselves configure.  Using Google, I can always go and reset the DNS settings to the default to regain access to everything.)

### Add your domain in Route53 (manual)

[Here's a guide on how to add your domain to Route53.](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/CreatingHostedZone.html)  I don't have anything fancy to add, so just use that.

### Add your domain in SES (manual)

Go to [AWS SES in the console](https://console.aws.amazon.com/ses/home?region=us-east-1#verified-senders-domain:), click "Verify a New Domain", and follow the instructions.  Again, I don't have anything fancy to add here, so just follow the instructions and google if you get stuck.

### Clone this repo (manual)

Clone this repo in GitHub.  AWS CodePipeline only lets you deploy repos in your account, which is kinda understandable.  

### Create the deployment pipeline (partly manual)

Follow [this guide](https://github.com/stevenorum/cloudformation-templates#codepipeline-githubcfjson) using the codepipeline template in this package.  For ParameterOverrides, put in ```{"EmailDomain":"yournewdomain.org","ForwardTo":"yourname@gmail.com"}``` (obviously with the values replaced with yours).

### Wait for this stack to finish creating.

Should take about a minute.  Go grab a soda or something.

### Go to CodePipeline and wait for the tequila stack to finish creating.

Should take 5 minutes or so.  Go watch [this](https://www.youtube.com/watch?v=st8-EY71K84) or some other comparable-length video.

### Go to SES and make the newly-created ruleset the active one.

Go [here](https://console.aws.amazon.com/ses/home?region=us-east-1#receipt-rules:), select the only RuleSet (if there are multiple, it means you've used SES previously and should know how to figure this all out on your own anyway), and click "Set as Active Rule Set".

### Test all the things.

Send an email to yourfancynewemailsystem@yournewdomain.org and see if it gets forwarded on to yourname@gmail.com and if it doesn't, you need to fix something.
