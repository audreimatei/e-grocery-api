#! /usr/bin/env bash

# Let the DB start
python src/backend_pre_start.py

# Run migrations
alembic upgrade head
