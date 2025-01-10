from dataclasses import dataclass
from enum import Enum


class X01TargetScore(Enum):
    TS301 = 301
    TS501 = 501
    TS701 = 701
    TS901 = 901
    TS1001 = 1001
    PLAYOFF = 0


@dataclass
class X01Rules:
    score: X01TargetScore
    parcheesi: bool = False
    run_and_gun: bool = False
    run_and_gun_time: int = 60
    play_off: bool = False
    double_in: bool = False
    double_out: bool = False
    master_out: bool = False
    equal_option: bool = False
    end_option: bool = False
    double_bull: bool = True

    def validate(self) -> bool:
        """
        Validates that no-nonsense options are chosen
        """
        if self.double_out and self.master_out:
            return False
        if self.equal_option and self.end_option:
            return False

        return True
