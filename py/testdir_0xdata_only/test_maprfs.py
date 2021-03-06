
import os, json, unittest, time, shutil, sys
sys.path.extend(['.','..','py'])

import h2o, h2o_cmd, h2o_hosts
import h2o_browse as h2b
import h2o_import as h2i
import time, random

class Basic(unittest.TestCase):
    def tearDown(self):
        h2o.check_sandbox_for_errors()

    @classmethod
    def setUpClass(cls):
        # assume we're at 0xdata with it's hdfs namenode
        global localhost
        localhost = h2o.decide_if_localhost()
        # hdfs_config='/opt/mapr/conf/mapr-clusters.conf', 
        if (localhost):
            h2o.build_cloud(1, 
                use_maprfs=True, 
                hdfs_version='mapr2.1.3', 
                hdfs_name_node='mr-0x1.0xdata.loc:7222')
        else:
            h2o_hosts.build_cloud_with_hosts(1, 
                use_maprfs=True, 
                hdfs_version='mapr2.1.3', 
                hdfs_name_node='mr-0x1.0xdata.loc:7222')

    @classmethod
    def tearDownClass(cls):
        h2o.tear_down_cloud()

    def test_B_hdfs_files(self):
        print "\nLoad a list of files from HDFS, parse and do 1 RF tree"
        print "\nYou can try running as hduser/hduser if fail"
        # larger set in my local dir
        # fails because classes aren't integers
        #    "allstate_claim_prediction_train_set.zip",
        csvFilenameAll = [
            "TEST-poker1000.csv",
        ]

        # pick 8 randomly!
        if (1==0):
            csvFilenameList = random.sample(csvFilenameAll,8)
        # Alternatively: do the list in order! Note the order is easy to hard
        else:
            csvFilenameList = csvFilenameAll

        # pop open a browser on the cloud
        # h2b.browseTheCloud()

        timeoutSecs = 200
        # save the first, for all comparisions, to avoid slow drift with each iteration
        firstglm = {}
        h2i.setupImportHdfs(
            path='/datasets', 
            schema='maprfs')

        for csvFilename in csvFilenameList:
            # creates csvFilename.hex from file in hdfs dir 
            print "Loading", csvFilename, 'from HDFS'
            parseKey = h2i.parseImportHdfsFile(
                csvFilename=csvFilename, 
                path='/datasets', 
                schema='maprfs', 
                timeoutSecs=1000)

            print csvFilename, 'parse time:', parseKey['response']['time']
            print "parse result:", parseKey['destination_key']

            print "\n" + csvFilename
            start = time.time()
            RFview = h2o_cmd.runRFOnly(trees=1,parseKey=parseKey,timeoutSecs=2000)
            h2b.browseJsonHistoryAsUrlLastMatch("RFView")
            # wait in case it recomputes it
            time.sleep(10)

            sys.stdout.write('.')
            sys.stdout.flush() 


if __name__ == '__main__':
    h2o.unit_main()
