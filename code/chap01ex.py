# Author: Kinnick Fox
# Date: 12/16/2022
# Ref:  Allen B. Downey

from __future__ import print_function, division
import nsfg
import thinkstats2

# read and store file as df
def ReadFemResp(dct_file='2002FemResp.dct',
                dat_file='2002FemResp.dat.gz',
                nrows=None):
    dct = thinkstats2.ReadStataDct(dct_file)
    df = dct.ReadFixedWidth(dat_file, compression='gzip', nrows=nrows)
    return df

def ValidatePregnum(resp):
    """Validate pregnum in the respondent file.

    resp: respondent DataFrame
    """
    # read the pregnancy frame
    preg = nsfg.ReadFemPreg()

    # make the map from caseid to list of pregnancy indices
    preg_map = nsfg.MakePregMap(preg)

    # iterate through the respondent pregnum series
    for index, pregnum in resp.pregnum.items():
        caseid = resp.caseid[index]
        indices = preg_map[caseid]

        # check that pregnum from the respondent file equals
        # the number of records in the pregnancy file
        if len(indices) != pregnum:
            print(caseid, len(indices), pregnum)
            return False

    return True


def main():
    resp = ReadFemResp()
    assert (len(resp) == 7643)
    assert (resp.pregnum.value_counts()[1] == 1267)
    assert (ValidatePregnum(resp))  # calls MakePregMap
    print('All tests passed.' )


if __name__ == '__main__':
    main()
