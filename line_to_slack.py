from typing import *
import datetime
import re


class Message:
    def __init__(self, dt: datetime.datetime, name: str, msg: str):
        self.dt = dt
        self.name = name
        self.msg = msg

    def __str__(self):
        return f'{self.dt}, {self.name}, {self.msg}'

    def to_csv_str(self):
        return f'"{int(self.dt.timestamp())}","line","{self.name}","{self.msg}"'


def parse_line_msgs(io, name_dict: Optional[Dict] = None) -> Iterator[Message]:
    """LINEの履歴の文字列をパースしてメッセージのイテレータを返します。

    日付を表す文字列が空行の後に続き、さらにその直後が改行されているとき、その文字列をメッセージの日付と解釈します。
    時刻を表す文字列が行頭がにあるとき、その文字列をメッセージの時間と解釈します。

    :param io: パースするファイル。
    :param name_dict: 名前を置換する表。
    :return: メッセージのイテレータ。
    """
    s = io.read().replace('"', '\\"')
    date_re = re.compile(r'\n\n[0-9]{4}/[0-9]{2}/[0-9]{2}\(.\)\n')
    time_re = re.compile('(?m)^[0-9]{1,2}:[0-9]{2}')
    for date_m, time_name_msg in zip(date_re.finditer(s), date_re.split(s)[1:]):
        date_str = date_m.group(0).strip()
        date = datetime.date.fromisoformat(date_str.split('(')[0].replace('/', '-'))

        hour = None
        minute = None
        name = None
        msg = None
        for line in time_name_msg.strip().splitlines():
            if time_re.match(line):
                if msg is not None:
                    yield Message(datetime.datetime(date.year, date.month, date.day, hour, minute), name, msg)
                time_str = time_re.match(line).group(0)
                hour, minute = map(lambda i: int(i), time_str.split(':'))
                hour %= 24
                name_msg = line[len(time_str):].strip()
                sep_pos = name_msg.find('	')
                name = name_msg[:sep_pos]
                if name_dict is not None and name in name_dict:
                    name = name_dict[name]
                msg = name_msg[sep_pos + 1:]
            else:
                msg += '\n' + line
        yield Message(datetime.datetime(date.year, date.month, date.day, hour, minute), name, msg)
