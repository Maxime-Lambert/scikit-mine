from src.CodeTable import CodeTable
from src.SQS_v2.Pattern import Pattern


class CodeTable(CodeTable):

    def private(self, pattern_to_private):
        print(self.patternMap)
        res = {}
        for pattern, codelength in self.patternMap.items():
            if pattern != pattern_to_private:
                res[pattern] = codelength
        return res

    def codetable_from_sqs(self, alignement):
        return CodeTable(alignement, self.data)

    def __getitem__(self, pattern_to_find):
        """
            Gives the corresponding code length to a pattern

            If the pattern isn't in the patternMap returns None

            :return: the code length corresponding to the pattern_to_find
            :rtype: double | None
        """
        for pattern, codelength in self.patternMap.items():
            if pattern == pattern_to_find:
                return codelength
        return None
