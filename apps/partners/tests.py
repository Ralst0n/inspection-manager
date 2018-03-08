from django.test import TestCase

from datetime import date

from partners.models import LetProject

class LetModelTest(TestCase):
    def setUp(self):
        LetProject.objects.create(
        district= 11,
        agreement_number= 'E04196',
        name = 'Construction Inspection for SR 422 L32',
        advance_date = '2018-08-01',
        cost= '$11,000,000',
        url= 'https=//www.dot14.state.pa.us/ECMS/SVPLP?action=ShowPlannedProject&PLP_ID=11,326',
        office= 'Pittsburgh',
        description= '''The Department will retain an engineering firm to provide a supplementary construction inspection staff of approximately four (4) inspectors, under the Department's Inspector(s)-in-Charge for construction inspection and documentation services, on the following projects:(ECMS # 92804) SR 422 L35: For the concrete pavement patching and bituminous overlay, drainage, guide rail, signing and pavement markings, signals, structure preservation and other miscellaneous construction in Union Township and the City of New Castle in Lawrence County.ANTP for Inspection Services: June 2018, Anticipated Completion: December 2018'''
        )

        LetProject.objects.create(
        district= 11,
        agreement_number= 'E04148',
        name= 'Construction Inspection for SR 19 A63',
        advance_date= '2018-08-01',
        cost= '$20,000,000',
        url= 'https=//www.dot14.state.pa.us/ECMS/SVPLP?action=ShowPlannedProject&PLP_ID=11,325',
        office= 'Pittsburgh',
        description= '''The Department will retain an engineering firm to provide a supplementary construction inspection staff of approximately six (6) inspectors, under the Department's Inspector(s)-in-Charge for construction inspection and documentation services, on the following projects:(ECMS # 96562) SR 19 A63: This project is the reconstruction of four lanes of S.R. 0019. The work includes pavement replacement, guiderail, drainage, and signing. Also, the two lane Shaler Street Bridge will be replaced. The project will include the lengthening of the Wabash Street deceleration lane and three sign structure replacements, one new sign structure. and other miscellaneous construction in the City of Pittsburgh, Allegheny County. ANTP for Inspection Services: June 2018, Anticipated Completion: April 2021
        ''')

        LetProject.objects.create(
        district= 3,
        agreement_number= 'E04193',
        name= 'Construction Inspection',
        advance_date= '2018-04-01',
        cost= '1.25 Mill',
        url= 'https=//www.dot14.state.pa.us/ECMS/SVPLP?action=ShowPlannedProject&PLP_ID=11,324',
        office= 'King of Prussia',
        description = """The Department of Transportation will retain an engineering
        firm for an Open End Agreement to provide supplementary construction
        inspection staff under the Department's Inspector(s)-in-Charge on various
        Department AND/OR Highway Occupancy Permit projects AND /OR Local Public
        Agency projects AND/OR Inspection services required for Utilities and Marcellus Shale gas drilling activities located within the boundaries of Engineering District 3-0, which includes the following counties: Columbia, Lycoming, Montour, Northumberland, Snyder, Sullivan, Tioga, Union, and Bradford. The contract will include roadway, bridge construction projects, material plant inspection, highway occupancy permit inspection, Department Administered Local Projects and Inspection services required to monitor roads and inspection of reconstruction/maintenance activities impacted by Marcellus Shale gas drilling activities. The contract will continue for a period of 5 years, with a maximum of $1.25 million.The inspection staff will include a maximum of 3 TCIS's, 12 TCI's, 2 TA's, and 2 Coatings Inspectors.
        """)

    def test_model_dates(self):
        # Latest scrapped_date is today
        obj = LetProject.objects.latest('scrapped_date')
        self.assertEqual(date.today(), obj.scrapped_date )
