#!/usr/bin/env python

__author__ = "Christopher Hahne"
__email__ = "inbox@christopherhahne.de"
__license__ = """
Copyright (c) 2017 Christopher Hahne <inbox@christopherhahne.de>

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
import sys, csv, datetime
sys.path.append("..")
import plenoptisign

def cgi_read():

    cgitb.enable()  # for troubleshooting

    # read from cgi field storage and convert to dict
    field_storage = cgi.FieldStorage()
    data = {}
    for key in field_storage.keys():
        data[key] = float(field_storage[key].value)

    return data


def main():

    # read input from cgi field storage
    data = cgi_read()

    # construct object
    object = plenoptisign.SpcLfGeo(data)

    # compute light field geometry
    ret_refo = object.refo()
    ret_tria = object.tria()
    if not (ret_refo or ret_tria):
        raise AssertionError('Calculation failed.')

    # convert distances to string while adding metric unit under consideration of infinity
    dec_place = 4  # number of decimals
    str_dist = str(round(object.d, dec_place)) + ' mm' if not "inf" in str(object.d) else "infinity"
    str_d_p = str(round(object.d_p, dec_place)) + ' mm' if not "inf" in str(object.d_p) else "infinity"
    str_d_m = str(round(object.d_m, dec_place)) + ' mm' if not "inf" in str(object.d_m) else "infinity"
    str_dof = str(round(object.dof, dec_place)) + ' mm' if not "inf" in str(object.dof) else "infinity"
    str_base = str(round(object.B, dec_place)) + ' mm' if not "inf" in str(object.B) else "infinity"
    str_phi = str(round(object.phi, dec_place)) + ' deg'
    str_tria = str(round(object.Z, dec_place)) + ' mm' if not "inf" in str(object.Z) else "infinity"
    console_msg = object.console_msg

    # save data to csv file
    t = 'Timestamp: {:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now())
    input_params = [object._pp, object._fs, object._hh, object._pm, object._dA, object._fU, object._HH, object._df, object._D, object._a, object._M, object._G, object._dx]
    output_params = [str_dist, str_dof, str_base, str_phi, str_tria, console_msg]
    with open('data.csv', 'a') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(t)
        spamwriter.writerow(input_params)
        spamwriter.writerow(output_params)
        spamwriter.writerow(console_msg)
        spamwriter.writerow('')
        csvfile.close()

    # HTML output
    refo_opt = bool(data['refo']) if 'refo' in data else False
    tria_opt = bool(data['tria']) if 'tria' in data else False
    if refo_opt or tria_opt:
        # HTML header
        print("Content-Type: text/html\n")
        print("<br />")
        print("<p style='font-size:12pt;'><b>Results</b></p>")
        print("<hr/>")
        print("<p>")
        print("<TABLE>")

    if refo_opt:
        # refocusing output
        print("<TR>")
        if tria_opt:
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

    if refo_opt and tria_opt:
        # blank space
        print("<TR>")
        print("<TD></TD>")
        print("<TD></TD>")
        print("<TD></TD>")
        print("</TR>")

    if tria_opt:
        # triangulation output
        print("<TR>")
        if refo_opt:
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

    if refo_opt or tria_opt:
        print("</TABLE>")
        print("</p>")
        print("<br />")
    if refo_opt and tria_opt:
        # console handling
        if console_msg:
            print("Console output: <br \>")
            for msg in console_msg:
                print("> %s <br \>" % msg)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(e)