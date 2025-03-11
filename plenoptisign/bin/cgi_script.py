#!/usr/bin/env python3

__author__ = "Christopher Hahne"
__email__ = "inbox@christopherhahne.de"
__license__ = """
Copyright (c) 2019 Christopher Hahne <inbox@christopherhahne.de>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import cgi, cgitb
import sys, csv, datetime, os.path
sys.path.append(os.path.abspath('../..'))
from plenoptisign.mainclass import MainClass
from plenoptisign.constants import PlenoptisignError, DEC_P

def cgi_read():

    # report errors in log file
    cgitb.enable(display=0, logdir='.')

    # read from cgi field storage and convert to dict
    field_storage = cgi.FieldStorage()
    data = {}
    for key in field_storage.keys():
        data[key] = float(field_storage[key].value)

    return data


def cgi_main():

    # construct object
    obj = MainClass()

    # read input from cgi field storage
    obj.data = cgi_read()

    # compute light field geometry
    ret_refo = obj.refo()
    ret_tria = obj.tria()
    if not (ret_refo or ret_tria):
        raise AssertionError('Calculation failed.')

    # convert distances to string while adding metric unit under consideration of infinity
    str_dist = str(round(obj.d, DEC_P)) + ' mm' if not "inf" in str(obj.d) else "infinity"
    str_d_p = str(round(obj.d_p, DEC_P)) + ' mm' if not "inf" in str(obj.d_p) else "infinity"
    str_d_m = str(round(obj.d_m, DEC_P)) + ' mm' if not "inf" in str(obj.d_m) else "infinity"
    str_dof = str(round(obj.dof, DEC_P)) + ' mm' if not "inf" in str(obj.dof) else "infinity"
    str_base = str(round(obj.B, DEC_P)) + ' mm' if not "inf" in str(obj.B) else "infinity"
    str_phi = str(round(obj.phi, DEC_P)) + ' deg'
    str_tria = str(round(obj.Z, DEC_P)) + ' mm' if not "inf" in str(obj.Z) else "infinity"
    console_msg = obj.console_msg

    # save data to csv file
    t = 'Timestamp: {:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now())
    input = [obj.pp, obj.fs, obj.hh, obj.pm, obj.dA, obj.fU, obj.HH, obj.df, obj.D, obj.a, obj.M, obj.G, obj.dx]
    output = [str_dist, str_dof, str_base, str_phi, str_tria, console_msg]
    with open('data.csv', 'a') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(t)
        spamwriter.writerow(input)
        spamwriter.writerow(output)
        spamwriter.writerow(console_msg)
        spamwriter.writerow('')
        csvfile.close()

    # HTML output
    if bool(obj.refo_opt) or bool(obj.tria_opt):
        # HTML header
        print("Content-Type: text/html\n")
        print("<br />")
        print("<p style='font-size:12pt;'><b>Results</b></p>")
        print("<hr/>")
        print("<p>")
        print("<TABLE>")

    if bool(obj.refo_opt):
        # refocusing output
        print("<TR>")
        if bool(obj.tria_opt):
            print("<TD><b>Refocusing</b></TD>")
        else:
            print("<TD></TD>")
        print("<TD>refocusing distance <i>d<sub style='line-height:0'>a</sub></i>: </TD><TD>%s</TD>" % str_dist)
        print("</TR>")
        print("<TR>")
        print("<TD></TD>")
        print("<TD>depth of field <i>DoF<sub style='line-height:0'>a</sub></i>: </TD><TD>%s</TD>" % str_dof)
        print("</TR>")
        print("<TR>")
        print("<TD></TD>")
        print("<TD>narrow DoF border <i>d<sub style='line-height:0'>a-</sub></i>: </TD><TD>%s</TD>" % str_d_m)
        print("</TR>")
        print("<TR>")
        print("<TD></TD>")
        print("<TD>far DoF border <i>d<sub style='line-height:0'>a+</sub></i>: </TD><TD>%s</TD>" % str_d_p)
        print("</TR>")

    if bool(obj.refo_opt) and bool(obj.tria_opt):
        # blank space
        print("<TR>")
        print("<TD></TD>")
        print("<TD></TD>")
        print("<TD></TD>")
        print("</TR>")

    if bool(obj.tria_opt):
        # triangulation output
        print("<TR>")
        if bool(obj.refo_opt):
            print("<TD><b>Triangulation</b></TD>")
        else:
            print("<TD></TD>")
        print("<TD>baseline <i>B<sub style='line-height:0'>G</sub></i>: </TD><TD>%s</TD>" % str_base)
        print("</TR>")
        print("<TR>")
        print("<TD></TD>")
        print("<TD>tilt angle <i>&Phi;<sub style='line-height:0'>G</sub></i>: </TD><TD>%s</TD>" % str_phi)
        print("</TR>")
        print("<TR>")
        print("<TD></TD>")
        print("<TD>tria. distance <i>Z<sub style='line-height:0'>G</sub></i>: </TD><TD>%s</TD>" % str_tria)
        print("</TR>")

    if bool(obj.refo_opt) or bool(obj.tria_opt):
        print("</TABLE>")
        print("</p>")
        print("<br />")
    if bool(obj.refo_opt) and bool(obj.tria_opt):
        # console handling
        if console_msg:
            print("Console output: <br \>")
            for msg in console_msg:
                print("> %s <br \>" % msg)


if __name__ == "__main__":
    try:
        sys.exit(cgi_main())
    except Exception as e:
        PlenoptisignError(e)
