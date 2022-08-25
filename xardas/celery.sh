#!/bin/bash
celery -A xardas worker --loglevel=debug --concurrency=4