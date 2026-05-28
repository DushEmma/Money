from app import app
from models import Worker

with app.app_context():
    workers = Worker.query.all()
    print(f'Total workers: {len(workers)}')
    for w in workers:
        print(f'Worker {w.id}: {w.user.full_name}, profile_picture: {w.profile_picture}')
