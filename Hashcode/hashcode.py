"""
Contributors
- name
- skills and their levels

Projects
- Name
- duration
- score
- each day >= due date deducts a point

- roles
    - one role per person. one project per person
    - has skill >= required level
    - one level below only if another has skills >= required level (mentoring)
    - contributor can mentor many, and can be mentored themselves

no skill === skill level 0

On completion...
Learning:
- contributors in roles >= skill level increase skill by 1
- others keep their level

Submission
- first line 0<=E<=P number of projects finished
- next E lines is 
    - name of project (mentioned only once)
    - name of contributors (Bob → first role, Anna → second role)
"""

from dataclasses import dataclass, field
from pprint import pprint as print
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


def put_output(file_name, completed):
    with open(file_name, "w") as file:
        file.write(str(len(completed)) + "\n")
        for pName in completed:
            file.write(pName + "\n")
            candidateNames = [candidate.name for candidate in completed[pName]]
            file.write(" ".join(candidateNames) + "\n")


"""
for every possible first project:
    assign people
    check if another project can be done simultaneously

    for every possible second project:
        ...
        for every possiblle third project:
            ...
"""

# Get all possible groups of contributors for a pro
def isolate_candidates(C, P, contributors, project):
    skill_sort = sorted(contributors, key=lambda x: len(x.skills))
    needs = project.skills
    covered = set()
    developers = []

    for need in needs:
        for contributor in contributors:
            if need[0] not in contributor.skills:
                contributor.skills[need[0]] = 0

            if (
                need not in covered
                and (
                    need[1] <= contributor.skills[need[0]]
                    or (
                        need[1] - 1 == contributor.skills[need[0]]
                        and any(
                            [
                                need[0] in p.skills and need[1] <= p.skills[need[0]]
                                for p in developers
                            ]
                        )
                    )
                )
                and contributor not in developers
            ):
                covered.add(need)
                # print(contributor)
                # exit()
                if need[1] - 1 == contributor.skills[need[0]] and any(
                    [
                        need[0] in p.skills and need[1] <= p.skills[need[0]]
                        for p in developers
                    ]
                ):
                    contributor.skills[need[0]] += 1

                developers.append(contributor)

    if len(covered) != len(needs):
        return []
    return developers


def solution(C, P, contributors, projects):
    # decision tree like struture for
    time = 0
    score = 0
    # lets find a way to choose the project for day 1 for everyone
    # we find the earliest project
    date_projects = sorted(
        projects.values(), key=lambda x: x.best_before - x.duration, reverse=True
    )  # list of projects that have yet to be completed
    busy = {name: -1 for name in contributors}  # list of contributors

    completed = dict()

    while time <= date_projects[-1].best_before + date_projects[-1].duration:
        current = date_projects.pop(0)
        # Get the current project to work on....aka the first one in the date_projects
        # Put all the busy people into the set
        # go to the next day and see if the next project is doable

        not_busy = [contributors[name] for name in contributors if busy[name] <= time]

        candidates = isolate_candidates(C, P, not_busy, current)

        # if no candidates match then add it back to date_projects
        # if not candidates:
        #     date_projects.append(current)

        if candidates:
            completed[current.name] = candidates
        else:
            date_projects.append(current)

        # update busy
        for candidate in candidates:
            busy[candidate.name] = time + current.duration

        time += 1

    return completed


def main():
    # print(get_input())

    # do work in here
    C, P, contributors, projects = get_input("in.txt")

    # print(sorted(projects, key=lambda x: x.score, reverse=True))
    completed = solution(C, P, contributors, projects)
    # output contents
    put_output("our_output.txt", completed)
    print("finished")


if __name__ == "__main__":
    main()
