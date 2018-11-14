[![Gitter chat](https://img.shields.io/badge/gitter-join%20chat-brightgreen.svg)](https://gitter.im/CiscoSecurity/Threat-Grid "Gitter chat")

### Rate Limit check

Sample script for checking the user and organization API rate limits given an API key

### Usage

To use this script you provide a valid Threat Grid API key as a command line paramter:
```
python check_rate_limit.py 139ec4f94a8c908e20e7c2dce5092af4
```

### Example script output
```
Your login is: jdoe

You have 1000 samples available (if 'None' there are no user specific limits)
You must wait 0 seconds before submitting another sample

Your org has 9864 samples available
Your org must wait 0 seconds before submitting another sample

```
