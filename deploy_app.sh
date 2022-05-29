docker-compose run --rm app sh -c "python manage.py collectstatic"
docker compose -f docker-compose-deploy.yml run --rm gcloud sh -c "gcloud app deploy --project bionic-obelisk-351710"