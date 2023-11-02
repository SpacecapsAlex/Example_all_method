from fastapi import FastAPI
import psycopg2
from dotenv import dotenv_values
from pydantic import BaseModel

config = dotenv_values(".env")

connect = psycopg2.connect(
    host=config['HOST'],
    port=config['PORT'],
    user=config['USER_ID'],
    password=config['USER_PD'],
    database=config['DB_NAME'],
)

cursor = connect.cursor()
app = FastAPI()


class vm_get_workers(BaseModel):
    id: int
    firstName: str
    position: str
    phone: str


class vm_get_worker(BaseModel):
    id: int
    firstName: str
    surName: str
    email: str
    phone: str
    address: str
    position: str
    salary: int


class vm_add_worker(BaseModel):
    firstName: str
    surName: str
    email: str
    phone: str
    address: str
    position: str
    salary: int


class vm_update_worker(BaseModel):
    id: int
    firstName: str
    surName: str
    email: str
    phone: str
    address: str
    position: str
    salary: int


@app.get("/")
def root():
    return {"message": "Start Server"}


@app.get("/get-workers")
def get_workers():
    try:
        cursor.execute("""
            SELECT id, first_name, position, phone
            FROM worker;
        """)
        result = cursor.fetchall()
        list_workers = []
        for worker in result:
            list_workers.append(vm_get_workers(
                id=worker[0],
                firstName=worker[1],
                position=worker[2],
                phone=worker[3]
            ))

        return {"workers": list_workers}
    except Exception as e:
        return {"error": e}


@app.get("/get-worker/{worker_id}")
def get_worker(worker_id: int):
    try:
        cursor.execute(f"""
            SELECT w.id, w.first_name, w.sur_name, w.email, w.phone, w.address, w.position, w.salary
            FROM worker w
            WHERE w.id = {worker_id};
        """)
        result = cursor.fetchone()
        worker = vm_get_worker(
            id=result[0],
            firstName=result[1],
            surName=result[2],
            email=result[3],
            phone=result[4],
            address=result[5],
            position=result[6],
            salary=result[7]
        )

        return {"worker": worker}
    except Exception as e:
        return {"error": e}


@app.post("/add-worker")
def add_worker(worker: vm_add_worker):
    try:
        cursor.execute(f"""
            INSERT INTO worker (first_name, sur_name, email, phone, address, position, salary)
            VALUES ('{worker.firstName}', '{worker.surName}', '{worker.email}', '{worker.phone}', '{worker.address}', '{worker.position}', {worker.salary});
        """)
        connect.commit()

        return {"message": "Success"}
    except Exception as e:
        return {"error": e}


@app.delete("/delete-worker/{worker_id}")
def delete_worker(worker_id: int):
    try:
        cursor.execute(f"""
            DELETE FROM worker
            WHERE id = {worker_id};
        """)
        connect.commit()

        return {"message": "Success"}
    except Exception as e:
        return {"error": e}


@app.put("/update-worker")
def update_worker(worker: vm_update_worker):
    try:
        cursor.execute(f"""
            UPDATE worker
            SET first_name = '{worker.firstName}', sur_name = '{worker.surName}', email = '{worker.email}', phone = '{worker.phone}', address = '{worker.address}', position = '{worker.position}', salary = {worker.salary}
            WHERE id = {worker.id};
        """)
        connect.commit()

        return {"message": "Success"}
    except Exception as e:
        return {"error": e}
