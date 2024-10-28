import paramiko


def get_airwave_files():
    hostname = 'secretHostname'
    port = 22
    username = 'secretUser'
    password = 'secretPassword'

    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(hostname, port, username, password)

    sftp = ssh.open_sftp()

    remote_file_path = ".\\toPi\\airwave\\"
    try:
        remote_files = sftp.listdir(remote_file_path)
        for remote_file in remote_files:
            if remote_file.endswith('.png'):
                local_file_path = "/home/pi/Desktop/Display/static/images/"
            elif remote_file.endswith('.webm'):
                local_file_path = "/home/pi/Desktop/Display/static/videos/"
            else:
                local_file_path = "/home/pi/Desktop/Display/unknown/"
                print("Unknown file extension")
            print(f"Copied file: {remote_file}")
            local_file_path += remote_file
            remote_file_with_path = remote_file_path + remote_file
            sftp.get(remote_file_with_path, local_file_path)
            print(f"Copied file to: {local_file_path}")
            
    except Exception as e:
        print("No file at location on remote computer")
        print(e)
    sftp.close()
    ssh.close()

get_airwave_files()