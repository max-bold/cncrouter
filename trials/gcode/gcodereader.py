import numpy as np


class gparser:
    def __init__(self):
        self.lastcom = None
        self.absmove = True
        self.absextrude = True
        self.cpos = np.zeros(7, float)
        self.cspeed = 0  # mm/s
        self.homepos = np.array((0, 0, 0, 0, 0, 0, 0))
        self.hspeed = 50  # mm/s

    def comtodict(self, line: str):
        """Strips comments and converts a line from g-code file to a dict like {'com': 'G1', 'e': -1.0, 'f': 300.0}. For comment lines (starting from ';') returns empty dict.

        Args:
            line (str): A line from g-code file

        Raises:
            ValueError: If command parameter has value and it can't be converted to a float.

        Returns:
            dict: Dictionary of command an parameters, where:
                'com' - Command
                'text' - M117 text value (for M117)

            rmk: If parameter has no value (i.e. as in G28) - dict will look like {'com': 'G28', 'x': None}
            rmk: All keys are converted to lower (i.e. X145 will be repr as {'x':145})
            rmk: Command are converted to upper and leading zeros are striped (i.e. g4, g002 and G01, will be repr as 'G4', 'G2' and 'G1')
        """
        line = line.split(";")[0]
        line = line.rstrip()
        res = {}
        if line:
            com = line.split(" ")
            if "M117" in line:
                res["com"] = "M117"
                res["text"] = line[line.find("M117") + 5 :]
            else:
                for param in com:
                    if param[0] in ["G", "M", "g", "m"]:
                        n = param[1:].lstrip("0")
                        if not n:
                            n = "0"
                        res["com"] = param[0].upper() + n
                        self.lastcom = param
                    elif len(param) == 1:
                        res[param.lower()] = None
                    else:
                        try:
                            param = param.replace(",", ".")
                            val = float(param[1:])
                        except:
                            raise ValueError(
                                f"Parameter {param} in line '{' '.join(com)}' can't be converted to float value"
                            )
                        else:
                            res[param[0].lower()] = val
            if "com" not in res:
                if self.lastcom:
                    res["com"] = self.lastcom
                else:
                    raise ValueError(
                        f"Command is opposed in {line} and was not set before"
                    )
        return res

    def dicttovector(self, com: dict):
        """Converts command dict to a movement vector for a linear move.

        Args:
            com (dict): command dict from gparser.comtodict

        Returns:
            ndarray: Movement vector of format (x,y,z,a,b,c,e,f), where x-e are coordinates, f - speed
        """
        res = np.zeros(8, float)
        npos = np.zeros(7, float)
        if self.absmove:
            npos[:6] = self.cpos[:6]
        if self.absextrude:
            npos[6] = self.cpos[6]
        for key, i in zip("xyzabce", range(7)):
            if key in com:
                npos[i] = com[key]
        if self.absmove:
            res[:6] = npos[:6] - self.cpos[:6]
            self.cpos[:6] = npos[:6]
        else:
            res[:6] = npos[:6]
            self.cpos[:6] = self.cpos[:6] + npos[:6]
        if self.absextrude:
            res[6] = npos[6] - self.cpos[6]
            self.cpos[6] = npos[6]
        else:
            res[6] = npos[6]
            self.cpos[6] += npos[6]
        if "f" in com:
            self.cspeed = com["f"] / 60  # Converting from mm/min to mm/s
        res[7] = self.cspeed
        return res

    def dicttoarc(self, com: dict):
        raise NotImplementedError

    def dicttohome(self, com: dict):
        """Implements homing G28 method. Homes parser to self.homepos with given axis and offset.

        Args:
            com (dict): command dict from gparser.comtodict

        Returns:
            ndarray: movement vector
        """
        npos = self.cpos.copy()
        res = np.zeros(8, float)
        for key, i in zip("xyzabce", range(7)):
            if key in com:
                val = com[key]
                if not val:
                    val = 0
                npos[i] = self.homepos[i] + val
        res[:7] = npos - self.cpos
        res[7] = self.hspeed
        self.cpos = npos
        return res

    def setcpos(self, com: dict):
        """Sets self.cpos for G92

        Args:
            com (dict): command dict from gparser.comtodict
        """
        for key, i in zip("xyzabce", range(7)):
            if key in com:
                self.cpos[i] = com[key]

    def parse(self, filepath):
        """Parses g-code file and returns a list of moves

        Args:
            filepath (_type_): Path to g-code file

        Returns:
            list: The list of moves
        """
        queue = []
        file = open(filepath)
        for line in file:
            d = self.comtodict(line)
            if d:
                match d["com"]:
                    case "G0" | "G1":
                        queue.append(self.dicttovector(d))
                    case "G2" | "G3":
                        queue.append(self.dicttoarc(d))
                    case "G28":
                        queue.append(self.dicttohome(d))
                    case "G90":
                        self.absmove = True
                        self.absextrude = True
                    case "G91":
                        self.absmove = False
                        self.absextrude = False
                    case "G92":
                        self.setcpos(d)
                    case "M82":
                        self.absextrude = True
                    case "M83":
                        self.absextrude = False
        return queue


if __name__ == "__main__":
    pass
