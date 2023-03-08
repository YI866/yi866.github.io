import requests
from concurrent.futures import ThreadPoolExecutor

task_list = [3, 4, 5, 6, 10, 24, 31, 34, 39, 45, 57, 67, 75, 85, 115, 116, 117, 118, 119, 120, 121, 122,
             123, 124, 125, 127, 129, 130, 131, 132, 126, 133, 128, 134, 135, 136, 137, 138, 139, 140, 
             141, 143, 142, 145, 144, 146, 147, 151, 149, 148]

def post_freeze(task_id):
    try:
        res = requests.post(
                url="http://192.168.10.185:18090/api/publish_task",
                json={"task_id": task_id, "op_type": "freeze"},
                headers=headers
            )
        if res.status_code == 200:
            print(f"task {task_id} unfreeze success.")
        else:
            print(f"task {task_id} unfreeze failed.")
    except Exception as e:
        print(e)

def post_copy(task_id):
    try:
        res = requests.post(
                url="http://192.168.10.185:18090/api/copy_task",
                json={"task_id": task_id},
                headers=headers
            )
        if res.status_code == 200:
            print(f"task {task_id} copy success.")
        else:
            print(f"task {task_id} copy failed.")
    except Exception as e:
        print(e)

def post_delete(task_id):
    try:
        res = requests.delete(
                url="http://192.168.10.185:18090/api/task/%s" % task_id,
                json={"task_id": task_id},
                headers=headers
            )
        if res.status_code == 200:
            print(f"task {task_id} delete success.")
        else:
            print(f"task {task_id} delete failed.")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    headers = {"Cookie": "token=eyJhbGciOiJIUzUxMiIsImlhdCI6MTY3Njk5NjEzNCwiZXhwIjoxNjc5NTg4MTM0fQ.eyJpZCI6MX0.oU9X6bnTdPG7hIrX99zQJeLkLpobCLHYhPMjIkcldPD1qGiyFgEsyh4Cj43tLjwebz-tQFV-iG0kRCxNr0zsxw",
               "Content-Type": "application/json"}

    with ThreadPoolExecutor(max_workers=10) as executor:
        for i in range(103, 151):
            executor.submit(post_freeze, i)
    
    print('exit')