from collections import Counter


class Solution:
    def findTheDifference(self, s: str, t: str) -> str:
        s, t = sorted(s) + [' '], sorted(t)
        for s1, t1 in zip(s, t):
            if s1 != t1:
                return t1

    def findTheDifference1(self, s: str, t: str) -> str:
        return (Counter(t) - Counter(s)).popitem()[0]

    def findTheDifference2(self, s: str, t: str) -> str:
        hash = [0] * 26
        for c in s:
            hash[ord(c) - ord('a')] += 1
        for c in t:
            hash[ord(c) - ord('a')] -= 1
            if hash[ord(c) - ord('a')] < 0:
                return c


if __name__ == '__main__':
    s = Solution()
    v = s.findTheDifference2('abcd', 'abcde')
    print(v)
