from src.CodeTable import CodeTable
from src.SQS_v2.Pattern import Pattern


class CodeTable(CodeTable):

    lower_key = 1

    def private(self, pattern_to_private):
        res = {}
        for pattern, codelength in self.patternMap.items():
            if pattern != pattern_to_private:
                res[pattern] = codelength
        return res

    def codetable_from_sqs(self, list_pattern):
        for pattern in list_pattern:
            self.add(pattern)
        #return CodeTable(tmp, self.data)

    def __repr__(self):
        """
            Gives a string representation of a Codetable

            :return: A String representing the Codetable
            :rtype: String
        """
        res = ""
        for pattern in self.patternMap.keys():
            res += str(pattern.elements) + "  #USG : "
            res += str(pattern.usage) + " \n"
            # res += " #CODELEN : " + str(self.patternMap[pattern]) + "\n"
        return res

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

    def get_list_pattern(self):
        res = []
        for pattern, codelength in self.patternMap.items():
            res.append(pattern)
        return res

    def add(self, pattern_to_add):
        """
            Adds a Pattern to the Codetable.

            :param pattern_to_add: The pattern you want to add to the Codetable
            :type pattern_to_add: Pattern
        """
        if pattern_to_add in self.patternMap:
            for k in self.patternMap.keys():
                if k.elements == pattern_to_add.elements:
                    k.usage += 1
                    k.support += 1
        else:
            self.patternMap[pattern_to_add] = pattern_to_add.usage
        self.update_usage()

    def update_usage(self):
        test = {}
        tmp = self.list_sort_key()
        delete = []
        for p in tmp:
            for pattern, usage in self.patternMap.items():
                if p.contains(pattern):
                    res = usage - p.usage
                    if res != 0:
                        test[pattern] = res
                    else:
                        delete.append(pattern)
                else:
                    if pattern not in test.keys():
                        test[pattern] = pattern.usage
        self.patternMap = test
        self.patternMap = self.delete(delete)

    def list_sort_key(self):
        tmp = []
        for pattern, usage in self.patternMap.items():
            tmp.append(pattern)
        old = []
        while tmp != old:
            old = tmp
            current = tmp[0]
            lower = []
            upper = []

            for i in range(1, len(tmp)):
                if len(tmp[i]) > len(current):
                    upper.append(tmp[i])
                else:
                    lower.append(tmp[i])
            tmp = upper + [current]
            tmp = tmp + lower
        return tmp

    def delete(self, list_deleted):
        res = {}
        for pattern in self.order_by_standard_cover_order():
            if pattern.usage != 0 :
                res[pattern] = pattern.usage
        return res

    def reduce(self):

        res = {}
        l = list(self.patternMap.keys())
        mini = l[0].usage
        tmp = [l[0].elements]
        for i in range(1, len(l)):
            if l[i].elements not in tmp:
                tmp.append(l[i].elements)
        for element in tmp:
            for pattern in self.order_by_standard_cover_order():
                if pattern.elements == element:
                    if pattern.usage < mini:
                        mini = pattern.usage
            p = Pattern(element)
            p.usage = mini
            res[p] = p.usage
        self.patternMap = res
        self.not_include()


    def not_include(self):
        change = True
        l = self.list_sort_key()
        res = {}
        pattern_delete = []
        while change:
            old = pattern_delete.copy()
            for p in l:
                for pattern in self.order_by_standard_cover_order():
                    if not p.is_sub_list(pattern):
                        if pattern.elements not in pattern_delete:
                            res[pattern] = pattern.usage
                    else:
                        if pattern.elements not in pattern_delete:
                            pattern_delete.append(pattern.elements)
            change = pattern_delete != old
        self.patternMap = res


        """pat = l[0]
        mini = pat.usage
        tmp = [pat]
        while tmp != []:
            pat = tmp[0]
            for pattern in self.order_by_standard_cover_order():
                if pattern.elements == pat.elements:
                    if pattern.usage < mini:
                        mini = pattern.usage
                else:
                    l_tmp = list(res.keys())
                    not_exist = True
                    i = 0
                    if l_tmp != []:
                        while i < len(l_tmp):
                            if l_tmp[i].elements == pattern.elements:
                                not_exist = not_exist and False
                            else:
                                not_exist = not_exist and True
                            i += 1
                        if not_exist:
                            tmp.append(pattern)
                    else:
                        tmp.append(pattern)
            res[pat] = mini
        self.patternMap = res """