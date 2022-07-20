makemigrations:
	sudo docker exec -it django_shop python manage.py makemigrations
migrate:
	sudo docker exec -it django_shop python manage.py migrate
django_shell:
	sudo docker exec -it django_shop python manage.py shell
create_superuser:
	sudo docker exec -it django_shop python manage.py createsuperuser
log_app:
	sudo docker logs django_shop -f
log_db:
	sudo docker logs django_db -f
test:
	sudo docker exec -it django_shop python manage.py test


