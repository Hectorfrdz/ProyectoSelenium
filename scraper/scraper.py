import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

class Scraper:
    def __init__(self, driver_path, actions_file):
        self.driver_path = driver_path
        self.actions_file = actions_file
        self.driver = None
        self.wait = None
        options = Options()
        options.add_argument("--ignore-certificate-errors")
        self.actions = self.load_actions()

    def load_actions(self):
        with open(self.actions_file, 'r') as file:
            return json.load(file)

    def setup_driver(self):
        service = Service(self.driver_path)
        self.driver = webdriver.Chrome(service=service)
        self.wait = WebDriverWait(self.driver, 10)

    def execute_actions(self):
        self.driver.get(self.actions['url'])
        for action in self.actions['actions']:
            if action['action'] == 'click':
                self.handle_click(action)
            elif action['action'] == 'wait':
                self.handle_wait(action)
            elif action['action'] == 'send_keys':
                self.handle_send_keys(action)
            elif action['action'] == 'extract':
                self.handle_extract(action)

    def handle_click(self, action):
        try:
            by = action['selector']['by'].upper().replace(" ", "_")
            element = self.wait.until(EC.element_to_be_clickable((getattr(By, by), action['selector']['value'])))
            element.click()
        except Exception as e:
            print(f"Error al realizar acción de clic: {e}")
            self.driver.quit()
            exit()

    def handle_extract(self, action):
        try:
            self.wait.until(EC.presence_of_element_located((getattr(By, action['selector']['by'].upper()), action['selector']['value'])))
            rows = self.find_elements(action['selector'])

            extracted_data = []
            for row in rows:
                # Verificar si el elemento contiene la celda 'Ver más' y omítelo
                if "Ver más" in row.text:
                    continue
                
                data = {}
                for field in action['extract']:
                    try:
                        element = row.find_element(by=getattr(By, field['selector']['by'].upper()), value=field['selector']['value'])
                        data[field['field']] = element.text.strip() if field['field'] != 'link' else element.get_attribute('href').strip()
                    except Exception as e:
                        data[field['field']] = ''
                extracted_data.append(data)

            # Guardar los datos en Excel
            self.save_to_excel(extracted_data, action.get('description', 'data'))
            
        except Exception as e:
            print(f"Error al extraer datos: {e}")
            self.driver.quit()
            exit()

    def find_element(self, selector):
        by = selector['by']
        value = selector['value']
        return self.driver.find_element(getattr(By, by.upper()), value)

    def find_elements(self, selector):
        by = selector['by']
        value = selector['value']
        return self.driver.find_elements(getattr(By, by.upper()), value)

    def save_to_excel(self, data, description):
        df = pd.DataFrame(data)
        excel_file = f'{description}_data.xlsx'
        df.to_excel(excel_file, index=False)
        print(f'Se han extraído {len(data)} elementos.')
        print(f'Los datos han sido guardados en "{excel_file}".')

    def handle_send_keys(self, action):
        try:
            element = self.wait.until(EC.presence_of_element_located((getattr(By, action['selector']['by'].upper()), action['selector']['value'])))
            element.send_keys(action['value'])
        except Exception as e:
            print(f"Error al enviar teclas: {e}")
            self.driver.quit()
            exit()

    def handle_wait(self, action):
        try:
            if action['selector']['by'] == 'seconds':
                time.sleep(action['selector']['value'])
            else:
                self.wait.until(EC.presence_of_element_located((getattr(By, action['selector']['by'].upper()), action['selector']['value'])))
        except Exception as e:
            print(f"Error al esperar elemento: {e}")
            self.driver.quit()
            exit()
                
    def quit(self):
        if self.driver:
            self.driver.quit()
