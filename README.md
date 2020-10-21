# mail_handler

## A CLI application to download and/or forward messages from your favorite terminal!

`mail_handler` is a CLI application written in 100% native Python 3 (3.6) with the objetive of making 'boring e-mail management' much easier through the terminal (and more fun). The choice of writing the application with only native libraries was made to ensure that it keeps working as intended as long as such libraries are supported by the language.

# Getting started

## Configuration

`mail_handler` uses a configuration file to "act" based on it. Your configuration file can be a simple `.txt` file with a few lines in it, consisting of a few `key=value` pairs.

Keep in mind that the `keys` **must be written exactly as shown in the examples**, they don't have to be in an specific order and there can be **only one key-value pair per line**.

### EMAIL

This is the e-mail address with which `mail_handler` will log-in: 

`EMAIL=myemailaddress@somedomain.com`

### APP_PASSWORD

The app_password is a password that `mail_handler` will use to log-in with the provided e-mail address in the `EMAIL` key:

`APP_PASSWORD=jkldsajldasu19`

The password can be either the actual account password or an app password made available to you by your account provider (Microsoft or Google's Gmail, for instance). If `mail_handler` cannot log-in with the provided information, an `EXCEPTION` message will be shown on your terminal.

### MAILBOX 

The current mailbox to look for e-mails: 

`MAILBOX=inbox`

### SEARCH

Tells `mail_handler` to look for the exact "part" of an e-mail in the configured `MAILBOX`. Any property that is a part of the RFC Standard should work as intended.

`SEARCH=FROM`, `SEARCH=SUBJECT`

### DATA_TO_LOOK_FOR

You can think of `SEARCH` as being the key for this configuration line. For example: 

`SEARCH=SUBJECT`

`DATA_TO_LOOK_FOR="Happy birthday, Jon!"`

### IMAP_ADDRESS

The IMAP address made available by your account provider, for example:

`IMAP_ADDRESS=imap.gmail.com`

`mail_handler` will connect to this address via an SSL connection and look for the data you requested.

### SMTP_ADDRESS

The SMTP address made available by your account provider, for example:

`SMTP_ADDRESS=smtp.gmail.com`

`mail_handler` will connect to this address to **forward your messages if requested**.

### OUTPUT

`mail_handler` will download all requested content in the specified directory:

`OUTPUT=~/users/bin/my_output_dir`

### ACTION

`ACTION` will be read by `mail_handler` as the **main goal of that execution**. The current available values are:

- `ACTION=download_message`: Will download the message's plain text content;
- `ACTION=download_attachment`: Will download the message's attachments;
- `ACTION=forward_message`: Will forward all of the 
message's content via an SMTP connection.

Any other value provided will raise a `NotImplementedError`.

### TO

A list of e-mail addresses to forward the requested message, **if so**.

Each item in the list must be separated by ", " (comma and space).

`TO=emailOne@domain.com, emailTwo@domain.com`