#!/bin/sh
# Adicionar no crontab:
# sudo crontab -e
# Ex: rodar a cada 2 horas
# 0 */2 * * * su -u ivan "/home/ivan/ajna/virasana/periodic_update.sh"

/home/ivan/ajna/virasana/virasana-venv/bin/python virasana/workers/periodic_tasks.py >> /var/log/virasana/periodic_updates.log
