module.exports = {
  apps: [
    {
      name: 'flask_automation_gunicorn',
      script: './scripts/gunicorn_start.sh'
    },
    {
      name: 'flask_automation_celery_worker',
      script: './scripts/celery_worker_start.sh'
    }
  ]
};
