# from hashcode import get_input
from pprint import pprint

from dataclasses import dataclass, field

# from pprint import pprint as print
from typing import List, Dict, Tuple


@dataclass
class Contributor:
    name: str = ""
    skills: Dict[str, int] = field(default_factory=dict)


@dataclass
class Project:
    name: str = ""
    duration: int = 0
    score: int = 0
    best_before: int = 0
    skills: List[Tuple[str, int]] = field(default_factory=list)


def get_input(file_name):
    contributors = {}
    projects = {}
    with open(file_name) as file:
        C, P = [int(x) for x in file.readline().split()]

        # Contributor Input
        for i in range(C):
            c = Contributor()
            c.name, skillN = file.readline().split()
            for j in range(int(skillN)):
                sName, sLevel = file.readline().split()
                c.skills[sName] = int(sLevel)
            contributors[c.name] = c

        # Project input
        for i in range(P):
            p = Project()

            p.name, p.duration, p.score, p.best_before, rolesN = [
                str(prop) if idx == 0 else int(prop)
                for idx, prop in enumerate(file.readline().split())
            ]

            for j in range(rolesN):
                sName, sLevel = file.readline().split()
                p.skills.append((sName, int(sLevel)))
            projects[p.name] = p

    return C, P, contributors, projects


def get_sol():
    out = []
    with open("our_output.txt", "r") as f:
        C = int(f.readline())
        for i in range(C):
            out.append((f.readline().strip(), f.readline().split()))
    return out


def get_project_score(project, start_time):
    return max(
        0, project.score + min(0, project.best_before - (project.duration + start_time))
    )


def score():
    pprint(get_input("in.txt"))
    s = get_sol()
    C, P, contributors, projects = get_input("in.txt")
    score = 0
    steps = 0
    current = []
    busy = set()
    while True:
        # add projects to current
        while s:
            # the current project
            check = s.pop(0)
            # check if busy
            if not any([person in busy for person in check[1]]):
                # check if levels are valid
                this_projects_contributors = [contributors[x] for x in check[1]]
                for required_skill, skill_level in projects[check[0]].skills:
                    can_do = False
                    for person in this_projects_contributors:
                        # Can the person do this?
                        if person.skills.get(required_skill, 0) >= skill_level:
                            can_do = True
                        # Can the person be mentored and do this?
                    if not can_do:
                        return None

                # add
                k = projects[check[0]]
                k.people = check[1]
                k.duration_c = k.duration
                current.append(k)
                for p in check[1]:
                    busy.add(p)
            else:
                s.insert(0, check)
                break

        # check if any project is now done
        for p in current:
            p.duration_c -= 1
            if p.duration_c < 1:
                # LEVEL UP THEM PEOPLE

                for required_skill, skill_level in p.skills:
                    print("FINISHED", required_skill, skill_level)
                    # can_do = False
                    for person in this_projects_contributors:
                        if person.skills.get(required_skill, 0) >= skill_level:
                            person.skills[required_skill] += 1

                for person in p.people:
                    busy.remove(person)
                # current = [x for x in current if x.name  != p.name]
                current.remove(p)
                score += get_project_score(p, (steps + 1) - p.duration)
                print(p.name, get_project_score(p, (steps + 1) - p.duration), steps)

        if not current and not s:
            break

        steps += 1

    return score


if __name__ == "__main__":
    # pass
    # This is a hack to get the program to return None when it can't find a
    # solution.
    print(score())
