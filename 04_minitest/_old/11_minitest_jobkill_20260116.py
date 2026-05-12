import sys
from system.lib.minescript import job_info, execute

# ==============================
# コマンドライン引数からジョブ名を取得
# ==============================
if len(sys.argv) < 2:
    print("Usage: python kill_job.py <job name>")
    sys.exit(1)

target_name = sys.argv[1]

# ==============================
# 現在のジョブ一覧を表示
# ==============================
print("=== Running Jobs ===")
jobs = job_info()
if not jobs:
    print("No active jobs.")
else:
    for job in jobs:
        print(f"ID: {job.job_id}, Command: {job.command}")

# ==============================
# 指定ジョブをkill
# ==============================
found = False
for job in jobs:
    if target_name in job.command:  # 部分一致
        execute(f"\\killjob {job.job_id}")
        print(f"Killed job: ID={job.job_id}, Command={job.command}")
        found = True

if not found:
    print(f"No job matching '{target_name}' found.")
