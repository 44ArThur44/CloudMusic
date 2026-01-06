## Scheduler (SO-level)

execução automática do pipeline:

Windows:
- Task Scheduler
- Comando:
  python run_pipeline.py

Linux:
- cron:
  0 10 * * * /path/venv/bin/python run_pipeline.py