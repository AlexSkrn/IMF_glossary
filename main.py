import os

from logging_config import get_logger

_logger = get_logger(logger_name=__name__)


def is_note(text: str) -> bool:
    if text.startswith('[') and text.endswith(']'):
        return True


def get_line(terms: list, num_elem: int) -> str:
    output = []
    for term in terms:
        term = term.strip()
        if len(output) % 2 == 0:  # term position
            if is_note(term):
                output.append('')
                output.append(term)
            else:
                output.append(term)
        else:  # note position
            if is_note(term):
                output.append(term)
            else:
                output.append('')
                output.append(term)
    output.extend(['']*(num_elem-len(output)))
    return '\t'.join(output)


def read_glossary(path: str) -> list:
    en_terms: list = []
    ru_terms: list = []
    with open(path, "r", encoding="utf-8") as from_file:
        for line in from_file:
            try:
                en, ru = line.strip().split('\t')
            except ValueError as err:
                _logger.debug(line)
                raise err
            en_term = en.split('|')
            ru_term = ru.split('|')
            en_terms.append(en_term)
            ru_terms.append(ru_term)
    return en_terms, ru_terms


if __name__ == "__main__":
    path = os.path.join('data', 'IMF_glossary.txt')

    en_terms, ru_terms = read_glossary(path)

    en_num_elem = len(max(en_terms, key=len))
    ru_num_elem = len(max(ru_terms, key=len))

    print('Max # of elements in English terms: ', en_num_elem)
    print('Max # of elements in Russian terms: ', ru_num_elem)

    target = os.path.join('data', 'IMF_glossary_structured.txt')

    en_title = 'en_term\ten_note\t' * en_num_elem
    ru_title = 'ru_term\tru_note\t' * ru_num_elem
    title = en_title + ru_title

    prev_elem_len = 0

    with open(target, 'w', encoding='utf-8') as tof:
        tof.write(title + '\n')
        for en, ru in zip(en_terms, ru_terms):
            line = get_line(en, en_num_elem * 2) + '\t' + get_line(ru, ru_num_elem * 2) + '\n'
            actual_len = len(line.split('\t'))
            if actual_len != prev_elem_len:
                prev_elem_len = actual_len
                _logger.debug(actual_len)
            tof.write(line)
