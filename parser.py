def parse_command(cmd):
    original_cmd = cmd.strip().rstrip(";")
    lowered_cmd = original_cmd.lower()

    if lowered_cmd.startswith("create table"):
        tokens = original_cmd.split()
        name = tokens[2]
        inside = original_cmd[original_cmd.find("(")+1 : original_cmd.find(")")]
        column_parts = [col.strip() for col in inside.split(",")]

        columns = []
        primary_key = None
        for col_def in column_parts:
            parts = col_def.split()
            col_name = parts[0]
            columns.append(col_name)
            if len(parts) > 2 and parts[1].upper() == "PRIMARY" and parts[2].upper() == "KEY":
                primary_key = col_name

        return ("CREATE", name, columns, primary_key)

    elif lowered_cmd.startswith("insert into"):
        tokens = original_cmd.split()
        name = tokens[2]
        inside = original_cmd[original_cmd.find("(")+1 : original_cmd.find(")")]
        values = [eval(x.strip()) for x in inside.split(",")]
        return ("INSERT", name, values)

    elif lowered_cmd.startswith("select"):
        where_clause = None
        if "where" in lowered_cmd:
            parts = original_cmd.split("WHERE")
            table = parts[0].split("FROM")[1].strip()
            column, _, value = parts[1].strip().split()
            value = eval(value)
            where_clause = lambda row, cols: row[cols.index(column)] == value
        else:
            table = original_cmd.split("FROM")[1].strip()
        return ("SELECT", table, where_clause)

    elif lowered_cmd.startswith("delete"):
        parts = original_cmd.split("WHERE")
        table = parts[0].split("FROM")[1].strip()
        column, _, value = parts[1].strip().split()
        value = eval(value)
        where_clause = lambda row, cols: row[cols.index(column)] == value
        return ("DELETE", table, where_clause)

    elif lowered_cmd.startswith("update"):
        parts = original_cmd.split("SET")
        table = parts[0].split()[1].strip()
        set_part = parts[1].split("WHERE")[0].strip()
        column, _, value = set_part.strip().split()
        value = eval(value)
        where_part = parts[1].split("WHERE")[1].strip()
        cond_col, _, cond_val = where_part.split()
        cond_val = eval(cond_val)
        where_clause = lambda row, cols: row[cols.index(cond_col)] == cond_val
        return ("UPDATE", table, column, value, where_clause)

    elif lowered_cmd.startswith("drop table"):
        tokens = original_cmd.split()
        name = tokens[2]
        return ("DROP", name)

    elif lowered_cmd.startswith("show tables"):
        return ("SHOW_TABLES",)

    elif lowered_cmd.startswith("describe"):
        tokens = original_cmd.split()
        name = tokens[1]
        return ("DESCRIBE", name)

    else:
        return ("UNKNOWN",)
