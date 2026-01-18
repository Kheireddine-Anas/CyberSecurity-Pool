.PHONY: all build up down clean test logs help

all: build up

build:
	@echo "Building Docker images..."
	docker-compose build

up:
	@echo "Starting containers..."
	docker-compose up -d
	@echo "Waiting for services to be ready..."
	@sleep 5
	@echo ""
	@echo "========================================="
	@echo "Environment is ready!"
	@echo "========================================="
	@echo "FTP Server:  172.20.0.10 (port 21)"
	@echo "FTP Client:  172.20.0.5"
	@echo "Username:    ftpuser"
	@echo "Password:    ftppass"
	@echo ""
	@echo "To run the attack:"
	@echo "  make attack"
	@echo ""
	@echo "To test FTP manually:"
	@echo "  make test"
	@echo ""
	@echo "To see logs:"
	@echo "  make logs"
	@echo "========================================="

down:
	@echo "Stopping containers..."
	docker-compose down

clean:
	@echo "Cleaning up containers and images..."
	docker-compose down -v --rmi all

attack:
	@echo "Getting MAC addresses..."
	@CLIENT_MAC=$$(docker exec ftp_client ip link show eth0 | grep ether | awk '{print $$2}'); \
	SERVER_MAC=$$(docker exec ftp_server ip link show eth0 | grep ether | awk '{print $$2}'); \
	echo "Client MAC: $$CLIENT_MAC"; \
	echo "Server MAC: $$SERVER_MAC"; \
	echo ""; \
	echo "Starting ARP poisoning attack..."; \
	echo "Press CTRL+C to stop and restore ARP tables"; \
	echo ""; \
	docker exec -it attacker python3 /app/inquisitor 172.20.0.5 $$CLIENT_MAC 172.20.0.10 $$SERVER_MAC

attack-verbose:
	@echo "Getting MAC addresses..."
	@CLIENT_MAC=$$(docker exec ftp_client ip link show eth0 | grep ether | awk '{print $$2}'); \
	SERVER_MAC=$$(docker exec ftp_server ip link show eth0 | grep ether | awk '{print $$2}'); \
	echo "Client MAC: $$CLIENT_MAC"; \
	echo "Server MAC: $$SERVER_MAC"; \
	echo ""; \
	echo "Starting ARP poisoning attack (VERBOSE MODE)..."; \
	echo "Press CTRL+C to stop and restore ARP tables"; \
	echo ""; \
	docker exec -it attacker python3 /app/inquisitor -v 172.20.0.5 $$CLIENT_MAC 172.20.0.10 $$SERVER_MAC

test:
	@echo "Running FTP test script..."
	@docker exec -it attacker /bin/bash /app/test_ftp.sh

shell-attacker:
	@docker exec -it attacker /bin/bash

shell-client:
	@docker exec -it client /bin/sh

shell-server:
	@docker exec -it ftp_server /bin/bash

logs:
	docker-compose logs -f

status:
	@echo "Container Status:"
	@docker-compose ps
	@echo ""
	@echo "Network Information:"
	@docker network inspect inquisitor_test_network | grep -A 3 "Containers"

help:
	@echo "Inquisitor - ARP Poisoning & FTP Sniffer"
	@echo ""
	@echo "Available commands:"
	@echo "  make build           Build Docker images"
	@echo "  make up              Start all containers"
	@echo "  make down            Stop all containers"
	@echo "  make clean           Clean up everything"
	@echo "  make attack          Run inquisitor (ARP poisoning + FTP sniffing)"
	@echo "  make attack-verbose  Run inquisitor in verbose mode"
	@echo "  make test            Run FTP test script"
	@echo "  make logs            Show container logs"
	@echo "  make status          Show container and network status"
	@echo "  make shell-attacker  Open shell in attacker container"
	@echo "  make shell-client    Open shell in client container"
	@echo "  make shell-server    Open shell in FTP server container"
