from copy import deepcopy


class LeaseDataStore:
    def __init__(self):
        self.main_dashboard_rows = [
            [
                "September 09, 2025",
                "REVISED REQUEST FOR MEMORANDUM ON THE APPROVED CONTRACT OF LEASE EXTENSION OFFICE",
                "",
                "",
                "OK 09.10.25",
                "OK 9.10.25",
                "OK 9.22.25",
                "OK 9.22.2025",
                "OK 9.22.25",
                "OK 10.08.25",
                "OK 10.7.25",
                "OK 10.07.25",
                "SENT TO MANOLO EO 10.8.25",
            ],
            [
                "October 06, 2025",
                "REQUEST FOR APPROVAL OF VARIOUS VISMIN STOCK ROOM FOR 2025 (LOT 2S / BATCH 1)",
                "",
                "",
                "OK 10.06.25",
                "OK 10.06.25",
                "OK 10.08.25",
                "OK 10.08.25",
                "OK 10.08.25",
                "OK 10.09.25",
                "OK 10.08.25",
                "OK 10.08.25",
                "SENT TO VARIOUS OFFICES 10.09.25",
            ],
            [
                "November 17, 2025",
                "REVISED REQUEST FOR APPROVAL RE LEASE CONTRACT FOR RENEWAL OF ACDI VISMIN TRANSIENT-STOCK ROOM FOR PR",
                "",
                "",
                "OK 11.17.25",
                "OK 11.17.25",
                "OK 11.25.25",
                "OK 11.27.25",
                "OK 11.27.25",
                "OK 11.27.25",
                "OK 12.04.25",
                "OK 12.09.25",
                "SENT TO VARIOUS OFFICES 12.09.25",
            ],
        ]

        self.expiry_rows = [
            ["VISMIN", "", "11-Apr-25", "1 YR", "", "", "", "1-Jun-23", "31-May-24", "80 sqm", "CMSG GSD MEMO 008-2023", "", "DONE"],
            ["CVAO", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["MBEAB", "18-Nov-24", "21-Jan-25", "1 YR", "MARY CRIS S PERALES", "", "", "1-Jan-25", "31-Dec-25", "221", "GS MEMO 026-2025", "31-Jan-25", "DONE"],
            ["LAPULAPU EO", "26-Jan-24", "30-Jan-24", "1 YR", "", "", "", "1-Feb-24", "1-Feb-25", "24.5", "GS MEMO 117-2024", "7-Oct-24", "DONE"],
            ["LAPULAPU EO", "20-Jun-25", "", "1 YR", "", "", "28-Feb-26", "1-May-25", "30-Apr-26", "24.5", "", "", "DONE - MAY PLANS FOR FINDING ANOTHER AREA"],
            ["TAGBILARAN", "24-Jan-24", "20-Dec-24", "1 YR", "", "", "", "1-Jun-24", "31-May-25", "60", "GSD MEMO 081-2025", "14-Jul-25", "DONE"],
            ["TAGBILARAN", "15-Jul-25", "", "1 YR", "", "", "31-Mar-26", "1-Jun-25", "31-May-26", "60", "VLG GS MEMO 004-2025", "22-Aug-25", "DONE - MAY PLANS FOR FINDING ANOTHER AREA"],
            ["CEBU", "28-Oct-24", "19-Nov-24", "5 YRS", "Milane C Fernandez- CVAO", "0917-629-4632", "31-Oct-29", "1-Jan-25", "31-Dec-29", "110", "GS MEMO 012-2025", "21-Jan-25", "Waiting for Notarized Contract"],
            ["DAVAO", "12-Jan-26", "", "1 YR", "Milane C Fernandez- CVAO", "0917-629-4632", "1-Sep-26", "1-Nov-25", "1-Nov-26", "20 sqm", "", "", "Waiting for Notarized Contract"],
            ["BOGO EO", "8-Jan-24", "12-Jan-24", "2 YRS", "", "", "", "1-Feb-24", "1-Feb-26", "32", "LUZON GSD MEMO 005-2024", "6-Feb-24", "DONE"],
            ["PGIAO", "", "", "", "", "", "", "", "", "", "", "", ""],
            ["ILOILO TRANSIENT", "16-Jul-25", "26-Aug-25", "3 YRS", "MARGIE HERAS FERRO", "", "30-Jun-28", "1-Sep-25", "31-Aug-28", "75 sqm", "VLG GSS MEMO NO. 007-2025", "4-Nov-25", "DONE"],
            ["SAN JOSE ANTIQUE MO (ILOILO)", "", "", "2 YRS", "", "", "31-May-26", "1-Aug-24", "31-Jul-26", "33 sqm", "LUZON GSD MEMO 068-2024", "28-May-24", "DONE"],
            ["KALIBO MO", "26-Feb-25", "3-Mar-25", "1 YR", "", "", "28-Feb-26", "1-May-25", "30-Apr-26", "30", "GS MEMO 075-2025", "10-Mar-25", "WILL LIPAT NG"],
            ["KALIBO MO", "4-Mar-24", "13-Mar-24", "1 YR", "", "", "", "1-May-24", "30-Apr-25", "30", "LUZON GSD MEMO 055-2024", "4-Jul-24", "DONE"],
            ["ROXAS EO", "22-Aug-24", "6-Sep-24", "5 YRS", "", "", "31-Aug-29", "1-Nov-24", "31-Oct-29", "100", "GS MEMO 137-2024", "17-Oct-24", "DONE"],
            ["ROXAS EO TRANSIENT", "24-Jun-24", "19-Jul-24", "1 YR", "", "", "", "15-Aug-24", "14-Aug-25", "28", "GS MEMO 118-2024", "29-Oct-24", "DONE"],
            ["ROXAS EO TRANSIENT", "16-Jul-25", "", "1 YR", "", "", "14-Jun-26", "15-Aug-25", "14-Aug-26", "28", "", "", ""],
        ]

        self.legend = [
            ("39", "Done Lease Contracts w/ Memo #"),
            ("15", "Routed Lease Contract"),
            ("34", "To. Terminated Lease Contracts"),
            ("2", "Consolidated or Old Lease Contracts"),
        ]

    def get_main_dashboard_rows(self):
        return deepcopy(self.main_dashboard_rows)

    def get_expiry_rows(self):
        return deepcopy(self.expiry_rows)

    def get_legend_rows(self):
        return deepcopy(self.legend)


store = LeaseDataStore()