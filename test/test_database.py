from os import path
import unittest

from comp62521.database import database
from comp62521 import views

class TestDatabase(unittest.TestCase):

    def setUp(self):
        dir, _ = path.split(__file__)
        self.data_dir = path.join(dir, "..", "data")

    def test_read(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        self.assertEqual(len(db.publications), 1)

    def test_read_invalid_xml(self):
        db = database.Database()
        self.assertFalse(db.read(path.join(self.data_dir, "invalid_xml_file.xml")))

    def test_read_missing_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "missing_year.xml")))
        self.assertEqual(len(db.publications), 0)

    def test_read_missing_title(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "missing_title.xml")))
        # publications with missing titles should be added
        self.assertEqual(len(db.publications), 1)

    def test_get_average_authors_per_publication(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-1.xml")))
        _, data = db.get_average_authors_per_publication(database.Stat.MEAN)
        self.assertAlmostEqual(data[0], 2.3, places=1)
        _, data = db.get_average_authors_per_publication(database.Stat.MEDIAN)
        self.assertAlmostEqual(data[0], 2, places=1)
        _, data = db.get_average_authors_per_publication(database.Stat.MODE)
        self.assertEqual(data[0], [2])

    def test_get_average_publications_per_author(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-2.xml")))
        _, data = db.get_average_publications_per_author(database.Stat.MEAN)
        self.assertAlmostEqual(data[0], 1.5, places=1)
        _, data = db.get_average_publications_per_author(database.Stat.MEDIAN)
        self.assertAlmostEqual(data[0], 1.5, places=1)
        _, data = db.get_average_publications_per_author(database.Stat.MODE)
        self.assertEqual(data[0], [0, 1, 2, 3])

    def test_get_average_publications_in_a_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-3.xml")))
        _, data = db.get_average_publications_in_a_year(database.Stat.MEAN)
        self.assertAlmostEqual(data[0], 2.5, places=1)
        _, data = db.get_average_publications_in_a_year(database.Stat.MEDIAN)
        self.assertAlmostEqual(data[0], 3, places=1)
        _, data = db.get_average_publications_in_a_year(database.Stat.MODE)
        self.assertEqual(data[0], [3])

    def test_get_average_authors_in_a_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-4.xml")))
        _, data = db.get_average_authors_in_a_year(database.Stat.MEAN)
        self.assertAlmostEqual(data[0], 2.8, places=1)
        _, data = db.get_average_authors_in_a_year(database.Stat.MEDIAN)
        self.assertAlmostEqual(data[0], 3, places=1)
        _, data = db.get_average_authors_in_a_year(database.Stat.MODE)
        self.assertEqual(data[0], [0, 2, 4, 5])
        # additional test for union of authors
        self.assertEqual(data[-1], [0, 2, 4, 5])

    def test_get_publication_summary(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_publication_summary()
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data[0]), 6,
            "incorrect number of columns in data")
        self.assertEqual(len(data), 2,
            "incorrect number of rows in data")
        self.assertEqual(data[0][1], 1,
            "incorrect number of publications for conference papers")
        self.assertEqual(data[1][1], 2,
            "incorrect number of authors for conference papers")

    def test_get_average_authors_per_publication_by_author(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "three-authors-and-three-publications.xml")))
        header, data = db.get_average_authors_per_publication_by_author(database.Stat.MEAN)
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 3,
            "incorrect average of number of conference papers")
        self.assertEqual(data[0][1], 1.5,
            "incorrect mean journals for author1")
        self.assertEqual(data[1][1], 2,
            "incorrect mean journals for author2")
        self.assertEqual(data[2][1], 1,
            "incorrect mean journals for author3")

    def test_get_publications_by_author(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_publications_by_author()
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 2,
            "incorrect number of authors")
        self.assertEqual(data[0][-1], 1,
            "incorrect total")

    def test_get_average_publications_per_author_by_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_average_publications_per_author_by_year(database.Stat.MEAN)
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 1,
            "incorrect number of rows")
        self.assertEqual(data[0][0], 9999,
            "incorrect year in result")

    def test_get_publications_by_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_publications_by_year()
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 1,
            "incorrect number of rows")
        self.assertEqual(data[0][0], 9999,
            "incorrect year in result")

    def test_get_author_totals_by_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_author_totals_by_year()
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 1,
            "incorrect number of rows")
        self.assertEqual(data[0][0], 9999,
            "incorrect year in result")
        self.assertEqual(data[0][1], 2,
            "incorrect number of authors in result")

    def test_calculate_first_last(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "dblp_curated_sample.xml")))
        self.assertEqual(db.calculate_first_last("Piero Fraternali"), (0, 7))
        self.assertEqual(db.calculate_first_last("Stefano Ceri"), (86, 33))
        self.assertEqual(db.calculate_first_last("aaa"), (0, 0))

    '''def test_sorting(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "dblp_curated_sample.xml")))

        #Test cases fo publications summary
        data = db.get_publication_summary()
        #Assert for non empty
        self.assertTrue(views.sorting(data, 1) != 0)
        self.assertTrue(views.sorting(data, 2) != 0)
        self.assertTrue(views.sorting(data, 3) != 0)
        self.assertTrue(views.sorting(data, 4) != 0)
        self.assertTrue(views.sorting(data, 5) != 0)
        #Assert if sorting
        self.assertEquals(views.sorting(data, 1),data)
        self.assertEquals(views.sorting(data, 2),data)
        self.assertEquals(views.sorting(data, 3), data)
        self.assertEquals(views.sorting(data, 4), data)
        self.assertEquals(views.sorting(data, 5), data)

        #Test cases fo publications per year
        data = db.get_publications_by_year()
        #Assert for non empty
        self.assertTrue(views.sorting(data, 1) != 0)
        self.assertTrue(views.sorting(data, 2) != 0)
        self.assertTrue(views.sorting(data, 3) != 0)
        self.assertTrue(views.sorting(data, 4) != 0)
        self.assertTrue(views.sorting(data, 5) != 0)
        #Assert if sorting
        self.assertEquals(views.sorting(data, 1),data)
        self.assertEquals(views.sorting(data, 2),data)
        self.assertEquals(views.sorting(data, 3), data)
        self.assertEquals(views.sorting(data, 4), data)
        self.assertEquals(views.sorting(data, 5), data)

        #Test cases for author totals by year
        data = db.get_author_totals_by_year()
        #Assert for non empty
        self.assertTrue(views.sorting(data, 1) != 0)
        self.assertTrue(views.sorting(data, 2) != 0)
        self.assertTrue(views.sorting(data, 3) != 0)
        self.assertTrue(views.sorting(data, 4) != 0)
        self.assertTrue(views.sorting(data, 5) != 0)
        #Assert if sorting
        self.assertEquals(views.sorting(data, 1),data)
        self.assertEquals(views.sorting(data, 2),data)
        self.assertEquals(views.sorting(data, 3), data)
        self.assertEquals(views.sorting(data, 4), data)
        self.assertEquals(views.sorting(data, 5), data)'''

    def test_searchAuthor(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "dblp_curated_sample.xml")))
        self.assertEqual(db.calculate_searchAuthors("testName"),(0,0,0,0,0,0))

        #Test case1: Number of publications
        self.assertEqual(db.calculate_searchAuthors("Carlo Batini"),(10,0,0,0,0,0))
        #Test case2: Number of conference papers
        self.assertEqual(db.calculate_searchAuthors("Carlo Batini"),(10,6,0,0,0,0))

if __name__ == '__main__':
    unittest.main()
