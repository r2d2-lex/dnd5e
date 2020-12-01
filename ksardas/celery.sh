#!/bin/bash
celery -A ksardas worker --loglevel=debug --concurrency=4