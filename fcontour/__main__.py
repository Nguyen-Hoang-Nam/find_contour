import os
import argparse

from scan import DocumentScanner
import utils

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image", action='store', help="Path to single image to be scanned")
    parser.add_argument("-t", "--test", action='store_true', help="test all image in test directory")

    args = parser.parse_args()

    if args.image:
        image_path = args.image 

        if utils.valid_imgage(image_path):
            scanner = DocumentScanner(image_path)
            scanner.detect()
            scanner.write()
        else:
            print('Error: Invalid path')
        
    elif args.test:
        test_directory = 'test'
        testcase_list = os.listdir(test_directory)

        for testcase in testcase_list:
            testcase_path = test_directory + '/' + testcase
            
            scanner = DocumentScanner(testcase_path)
            scanner.detect()
            scanner.test(testcase)
    

if __name__ == '__main__':
    main()