# Technical Challenge

## Goal

Develop a REST API capable of:

- Importing associates from a CSV file.
- Persisting the data in MongoDB.
- Returning associates that belong to the same economic group.
- Excluding the queried associate from the response.

## Stack

- Python
- FastAPI
- MongoDB
- Beanie

## Endpoint

GET /associates/{account_number}

## Import

CSV executed by scheduler.

## Response

[
  {
    "name": "...",
    "cpf_cnpj": "..."
  }
]