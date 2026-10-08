"""Test module to show a suspected bug"""

def testpass(valx, valy, valz):
    """Test method that pylint is okay with

    Parameters
    ----------
    valx : int
        description of valx
    valy : int
        description of valy
    valz : int
        description of valz

    Return
    ------
    int
        sum of valx, valy, valz
    """
    return valx + valy + valz

def testpass2(valx, valy, valz):
    """Test method that pylint is okay with

    Parameters
    ----------
    valx, valy, valz : int
        description of valx, valy, valz

    Return
    ------
    int
        sum of valx, valy, valz
    """
    return valx + valy + valz

def testfail(valx, valy, valz, factor):
    """Test method that pylint is NOT okay with

    Parameters
    ----------
    valx, valy, valz : int
        description of valx, valy, valz
    factor: int
        description of factor

    Return
    ------
    int
        sum of valx, valy, valz multiplied by factor
    """
    return (valx + valy + valz) * factor

