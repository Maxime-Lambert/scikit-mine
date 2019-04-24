from src.CodeTable import CodeTable
from src.SQS_v2.Pattern import Pattern


class CodeTable(CodeTable):

    def private(self, pattern_to_private):
        res = {}
        print("patternMap")
        print(self.patternMap)
        for pattern, codelength in self.patternMap.items():
            if pattern != pattern_to_private:
                res[pattern] = codelength
        return res

    def codetable_from_sqs(self, list_alignement):
        tmp = {}
        for alignement in list_alignement:
            if alignement.pattern in tmp:
                tmp[alignement.pattern] += 1
            else:
                tmp[alignement] = 1
        return CodeTable(tmp, self.data)

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
