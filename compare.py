
import datetime
import os

def get_indexes_for_record(current_values, old_file_values, shop):
    print('current_values', len(current_values))
    print('old_file_values', len(old_file_values))
    print('\n\n\n\n\n\n\n\n\n\n')
    result = list()
    sub_current_values = current_values
    for index in old_file_values.keys():
        values_list = old_file_values[index]
        title_old = values_list[1]
        size_old = values_list[2]
        print(values_list)
        print('title_old', title_old)
        for record in current_values:
            print(record)
            if shop == 'FAMILY BOARDSHOP':
                try:
                    if len(record) > 3:
                        title_current = record[0]
                        sizes_current = record[3]
                        if title_current == title_old and size_old in sizes_current:
                            result.append([index] + record)
                            sub_current_values.remove(record)
                    else:
                        title_current = record[0]
                        if title_current == title_old:
                            result.append([index] + record)
                            sub_current_values.remove(record)
                except:
                    pass
            elif shop == 'Rollershop':
                title_current = record[1]
                sizes_current = record[3]
                if title_current == title_old and size_old in sizes_current:
                    result.append([index] + record)
                    sub_current_values.remove(record)
            elif shop == 'Dominant':
                title_current = record[0]
                sizes_current = record[2]
                if title_current == title_old and size_old in sizes_current:
                    result.append([index] + record)
                    sub_current_values.remove(record)
    # print(result)
    return result, sub_current_values
