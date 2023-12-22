import math
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
                allowed = range(1, value)
            elif rule_spec['op'] == '>':
                allowed = range(value + 1, 4001)
            else:  # rule_spec['op'] is None
                allowed = range(1, 4001)
            return field, allowed, result

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
            for field, allowed_range, target in workflows[flow]:
                if not field or part[field] in allowed_range:
                    flow = target
                    break
        if flow == 'A':
            accepted.append(part)
    return sum(sum(part.values()) for part in accepted)


def intersect(r1, r2):
    return range(max(r1.start, r2.start), min(r1.stop, r2.stop))


def complement(rule):
    if rule.start == 1:
        return range(rule.stop, 4001)
    return range(1, rule.start)


def part2(filename):
    workflows, _ = parse_input(filename)

    def count_paths(label, restrictions):
        if label == 'A':
            return math.prod(len(r) for r in restrictions.values())
        if label == 'R':
            return 0
        workflow = workflows[label]
        total = 0
        for field, rule, target in workflow:
            if field:
                # There is a condition and we have to consider two possibilities
                current_range = restrictions[field]
                success_range = intersect(current_range, rule)
                fail_range = intersect(current_range, complement(rule))
                if success_range:
                    # Success condition is possible, count its paths
                    success_restrictions = restrictions.copy()
                    success_restrictions[field] = success_range
                    total += count_paths(target, success_restrictions)
                if fail_range:
                    # Fail condition is possible, consider the next rule
                    restrictions = restrictions.copy()
                    restrictions[field] = fail_range
                else:
                    # If we can't fail, we can't reach the next rule(s)
                    break
            else:
                # Final rule, with automatic forwarding
                total += count_paths(target, restrictions)
        return total

    init_restrictions = {
        'x': range(1, 4001),
        'm': range(1, 4001),
        'a': range(1, 4001),
        's': range(1, 4001),
    }
    return count_paths('in', init_restrictions)


if __name__ == '__main__':
    assert part1('inputs/sample19.txt') == 19114
    print('Part 1:', part1('inputs/day19.txt'))
    assert part2('inputs/sample19.txt') == 167409079868000
    print('Part 2:', part2('inputs/day19.txt'))
