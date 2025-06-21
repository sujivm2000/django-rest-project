import os
import sys

sys.path.insert(1, os.getcwd())

import traceback, logging, json, requests
from pprint import pprint
from optparse import OptionParser

from deepdiff import DeepDiff

from base.utils import standalone_main, init_logger, close_logger, makedir_p, import_module_var


class TestRunner:
    def parse(self):
        self.parser = OptionParser()
        self.add_parser_options(self.parser)
        (self.options, args) = self.parser.parse_args()

        self.init()

    def add_parser_options(self, parser):

        parser.add_option("-d", "--debug", dest="debug", help="Debug logs", default=False, action='store_true')

        parser.add_option("", "--name", dest="name", default='', help="Name of the test run.")

        parser.add_option("", "--api", dest="api", default='', help="autotest server api")
        parser.add_option("", "--sourceschema_api", dest="sourceschema_api", default='', help="sourceschema server api")

        parser.add_option("", "--download-dir", dest="download_dir", default='', help="Relative path of Download dir.")

        parser.add_option("", "--code-dir", dest="code_dir", default='.', help="Relative path of code dir.")
        parser.add_option("", "--func-path", dest="func_path", default='',
                          help="Relative path of function from code dir.")

        parser.add_option("", "--ignore-empty-none", dest="ignore_empty_none", default=False, action='store_true',
                          help="Ignore empty value vs None failures")
        parser.add_option("", "--ignore-order", dest="ignore_order", default=False, action='store_true',
                          help="Ignore event orders of dicts")
        parser.add_option("", "--ignore-additionalinfo", dest="ignore_additionalinfo", default=False,
                          action='store_true', help="Ignore additionalinfo values")
        parser.add_option("", "--ignore-terminal", dest="ignore_terminal", default=False, action='store_true',
                          help="Ignore terminal names")
        parser.add_option("-v", "--ignore-matched-values", dest="ignore_matched_values", default=False,
                          action='store_true', help="Display only values changed info")
        parser.add_option("", "--filter-failures", dest="filter_failures", default=False, action='store_true',
                          help="Display only failure testcases")

    def init(self):
        if not (self.options.name and self.options.api and self.options.code_dir and self.options.func_path):
            self.parser.print_help()
            raise Exception('Invalid options')

        self.log = init_logger(
            os.path.join(__file__[:-3] + '.log'),
            level=logging.DEBUG if self.options.debug else logging.INFO,
        )
        self.model = self.options.api.split('/')[-3]
        if self.options.sourceschema_api:
            self.sourceschema_model = self.options.sourceschema_api.split('/')[-2]

    def process(self):
        self.data = self.download(self.options.api, self.model)
        self.sourceschema_data = None
        if hasattr(self, 'sourceschema_model'):
            self.sourceschema_data = self.download(self.options.sourceschema_api, self.sourceschema_model)
        self.test()

    def close(self):
        close_logger(self.log)

    def download(self, api, model):
        if self.options.download_dir:
            makedir_p(self.options.download_dir)

        filename = os.path.join(self.options.download_dir, '%s.%s.json' % (self.options.name, model))

        if self.options.download_dir and os.path.exists(filename):
            self.log.info('Loading from local file %s' % filename)
            try:
                data = json.load(open(filename, 'r'))
                return data
            except Exception as e:
                self.log.error('Loading from local file %s: %s' % (filename, e))

        self.log.info('Downloading from api %s' % api)
        response = requests.get(api)
        if not response.status_code == 200:
            raise Exception('Invalid response %s' % response.status_code)
        data = json.loads(response.text)
        if not data:
            raise Exception('Invalid data')

        if self.options.download_dir:
            open(filename, 'w').write(json.dumps(data))
        return data

    def test(self):
        os.chdir(self.options.code_dir)
        sys.path.insert(0, self.options.code_dir)
        self.func = import_module_var(self.options.func_path, None)
        if not self.func:
            raise Exception('Unable to import func %s' % self.options.func_path)

        self.tc_total, self.tc_success = 0, 0
        print('\n.................................... Test Run - %s .................' % self.options.name)
        if self.model == 'suite':
            for category in self.data.get('categories', []):
                for tc in category.get('testcases', []):
                    self.run_testcase(tc, 'suite-%s/category-%s/' % (self.data['id'], category['id']))
        elif self.model == 'category':
            for tc in self.data.get('testcases', []):
                self.run_testcase(tc, 'category-%s/' % self.data['id'])

        elif self.model == 'testcase':
            self.run_testcase(self.data)
        else:
            raise Exception('Invalid model %s in api %s' % (self.model, self.api))

        print('.................................... Stats ..........................')
        if self.tc_total:
            print('Total testcases=%d, success=%d. success rate %.2f%%' % (
                self.tc_total, self.tc_success, (self.tc_success * 100.0 / self.tc_total)))
        else:
            print('No Testcases run')

        print('.................................... Done ...........................')

    def run_testcase(self, tc, prefix=''):
        errors = None
        exclude_regex_paths = None
        try:
            output = self.func(tc['input'], tc['config'] or {}, self.sourceschema_data)
        except Exception as e:
            print(e, traceback.print_exc())
            errors = 'Error in func %s: %s' % (self.func, e)

        if not errors:
            if output == None:
                errors = 'Invalid TestCase'
            else:
                try:
                    tc_output = tc['output']['data']
                    ignore_order = self.options.ignore_order and len(tc_output) == len(output)
                    ignore_addtnlinfo = self.options.ignore_additionalinfo
                    ignore_terminal = self.options.ignore_terminal
                    if ignore_addtnlinfo:
                        exclude_regex_paths = [
                            r"root\['additionalInfo']",
                            r"root\['events']\[\d+\]\['additionalInfo']"
                        ]
                    if ignore_terminal:
                        exclude_regex_paths.extend([
                            r"root\['stops']\[\d+\]\['location']\['terminal']",
                            r"root\['events']\[\d+\]\['location']\['terminal']",
                        ])
                    errors = DeepDiff(tc_output, output, ignore_order=ignore_order,
                                      exclude_regex_paths=exclude_regex_paths)
                    if self.options.ignore_empty_none:
                        errors = self.remove_empty_none_errors(errors, tc_output, output)

                except Exception as e:
                    print(e, traceback.print_exc())
                    errors = 'Output verification failed: %s' % e
        if errors:
            status = 'Failed'
        else:
            status = 'Success'
            self.tc_success += 1
        self.tc_total += 1

        if self.options.filter_failures and status == 'Failed':
            print('%sTestcase/%s: %s' % (prefix, tc['id'], status))
            pprint(errors)
        if not self.options.filter_failures:
            print('%sTestcase/%s: %s' % (prefix, tc['id'], status))
            pprint(errors)

    def remove_empty_none_errors(self, errors, tc_output, output):
        for key, root in [
            ('dictionary_item_added', output),
            ('dictionary_item_removed', tc_output)
        ]:
            values = errors.get(key, [])
            errors[key] = []
            for val in values:
                if eval(val):
                    errors[key].append(val)
            if not errors[key]:
                del errors[key]

        key = 'type_changes'
        val_dict = errors.get(key, {})
        errors[key] = {}
        for val, err in val_dict.items():
            if err['old_value'] or err['new_value']:
                errors[key][val] = err
        if not len(errors[key]):
            del errors[key]

        if not self.options.ignore_matched_values:
            return errors

        values_changed_type = 'values_changed'
        values_changed_dict = errors.get(values_changed_type, {})
        errors[values_changed_type] = {}
        for diff_key, diff in values_changed_dict.items():
            diff_data = self.find_diff(diff['new_value'], diff['old_value'], data={})
            if self.is_empty_dict(diff_data):
                old_data = self.find_diff(diff['old_value'], diff['new_value'], data={})
                merged_data = self.merge_diffs(diff_data, old_data)
                errors[values_changed_type][diff_key] = merged_data

        if not len(errors[values_changed_type]):
            del errors[values_changed_type]

        return errors

    def merge_diffs(self, diff_data, old_data):
        for parent, child in diff_data.items():
            if not (isinstance(child, dict) and child.get('old_value')):
                continue
            for old_key in list(child.get('old_value', [])):
                if child['old_value'][old_key] == 'key-not-found':
                    del child['old_value'][old_key]
            child['old_value'].update(old_data[parent]['new_value'])
        return diff_data

    def is_empty_dict(self, raw_dict):
        for k, v in raw_dict.items():
            if v:
                return True
        return False

    def find_diff(self, new, old, data, path=''):
        if not isinstance(new, dict) and new != old:
            data.update({
                'new_value': new,
                'old_value': old
            })
        else:
            for key, val in new.items():
                old_value = old.get(key, 'key-not-found') if isinstance(old, dict) else None

                if val == old_value:
                    continue

                if isinstance(val, dict):
                    self.find_diff(val, old_value, data, key)
                else:
                    data.update(self.get_err_data(path, val, old_value, key))
        return data

    def get_err_data(self, path, new_value, old_value, key):
        err = {
            'new_value': {
                key: new_value
            },
            'old_value': {
                key: old_value
            }
        }
        if path:
            return {path: err}
        return err


if __name__ == '__main__':
    standalone_main(TestRunner)
