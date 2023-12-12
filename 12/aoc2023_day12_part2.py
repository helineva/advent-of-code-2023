""" Advent of Code 2023 (https://adventofcode.com/)
    Day 12 Part 2. (dynamic programming, quite fast) """


def compute(row, groups):
    """compute the number of ways of replacing ?'s of 'row' by .'s or #'s
    to produce a string having the group arrangement 'groups'

    use dynamic programming
    let c1 c2 c3 ... cn be the characters in 'row'
    let g1 g2 ... gk be the groups in 'groups'
    make a table T of n+1 columns and k+1 rows
    T[i,j] describes the number of ways of replacing ?'s in the string
      c1 c2 ... cj to produce a string having the group arrangement g1 g2 ... gi
    the desired number is then the entry in the lower right corner T[k,n]
    recursion is as follows:
      T[0,0] = 1 (empty string fulfils the group arrangement given by no groups)
      when j>0, T[0,j] = 0 if cj is "#", otherwise T[0,j] = T[0,j-1]
      in other words, T[0,j] is 1 until the first "#" is met, then it is 0.

      assume i>0
      T[i,0] = 0 (empty string does not fulfil the arrangement given by nonempty set of groups)
      assume j>0
      three cases:
        1) cj == "."
           there is a one-to-one correspondence of strings counted by T[i,j-1] and
           strings counted by T[i,j], given by S -> S.  (S concatenated with ".")
           hence T[i,j] = T[i,j-1]
        2) cj == "#"
           subcase gi > j: i.e. the strings considered are too short -> T[i,j] = 0
           assume gi <= j
           cj is a part of the group gi, its last element
           a string counted by T[i,j] must then end with gi #'s and hence
           c(j-gi+1) c(j-gi+2) ... cj must not contain any .'s (if it contains, then T[i,j] = 0)
           if gi == j then T[i,j] = 1 if and only if i == 1, otherwise T[i,j] = 0
           in other words T[i,j] = T[i-1,0]
           assume gi < j
           the group gi must be separated from the previous group
           hence c(j-gi) must not be #, otherwise T[i,j] = 0
           there is a one-to-one correspondence of strings counted by T[i-1,j-gi-1]
           and strings counted by T[i,j], given by S -> S.##...# (gi #'s at the end)
           hence T[i,j] = T[i-1,j-gi-1]
    T can be computed row-wise, keeping only the previous row in memory
    """
    curr = [1]
    for c in row:
        curr.append(0 if c == "#" else curr[-1])

    for g in groups:
        new = [0]

        for j, c in enumerate(row):
            x0 = new[-1]
            if c == ".":
                new.append(x0)
                continue
            x1 = 0
            if g == j + 1 and "." not in row[:j]:
                x1 = curr[0]
            if g < j + 1 and "." not in row[j - g + 1 : j] and row[j - g] in ".?":
                x1 = curr[j - g]
            new.append(x1 if c == "#" else x0 + x1)

        curr = new

    return curr[-1]


def solve_day12_part2():
    """Solve the problem"""

    repeat = 5
    count = 0

    with open("input.txt", "r", encoding="utf-8") as f:
        for line in f:
            row, groups = line.strip().split()
            row = "?".join([row] * repeat)
            groups = [int(n) for n in groups.split(",")] * repeat
            count += compute(row, groups)

    print(count)


if __name__ == "__main__":
    solve_day12_part2()
