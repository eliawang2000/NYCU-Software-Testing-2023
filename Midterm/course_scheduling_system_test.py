import unittest
import course_scheduling_system
from unittest import mock

class CourseTest(unittest.TestCase):
    css = course_scheduling_system.CSS()
    classes = []
    @mock.patch('course_scheduling_system.CSS.check_course_exist')
    def testq1_1(self, my_mock):
        assert my_mock is course_scheduling_system.CSS.check_course_exist
        my_mock.return_value = True
        self.classes.append(('Algorithms', 'Monday', 3, 4))
        check_add_class = self.css.add_course(self.classes[0])
        self.assertEqual(check_add_class, True)
        
        course_list = self.css.get_course_list()
        print("q1_1 course: ", course_list)

    @mock.patch('course_scheduling_system.CSS.check_course_exist')
    def testq1_2(self, my_mock):
        assert my_mock is course_scheduling_system.CSS.check_course_exist
        my_mock.return_value = True
        self.classes.append(('Network Security', 'Tuesday', 3, 4))
        self.classes.append(('SA', 'Tuesday', 3, 4))
        bool1 = self.css.add_course(self.classes[1])
        print("q1_2 add class1: ",bool1)
        bool2 = self.css.add_course(self.classes[2])
        print("q1_2 add class2: ",bool2)

    @mock.patch('course_scheduling_system.CSS.check_course_exist')
    def testq1_3(self, my_mock):
        assert my_mock is course_scheduling_system.CSS.check_course_exist
        my_mock.return_value = False
        self.classes.append(('NA', 'Wednesday', 5, 6))
        bool3 = self.css.add_course(self.classes[3])
        print("q1_3 add class3: ",bool3)

    @mock.patch('course_scheduling_system.CSS.check_course_exist')
    def testq1_4(self, my_mock):
        assert my_mock is course_scheduling_system.CSS.check_course_exist
        my_mock.return_value = True
        with self.assertRaises(TypeError):
            bool4 = self.css.add_course('Operating system')

    
    @mock.patch('course_scheduling_system.CSS.check_course_exist')
    def test_q1_5(self,my_mock):
        print("\n===== q1_5 =====")
        assert my_mock is course_scheduling_system.CSS.check_course_exist
        my_mock.return_value = True
        # self.classes.append(('c1', 'Friday', 1, 2))
        # self.classes.append(('c2', 'Friday', 3, 4))
        # self.classes.append(('c3', 'Friday', 5, 6))
        tmp = []
        tmp.append(('c1', 'Friday', 1, 2))
        tmp.append(('c2', 'Friday', 3, 4))
        tmp.append(('c3', 'Friday', 5, 6))
        self.assertEqual(self.css.add_course(tmp[0]), True)
        self.assertEqual(self.css.add_course(tmp[1]), True)
        self.assertEqual(self.css.add_course(tmp[2]), True)
        self.assertEqual(self.css.remove_course(tmp[1]), True)
        self.assertNotIn(tmp[1], self.css.get_course_list())
        self.assertEqual(course_scheduling_system.CSS.check_course_exist.call_count, 4)
        print(self.css)






if __name__ == "__main__":
    unittest.main()
    
    
