import subprocess
import chardet


def extract_wifi_passwords():
    codings = chardet.detect(subprocess.check_output('netsh wlan show profiles'))
    profiles_data = subprocess.check_output('netsh wlan show profiles').decode(codings['encoding']).split('\n')
    profiles = [i.split(':')[1].strip() for i in profiles_data if 'All User Profile' and 'Все профили пользователей' in i]

    for profile in profiles:
        profile_info = subprocess.check_output(f'netsh wlan show profile "{profile}" key=clear').decode(codings['encoding']).split('\n')
        try:
            password = [i.split(':')[1].strip() for i in profile_info if 'Key Content' and 'Содержимое ключа' in i]
        except IndexError:
            password = None
        with open(file="wifi_local_passwords.txt", mode='a', encoding='utf-8') as file:
            file.write(f'Profile {profile}\n Password {password}\n{"#" * 20}')

def main():
    extract_wifi_passwords()

if __name__ == '__main__':
    main()
