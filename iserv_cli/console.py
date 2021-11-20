import pandas as pd
import json
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()

output_directory = os.environ['ISERV_OUTPUT_DIRECTORY']


class ConsoleDisplayCli:
    def write_list(self, values):
        display = '\n'.join(values)
        print(display)

    def generate_display_content(self, content, output_type):
        if output_type == 'table':
            return pd.DataFrame(content)
        if output_type == 'json':
            data = pd.DataFrame(content).to_dict(orient='records')
            return json.dumps(data, indent=True)
        if output_type == 'text':
            return content
        if output_type == 'list':
            if isinstance(content, list):
                return '\n'.join(content)

        raise Exception(f'{output_type} is not a valid output type')

    def write(self, content, output_type):
        if output_type == 'file-json':
            content = self.generate_display_content(
                content=content, output_type='json')
            self.write_file(content, 'json')
        elif output_type == 'file-table':
            content = self.generate_display_content(
                content=content, output_type='table')
            self.write_file(content.to_string(), 'txt')
        elif output_type == 'file-csv':
            content = self.generate_display_content(
                content=content, output_type='table')
            filename = datetime.now().strftime('%Y%m%d%H%M%S') + '.csv'
            content.to_csv(filename, index=False)
        else:
            content = self.generate_display_content(
                content=content, output_type=output_type)

        print(content)

    def write_file(self, content, file_type, path=None):
        try:
            filename = datetime.now().strftime('%Y%m%d%H%M%S')
            if path is None:
                with open(f'{output_directory}/{filename}.{file_type}', 'w') as file:
                    file.write(content)
            else:
                with open(f'{output_directory}/{filename}.{file_type}', 'w') as file:
                    file.write(content)
        except Exception as ex:
            raise Exception(f'Failed to write output to file: {str(ex)}')
