.. _modules_api:

==========
API module
==========

The `api` module contains tools for developing endpoints using FastAPI.

Request scope
=============

Requests sent to/between our services are required to carry a JWT token among other headers.
The idea is to centralize these data into an easily accessible object.


