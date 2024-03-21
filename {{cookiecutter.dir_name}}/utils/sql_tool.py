import re
import json
import datetime


def list2str(datas):
    """
    列表转字符串
    :param datas: [1, 2]
    :return: (1, 2)
    """
    data_str = str(tuple(datas))
    data_str = re.sub(",\)$", ")", data_str)
    return data_str


def format_sql_value(value):
    if isinstance(value, str):
        value = value.strip()

    elif isinstance(value, (list, dict)):
        value = json.dumps(value)

    elif isinstance(value, (datetime.date, datetime.time)):
        value = str(value)

    elif isinstance(value, bool):
        value = int(value)

    return value


# 查询sql
def make_find_sql(
        table, columns, condition
):
    """
    @param table:
    @param columns: 要查询的字段名
    @param condition: 查询条件
    """
    select_columns = ','.join(["`{}`".format(key) for key in columns])
    if condition:
        sql = (
            "select {select_columns} from `{table}` where {condition}"
        )
        sql = sql.format(select_columns=select_columns, table=table, condition=condition)
    else:
        sql = (
            "select {select_columns} from `{table}`"
        )
        sql = sql.format(select_columns=select_columns, table=table)
    return sql


# 插入sql，存在即更新
def make_insert_sql(
        table, data, auto_update=False, update_columns=(), insert_ignore=False
):
    """
    @summary: 适用于mysql， oracle数据库时间需要to_date 处理（TODO）
    ---------
    @param table:
    @param data: 表数据 json格式
    @param auto_update: 使用的是replace into， 为完全覆盖已存在的数据
    @param update_columns: 需要更新的列 默认全部，当指定值时，auto_update设置无效，当duplicate key冲突时更新指定的列
    @param insert_ignore: 数据存在忽略
    ---------
    @result:
    """
    keys = ["`{}`".format(key) for key in data.keys()]
    keys = list2str(keys).replace("'", "")

    values = [format_sql_value(value) for value in data.values()]
    values = list2str(values)

    if update_columns:
        if not isinstance(update_columns, (tuple, list)):
            update_columns = [update_columns]
        update_columns_ = ", ".join(
            ["{key}=values({key})".format(key=key) for key in update_columns]
        )
        sql = (
                "insert%s into `{table}` {keys} values {values} on duplicate key update %s"
                % (" ignore" if insert_ignore else "", update_columns_)
        )
    elif auto_update:
        sql = "replace into `{table}` {keys} values {values}"
    else:
        sql = "insert%s into `{table}` {keys} values {values}" % (
            " ignore" if insert_ignore else ""
        )

    sql = sql.format(table=table, keys=keys, values=values).replace("None", "null")
    return sql


def make_batch_sql(
        table, datas, auto_update=False, update_columns=(), update_columns_value=()
):
    """
    @summary: 生产批量的sql
    ---------
    @param table:
    @param datas: 表数据 [{...}]
    @param auto_update: 使用的是replace into， 为完全覆盖已存在的数据
    @param update_columns: 需要更新的列 默认全部，当指定值时，auto_update设置无效，当duplicate key冲突时更新指定的列
    @param update_columns_value: 需要更新的列的值 默认为datas里边对应的值, 注意 如果值为字符串类型 需要主动加单引号， 如 update_columns_value=("'test'",)
    ---------
    @result:
    """
    if not datas:
        return

    keys = list(datas[0].keys())
    values_placeholder = ["%s"] * len(keys)

    values = []
    for data in datas:
        value = []
        for key in keys:
            current_data = data.get(key)
            current_data = format_sql_value(current_data)

            value.append(current_data)

        values.append(value)

    keys = ["`{}`".format(key) for key in keys]
    keys = list2str(keys).replace("'", "")

    values_placeholder = list2str(values_placeholder).replace("'", "")

    if update_columns:
        if not isinstance(update_columns, (tuple, list)):
            update_columns = [update_columns]
        if update_columns_value:
            update_columns_ = ", ".join(
                [
                    "`{key}`={value}".format(key=key, value=value)
                    for key, value in zip(update_columns, update_columns_value)
                ]
            )
        else:
            update_columns_ = ", ".join(
                ["`{key}`=values(`{key}`)".format(key=key) for key in update_columns]
            )
        sql = "insert into `{table}` {keys} values {values_placeholder} on duplicate key update {update_columns}".format(
            table=table,
            keys=keys,
            values_placeholder=values_placeholder,
            update_columns=update_columns_,
        )
    elif auto_update:
        sql = "replace into `{table}` {keys} values {values_placeholder}".format(
            table=table, keys=keys, values_placeholder=values_placeholder
        )
    else:
        sql = "insert ignore into `{table}` {keys} values {values_placeholder}".format(
            table=table, keys=keys, values_placeholder=values_placeholder
        )

    return sql, values


def make_update_sql(table, data, condition):
    """
    @summary: 适用于mysql， oracle数据库时间需要to_date 处理（TODO）
    ---------
    @param table:
    @param data: 表数据 json格式
    @param condition: where 条件
    ---------
    @result:
    """
    key_values = []

    for key, value in data.items():
        value = format_sql_value(value)
        if isinstance(value, str):
            key_values.append("`{}`={}".format(key, repr(value)))
        elif value is None:
            key_values.append("`{}`={}".format(key, "null"))
        else:
            key_values.append("`{}`={}".format(key, value))

    key_values = ", ".join(key_values)

    sql = "update `{table}` set {key_values} where {condition}"
    sql = sql.format(table=table, key_values=key_values, condition=condition)
    return sql
