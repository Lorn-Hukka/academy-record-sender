import random, os, string, subprocess, shutil, requests
from discord import Webhook, RequestsWebhookAdapter, Embed
from dotenv import dotenv_values
import argparse, colorama
from colorama import Fore


class Settings():
    def __init__(self):
        for k, v in dotenv_values(".settings").items():
            setattr(self, k, v)


class App():
    def __init__(self, config):
        self.config = config
        self.webhook = Webhook.from_url(self.config.WEBHOOK, adapter=RequestsWebhookAdapter())
        self.output_path = self.config.RECORDS_PATH + '\\output\\'
        self.processed_path = self.config.RECORDS_PATH + '\\processed\\'

    def gen_pass(self, lenght):
        chars = string.ascii_letters + string.digits + "!#$%&()*+<=>?@[]^_|~"
        password = ''.join(random.choices(chars, k=lenght))
        return password

    def _check_7zip(self):
        if not os.path.isfile(self.config._7ZIP):
            exit(f'{Fore.RED}WRONG path to 7ZIP executable. Program Exited.')

    def _generate_dirs(self):
        if not os.path.isdir(self.processed_path):
            os.mkdir(self.processed_path)
            print(f'{Fore.YELLOW}Path for proccsed records not found. Created one for you.')

        if not os.path.isdir(self.output_path):
            os.mkdir(self.output_path)
            print(f'{Fore.YELLOW}Output path not found. Created one for you.')


    def process_files(self):
        with open('passwords', 'a+', encoding="utf-8") as f:
            for fn in os.listdir(self.config.RECORDS_PATH):
                if fn.endswith(self.config.EXTENSION):
                    file_password, link_password = self.gen_pass(16), self.gen_pass(16)
                    command = [self.config._7ZIP, 'a -mx9 -mhe=on -y -r', f'-p"{file_password}"',
                                 '--', f'"{self.output_path + fn[:-len(self.config.EXTENSION)]}.7z"', f'"{self.config.RECORDS_PATH}\\{fn}"']
                    subprocess.run(" ".join(command))
                    shutil.move(self.config.RECORDS_PATH + '\\' + fn, self.processed_path + fn)
                    f.write(f'F: {fn} | FP: {file_password} | LP: {link_password} | L: \n')

    def send_2_discord(self):
        data = None
        with open('passwords', 'r', encoding="utf-8") as f:
            data = [line.strip('\n').split(' | ') for line in f.readlines()]

        with open('passwords', 'w+', encoding="utf-8") as f:
            for line in data:
                fn = line[0][2::]
                file_password = line[1][3::]
                link_password = line[2][3::]
                link = line[3][2::].strip(' ')


                if link == '':
                    print(f'{Fore.YELLOW}{fn} SKIPPED - No SHARE LINK specified.')
                    f.write(' | '.join(line) + '\n')
                    continue

                if line[0][0] == '*':
                    f.write(' | '.join(line) + '\n')
                    continue
                else:
                    f.write('*' + ' | '.join(line) + '\n')


                    msg = {
                        'title': f'{fn}',
                        'description': 'W razie wątpliwości pytać na <#809980920249319465>;',
                        'fields': [
                            {'name': 'Link do nagrania:', 'value': f'[Kliknij, aby się przenieść.]({link})', 'inline': False},
                            {'name': 'Hasło dostępu:', 'value': f'```{link_password}```', 'inline': True},
                            {'name': 'Hasło do pliku:', 'value': f'```{file_password}```', 'inline': True}
                        ],
                        'footer': {
                            'text': f'~{self.config.NAME}', 'inline': True
                        }
                    }

                    self.webhook.send('Nowe nagranie zostało udostępnione.', username='Student.', embed=Embed().from_dict(msg),
                                avatar_url="https://cdn4.iconfinder.com/data/icons/science-131/64/265-512.png")


    def run(self):
        self._check_7zip()
        self._generate_dirs()
        self.process_files()
        self.send_2_discord()


if __name__ == "__main__":
    colorama.init(autoreset=True)
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="Display errors in console.", action="store_true", default=False)
    args = parser.parse_args()

    CONFIG = Settings()
    app = App(CONFIG)
    try:
        app.run()
    except Exception as e:
        if args.verbose:
            print(e)
        exit(f'{Fore.RED}An Error occured program will exit.')
