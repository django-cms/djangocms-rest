Health check
============

**A minimal health check endpoint for API monitoring.**

* Returns a simple status response to confirm the API is running.
* Useful for uptime monitoring tools.
* No authentication required.


Endpoints
---------

Health Check
~~~~~~~~~~~~

**GET** ``/api/healthcheck/``

Returns a simple status response.

**Example Request:**

.. code-block:: bash

    GET /api/healthcheck/

**Example Response:**

.. code-block:: json

    {
        "status": "ok"
    }
