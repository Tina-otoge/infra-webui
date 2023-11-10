# infra-webui

A dead-simple Web UI to manage infra components.

From the Web UI you are able to see the status of infra components, stop and
start them.

Currently supported items:

- AWS EC2

## Running

Create a `inventory.yml` and a `secrets.yml` file, following the examples with
the same names.

Describe your components in the inventory file.

In the secrets file, in addition to your access keys, you must create a list of
password to authorize clients. You can fill the passwords in plain text, but you
are encouraged to hash them. To create a hashed password, run `python -m
src.password <password here>`.

You can run the server using `python -m src`, this will run a Flask debug
instance. Otherwise, use a WSGI server like *gunicorn*.
