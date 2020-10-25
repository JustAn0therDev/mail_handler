# mail_handler

## A CLI application to download and/or forward messages from your favorite terminal!

`mail_handler` is a CLI application written in 100% native Python 3 (3.6) with the objective of making 'boring e-mail management' much easier through the terminal (and more fun). The choice of writing the application with only native libraries was made to ensure that it keeps working as intended as long as such libraries are supported by the language the way they were implemented.

# Getting started

## Running the application

You can run it by typing the following in your terminal of choice:

`/path_you_chose/mail_handler/mail_handler.py path_you_chose/configs.txt`

The only argument when calling the application via command line should be the path to your configuration file of choice. If the configuration file/file path is not specified, the application will warn you and stop its execution.

You can also map the `mail_handler.py` path to your PATH environment, such as a `mail_handler` command:

`mail_handler path_you_chose/configs.txt`

## Output

Currently, the application can either forward messages or download their content/attachments. **If mail_handler finds a list of messages, their content/attachments will be download/forwarded.** So if while looking for an e-mail subject `mail_handler` finds three messages with the provided `SUBJECT`, those three messages will receive the same treatment (all of them will be downloaded or forwarded).

## Virtual Environments

If for some reason your Python version is not letting the application run smoothly, you can always create a virtual environment and use a custom Python interpreter for it. You can find more about virtual environments in Python [here](https://docs.python.org/3/tutorial/venv.html). 

Your virtual Python environment can be configured in many ways, such as natively with `venv` or using a package like `virtualenv` (can be installed with `pip install virtualenv`, for example).

## Configuration

`mail_handler` uses a configuration file to "act" based on it. Your configuration file can be a simple `.txt` file with a few lines in it, consisting of a few `key=value` pairs.

Think of this configuration file as a set of **instructions and values** that will tell `mail_handler` what to do with that same information.

Keep in mind that the keys **must be written exactly as shown in the examples**, they don't have to be in an specific order and there can be **only one key-value pair per line**, if not **the last value will overwrite the previous one**, e.g.:

`SEARCH=FROM`

`SEARCH=TO`

`SEARCH=SUBJECT`

The final value for the `SEARCH` key will be `SUBJECT` in this example.

All of the values below **must be present in the configuration folder, even if some are not used for the specified ACTION value**.

### EMAIL

This is the e-mail address that `mail_handler` will use to log-in: 

`EMAIL=myemailaddress@somedomain.com`

### APP_PASSWORD

The app_password is a password that `mail_handler` will use to log-in with the provided e-mail address in the `EMAIL` key:

`APP_PASSWORD=jkldsajldasu19`

The password can be either the actual account password or an app password made available to you by your account provider (Microsoft or Google's Gmail, for instance). If `mail_handler` cannot log-in with the provided information, an `EXCEPTION` message will be shown in the terminal.

### MAILBOX 

The current mailbox to look for e-mails: 

`MAILBOX=inbox`

### SEARCH

Tells `mail_handler` to look for the exact "part" of an e-mail in the configured `MAILBOX`. Any property that complies with the RFC should work as intended.

`SEARCH=FROM` or `SEARCH=SUBJECT`

### DATA_TO_LOOK_FOR

You can think of `SEARCH` as being the key for this configuration line. For example: 

`SEARCH=SUBJECT`

`DATA_TO_LOOK_FOR="Happy birthday, Jon!"`

In this particular case, `mail_handler` will look for e-mails that have their `SUBJECT` equal to `"Happy birthday, Jon!"`.

### IMAP_ADDRESS

The IMAP address made available by your account provider, for example:

`IMAP_ADDRESS=imap.gmail.com`

`mail_handler` will connect to this address via an SSL connection and look for the data you requested.

### SMTP_ADDRESS

The SMTP address made available by your account provider, for example:

`SMTP_ADDRESS=smtp.gmail.com`

`mail_handler` will connect to this address to **forward your messages if requested**.

### OUTPUT

`mail_handler` will download all requested content in the specified directory.

Since your file system might differ from OS to OS, here are some examples for Unix based operating systems and Windows, respectively:

`OUTPUT=/bin/my_output_dir`

`OUTPUT=C:/Users/SomeUser/source/outputFolder`

For a Windows operating system, the file path **must be mapped from the root directory of your hard drive to the directory of choice**.

### ACTION

`ACTION` will be read by `mail_handler` as the **main goal of that execution**. The currently available values are:

- `ACTION=download_message`: Will download the message's plain text content;
- `ACTION=download_attachment`: Will download the message's attachments;
- `ACTION=forward_message`: Will forward all of the 
message's content via SMTP.

Any other value provided will raise a `NotImplementedError`.

### TO

A list of e-mail addresses to forward the requested message, **if requested**.

Each e-mail address in the list must be separated by ", " (comma, space).

`TO=emailOne@domain.com, emailTwo@domain.com`

## Complete configuration file

An example of a complete configuration file would look like this, **with no empty lines**:

`EMAIL=myemailaddress@somedomain.com`

`APP_PASSWORD=jkldsajldasu19`

`MAILBOX=inbox`

`SEARCH=SUBJECT`

`DATA_TO_LOOK_FOR="Happy birthday, Jon!"`

`IMAP_ADDRESS=imap.gmail.com`

`SMTP_ADDRESS=smtp.gmail.com`

`OUTPUT=~/users/bin/my_output_dir`

`ACTION=download_message`

`TO=emailOne@domain.com, emailTwo@domain.com`

## Use-cases

A use-case for could be a job that runs on your server or local machine at a specified time of day and downloads (or forwards) a list of e-mails, much like a notification for some addresses (sys-admins, for example).

Another use-case could be having e-mails sent as notifications from an action in a Web Application or an unexpected behaviour from your data through some connection to a database that triggers a `mail_handler` execution.

### Final Considerations

If you used the application and liked it, please consider giving it a star and contributing to it! 
