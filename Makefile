

migration: ## Create migrations using alembic
	#docker-compose exec api alembic revision --autogenerate -m "$(m)"
	exec alembic revision --autogenerate -m "$(m)"

upgrade: ## Run migrations using alembic
	exec alembic upgrade head

upgrade1: ## Run migrations using alembic
	exec alembic upgrade +1

downgrade1:
	exec alembic downgrade -1

downgrade-base:
	exec alembic downgrade base