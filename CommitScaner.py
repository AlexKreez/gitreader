import git
import json
import time
import keyboard



try:
    print('Клонируем репозиторий')
    full_local_path = '_clone'
    remote = 'https://github.com/db1000n-coordinators/LoadTestConfig.git'
    repo = git.Repo.clone_from(remote, full_local_path, )
except:
    print('Репозиторий уже клонирован')
    repo = git.Repo('C:/Users/Алексей/PycharmProjects/Zadanie/_clone')
kk = 0
NameCount = 0
AllNames = []
AllDates = []
Run = False
Writing = True


def Stop():
    global Run
    if keyboard.is_pressed('q'):
        print('STOP')
        Run = True


while kk > -1:
    with open("LastCommitDate.txt", "r") as f:
        date_check = f.read()
    Stop()
    for commit in repo.iter_commits("main"):
        tree = commit.tree
        AllDates.append(str(commit.committed_datetime))
        Stop()
        if date_check == str(AllDates[0] + '\n'):
            print("Нет изменений")
            Writing = False
            break
        if len(AllDates) > 15:
            print('Проверка')
            if AllDates[kk] == AllDates[0]:
                print('Нажимайте "q" что бы завершить программу', kk)
                Stop()
                time.sleep(10)
                break
        kk += 1
        for b in tree.blobs:
            if b.name.find('config.', 0) == -1: continue
            try:
                rawest = b.data_stream.read()
                conf = json.loads(rawest)
            except:
                break
            data = AllDates[kk - 1]
            changes = 0
            for jobs in conf['jobs']:
                if dict.get(jobs, 'name') is not None:
                    changes += 1
                    AllNames.append(str("Commit №" + str(kk) + " Date:" + data) + "____" + "Name Chamge №:" + str(
                        changes) + "  " + (dict.get(jobs, 'name')))
    time.sleep(60)
    if Run:
        break
print(len(AllDates), len(AllNames))
if Writing == True:
    with open("LastCommitDate.txt", "w") as f:
        print(AllDates[0], file=f)
    with open("имена.txt", "w") as file:
        for st in range(len(AllNames)):
            print(AllNames[st], file=file)
        print(" ", file=file)
