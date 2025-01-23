import yaml
import sys


def mandatory(aws_resources, mandatory_list):
    errors = []
    data_no = 1
    for aws_resource in aws_resources:
        for mandatory in mandatory_list:
            if mandatory not in aws_resource:
                errors.append(f'In data No {data_no}, {mandatory} key is not present')
            elif aws_resource.get(mandatory) is None:
                errors.append(f'In data No {data_no}, the value of {mandatory} is not present')
        data_no += 1
    return errors


def dependency(aws_resources, dependency_list):
    errors = []
    data_no = 1
    for aws_resource in aws_resources:
        for dependency, rules in dependency_list.items():
            if dependency in aws_resource:
                if aws_resource[dependency]:  # Condition is True
                    for key in rules.get("mandatory", []):
                        if key not in aws_resource or aws_resource.get(key) is None:
                            errors.append(f"In data No {data_no}, key '{key}' is mandatory if '{dependency}' is true.")
                else:  # Condition is False
                    for key in rules.get("mandatory", []):
                        if key in aws_resource and aws_resource.get(key) is not None:
                            errors.append(
                                f"In data No {data_no}, '{dependency}' is false, but key '{key}' is present.")
        data_no += 1
    return errors


def type_check(aws_resources, type_list):
    errors = []
    data_no = 1
    for aws_resource in aws_resources:
        for key, expected_type in type_list.items():
            if key in aws_resource and aws_resource[key] is not None:
                if type(aws_resource[key]).__name__ != expected_type:
                    errors.append(f'In data No {data_no}, data type is mismatch for {key}')
        data_no += 1
    return errors


def length_check(aws_resources, length_list):
    errors = []
    data_no = 1
    for aws_resource in aws_resources:
        for key, length_constraints in length_list.items():
            if key in aws_resource and aws_resource[key] is not None:
                value = aws_resource[key]
                if isinstance(value, (str, int)):
                    value_length = len(str(value))
                    if len(length_constraints) == 1:
                        if value_length != length_constraints[0]:
                            errors.append(f"In data No {data_no}, Length of the {key} is mismatched")
                    elif len(length_constraints) == 2:
                        if not (length_constraints[0] <= value_length <= length_constraints[1]):
                            errors.append(f"In data No {data_no}, Length of the {key} is mismatched")
        data_no += 1
    return errors


def main():
    fun_file = sys.argv[1]
    conditions_file = sys.argv[2]

    with open(fun_file, 'r') as file:
        aws_resources = yaml.safe_load(file)

    with open(conditions_file, 'r') as file:
        conditions = yaml.safe_load(file)

    all_errors = []
    if "mandatory" in conditions:
        all_errors.extend(mandatory(aws_resources, conditions["mandatory"]))
    if "dependency" in conditions:
        all_errors.extend(dependency(aws_resources, conditions["dependency"]))
    if "type" in conditions:
        all_errors.extend(type_check(aws_resources, conditions["type"]))
    if "length" in conditions:
        all_errors.extend(length_check(aws_resources, conditions["length"]))

    if all_errors:
        print("\n".join(all_errors))
        sys.exit(1)  # Exit with error status
    else:
        print("Validation successful!")
        sys.exit(0)  # Exit with success status


if __name__ == "__main__":
    main()
