import re


def parse_input(filename):
    match_rating = re.compile(r'\{x=(?P<x>\d+),m=(?P<m>\d+),a=(?P<a>\d+),s=(?P<s>\d+)').match
    rule_parts = re.compile(r'(?:(?P<field>[xmas])(?P<op>[<>])(?P<value>\d+):)?(?P<result>\w+)').fullmatch
    with open(filename) as f:
        workflows = {}

        def parse_rule(rule):
            rule_spec = rule_parts(rule)
            field = rule_spec['field']
            value = int(rule_spec['value'] or 0)
            result = rule_spec['result']
            if rule_spec['op'] == '<':
                def func(part):
                    if part[field] < value:
                        return result

                func.__qualname__ = f'{field}_less_than_{value}_to_{result}'
            elif rule_spec['op'] == '>':
                def func(part):
                    if part[field] > value:
                        return result

                func.__qualname__ = f'{field}_greater_than_{value}_to_{result}'
            else:  # rule_spec['op'] is None
                def func(part):
                    return result

                func.__qualname__ = f'to_{result}'
            return func

        for line in f:
            if not line.strip():
                break
            open_brace = line.index('{')
            close_brace = line.index('}')
            label = line[:open_brace]
            rules = line[open_brace + 1:close_brace].split(',')
            workflows[label] = [parse_rule(r) for r in rules]
        ratings = []
        for line in f:
            ratings.append({
                k: int(v)
                for k, v in match_rating(line).groupdict().items()
            })
    return workflows, ratings


def part1(filename):
    workflows, parts = parse_input(filename)
    accepted = []
    for part in parts:
        flow = 'in'
        while flow not in 'AR':
            for rule in workflows[flow]:
                if (target := rule(part)) is not None:
                    flow = target
                    break
        if flow == 'A':
            accepted.append(part)
    return sum(sum(part.values()) for part in accepted)


if __name__ == '__main__':
    assert part1('inputs/sample19.txt') == 19114
    print('Part 1:', part1('inputs/day19.txt'))