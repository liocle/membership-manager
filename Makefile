.PHONY: all clean get_images_id re up_all logs logs_errors logs_grep logs_postgres logs_api ps ps_short ps_inspect exec_backend exec_db stop_all stats sys_df help nuke re_no_cache re_rm_volumes

include .env

################################################################################
# Build and Start
################################################################################
# Default target: Build and start all services except ELK stack
all: up_no_elk

# Start all services except ELK stack and rebuild if necessary
up_no_elk:
	docker compose -f ./docker-compose.yml up --build -d postgres api pgadmin

# Start all services including ELK stack and rebuild if necessary
up_all:
	docker compose -f ./docker-compose.yml up --build -d

################################################################################
# Clean and Remove
################################################################################
# Capture image IDs to .image_ids before bringing containers down
get_images_id:
	@images=$$(docker compose -f ./docker-compose.yml images -q); \
  if [ -n "$$images" ]; then \
  	echo "$$images" >> .image_ids; \
  else \
  	echo "get_images_id: no images to be deleted"; \
  fi; \
  sort .image_ids | uniq > .image_ids.tmp && mv .image_ids.tmp .image_ids; \
  echo "get_images_id: images to be deleted identified"; \
  cat .image_ids

# Stop and remove containers, networks, and volumes
down: get_images_id
	docker compose -f ./docker-compose.yml down

# Clean up volumes and reset persistent data
clean_volumes: get_images_id
	docker compose -f ./docker-compose.yml down -v

# Clean up orphans to remove containers that are no longer defined in the current docker-compose.yml
clean_orphans: get_images_id
	docker compose -f ./docker-compose.yml down --remove-orphans

# Clean up images present in .image_ids, delete the file, and remove all Docker images
clean_images:
	@if [ -f .image_ids ]; then \
 	echo "clean_images: remove following images"; \
 	cat .image_ids; \
 	images=$$(cat .image_ids); \
 	if [ -n "$$images" ]; then \
 		for image in $$images; do \
 			docker image rm -f $$image || true; \
 		done; \
 		echo "clean_images: Images removed"; \
 	else \
 		echo "clean_images: No images to remove"; \
 	fi; \
 	rm -f .image_ids; \
 else \
 	echo "clean_images: .image_ids file not found"; \
 fi

# Clean up all: containers, networks, volumes, and images
# Use this for a full cleanup of the Docker environment
clean_all: clean_orphans clean_volumes clean_images

# Use this to reset data and ensure only defined services are running
# Clean up: containers, networks, volumes, and orphans (default clean)
clean: clean_orphans clean_volumes

################################################################################
# Rebuild and Restart
################################################################################
# Rebuild and start all services without removing volumes
re: clean_orphans up_no_elk

# Rebuild and start all services: clean orphans and volumes, keep images
re_rm_volumes: clean_orphans clean_volumes up_no_elk

# Rebuild and start all services: clean orphans and volumes, keep images
re_rm_volumes_cache: clean_orphans clean_volumes
	docker compose -f ./docker-compose.yml build --no-cache
	$(MAKE) up_no_elk

# Rebuild with no-cache and start all services without removing volumes
re_no_cache: clean_orphans
	docker compose -f ./docker-compose.yml build --no-cache
	$(MAKE) up_no_elk


################################################################################
# Logging
################################################################################
# Tail logs from specific services
logs_postgres:
	docker compose -f ./docker-compose.yml logs -f postgres

logs_api:
	docker compose -f ./docker-compose.yml logs -f api

logs_pgadmin:
	docker compose -f ./docker-compose.yml logs -f pgadmin

# Tail all logs with timestamps
logs:
	docker compose -f ./docker-compose.yml logs -f -t

# Tail ERROR logs with timestamps
logs_errors:
	docker compose -f ./docker-compose.yml logs -f -t | grep "ERROR"

# Tail logs containing keyword input by user with timestamps
logs_grep:
	@read -p "Enter keyword to search in logs: " keyword; docker compose -f ./docker-compose.yml logs -f -t | grep "$$keyword"

################################################################################
# Status
################################################################################
# Check status of running containers
ps:
	docker compose -f ./docker-compose.yml ps

# Check status of running containers with concise output
ps_short:
	@docker container ls -a --format "table {{.ID}}\t{{.Names}}\t{{.RunningFor}}\t{{.Status}}"

# Inspect a specific container
ps_inspect: ps_short
	@echo ""
	@read -p "Enter container name: " name; docker inspect $$name

################################################################################
# Exec into Containers
################################################################################
# Open a shell in a specific container
exec_postgres:
	docker compose -f ./docker-compose.yml exec postgres bash

exec_api:
	docker compose -f ./docker-compose.yml exec api bash

################################################################################
# Stop services
################################################################################
# Stop all services without removing them
stop_all:
	docker compose -f ./docker-compose.yml stop

################################################################################
# Monitoring
################################################################################
stats:
	docker stats

sys_df:
	docker system df

################################################################################
# Reset repository to last commit (destructive action)
################################################################################
nuke:
	git clean -dxf
	git reset --hard

################################################################################
# Tests
################################################################################

# Run pytest
run_pytest:
	pytest tests/

################################################################################
# Tools and Utilities
################################################################################

create_db:
	docker compose -f ./docker-compose.yml exec api python create_tables.py

# Seed the database with sample data
seed_db:
	docker compose exec api python seed/seed_data.py

alembic_generate_migration:
	@read -p "Enter migration message: " keyword; docker compose exec api alembic revision --autogenerate -m "$$keyword"

alembic_upgrade_head:
	docker compose exec api alembic upgrade head

alembic_history:
	docker compose exec api alembic history

alembic_downgrade:
	docker compose exec api alembic downgrade -1

alembic_copy_version:
	docker container cp membermgr_api:/app/alembic/versions/. ./app/alembic/versions/

alembic_upload_version:
	docker container cp ./app/alembic/versions/. membermgr_api:/app/alembic/versions/



################################################################################
# PSQL
################################################################################
psql_members:
	@echo "Show structure of 'members' table (inside Docker)"
	docker exec -it membermgr_postgres_db psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) -c "\d members"

psql_docker:
	@echo "Connecting to PostgreSQL inside Docker container..."
	docker exec -it membermgr_postgres_db psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)

psql_local:
	@echo "Connecting to local PostgreSQL service..."
	@PGPASSWORD=$(POSTGRES_PASSWORD) psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) -h $(POSTGRES_HOST_LOCAL) -p $(POSTGRES_PORT)

show_memberships:
	@echo "🔍 Showing content of 'memberships' table..."
	docker exec -it membermgr_postgres_db \
		psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) \
		-c "SELECT * FROM memberships ORDER BY member_id, year;"

show_members:
	@echo "👥 Showing content of 'members' table..."
	docker exec -it membermgr_postgres_db \
		psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) \
		-c "SELECT  FROM members ORDER BY id;"

show_all:
	@echo "👥 Members:"
	docker exec -it membermgr_postgres_db \
		psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) \
		-c "SELECT id, full_name, email FROM members ORDER BY id;"
	@echo ""
	@echo "📆 Memberships:"
	docker exec -it membermgr_postgres_db \
		psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) \
		-c "SELECT * FROM memberships ORDER BY member_id, year;"

################################################################################
# Help
################################################################################
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo ""
	@echo "Build and Start:"
	@echo "  all            Build and start all services except ELK stack"
	@echo ""
	@echo "Stop:"
	@echo "  stop_all       Stop all running services (without removing containers)"
	@echo ""
	@echo "Clean and Remove:"
	@echo "  down           Stop and remove containers, networks, and volumes"
	@echo "  clean_volumes  Remove volumes and reset persistent data"
	@echo "  clean_orphans  Remove orphaned containers not defined in the current docker-compose.yml"
	@echo "  clean_images   Remove all Docker images"
	@echo "  clean_all      Full RESET: Removes containers, networks, volumes, and images"
	@echo "  clean          Default clean: reset data and ensure only defined services are running"
	@echo ""
	@echo "Rebuild and Restart:"
	@echo "  re             Restart services after cleaning orphans, keeping data"
	@echo "  re_no_cache    Force full rebuild from scratch (no cache, fresh layers)"
	@echo "  re_rm_volumes  Restart services after removing ALL volumes (fresh DB)"
	@echo "  re_rm_volumes_cache   Restart services after removing ALL volumes and cache"
	@echo ""
	@echo "Logging:"
	@echo "  logs_postgres  Tail logs from the postgres service"
	@echo "  logs_api       Tail logs from the Api service"
	@echo "  logs_pgadmin   Tail logs from pgAdmin"
	@echo "  logs           Tail all logs with timestamps"
	@echo "  logs_errors    Tail logs with timestamps and filter for ERROR messages"
	@echo "  logs_grep      Tail logs with timestamps and filter by a keyword"
	@echo ""
	@echo "Status:"
	@echo "  ps             Check status of running containers"
	@echo "  ps_short       Check status of running containers with concise output"
	@echo "  ps_inspect     Inspect a specific container"
	@echo ""
	@echo "Exec into Containers:"
	@echo "  exec_api       Open a shell in the api container"
	@echo "  exec_postgres  Open a shell in the postgres container"
	@echo ""
	@echo "Monitoring:"
	@echo "  stats          Show resource utilization statistics for running containers"
	@echo "  sys_df         Show Docker system disk usage"
	@echo ""
	@echo "Reset repository:"
	@echo "  nuke           Reset repository to the last commit (destructive action, removes all untracked files)"
	@echo ""
	@echo "Tests:"
	@echo "  run_pytest     Run pytest"
	@echo ""
	@echo "Tools and utilities:"
	@echo "  create_db      runs the create_tables.py script to create the database tables"
	@echo "  seed_db        Seed the database with sample data"
	@echo "  alembic_generate_migration      Generate a new migration with alembic"
	@echo "  alembic_upgrade_head            Upgrade to the latest migration"
	@echo "  alembic_history                 Show the migration history"
	@echo "  alembic_downgrade               Downgrade the database by one migration"
	@echo "  alembic_copy_version            Copy the alembic versions from the container to the local directory"
	@echo "  alembic_upload_version          Copy the alembic versions from the local directory to the container"
	@echo ""
	@echo "PSQL:"
	@echo "  psql_members    Show structure of 'members' table from inside Docker"
	@echo "  psql_docker     Connect to PostgreSQL inside Docker container"
	@echo "  psql_local      Connect to local PostgreSQL service (requires system PostgreSQL running)"
	@echo "  show_memberships Show content of 'memberships' table from inside Docker"
	@echo "  show_members 	 Show  content of 'members' table from inside Docker"
	@echo "  show_all        Show content of 'members' and 'memberships' tables from inside Docker"
	@echo ""
	@echo "Help:"
	@echo "  help           Show this help message"

